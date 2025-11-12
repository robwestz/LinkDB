"""
Hämta customer_id för lista av kundnamn
"""
import sqlite3
from pathlib import Path

# Kundlista
customers = """
Acnespecialisten
Aerius Ventilation
4him4her
Cdbilvård
A Retro Tale
Dryft
Ekström & Garay
Arctic
Bergets-Ro
OptiOne
Optitech Sverige
Bethard
Chattanoogarehab
Seniorabatt
Cherry
comfydence.se
Crystal Beverage Company
D-Bet
Discountsover60
Distansinstitutet
Epidemic Sounds
Fair Investments
Flax Casino
Hajper.com
Vardagsfrid
Happy Casino
Himala.ai
Jakt.se
Indoorprofessional
Kelleher International
Kleer
Kungaslottet
KvarnX
Lansfast
Jour Eliten
Coface
Cateringfabriken.se
Casinogringo
Låsjouren
Rörjour247
Leaptodigital
Leovegas
Lilla-Världen
LSB
Oljedroppen.se
Lucky Casino
Pontech
Pontonhamnar
Snuset
Nettotobak
Mäklarringen
Tiger Of Sweden
Upplevelse.com
Megariches
Svenskafonster
Mockfjärds
Petster.se
Ataraxia
CDG
Merchoteket
MrNicco
Nodeposit
Michaelofrisorerna
Kamux
Minifinder
MrVegas
Clearfuze
Racha Organics, Inc
MyNicco (US)
Nbi Nordic Beauty Import Oy
Nordic Knots
NorthTracker
Socialcatfish
Mobot
Bettingsyndikatet
Purakliniken
Rusta
SvenskIPTV
Säkra rör AB
Sesec
Glassfactory
Spelklubben
Tandea (Haninge)
Standupsverige
Startmotor
Flygbussarna
Bus4You
Ekonomico
Sthlm Physique
Invozio
Stockholm Rör & VVS
Striveon
Supernormal
Sweden Longstay
Swedoffice
Tandea
Tandlakare.se
Zmarta Finland
Bokahandyman
Flyttgaranti
Snickare.online
Technobark
Technomeow
Tiotak
TKW
Tryggbil
Turner.fi
Videoslots
Villasandudden.se
Violamilano
Wellio
Willabgarden
Yourgild
Zmarta Sverige
T2H Rakkenus
Lessworries.com
Vera&John
Florister I Sverige
Mynt.com
""".strip().split('\n')

# Connect to database
base_dir = Path(__file__).parent
db_path = base_dir / "data" / "output" / "linkops_history.db"

con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row

results = []

print("="*80)
print("CUSTOMER_ID MATCHNING")
print("="*80)
print()

for customer_name in customers:
    customer_name = customer_name.strip()
    if not customer_name:
        continue

    # Try multiple methods to find customer
    customer = None

    # Method 1: Exact match on canonical_root
    customer = con.execute(
        "SELECT id, canonical_root, brand FROM customers WHERE canonical_root = ?",
        (customer_name,)
    ).fetchone()

    # Method 2: LIKE match on canonical_root
    if not customer:
        customer = con.execute(
            "SELECT id, canonical_root, brand FROM customers WHERE canonical_root LIKE ?",
            (f'%{customer_name}%',)
        ).fetchone()

    # Method 3: LIKE match on brand
    if not customer:
        customer = con.execute(
            "SELECT id, canonical_root, brand FROM customers WHERE brand LIKE ?",
            (f'%{customer_name}%',)
        ).fetchone()

    # Method 4: Fuzzy match - remove common suffixes
    if not customer:
        clean_name = customer_name.replace('.com', '').replace('.se', '').replace('.no', '').replace('.fi', '').replace('.io', '')
        customer = con.execute(
            "SELECT id, canonical_root, brand FROM customers WHERE canonical_root LIKE ? OR brand LIKE ?",
            (f'%{clean_name}%', f'%{clean_name}%')
        ).fetchone()

    if customer:
        results.append({
            'customer_name': customer_name,
            'customer_id': customer['id'],
            'canonical_root': customer['canonical_root'],
            'brand': customer['brand']
        })
        print(f"✓ {customer_name:<40} → {customer['id']:<5} ({customer['canonical_root']})")
    else:
        results.append({
            'customer_name': customer_name,
            'customer_id': None,
            'canonical_root': None,
            'brand': None
        })
        print(f"✗ {customer_name:<40} → INTE HITTAD")

con.close()

# Create output files
print()
print("="*80)
print("RESULTAT")
print("="*80)

matched = sum(1 for r in results if r['customer_id'] is not None)
not_found = sum(1 for r in results if r['customer_id'] is None)

print(f"Matchade: {matched}")
print(f"Ej funna: {not_found}")
print()

# Create CSV for Google Sheets
output_csv = base_dir / "data" / "customer_id_mapping.csv"
with open(output_csv, 'w', encoding='utf-8') as f:
    f.write("Kund,customer_id,canonical_root,brand\n")
    for r in results:
        cid = r['customer_id'] if r['customer_id'] is not None else ''
        root = r['canonical_root'] if r['canonical_root'] else ''
        brand = r['brand'] if r['brand'] else ''
        f.write(f'"{r["customer_name"]}",{cid},"{root}","{brand}"\n')

print(f"Sparad CSV: {output_csv}")
print()

# Print not found for easy copy
if not_found > 0:
    print("="*80)
    print("EJ FUNNA KUNDER (måste läggas till i databasen eller korrigeras):")
    print("="*80)
    for r in results:
        if r['customer_id'] is None:
            print(f"  - {r['customer_name']}")
    print()

# Print matched for Google Sheets
print("="*80)
print("MATCHADE - KOPIERA TILL GOOGLE SHEETS:")
print("="*80)
print("Kund\tcustomer_id\tcanonical_root")
for r in results:
    if r['customer_id'] is not None:
        print(f"{r['customer_name']}\t{r['customer_id']}\t{r['canonical_root']}")

