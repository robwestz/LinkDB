"""
Link Planning GUI - Flask Web Application

Ett modernt webbgränssnitt för intelligent länkplanering.
"""
from flask import Flask, render_template, jsonify, request, send_file
from pathlib import Path
import sys
import json
import sqlite3
from datetime import datetime
from collections import Counter
import pandas as pd

# Fix imports
sys.path.insert(0, str(Path(__file__).parent))

from app.planning.volume_detector import PlanningVolumeDetector
from app.planning.basic_plan_generator import BasicPlanGenerator
from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.analyzers.monthly_link_viewer import MonthlyLinkViewer

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # För svenska tecken

# Paths
BASE_DIR = Path(__file__).parent
HISTORY_DB = BASE_DIR / "data" / "output" / "linkops_history.db"
CUSTOMERS_DIR = BASE_DIR / "data" / "output" / "customers"
OUTPUT_DIR = BASE_DIR / "data" / "output"


@app.route('/')
def index():
    """Huvudsida - Dashboard."""
    return render_template('index.html')


@app.route('/api/customers')
def get_customers():
    """Hämta alla kunder med metadata."""
    try:
        import sqlite3
        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row

        customers = con.execute("""
            SELECT 
                c.id,
                c.canonical_root,
                c.brand,
                COUNT(lh.id) as total_links,
                COUNT(DISTINCT lh.pub_domain) as unique_pub_domains
            FROM customers c
            LEFT JOIN links_history lh ON c.id = lh.customer_id
            GROUP BY c.id
            ORDER BY c.canonical_root
        """).fetchall()

        con.close()

        result = []
        for c in customers:
            result.append({
                'id': c['id'],
                'canonical_root': c['canonical_root'],
                'brand': c['brand'] or c['canonical_root'],
                'total_links': c['total_links'],
                'unique_pub_domains': c['unique_pub_domains']
            })

        return jsonify({'customers': result, 'count': len(result)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/customer/<int:customer_id>/history')
def get_customer_history(customer_id):
    """Hämta historik för en kund."""
    try:
        analyzer = LinkHistoryAnalyzer(str(HISTORY_DB))
        analysis = analyzer.analyze_customer(customer_id)

        if not analysis:
            return jsonify({'error': 'Customer not found'}), 404

        return jsonify({
            'customer_id': analysis.customer_id,
            'canonical_root': analysis.canonical_root,
            'brand': analysis.brand,
            'total_links': analysis.total_links,
            'unique_pub_domains': analysis.unique_pub_domains,
            'unique_target_urls': analysis.unique_target_urls,
            'first_link_date': analysis.first_link_date,
            'last_link_date': analysis.last_link_date,
            'links_per_month': round(analysis.links_per_month, 1),
            'anchor_diversity_score': round(analysis.anchor_diversity_score, 2),
            'anchor_types': analysis.anchor_types,
            'most_common_anchors': analysis.most_common_anchors[:10],
            'primary_strategy': analysis.primary_strategy,
            'recommendations': analysis.recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/customer/<int:customer_id>/monthly')
def get_customer_monthly(customer_id):
    """Hämta månadshistorik för en kund."""
    try:
        # Hitta customer database
        import sqlite3
        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row
        customer = con.execute("SELECT canonical_root FROM customers WHERE id = ?", (customer_id,)).fetchone()
        con.close()

        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        customer_db = CUSTOMERS_DIR / customer['canonical_root'] / "customer.db"

        if not customer_db.exists():
            return jsonify({'error': 'Customer database not found'}), 404

        viewer = MonthlyLinkViewer(str(customer_db))
        groups = viewer.get_monthly_groups()

        result = []
        for group in groups:
            result.append({
                'year': group.year,
                'month': group.month,
                'month_name': group.month_name,
                'period': group.period,
                'display_name': group.display_name,
                'link_count': group.link_count,
                'unique_pub_domains': group.unique_pub_domains,
                'unique_target_urls': group.unique_target_urls,
                'anchor_types': group.anchor_types,
                'most_common_anchors': group.most_common_anchors[:5],
                'target_url_distribution': group.target_url_distribution[:5]
            })

        return jsonify({'months': result, 'count': len(result)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect-volume', methods=['POST'])
def detect_volume():
    """Detektera volym för planering."""
    try:
        data = request.get_json()
        planning_data = data.get('planning_data', {})

        # Konvertera string keys till int
        planning_data = {int(k): v for k, v in planning_data.items()}

        detector = PlanningVolumeDetector(str(HISTORY_DB))
        volumes = detector.detect_from_dict(planning_data)

        result = []
        for v in volumes:
            result.append({
                'customer_id': v.customer_id,
                'canonical_root': v.canonical_root,
                'brand': v.brand,
                'planned_links': v.planned_links,
                'historical_total': v.historical_total,
                'historical_monthly_avg': round(v.historical_monthly_avg, 1),
                'recommended_strategy': v.recommended_strategy,
                'can_cluster': v.can_cluster,
                'can_build_authority': v.can_build_authority,
                'semantic_planning_possible': v.semantic_planning_possible,
                'semantic_complexity': v.semantic_complexity
            })

        return jsonify({'volumes': result, 'count': len(result)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/import-sheets', methods=['POST'])
def import_sheets():
    """Importera data från Google Sheets."""
    try:
        data = request.get_json()
        sheets_url = data.get('sheets_url', '')
        sheet_name = data.get('sheet_name', 'November')

        # Extrahera spreadsheet ID från URL
        import re
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheets_url)
        if not match:
            return jsonify({'error': 'Ogiltig Google Sheets URL'}), 400

        spreadsheet_id = match.group(1)

        # Försök läsa från sheets
        all_rows = []

        try:
            import gspread

            # Kolla om credentials.json finns
            creds_path = Path(__file__).parent / 'credentials.json'

            if creds_path.exists():
                # Använd service account
                gc = gspread.service_account(filename=str(creds_path))
                spreadsheet = gc.open_by_key(spreadsheet_id)
                worksheet = spreadsheet.worksheet(sheet_name)
                all_rows = worksheet.get_all_records()
            else:
                # Returnera instruktioner
                return jsonify({
                    'error': 'Google Sheets credentials saknas',
                    'message': 'För att använda Google Sheets-import:\n\n1. Gå till Google Cloud Console\n2. Skapa ett projekt\n3. Aktivera Google Sheets API\n4. Skapa Service Account\n5. Ladda ner credentials.json\n6. Lägg filen i projektmappen\n\nAlternativt: Lägg till länkar manuellt nedan!'
                }), 400

        except Exception as e:
            print(f"Sheets error: {e}")
            return jsonify({
                'error': f'Kunde inte läsa från Google Sheets: {str(e)}',
                'message': 'Kontrollera att:\n1. URL:en är korrekt\n2. Sheet-namnet stämmer\n3. Sheetet är delat med service account email\n\nAlternativt: Lägg till länkar manuellt!'
            }), 400

        # Parse data
        if not all_rows:
            return jsonify({
                'error': 'Inga rader hittades i sheetet',
                'message': 'Kontrollera att:\n1. Sheet-namnet är korrekt\n2. Det finns data i sheetet\n3. Första raden har kolumnrubriker'
            }), 400

        result_rows = []
        skipped_rows = []
        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row

        for idx, row in enumerate(all_rows, start=2):  # start=2 eftersom rad 1 är headers
            pub_domain = row.get('Domain', '').strip()
            customer_name = row.get('Kund', '').strip()

            # Försök hitta target URL i olika kolumner
            target_url = (row.get('Targeting URL', '').strip() or
                         row.get('IsCustomer', '').strip() or
                         row.get('Target URL', '').strip())

            anchor_text = row.get('Anchor', '').strip()

            if not pub_domain:
                skipped_rows.append(f"Rad {idx}: Saknar Domain")
                continue

            if not customer_name:
                skipped_rows.append(f"Rad {idx}: Saknar Kund")
                continue

            # Hitta customer_id - försök flera matchningsmetoder
            customer = None

            # Metod 1: Exakt match på canonical_root
            customer = con.execute(
                "SELECT id, canonical_root FROM customers WHERE canonical_root = ?",
                (customer_name,)
            ).fetchone()

            # Metod 2: LIKE match på canonical_root
            if not customer:
                customer = con.execute(
                    "SELECT id, canonical_root FROM customers WHERE canonical_root LIKE ?",
                    (f'%{customer_name}%',)
                ).fetchone()

            # Metod 3: Match på brand
            if not customer:
                customer = con.execute(
                    "SELECT id, canonical_root FROM customers WHERE brand LIKE ?",
                    (f'%{customer_name}%',)
                ).fetchone()

            if customer:
                result_rows.append({
                    'pub_domain': pub_domain,
                    'customer_name': customer_name,
                    'customer_id': customer['id'],
                    'canonical_root': customer['canonical_root'],
                    'target_url': target_url if target_url else None,
                    'anchor_text': anchor_text if anchor_text else None
                })
            else:
                skipped_rows.append(f"Rad {idx}: Kund '{customer_name}' hittades inte i databasen")

        con.close()

        # Returnera resultat med info om skippade rader
        response = {
            'rows': result_rows,
            'count': len(result_rows),
            'total_processed': len(all_rows),
            'skipped_count': len(skipped_rows)
        }

        if skipped_rows:
            response['skipped_rows'] = skipped_rows[:10]  # Max 10 för att inte överväldiga
            response['warning'] = f'{len(skipped_rows)} rader skippades. Se detaljer nedan.'

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/load-preflight', methods=['POST'])
def load_preflight():
    """Ladda preflight från Google Sheets och validera mot client_index."""
    try:
        data = request.get_json()
        sheets_url = data.get('sheets_url', '')
        sheet_name = data.get('sheet_name', 'November')
        start_row = data.get('start_row', 2)
        end_row = data.get('end_row', 175)

        # Extrahera spreadsheet ID
        import re
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheets_url)
        if not match:
            return jsonify({'error': 'Ogiltig Google Sheets URL'}), 400

        spreadsheet_id = match.group(1)

        # Ladda client_index
        client_index_path = BASE_DIR / "data" / "client_index_matched.xlsx"

        if not client_index_path.exists():
            return jsonify({
                'error': 'Client index saknas',
                'message': 'Kör först: python data/match_customer_ids.py'
            }), 400

        import pandas as pd
        client_index = pd.read_excel(client_index_path)
        client_index_dict = {}

        for _, row in client_index.iterrows():
            if pd.notna(row.get('customer_name')) and pd.notna(row.get('customer_id')):
                client_index_dict[row['customer_name'].lower().strip()] = {
                    'customer_id': int(row['customer_id']),
                    'customer_name': row['customer_name'],
                    'client_domain': row.get('client_domain', ''),
                    'monthly_budget': row.get('monthly_budget', 0)
                }

        # Försök läsa från sheets
        all_rows = []

        try:
            import gspread
            creds_path = Path(__file__).parent / 'credentials.json'

            if creds_path.exists():
                gc = gspread.service_account(filename=str(creds_path))
                spreadsheet = gc.open_by_key(spreadsheet_id)
                worksheet = spreadsheet.worksheet(sheet_name)
                all_rows = worksheet.get_all_records()
            else:
                return jsonify({
                    'error': 'Google Sheets credentials saknas',
                    'message': 'Lägg till credentials.json för att använda automatisk import'
                }), 400
        except Exception as e:
            return jsonify({
                'error': f'Kunde inte läsa från Google Sheets: {str(e)}',
                'message': 'Kontrollera credentials och att sheetet är delat'
            }), 400

        # Parse data från valda rader
        preflight_items = []
        validation_errors = []
        skipped = []

        for idx, row in enumerate(all_rows, start=2):  # start=2 för att matcha Excel
            if idx < start_row or idx > end_row:
                continue

            pub_domain = row.get('Domain', '').strip()
            customer_name = row.get('Kund', '').strip()

            if not pub_domain:
                skipped.append(f"Rad {idx}: Saknar Domain")
                continue

            if not customer_name:
                skipped.append(f"Rad {idx}: Saknar Kund")
                continue

            # Hitta i client_index
            customer_key = customer_name.lower().strip()
            client_info = client_index_dict.get(customer_key)

            if not client_info:
                # Försök fuzzy match
                for key, info in client_index_dict.items():
                    if customer_name.lower() in key or key in customer_name.lower():
                        client_info = info
                        break

            if client_info:
                preflight_items.append({
                    'row': idx,
                    'pub_domain': pub_domain,
                    'customer_id': client_info['customer_id'],
                    'customer_name': client_info['customer_name'],
                    'client_domain': client_info['client_domain']
                })
            else:
                validation_errors.append(f"Rad {idx}: Kund '{customer_name}' saknas i client_index")

        # Gruppera per kund för översikt
        customer_summary = {}
        for item in preflight_items:
            cid = item['customer_id']
            if cid not in customer_summary:
                customer_summary[cid] = {
                    'customer_id': cid,
                    'customer_name': item['customer_name'],
                    'client_domain': item['client_domain'],
                    'link_count': 0,
                    'pub_domains': set()
                }
            customer_summary[cid]['link_count'] += 1
            customer_summary[cid]['pub_domains'].add(item['pub_domain'])

        # Konvertera sets till lists för JSON
        for cid in customer_summary:
            customer_summary[cid]['pub_domains'] = list(customer_summary[cid]['pub_domains'])

        return jsonify({
            'preflight_items': preflight_items,
            'total_items': len(preflight_items),
            'total_customers': len(customer_summary),
            'customer_summary': list(customer_summary.values()),
            'validation_errors': validation_errors[:20],  # Max 20
            'skipped': skipped[:20],
            'total_errors': len(validation_errors),
            'total_skipped': len(skipped)
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-monthly-plan', methods=['POST'])
def generate_monthly_plan():
    """Generera automatisk månadlig planering baserat på historik."""
    try:
        data = request.get_json()
        month = data.get('month')
        year = data.get('year')

        if not month or not year:
            return jsonify({'error': 'Month and year required'}), 400

        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row

        # Hämta alla aktiva kunder (de som haft länkar senaste 6 månaderna)
        six_months_ago = f"{year}-{max(1, month-6):02d}-01"

        active_customers = con.execute("""
            SELECT DISTINCT c.id, c.canonical_root, c.brand,
                   COUNT(lh.id) as recent_links,
                   AVG(CASE WHEN lh.created_at >= ? THEN 1 ELSE 0 END) as activity_score
            FROM customers c
            LEFT JOIN links_history lh ON c.id = lh.customer_id
            WHERE lh.created_at >= ?
            GROUP BY c.id
            HAVING recent_links > 0
            ORDER BY recent_links DESC
        """, (six_months_ago, six_months_ago)).fetchall()

        suggestions = []

        for customer in active_customers:
            customer_id = customer['id']
            canonical_root = customer['canonical_root']
            recent_links = customer['recent_links']

            # Beräkna föreslaget antal länkar baserat på historik
            suggested_count = max(1, int(recent_links / 6))  # Genomsnitt per månad

            # Hämta vanligaste publiceringssajter
            common_pubs = con.execute("""
                SELECT pub_domain, COUNT(*) as cnt
                FROM links_history
                WHERE customer_id = ? AND pub_domain IS NOT NULL
                GROUP BY pub_domain
                ORDER BY cnt DESC
                LIMIT 10
            """, (customer_id,)).fetchall()

            # Hämta vanligaste målsidor
            common_targets = con.execute("""
                SELECT target_url, COUNT(*) as cnt
                FROM links_history
                WHERE customer_id = ? AND target_url IS NOT NULL
                GROUP BY target_url
                ORDER BY cnt DESC
                LIMIT 5
            """, (customer_id,)).fetchall()

            # Hämta vanligaste ankartexter
            common_anchors = con.execute("""
                SELECT anchor_text, COUNT(*) as cnt
                FROM links_history
                WHERE customer_id = ? AND anchor_text IS NOT NULL
                GROUP BY anchor_text
                ORDER BY cnt DESC
                LIMIT 10
            """, (customer_id,)).fetchall()

            # Skapa länkar-förslag
            links = []
            for i in range(suggested_count):
                # Rotera genom pub domains
                pub_domain = common_pubs[i % len(common_pubs)]['pub_domain'] if common_pubs else None

                # Rotera genom målsidor
                target_url = common_targets[i % len(common_targets)]['target_url'] if common_targets else None

                # Rotera genom ankartexter
                anchor_text = common_anchors[i % len(common_anchors)]['anchor_text'] if common_anchors else None

                if pub_domain:  # Endast om vi har en pub domain
                    links.append({
                        'customer_id': customer_id,
                        'pub_domain': pub_domain,
                        'target_url': target_url,
                        'anchor_text': anchor_text
                    })

            if links:
                suggestions.append({
                    'customer_id': customer_id,
                    'canonical_root': canonical_root,
                    'brand': customer['brand'],
                    'suggested_count': suggested_count,
                    'links': links
                })

        # Självkorrigera planeringen innan den returneras
        corrected_suggestions, corrections = self_correct_planning(suggestions, con)

        con.close()

        # Logga korrigeringar
        if corrections:
            print("\n" + "="*70)
            print("🔧 SJÄLVKORRIGERINGAR GENOMFÖRDA")
            print("="*70)
            for correction in corrections:
                print(f"  • {correction}")
            print("="*70 + "\n")

        return jsonify({
            'month': month,
            'year': year,
            'suggestions': corrected_suggestions,
            'total_customers': len(corrected_suggestions),
            'total_links': sum(s['suggested_count'] for s in corrected_suggestions),
            'corrections_made': len(corrections),
            'corrections': corrections[:10] if corrections else []  # Max 10 för att inte överväldiga
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/semantic-preflight', methods=['POST'])
def semantic_preflight():
    """Genomför semantisk preflight-analys av planering med target URL-validering."""
    try:
        data = request.get_json()
        raw_planning_data = data.get('planning_data', {})

        # Validera target URLs mot client_domains
        client_index_path = BASE_DIR / "data" / "client_index_matched.xlsx"
        url_validation = {'valid': True, 'errors': [], 'warnings': []}

        if client_index_path.exists():
            import pandas as pd
            client_index = pd.read_excel(client_index_path)
            client_domains = {}

            for _, row in client_index.iterrows():
                if pd.notna(row.get('customer_id')) and pd.notna(row.get('client_domain')):
                    client_domains[int(row['customer_id'])] = row['client_domain'].strip()

            # Validera
            for key, item in raw_planning_data.items():
                if not isinstance(item, dict):
                    continue

                customer_id = item.get('customer_id')
                target_url = item.get('target_url')

                if not target_url:
                    continue

                client_domain = client_domains.get(customer_id)
                if not client_domain:
                    url_validation['warnings'].append(f"Kund ID {customer_id} saknas i client_index")
                    continue

                # Normalisera
                target_clean = target_url.lower().replace('http://', '').replace('https://', '').replace('www.', '')
                domain_clean = client_domain.lower().replace('http://', '').replace('https://', '').replace('www.', '')

                if not target_clean.startswith(domain_clean):
                    url_validation['valid'] = False
                    url_validation['errors'].append(
                        f"Target URL '{target_url}' matchar inte domän '{client_domain}' för kund ID {customer_id}"
                    )

        # Aggregera per kund
        customer_aggregation = {}
        for key, item in raw_planning_data.items():
            if isinstance(item, dict):
                cid = item['customer_id']
                if cid not in customer_aggregation:
                    customer_aggregation[cid] = {
                        'customer_id': cid,
                        'links': []
                    }
                customer_aggregation[cid]['links'].append(item)

        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row

        customer_analyses = []
        total_clusters = 0
        total_entities = 0
        recommendations = []

        for cid, agg in customer_aggregation.items():
            customer = con.execute("SELECT * FROM customers WHERE id = ?", (cid,)).fetchone()

            planned_links = len(agg['links'])

            # Bestäm strategi
            strategy = get_strategy_for_count(planned_links)

            # Bedöm semantisk kapacitet
            semantic_possible = planned_links >= 6
            can_build_authority = planned_links >= 10

            # Simulera kluster-identifiering (i verkligheten skulle detta analysera målsidor)
            recommended_clusters = []
            if semantic_possible:
                # Hämta vanliga topics från historik
                topics = con.execute("""
                    SELECT DISTINCT anchor_text
                    FROM links_history
                    WHERE customer_id = ?
                    LIMIT 5
                """, (cid,)).fetchall()

                recommended_clusters = [t['anchor_text'][:20] for t in topics if t['anchor_text']]
                total_clusters += len(recommended_clusters)
                total_entities += planned_links  # Approximation

            customer_analyses.append({
                'customer_id': cid,
                'canonical_root': customer['canonical_root'],
                'brand': customer['brand'],
                'planned_links': planned_links,
                'strategy': strategy,
                'semantic_analysis_possible': semantic_possible,
                'can_build_authority': can_build_authority,
                'recommended_clusters': recommended_clusters if recommended_clusters else None
            })

            # Rekommendationer
            if semantic_possible:
                recommendations.append(f"{customer['canonical_root']}: Kan bygga semantiska kluster")
            if can_build_authority:
                recommendations.append(f"{customer['canonical_root']}: Kan bygga topical authority")
            if planned_links < 6:
                recommendations.append(f"{customer['canonical_root']}: Överväg fler länkar för semantisk analys")

        con.close()

        return jsonify({
            'total_customers': len(customer_analyses),
            'total_links': sum(ca['planned_links'] for ca in customer_analyses),
            'semantic_clusters': total_clusters,
            'entities_found': total_entities,
            'topical_authority_opportunities': sum(1 for ca in customer_analyses if ca['can_build_authority']),
            'customer_analyses': customer_analyses,
            'recommendations': recommendations,
            'url_validation': {
                'valid': url_validation['valid'],
                'errors': url_validation['errors'][:10],
                'warnings': url_validation['warnings'][:10],
                'total_errors': len(url_validation['errors']),
                'total_warnings': len(url_validation['warnings'])
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """Generera en länkplan med AI-assistans."""
    try:
        data = request.get_json()
        raw_planning_data = data.get('planning_data', {})
        plan_name = data.get('plan_name', f"Plan {datetime.now().strftime('%Y-%m-%d')}")
        ai_instructions = data.get('ai_instructions', '')

        # Konvertera planningData till format som BasicPlanGenerator förväntar sig
        # Gamla formatet: {customer_id: link_count}
        # Nya formatet: {key: {customer_id, link_count, pub_domain, target_url, anchor_text}}

        planning_data = {}
        target_urls_map = {}

        for key, item in raw_planning_data.items():
            if isinstance(item, dict):
                # Nytt format
                customer_id = int(item['customer_id'])
                link_count = item['link_count']

                # Aggregera länkar per customer
                planning_data[customer_id] = planning_data.get(customer_id, 0) + link_count

                # Spara target_urls om de finns
                if item.get('target_url'):
                    if customer_id not in target_urls_map:
                        target_urls_map[customer_id] = []
                    target_urls_map[customer_id].append(item['target_url'])
            else:
                # Gammalt format (backup)
                planning_data[int(key)] = item

        # Generera AI-prompt för semantisk bedömning
        ai_prompt = generate_ai_prompt(raw_planning_data, planning_data, ai_instructions)
        
        # Logga AI-prompten så användaren kan se den
        print("\n" + "="*70)
        print("🤖 AI-PROMPT FÖR LÄNKPLANERING")
        print("="*70)
        print(ai_prompt)
        print("="*70 + "\n")
        
        generator = BasicPlanGenerator(str(HISTORY_DB))
        plan = generator.generate_plan(
            planning_data=planning_data,
            target_urls=target_urls_map if target_urls_map else None,
            plan_name=plan_name
        )
        
        # Lägg till AI-prompt i plan metadata
        plan.ai_prompt = ai_prompt
        plan.ai_instructions = ai_instructions
        
        # Exportera till CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"link_plan_{timestamp}.csv"
        csv_path = OUTPUT_DIR / csv_filename

        generator.export_to_csv(plan, str(csv_path))

        # Konvertera plan till JSON
        result = {
            'plan_name': plan.plan_name,
            'created_at': plan.created_at.isoformat(),
            'total_customers': plan.total_customers,
            'total_links': plan.total_links,
            'strategy_summary': plan.strategy_summary,
            'csv_file': csv_filename,
            'ai_prompt': ai_prompt,
            'ai_instructions': ai_instructions,
            'customers': []
        }

        for customer in plan.customers:
            customer_links = [l for l in plan.planned_links if l.customer_id == customer.customer_id]

            # Räkna anchor types
            anchor_counts = {}
            for link in customer_links:
                anchor_counts[link.anchor_type] = anchor_counts.get(link.anchor_type, 0) + 1

            result['customers'].append({
                'customer_id': customer.customer_id,
                'canonical_root': customer.canonical_root,
                'brand': customer.brand,
                'planned_links': customer.planned_links,
                'strategy': customer.recommended_strategy,
                'anchor_distribution': anchor_counts,
                'links': [
                    {
                        'target_url': l.target_url,
                        'anchor_text': l.anchor_text,
                        'anchor_type': l.anchor_type,
                        'priority_score': round(l.priority_score, 2),
                        'reasoning': l.reasoning
                    }
                    for l in customer_links[:10]  # Första 10 för preview
                ]
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Ladda ner en exporterad fil."""
    try:
        file_path = OUTPUT_DIR / filename
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Hämta övergripande statistik."""
    try:
        import sqlite3
        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row

        # Total statistik
        stats = con.execute("""
            SELECT 
                COUNT(DISTINCT c.id) as total_customers,
                COUNT(lh.id) as total_links,
                COUNT(DISTINCT lh.pub_domain) as unique_pub_domains,
                COUNT(DISTINCT lh.target_domain) as unique_target_domains
            FROM customers c
            LEFT JOIN links_history lh ON c.id = lh.customer_id
        """).fetchone()

        con.close()

        return jsonify({
            'total_customers': stats['total_customers'],
            'total_links': stats['total_links'],
            'unique_pub_domains': stats['unique_pub_domains'],
            'unique_target_domains': stats['unique_target_domains']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_ai_prompt(raw_planning_data, planning_data, ai_instructions):
    """Generera en AI-prompt för semantisk länkplanering."""
    
    # Hämta kundinfo
    con = sqlite3.connect(HISTORY_DB)
    con.row_factory = sqlite3.Row
    
    prompt_parts = []
    
    prompt_parts.append("# 🤖 LÄNKPLANERINGSPROMPT")
    prompt_parts.append("")
    prompt_parts.append("Du är en expert på SEO och länkbyggnad med djup förståelse för semantisk SEO och topical authority.")
    prompt_parts.append("")
    prompt_parts.append("## 📋 UPPGIFT:")
    prompt_parts.append("Generera en intelligent länkplan baserat på nedanstående data. För varje länk ska du:")
    prompt_parts.append("1. Analysera målsidan (om angiven) eller välj lämplig målsida från historik")
    prompt_parts.append("2. Generera semantiskt relevant ankartext (om inte angiven)")
    prompt_parts.append("3. Bestäm anchor type (exact, partial, branded, generic, lsi)")
    prompt_parts.append("4. Säkerställ naturlig anchor distribution enligt strategin")
    prompt_parts.append("5. Bygga topical authority där möjligt genom att länka relaterade sidor")
    prompt_parts.append("")
    
    if ai_instructions:
        prompt_parts.append("## 💡 SPECIELLA INSTRUKTIONER:")
        prompt_parts.append(ai_instructions)
        prompt_parts.append("")
    
    prompt_parts.append("## 📊 PLANERINGSDATA:")
    prompt_parts.append("")
    
    # Gruppera per kund
    customer_data = {}
    for key, item in raw_planning_data.items():
        if isinstance(item, dict):
            cid = item['customer_id']
            if cid not in customer_data:
                customer = con.execute("SELECT * FROM customers WHERE id = ?", (cid,)).fetchone()
                customer_data[cid] = {
                    'customer': customer,
                    'items': []
                }
            customer_data[cid]['items'].append(item)
    
    for cid, data in customer_data.items():
        customer = data['customer']
        items = data['items']
        
        prompt_parts.append(f"### Kund: {customer['canonical_root']} (Brand: {customer['brand']})")
        prompt_parts.append(f"- **Totalt länkar:** {sum(item['link_count'] for item in items)}")
        prompt_parts.append(f"- **Rekommenderad strategi:** {get_strategy_for_count(sum(item['link_count'] for item in items))}")
        prompt_parts.append("")
        
        # Hämta historisk data
        history_count = con.execute("SELECT COUNT(*) as cnt FROM links_history WHERE customer_id = ?", (cid,)).fetchone()['cnt']
        prompt_parts.append(f"- **Historik:** {history_count} länkar totalt")
        
        # Vanligaste ankartexter från historik
        common_anchors = con.execute("""
            SELECT anchor_text, COUNT(*) as cnt 
            FROM links_history 
            WHERE customer_id = ? AND anchor_text IS NOT NULL
            GROUP BY anchor_text 
            ORDER BY cnt DESC 
            LIMIT 5
        """, (cid,)).fetchall()
        
        if common_anchors:
            prompt_parts.append("- **Vanliga ankartexter i historik:**")
            for anchor in common_anchors:
                prompt_parts.append(f"  - \"{anchor['anchor_text']}\" ({anchor['cnt']}x)")
        
        prompt_parts.append("")
        prompt_parts.append("**Länkar att planera:**")
        
        for i, item in enumerate(items, 1):
            prompt_parts.append(f"{i}. **{item['link_count']} länkar** på **{item['pub_domain']}**")
            if item.get('target_url'):
                prompt_parts.append(f"   - Målsida: {item['target_url']}")
            if item.get('anchor_text'):
                prompt_parts.append(f"   - Ankartext: \"{item['anchor_text']}\"")
            prompt_parts.append("")
    
    con.close()
    
    prompt_parts.append("## 🎯 OUTPUT-FORMAT:")
    prompt_parts.append("För varje länk, ange:")
    prompt_parts.append("- Target URL")
    prompt_parts.append("- Anchor text")
    prompt_parts.append("- Anchor type (exact/partial/branded/generic/lsi)")
    prompt_parts.append("- Reasoning (kort förklaring av valet)")
    prompt_parts.append("")
    prompt_parts.append("## 📈 SEO-PRINCIPER ATT FÖLJA:")
    prompt_parts.append("1. **Natural Distribution:** Följ strategins anchor distribution")
    prompt_parts.append("2. **Semantic Relevance:** Ankartexter ska vara semantiskt relevanta för målsidan")
    prompt_parts.append("3. **Diversity:** Variera ankartexter även inom samma kategori")
    prompt_parts.append("4. **Topical Authority:** Länka relaterade sidor för att bygga authority")
    prompt_parts.append("5. **Avoid Over-Optimization:** Undvik för aggressiva exact match anchors")
    prompt_parts.append("")
    prompt_parts.append("---")
    prompt_parts.append("")
    prompt_parts.append("🚀 **BÖRJA PLANERINGEN NU!**")
    
    return "\n".join(prompt_parts)


def get_strategy_for_count(link_count):
    """Returnera strategi baserat på antal länkar."""
    if link_count == 1:
        return "single_focus"
    elif link_count <= 5:
        return "diversified_basics"
    elif link_count <= 15:
        return "semantic_foundation"
    elif link_count <= 30:
        return "topical_authority"
    else:
        return "enterprise_authority"


def self_correct_planning(suggestions, con):
    """
    Självkorrigerar planeringen innan den visas för användaren.

    Kontrollerar och fixar:
    1. Duplicerade pub_domains per kund
    2. För mycket exakt match på samma målsida
    3. Anchor text-variation
    4. Balans mellan olika målsidor
    5. Kvalitet på publiceringssajter
    """
    corrected_suggestions = []
    corrections_made = []

    for suggestion in suggestions:
        customer_id = suggestion['customer_id']
        canonical_root = suggestion['canonical_root']
        links = suggestion['links']

        # Räknare för självkorrigering
        pub_domain_usage = Counter()
        target_url_usage = Counter()
        anchor_text_usage = Counter()

        corrected_links = []

        for link in links:
            pub_domain = link['pub_domain']
            target_url = link.get('target_url')
            anchor_text = link.get('anchor_text')

            # REGEL 1: Undvik att använda samma pub_domain mer än 2 gånger per kund
            if pub_domain_usage[pub_domain] >= 2:
                # Hitta alternativ pub_domain
                alternative_pubs = con.execute("""
                    SELECT pub_domain, COUNT(*) as cnt
                    FROM links_history
                    WHERE customer_id = ? AND pub_domain IS NOT NULL
                    AND pub_domain != ?
                    GROUP BY pub_domain
                    ORDER BY cnt DESC
                    LIMIT 5
                """, (customer_id, pub_domain)).fetchall()

                for alt_pub in alternative_pubs:
                    if pub_domain_usage[alt_pub['pub_domain']] < 2:
                        old_pub = pub_domain
                        pub_domain = alt_pub['pub_domain']
                        corrections_made.append(
                            f"{canonical_root}: Bytte pub_domain från {old_pub} till {pub_domain} (undviker överanvändning)"
                        )
                        break

            pub_domain_usage[pub_domain] += 1

            # REGEL 2: Variera målsidor - max 3 länkar till samma URL
            if target_url and target_url_usage[target_url] >= 3:
                # Hitta alternativ målsida
                alternative_targets = con.execute("""
                    SELECT target_url, COUNT(*) as cnt
                    FROM links_history
                    WHERE customer_id = ? AND target_url IS NOT NULL
                    AND target_url != ?
                    GROUP BY target_url
                    ORDER BY cnt DESC
                    LIMIT 5
                """, (customer_id, target_url)).fetchall()

                for alt_target in alternative_targets:
                    if target_url_usage[alt_target['target_url']] < 3:
                        old_target = target_url
                        target_url = alt_target['target_url']
                        corrections_made.append(
                            f"{canonical_root}: Bytte målsida för bättre variation (undviker över-optimering)"
                        )
                        break

            if target_url:
                target_url_usage[target_url] += 1

            # REGEL 3: Undvik exakt samma ankartext mer än 2 gånger
            if anchor_text and anchor_text_usage[anchor_text] >= 2:
                # Hitta alternativ ankartext
                alternative_anchors = con.execute("""
                    SELECT anchor_text, COUNT(*) as cnt
                    FROM links_history
                    WHERE customer_id = ? AND anchor_text IS NOT NULL
                    AND anchor_text != ?
                    GROUP BY anchor_text
                    ORDER BY cnt DESC
                    LIMIT 10
                """, (customer_id, anchor_text)).fetchall()

                for alt_anchor in alternative_anchors:
                    if anchor_text_usage[alt_anchor['anchor_text']] < 2:
                        old_anchor = anchor_text
                        anchor_text = alt_anchor['anchor_text']
                        corrections_made.append(
                            f"{canonical_root}: Varierade ankartext från '{old_anchor}' till '{anchor_text}'"
                        )
                        break

            if anchor_text:
                anchor_text_usage[anchor_text] += 1

            # Lägg till korrigerad länk
            corrected_links.append({
                'customer_id': customer_id,
                'pub_domain': pub_domain,
                'target_url': target_url,
                'anchor_text': anchor_text
            })

        # REGEL 4: Säkerställ minimum variation
        unique_pubs = len(set(l['pub_domain'] for l in corrected_links))
        unique_targets = len(set(l['target_url'] for l in corrected_links if l['target_url']))
        unique_anchors = len(set(l['anchor_text'] for l in corrected_links if l['anchor_text']))

        total_links = len(corrected_links)

        # Om för lite variation, logga varning
        if total_links > 5:
            if unique_pubs < total_links * 0.5:  # Mindre än 50% unika pub_domains
                corrections_made.append(
                    f"{canonical_root}: ⚠️ Låg variation på pub_domains ({unique_pubs}/{total_links})"
                )
            if unique_targets > 0 and unique_targets < min(3, total_links * 0.4):
                corrections_made.append(
                    f"{canonical_root}: ⚠️ Låg variation på målsidor ({unique_targets}/{total_links})"
                )

        corrected_suggestions.append({
            'customer_id': customer_id,
            'canonical_root': canonical_root,
            'brand': suggestion['brand'],
            'suggested_count': len(corrected_links),
            'links': corrected_links,
            'quality_metrics': {
                'unique_pub_domains': unique_pubs,
                'unique_target_urls': unique_targets,
                'unique_anchors': unique_anchors,
                'variation_score': round((unique_pubs + unique_targets + unique_anchors) / (total_links * 3) * 100, 1)
            }
        })

    return corrected_suggestions, corrections_made


@app.route('/api/load-november-plan', methods=['POST'])
def load_november_plan():
    """Laddar november_plan.csv och analyserar per kund för AI-agents."""
    try:
        # Läs november_plan.csv
        csv_path = BASE_DIR / "november_plan.csv"

        if not csv_path.exists():
            return jsonify({'error': 'november_plan.csv saknas'}), 404

        df = pd.read_csv(csv_path)
        df = df.dropna(how='all')  # Ta bort helt tomma rader

        # Gruppera per kund
        customer_plans = {}

        for idx, row in df.iterrows():
            pub_domain = str(row.get('publication_domain', '')).strip()
            customer = str(row.get('kund_brand', '')).strip()
            market = str(row.get('market', 'SE')).strip()
            target_url = str(row.get('target_url', '')).strip()
            anchor = str(row.get('link_anchor', '')).strip()

            if not pub_domain or not customer or customer == 'nan':
                continue

            needs_target = not target_url or target_url == 'nan' or target_url == ''
            needs_anchor = not anchor or anchor == 'nan' or anchor == ''

            if customer not in customer_plans:
                customer_plans[customer] = []

            customer_plans[customer].append({
                'row_index': int(idx),
                'pub_domain': pub_domain,
                'market': market,
                'target_url': target_url if not needs_target else None,
                'anchor': anchor if not needs_anchor else None,
                'needs_target': needs_target,
                'needs_anchor': needs_anchor
            })

        # Analysera varje kund med historik från databas
        con = sqlite3.connect(HISTORY_DB)
        con.row_factory = sqlite3.Row

        customer_analyses = []

        for customer_name, links in customer_plans.items():
            # Hitta customer_id
            customer = con.execute(
                "SELECT id, canonical_root, brand FROM customers WHERE canonical_root LIKE ? OR brand LIKE ?",
                (f'%{customer_name}%', f'%{customer_name}%')
            ).fetchone()

            if not customer:
                customer_analyses.append({
                    'customer_name': customer_name,
                    'status': 'not_found',
                    'total_links': len(links),
                    'needs_target': sum(1 for l in links if l['needs_target']),
                    'needs_anchor': sum(1 for l in links if l['needs_anchor'])
                })
                continue

            customer_id = customer['id']

            # Hämta historisk data
            common_targets = con.execute("""
                SELECT target_url, COUNT(*) as cnt
                FROM links_history
                WHERE customer_id = ? AND target_url IS NOT NULL
                GROUP BY target_url
                ORDER BY cnt DESC
                LIMIT 10
            """, (customer_id,)).fetchall()

            common_anchors = con.execute("""
                SELECT anchor_text, COUNT(*) as cnt
                FROM links_history
                WHERE customer_id = ? AND anchor_text IS NOT NULL
                GROUP BY anchor_text
                ORDER BY cnt DESC
                LIMIT 20
            """, (customer_id,)).fetchall()

            customer_analyses.append({
                'customer_name': customer_name,
                'customer_id': customer_id,
                'canonical_root': customer['canonical_root'],
                'brand': customer['brand'],
                'status': 'ready',
                'links': links,
                'total_links': len(links),
                'needs_target': sum(1 for l in links if l['needs_target']),
                'needs_anchor': sum(1 for l in links if l['needs_anchor']),
                'needs_both': sum(1 for l in links if l['needs_target'] and l['needs_anchor']),
                'markets': list(set(l['market'] for l in links)),
                'common_targets': [dict(t) for t in common_targets],
                'common_anchors': [dict(a) for a in common_anchors]
            })

        con.close()

        return jsonify({
            'total_customers': len(customer_analyses),
            'customers': customer_analyses,
            'total_links': sum(c.get('total_links', 0) for c in customer_analyses),
            'total_needs_target': sum(c.get('needs_target', 0) for c in customer_analyses),
            'total_needs_anchor': sum(c.get('needs_anchor', 0) for c in customer_analyses)
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-customer-agent-prompt', methods=['POST'])
def generate_customer_agent_prompt():
    """Genererar en AI-agent prompt för en specifik kund."""
    try:
        data = request.get_json()
        customer_data = data.get('customer')

        if not customer_data:
            return jsonify({'error': 'Customer data required'}), 400

        # Bygg AI-prompt för denna kund
        prompt = generate_customer_specific_agent_prompt(customer_data)

        return jsonify({
            'customer_name': customer_data['customer_name'],
            'prompt': prompt,
            'links_to_process': customer_data['total_links'],
            'needs_target': customer_data['needs_target'],
            'needs_anchor': customer_data['needs_anchor']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def generate_customer_specific_agent_prompt(customer_data):
    """Genererar en specifik AI-agent prompt för en kund."""

    prompt_parts = []

    prompt_parts.append(f"# 🤖 AI-AGENT FÖR {customer_data['customer_name'].upper()}")
    prompt_parts.append("")
    prompt_parts.append("Du är en specialist-agent för länkplanering, dedikerad till denna specifika kund.")
    prompt_parts.append("")

    prompt_parts.append("## 📊 KUNDINFORMATION:")
    prompt_parts.append(f"- **Kund:** {customer_data['customer_name']}")
    prompt_parts.append(f"- **Canonical Root:** {customer_data.get('canonical_root', 'N/A')}")
    prompt_parts.append(f"- **Brand:** {customer_data.get('brand', 'N/A')}")
    prompt_parts.append(f"- **Marknader:** {', '.join(customer_data.get('markets', ['SE']))}")
    prompt_parts.append("")

    prompt_parts.append("## 🎯 UPPGIFT:")
    prompt_parts.append(f"Du ska komplettera **{customer_data['total_links']} länkar** för november 2025:")
    prompt_parts.append(f"- **{customer_data['needs_target']} länkar** behöver målsida")
    prompt_parts.append(f"- **{customer_data['needs_anchor']} länkar** behöver ankartext")
    prompt_parts.append(f"- **{customer_data.get('needs_both', 0)} länkar** behöver både målsida och ankartext")
    prompt_parts.append("")

    if customer_data.get('common_targets'):
        prompt_parts.append("## 🎯 HISTORISKA MÅLSIDOR (vanligaste):")
        for target in customer_data['common_targets'][:5]:
            prompt_parts.append(f"- {target['target_url']} ({target['cnt']}x använd)")
        prompt_parts.append("")

    if customer_data.get('common_anchors'):
        prompt_parts.append("## 📝 HISTORISKA ANKARTEXTER (vanligaste):")
        for anchor in customer_data['common_anchors'][:10]:
            prompt_parts.append(f"- \"{anchor['anchor_text']}\" ({anchor['cnt']}x använd)")
        prompt_parts.append("")

    prompt_parts.append("## 📋 LÄNKAR ATT KOMPLETTERA:")
    prompt_parts.append("")

    for idx, link in enumerate(customer_data.get('links', []), 1):
        prompt_parts.append(f"### Länk {idx}:")
        prompt_parts.append(f"- **Pub Domain:** {link['pub_domain']}")
        prompt_parts.append(f"- **Marknad:** {link['market']}")

        if link.get('target_url'):
            prompt_parts.append(f"- **Target URL:** {link['target_url']} ✅")
        else:
            prompt_parts.append(f"- **Target URL:** BEHÖVER SÄTTAS ❌")

        if link.get('anchor'):
            prompt_parts.append(f"- **Anchor:** \"{link['anchor']}\" ✅")
        else:
            prompt_parts.append(f"- **Anchor:** BEHÖVER SÄTTAS ❌")

        prompt_parts.append("")

    prompt_parts.append("## 📐 REGLER:")
    prompt_parts.append("1. **Målsidor:** Välj från historiska målsidor eller skapa nya som matchar kundens domän")
    prompt_parts.append("2. **Ankartexter:** Skapa naturliga, varierade ankartexter (exact/partial/branded/LSI)")
    prompt_parts.append("3. **Variation:** Undvik att upprepa samma ankartext för många gånger")
    prompt_parts.append("4. **Marknad:** Anpassa språk efter marknad (SE=svenska, UK/US=engelska, DK=danska)")
    prompt_parts.append("5. **SEO-säkerhet:** Följ natural anchor distribution")
    prompt_parts.append("")

    prompt_parts.append("## 📤 OUTPUT-FORMAT:")
    prompt_parts.append("För varje länk, returnera:")
    prompt_parts.append("```json")
    prompt_parts.append("{")
    prompt_parts.append('  "link_index": 1,')
    prompt_parts.append('  "target_url": "https://...",')
    prompt_parts.append('  "anchor_text": "...",')
    prompt_parts.append('  "anchor_type": "partial/exact/branded/lsi",')
    prompt_parts.append('  "reasoning": "Kort förklaring"')
    prompt_parts.append("}")
    prompt_parts.append("```")
    prompt_parts.append("")
    prompt_parts.append("🚀 **BÖRJA KOMPLETTERA LÄNKARNA NU!**")

    return "\n".join(prompt_parts)


@app.route('/api/mainsheet', methods=['GET'])
def get_mainsheet():
    """Hämta data från main_sheet.xlsx."""
    try:
        search = request.args.get('search', '').lower()
        column = request.args.get('column', '')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        # Läs main_sheet.xlsx
        main_sheet_path = BASE_DIR / "data" / "input" / "main_sheet.xlsx"

        if not main_sheet_path.exists():
            return jsonify({'error': 'main_sheet.xlsx saknas'}), 404

        df = pd.read_excel(main_sheet_path)

        # Filtrera om sökning finns
        if search:
            if column and column in df.columns:
                # Sök i specifik kolumn
                mask = df[column].astype(str).str.lower().str.contains(search, na=False)
                df_filtered = df[mask]
            else:
                # Sök i alla kolumner
                mask = df.astype(str).apply(lambda x: x.str.lower().str.contains(search, na=False)).any(axis=1)
                df_filtered = df[mask]
        else:
            df_filtered = df

        # Statistik
        total_rows = len(df)
        filtered_rows = len(df_filtered)
        unique_customers = df_filtered['canonical_root'].nunique() if 'canonical_root' in df_filtered.columns else 0

        # Paginering
        df_page = df_filtered.iloc[offset:offset+limit]

        # Konvertera till records
        records = []
        for idx, row in df_page.iterrows():
            records.append({
                'index': int(idx),
                'canonical_root': str(row.get('canonical_root', '')),
                'root_url': str(row.get('Root URL', '')),
                'pub_page_url': str(row.get('pub_page_url', '')),
                'target_url': str(row.get('target_url', '')),
                'anchor_text': str(row.get('anchor_text', '')),
                'brand': str(row.get('brand', '')),
                'link_type': str(row.get('link_type', '')),
                'language': str(row.get('language', '')),
                'published_at': str(row.get('published_at', ''))
            })

        return jsonify({
            'records': records,
            'total': total_rows,
            'filtered': filtered_rows,
            'unique_customers': unique_customers,
            'showing': len(records),
            'offset': offset,
            'limit': limit,
            'has_more': (offset + limit) < filtered_rows
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 LINK PLANNING GUI - Starting...")
    print("="*70)
    print(f"\n📁 Database: {HISTORY_DB}")
    print(f"📁 Customers: {CUSTOMERS_DIR}")
    print(f"\n🌐 Opening browser at: http://127.0.0.1:5000")
    print("\n💡 Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

