# Google Sheets Integration Setup

## 📝 Vad du kan göra NU (utan setup):

✅ **Lägg till länkar manuellt** - Fungerar direkt!
- Välj kund
- Ange publiceringssajt (obligatoriskt)
- Valfri målsida och ankartext
- Klicka "Lägg till"

---

## 🔧 För att aktivera Google Sheets import:

### Steg 1: Skapa Google Cloud Project

1. Gå till: https://console.cloud.google.com/
2. Skapa nytt projekt (eller välj befintligt)
3. Namnge projektet (t.ex. "LinkDB Integration")

### Steg 2: Aktivera Google Sheets API

1. I Cloud Console, gå till **APIs & Services > Library**
2. Sök efter "Google Sheets API"
3. Klicka på det och välj **Enable**

### Steg 3: Skapa Service Account

1. Gå till **APIs & Services > Credentials**
2. Klicka **Create Credentials > Service Account**
3. Namnge den (t.ex. "linkdb-sheets-reader")
4. Klicka **Create and Continue**
5. Hoppa över "Grant access" (klicka Continue)
6. Klicka **Done**

### Steg 4: Skapa och ladda ner nyckel

1. Klicka på din nya Service Account
2. Gå till fliken **Keys**
3. Klicka **Add Key > Create new key**
4. Välj **JSON**
5. Klicka **Create**
6. En `credentials.json` fil laddas ner

### Steg 5: Placera credentials-filen

1. Flytta `credentials.json` till:
   ```
   C:\Users\robin\PycharmProjects\linkdb\credentials.json
   ```

### Steg 6: Dela Google Sheet

1. Öppna din credentials.json fil
2. Kopiera `client_email` värdet (ser ut som xxx@yyy.iam.gserviceaccount.com)
3. Gå till ditt Google Sheet
4. Klicka **Share**
5. Klistra in service account email
6. Ge **Viewer** access
7. Klicka **Send**

### Steg 7: Testa!

1. Starta om GUI-servern
2. Gå till Planering-fliken
3. Sheets URL är redan ifylld
4. Ändra "Sheet namn" till din flik (t.ex. "November")
5. Klicka **📥 Importera**

---

## 📊 Format på Google Sheet:

GUI:n förväntar sig dessa kolumner:

| Kolumn | Beskrivning | Exempel |
|--------|-------------|---------|
| **Domain** | Publiceringssajt | kingsizemag.se |
| **Kund** | Kundnamn/brand | bethard.com |
| **Targeting URL** eller **IsCustomer** | Målsida (valfri) | https://bethard.com/sv/sports |
| **Anchor** | Ankartext (valfri) | betting på fotboll |

### Exempel:

```
Domain              | Kund          | Targeting URL                      | Anchor
--------------------|---------------|------------------------------------|-----------------
kingsizemag.se      | bethard.com   | https://bethard.com/sv/sports     | odds på sport
djungeltrumman.se   | bethard.com   | https://bethard.com/sv/casino     | casino bonus
example.com         | cherry.com    |                                    | 
```

---

## ⚠️ Troubleshooting

### Problem: "Google Sheets credentials saknas"
**Lösning:** Följ steg 1-5 ovan

### Problem: "Permission denied"
**Lösning:** 
- Kontrollera att du delat sheetet med service account email
- Kolla att emailen är korrekt kopierad

### Problem: "Worksheet not found"
**Lösning:**
- Kontrollera att sheet-namnet stämmer exakt (case-sensitive)
- Försök med "November" eller det exakta namnet på din flik

### Problem: "Inga rader importerades"
**Lösning:**
- Kontrollera att kolumnerna heter exakt: Domain, Kund, Targeting URL, Anchor
- Se till att det finns data i raderna
- Kolla att kundnamnen matchar i databasen

---

## 🎯 Manuell metod (fungerar alltid!)

Om Google Sheets inte fungerar kan du alltid:

1. **Öppna ditt Google Sheet**
2. **Kopiera en rad i taget:**
   - Domain: Klistra in i "Publiceringssajt"
   - Välj kund från dropdown
   - Targeting URL: Klistra in i "Målsida"
   - Anchor: Klistra in i "Ankartext"
3. **Klicka "Lägg till"**

Det går snabbt när du väl är igång!

---

## 📝 Exempel credentials.json struktur:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "linkdb-sheets-reader@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
```

**VIKTIGT:** Dela aldrig denna fil offentligt! Den innehåller privata nycklar.

---

## ✅ När det fungerar:

Du kan då:
1. Klicka "Importera från Google Sheets"
2. Se alla rader läsas in automatiskt
3. Granska importerade länkar
4. Klicka "Generera plan"
5. Ladda ner färdig CSV!

**Detta sparar MASSOR av tid! 🚀**

---

**Frågor? Se GUI_README.md för mer info eller kontakta support.**

