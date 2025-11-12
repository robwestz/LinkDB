# Airtable CSV Export Tool

## Översikt
Detta verktyg exporterar alla kunddatabaser till CSV-filer som är redo att importeras till Airtable.

## Användning

### Alternativ 1: Kör direkt med Python
```bash
python export_to_airtable_csv.py
```

### Alternativ 2: Kör batch-filen (Windows)
```bash
run_export.bat
```

## Vad exporteras?

Skriptet skapar fyra CSV-filer i `data/output/airtable_export/`:

### 1. customers_[timestamp].csv
Innehåller alla kunder med följande kolumner:
- **Database_ID**: Internt ID för kunden
- **Canonical_Root**: Kundens huvuddomän
- **Brand**: Varumärke/företagsnamn
- **Directory_Name**: Mappnamn där kundens databas finns
- **Created_At**: När kunden skapades
- **Total_Links**: Totalt antal länkar för kunden
- **Unique_Pub_Domains**: Antal unika publiceringsdomäner

### 2. links_[timestamp].csv
Innehåller alla länkar från alla kunder med följande kolumner:
- **Link_ID**: Unikt ID för länken
- **Customer_ID**: ID för kunden som länken tillhör
- **Customer_Name**: Mappnamn för kunden
- **Canonical_Root**: Kundens huvuddomän
- **Brand**: Kundens varumärke
- **Pub_Page_URL**: URL till sidan där länken publicerades
- **Pub_Domain**: Domän där länken publicerades
- **Target_URL**: Länkens målsida
- **Target_Domain**: Måldomän för länken
- **Anchor_Text**: Länktext
- **Link_Type**: Typ av länk (t.ex. dofollow, nofollow)
- **Language**: Språk
- **Published_At**: När länken publicerades
- **Topic_Tags**: Ämnestaggar
- **Context_Excerpt**: Textutdrag från kontexten
- **Anchor_Type**: Typ av ankartext
- **Created_At**: När länken skapades i systemet

### 3. priority_pages_[timestamp].csv
Innehåller prioriterade sidor från alla kunder med följande kolumner:
- **Page_ID**: Unikt ID för sidan
- **Customer_Name**: Mappnamn för kunden
- **Canonical_Root**: Kundens huvuddomän
- **Brand**: Kundens varumärke
- **URL**: Sidans URL
- **Priority_Score**: Prioritetspoäng (högre = viktigare)
- **Intent**: Sidans intent/syfte
- **Keywords**: Nyckelord kopplade till sidan

### 4. summary_[timestamp].csv
Sammanfattande statistik för hela exporten:
- Export Date
- Total Customers
- Total Links
- Total Priority Pages
- Unique Publishing Domains

## Importera till Airtable

### Steg-för-steg guide:

1. **Skapa en ny Base i Airtable** eller använd en befintlig

2. **Importera Customers-tabellen:**
   - Skapa en ny tabell eller använd befintlig
   - Klicka på "+" för att lägga till data
   - Välj "Import" → "CSV file"
   - Ladda upp `customers_[timestamp].csv`
   - Airtable kommer automatiskt att skapa kolumner baserat på CSV-headern

3. **Importera Links-tabellen:**
   - Upprepa samma process med `links_[timestamp].csv`
   - **Tips:** Länka Customer_ID till Customers-tabellen för relationer

4. **Importera Priority Pages-tabellen:**
   - Upprepa samma process med `priority_pages_[timestamp].csv`

5. **Skapa relationer mellan tabeller:**
   - I Links-tabellen, konvertera Customer_ID till en "Linked Record" som pekar på Customers
   - Detta gör det möjligt att se alla länkar för en specifik kund

## Kolumntyper i Airtable (rekommendationer)

### Customers-tabellen:
- Database_ID: Number
- Canonical_Root: Single line text
- Brand: Single line text
- Directory_Name: Single line text
- Created_At: Date
- Total_Links: Number
- Unique_Pub_Domains: Number

### Links-tabellen:
- Link_ID: Number
- Customer_ID: Linked Record (till Customers)
- Pub_Page_URL: URL
- Target_URL: URL
- Anchor_Text: Long text
- Link_Type: Single select
- Language: Single select
- Published_At: Date
- Topic_Tags: Multiple select (eller Long text)
- Context_Excerpt: Long text

### Priority Pages-tabellen:
- Page_ID: Number
- Customer_Name: Linked Record (till Customers)
- URL: URL
- Priority_Score: Number
- Intent: Single select
- Keywords: Long text (eller Multiple select)

## Filformat

- **Encoding**: UTF-8 med BOM (för korrekt visning av svenska tecken)
- **Delimiter**: Komma (,)
- **Line endings**: Windows-stil (CRLF)
- **Quotes**: Fält med kommatecken eller radbrytningar är quoted

## Felsökning

### Problem: "No customer databases found"
**Lösning:** Kontrollera att `data/output/customers/` innehåller kunddatabaser och att varje kundmapp har en `customer.db` fil.

### Problem: Svenska tecken visas inte korrekt i Airtable
**Lösning:** Filen använder UTF-8 med BOM. Om problem kvarstår:
1. Öppna CSV-filen i Excel
2. Spara som "CSV UTF-8 (Comma delimited)"
3. Importera den nya filen till Airtable

### Problem: För stor fil för Airtable
**Lösning:** Airtable har en gräns på 5MB per import. Om `links_[timestamp].csv` är för stor:
1. Dela upp filen manuellt i mindre delar
2. Eller använd Airtable's API för större importer

## Tekniska detaljer

- **Programmeringsspråk**: Python 3.8+
- **Beroenden**: sqlite3 (inbyggd), csv (inbyggd), pathlib (inbyggd), rich (för formaterad output)
- **Databas**: SQLite
- **Prestanda**: Hanterar tusentals kunder och miljontals länkar

## Uppdateringar och underhåll

För att uppdatera skriptet eller lägga till fler exportfunktioner, redigera `export_to_airtable_csv.py`.

## Support

Vid problem, kontrollera:
1. Att alla kunddatabaser finns i `data/output/customers/`
2. Att Python 3.8+ är installerat
3. Att `rich`-paketet är installerat: `pip install rich`

## Exempel på output

```
═══════════════════════════════════════════════
  Airtable CSV Export Tool
═══════════════════════════════════════════════

Found 234 customer databases

✓ Exported customers to: customers_20250205_143022.csv
✓ Exported 15,432 links to: links_20250205_143022.csv
✓ Exported 2,808 priority pages to: priority_pages_20250205_143022.csv
✓ Exported summary statistics to: summary_20250205_143022.csv

═══════════════════════════════════════════════
  Export Complete!
═══════════════════════════════════════════════

All files exported to: data\output\airtable_export

Files created:
  • customers_20250205_143022.csv
  • links_20250205_143022.csv
  • priority_pages_20250205_143022.csv
  • summary_20250205_143022.csv
```

