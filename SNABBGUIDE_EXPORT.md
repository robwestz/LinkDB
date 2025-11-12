# Snabbguide: Exportera till Airtable

## Enkel export (alla kunder)

```bash
python export_to_airtable_csv.py
```

eller

```bash
run_export.bat
```

Detta skapar 4 CSV-filer i `data/output/airtable_export/`:
- `customers_[datum].csv` - Alla kunder
- `links_[datum].csv` - Alla länkar
- `priority_pages_[datum].csv` - Alla prioriterade sidor
- `summary_[datum].csv` - Sammanfattning

## Avancerad export (välj specifika kunder)

### Interaktivt läge
```bash
python export_advanced.py
```

### Lista alla kunder
```bash
python export_advanced.py --list
```

### Exportera specifika kunder (nummer 1, 3, och 5-10)
```bash
python export_advanced.py --customers "1,3,5-10"
```

### Exportera alla kunder med specifikt varumärke
```bash
python export_advanced.py --brand "Happy Socks"
```

### Exportera alla kunder med domänmönster
```bash
python export_advanced.py --domain ".se"
```

### Exportera alla kunder (samma som enkel export)
```bash
python export_advanced.py --all
```

## Importera till Airtable

1. Gå till din Airtable Base
2. Klicka på "+" för att lägga till ny tabell
3. Välj "Import" → "CSV file"
4. Ladda upp CSV-filen
5. Bekräfta kolumntyper
6. Klart!

### Tips:
- Importera `customers_[datum].csv` först
- Sedan `links_[datum].csv` och länka Customer_ID till Customers-tabellen
- Slutligen `priority_pages_[datum].csv`

## Var finns exporterade filer?

```
data/output/airtable_export/
```

## Kolumntyper för Airtable

### Customers
- Database_ID → Number
- Canonical_Root → Single line text
- Brand → Single line text
- Total_Links → Number

### Links
- Link_ID → Number
- Customer_ID → Linked Record (till Customers)
- Pub_Page_URL → URL
- Target_URL → URL
- Anchor_Text → Long text
- Published_At → Date

### Priority Pages
- Page_ID → Number
- URL → URL
- Priority_Score → Number
- Customer_Name → Linked Record (till Customers)

## Felsökning

**Problem:** "No customer databases found"
**Lösning:** Kör först `python app/build_all_customer_dbs.py`

**Problem:** Svenska tecken syns konstigt
**Lösning:** Filerna använder UTF-8 med BOM, vilket fungerar i Airtable

**Problem:** Filen är för stor för Airtable (>5MB)
**Lösning:** Använd `export_advanced.py` för att exportera färre kunder åt gången

## Exempel

Exportera alla .se-domäner:
```bash
python export_advanced.py --domain ".se"
```

Exportera kunder 1-50:
```bash
python export_advanced.py --customers "1-50"
```

Exportera alla "Casino"-relaterade kunder:
```bash
python export_advanced.py --brand "casino"
```

