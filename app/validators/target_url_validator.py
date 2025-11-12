"""
Target URL Validator - Kontrollerar att målsidor matchar kundens domän
"""
from pathlib import Path
import sqlite3
import pandas as pd

def validate_target_urls(planning_data, client_index_path):
    """
    Validerar att alla target_urls börjar med kundens client_domain.

    Args:
        planning_data: Dict med planering
        client_index_path: Path till client_index_matched.xlsx

    Returns:
        validation_results: Dict med resultat
        errors: Lista med fel
    """
    # Ladda client_index
    if not Path(client_index_path).exists():
        return {'valid': False, 'errors': ['Client index saknas']}

    client_index = pd.read_excel(client_index_path)
    client_domains = {}

    for _, row in client_index.iterrows():
        if pd.notna(row.get('customer_id')) and pd.notna(row.get('client_domain')):
            client_domains[int(row['customer_id'])] = row['client_domain'].strip()

    # Validera varje länk
    errors = []
    warnings = []
    valid_count = 0
    total_count = 0

    for key, item in planning_data.items():
        if not isinstance(item, dict):
            continue

        customer_id = item.get('customer_id')
        target_url = item.get('target_url')

        if not target_url:
            # Ingen målsida angiven - OK, ska fyllas i senare
            continue

        total_count += 1

        # Hämta kundens client_domain
        client_domain = client_domains.get(customer_id)

        if not client_domain:
            warnings.append(f"Kund ID {customer_id}: Saknas i client_index")
            continue

        # Normalisera URLs
        target_clean = target_url.lower().replace('http://', '').replace('https://', '').replace('www.', '')
        domain_clean = client_domain.lower().replace('http://', '').replace('https://', '').replace('www.', '')

        # Kontrollera om target_url börjar med client_domain
        if not target_clean.startswith(domain_clean):
            errors.append(f"Kund ID {customer_id}: Target URL '{target_url}' matchar inte domän '{client_domain}'")
        else:
            valid_count += 1

    return {
        'valid': len(errors) == 0,
        'total_checked': total_count,
        'valid_count': valid_count,
        'error_count': len(errors),
        'warning_count': len(warnings),
        'errors': errors,
        'warnings': warnings
    }


if __name__ == '__main__':
    # Test
    base_dir = Path(__file__).parent.parent
    client_index_path = base_dir / 'data' / 'client_index_matched.xlsx'

    # Exempel planering
    test_planning = {
        'test_1': {
            'customer_id': 117,  # bethard.com
            'target_url': 'https://bethard.com/sv/sports',
            'pub_domain': 'example.com'
        },
        'test_2': {
            'customer_id': 117,
            'target_url': 'https://wrong-domain.com/page',  # FELAKTIG!
            'pub_domain': 'example.com'
        },
        'test_3': {
            'customer_id': 110,  # cherry.com
            'target_url': 'https://cherry.com/sv/casino',
            'pub_domain': 'example.com'
        }
    }

    result = validate_target_urls(test_planning, client_index_path)

    print("="*70)
    print("TARGET URL VALIDERING - TEST")
    print("="*70)
    print(f"Valid: {result['valid']}")
    print(f"Totalt kontrollerade: {result['total_checked']}")
    print(f"Giltiga: {result['valid_count']}")
    print(f"Fel: {result['error_count']}")
    print(f"Varningar: {result['warning_count']}")

    if result['errors']:
        print("\nFel:")
        for error in result['errors']:
            print(f"  ❌ {error}")

    if result['warnings']:
        print("\nVarningar:")
        for warning in result['warnings']:
            print(f"  ⚠️ {warning}")

