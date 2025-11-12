            ORDER BY cnt DESC
            LIMIT 10
        """, (customer_id,)).fetchall()
        
        # Hämta vanligaste ankartexter
        common_anchors = con.execute("""
            SELECT anchor_text, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ? AND anchor_text IS NOT NULL
            GROUP BY anchor_text
            ORDER BY cnt DESC
            LIMIT 20
        """, (customer_id,)).fetchall()
        
        # Räkna behov
        total_links = len(links)
        needs_target = sum(1 for l in links if l['needs_target'])
        needs_anchor = sum(1 for l in links if l['needs_anchor'])
        needs_both = sum(1 for l in links if l['needs_target'] and l['needs_anchor'])
        
        customer_analyses[customer_name] = {
            'customer_id': customer_id,
            'canonical_root': canonical_root,
            'brand': customer.get('brand'),
            'links': links,
            'total_links': total_links,
            'needs_target': needs_target,
            'needs_anchor': needs_anchor,
            'needs_both': needs_both,
            'historical_links': [dict(l) for l in historical_links],
            'common_targets': [dict(l) for l in common_targets],
            'common_anchors': [dict(l) for l in common_anchors],
            'markets': list(set(l['market'] for l in links))
        }
    
    con.close()
    return customer_analyses


if __name__ == '__main__':
    base_dir = Path(__file__).parent
    csv_path = base_dir / 'november_plan.csv'
    db_path = base_dir / 'data' / 'output' / 'linkops_history.db'
    
    print("="*70)
    print("NOVEMBER PLAN ANALYS")
    print("="*70)
    
    # Parsa CSV
    customer_plans = parse_november_plan(csv_path)
    
    print(f"\nTotalt {len(customer_plans)} unika kunder")
    
    # Analysera behov
    analyses = analyze_customer_needs(customer_plans, db_path)
    
    print(f"\n{len(analyses)} kunder matchade i databasen")
    print("\n" + "="*70)
    print("ANALYS PER KUND:")
    print("="*70)
    
    for customer_name, analysis in analyses.items():
        print(f"\n{customer_name} (ID: {analysis['customer_id']})")
        print(f"  Totalt länkar: {analysis['total_links']}")
        print(f"  Behöver målsida: {analysis['needs_target']}")
        print(f"  Behöver ankartext: {analysis['needs_anchor']}")
        print(f"  Behöver båda: {analysis['needs_both']}")
        print(f"  Marknader: {', '.join(analysis['markets'])}")
        print(f"  Historiska länkar: {len(analysis['historical_links'])}")
        print(f"  Vanligaste målsidor: {len(analysis['common_targets'])}")
        print(f"  Vanligaste ankare: {len(analysis['common_anchors'])}")
"""
November Plan Parser - Parsar november_plan.csv och förbereder för AI-agents
"""
import pandas as pd
from pathlib import Path
import sqlite3
from collections import defaultdict

def parse_november_plan(csv_path):
    """
    Parsar november_plan.csv med kolumner:
    publication_domain, kund_brand, market, target_url, link_anchor
    """
    df = pd.read_csv(csv_path)
    
    print(f"Totalt rader: {len(df)}")
    print(f"Kolumner: {df.columns.tolist()}")
    
    # Rensa bort helt tomma rader
    df = df.dropna(how='all')
    
    # Gruppera per kund för analys
    customer_plans = defaultdict(list)
    
    for idx, row in df.iterrows():
        pub_domain = str(row.get('publication_domain', '')).strip()
        customer = str(row.get('kund_brand', '')).strip()
        market = str(row.get('market', 'SE')).strip()
        target_url = str(row.get('target_url', '')).strip()
        anchor = str(row.get('link_anchor', '')).strip()
        
        # Skippa om både pub_domain och customer saknas
        if not pub_domain or not customer or customer == 'nan':
            continue
        
        # Bestäm om målsida/ankar saknas
        needs_target = not target_url or target_url == 'nan'
        needs_anchor = not anchor or anchor == 'nan'
        
        customer_plans[customer].append({
            'row_index': idx,
            'pub_domain': pub_domain,
            'customer': customer,
            'market': market,
            'target_url': target_url if not needs_target else None,
            'anchor': anchor if not needs_anchor else None,
            'needs_target': needs_target,
            'needs_anchor': needs_anchor
        })
    
    return dict(customer_plans)


def analyze_customer_needs(customer_plans, db_path):
    """
    Analyserar varje kunds behov och samlar kontext från historik
    """
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    
    customer_analyses = {}
    
    for customer_name, links in customer_plans.items():
        # Hitta customer_id
        customer = con.execute(
            "SELECT id, canonical_root, brand FROM customers WHERE canonical_root LIKE ? OR brand LIKE ?",
            (f'%{customer_name}%', f'%{customer_name}%')
        ).fetchone()
        
        if not customer:
            print(f"⚠️  Kund '{customer_name}' ej funnen i databas - skippar")
            continue
        
        customer_id = customer['id']
        canonical_root = customer['canonical_root']
        
        # Hämta historisk data
        historical_links = con.execute("""
            SELECT target_url, anchor_text, pub_domain, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ?
            GROUP BY target_url, anchor_text
            ORDER BY cnt DESC
            LIMIT 50
        """, (customer_id,)).fetchall()
        
        # Hämta vanligaste målsidor
        common_targets = con.execute("""
            SELECT target_url, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ? AND target_url IS NOT NULL
            GROUP BY target_url

