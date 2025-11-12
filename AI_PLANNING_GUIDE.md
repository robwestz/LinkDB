
### **6. Lärande från historik**
AI ser vad som fungerat tidigare och bygger vidare på det

---

## 🔧 Tekniska detaljer:

### **Backend:**
- `generate_ai_prompt()` - Skapar prompten
- Loggas till konsollen när plan genereras
- Inkluderas i JSON-response

### **Frontend:**
- `showAIPromptDialog()` - Visar dialog före generering
- `confirmAIGeneration()` - Startar med AI-instruktioner
- `toggleAIPrompt()` - Visa/dölj prompt i resultat
- `copyAIPrompt()` - Kopiera till urklipp

### **Data som inkluderas:**
- Kundinfo (canonical_root, brand)
- Antal länkar per kund
- Rekommenderad strategi
- Historiska ankartexter (top 5)
- Publiceringssajter
- Angivna målsidor och ankartexter
- Custom AI-instruktioner

---

## 💡 Best Practices:

### **För bästa resultat:**

1. **Ge kontext i instruktioner**
   - ✅ "Fokusera på casino-termer för Q4-kampanj"
   - ❌ "Gör bra ankartexter"

2. **Använd historik**
   - Systemet visar automatiskt vanliga ankartexter
   - AI kan bygga vidare på dessa

3. **Ange målsidor när möjligt**
   - Mer specifika målsidor = bättre ankartexter
   - AI kan analysera sidans innehåll

4. **Granska AI-förslag**
   - AI är smart men inte perfekt
   - Kopiera prompten och få flera förslag
   - Välj det bästa

5. **Iterera**
   - Testa olika instruktioner
   - Se vad som fungerar bäst
   - Förbättra över tid

---

## 🐛 Troubleshooting:

### **Problem: AI-prompt visas inte**
**Lösning:** Ladda om sidan (Ctrl + F5)

### **Problem: Kan inte kopiera prompt**
**Lösning:** 
- Klicka "Visa/Dölj prompt"
- Markera texten manuellt
- Högerklicka → Kopiera

### **Problem: Prompten är för lång**
**Lösning:** 
- Detta är normalt för många kunder
- Dela upp i flera mindre planer
- Eller använd AI som kan hantera långa prompts (Claude)

---

## 🎊 Sammanfattning:

**AI-assisterad planering ger dig:**
- ✅ Intelligent semantisk analys
- ✅ Naturliga ankartexter
- ✅ Strategisk distribution
- ✅ Topical authority-byggande
- ✅ Flexibilitet med instruktioner
- ✅ Kopierbara prompts för egen AI-användning

**Workflow:**
1. Lägg till länkar → 2. Klicka "Generera plan" → 3. Ge instruktioner → 4. Starta → 5. Kopiera prompt (om du vill) → 6. Ladda ner CSV

**Detta gör länkplanering både smartare och snabbare! 🚀**

---

## 📖 Relaterade filer:

- `PLANERING_UPDATE.md` - Alla nya funktioner
- `GOOGLE_SHEETS_SETUP.md` - Sheets integration
- `GUI_README.md` - Allmän dokumentation
# 🤖 AI-Assisterad Länkplanering - Guide

## ✨ Vad är det?

När du klickar på "Generera plan" aktiveras nu en AI-assisterad planeringsfunktion som:

1. **Visar en sammanfattning** av din planering
2. **Ger dig möjlighet att ge instruktioner** till AI
3. **Genererar en detaljerad AI-prompt** med all kontext
4. **Låter dig kopiera prompten** för användning med AI-tjänster

---

## 🔄 Hur det fungerar:

### Steg 1: Lägg till länkar som vanligt
- Välj kunder
- Ange publiceringssajter
- Valfritt: målsidor och ankartexter

### Steg 2: Klicka "Generera plan"
En dialog öppnas som visar:

```
🤖 AI-assisterad Länkplanering

📊 Planerings-sammanfattning:
- Totalt antal länkar: 23
- Antal kunder: 2
  • bethard.com: 15 länkar
  • cherry.com: 8 länkar

💡 AI kommer att:
- Analysera målsidor semantiskt
- Generera relevanta ankartexter baserat på innehåll
- Distribuera länkar optimalt för SEO
- Bygga topical authority där möjligt
- Följa naturlig anchor distribution

📝 Instruktioner till AI (valfritt):
[Textfält för dina instruktioner]

[Avbryt] [🚀 Starta AI-planering]
```

### Steg 3: (Valfritt) Ge instruktioner
Du kan ge specifika instruktioner, t.ex.:
- "Fokusera på casino-relaterade termer"
- "Undvik överdrivet optimerade ankartexter"
- "Prioritera branded anchors för denna kampanj"
- "Bygg topical authority kring 'sportbetting'"

### Steg 4: Starta planeringen
Klicka "🚀 Starta AI-planering"

### Steg 5: Se resultatet
Efter generering visas:
- Färdig plan med länkar
- **AI-prompt som användes** (kan kopieras)
- CSV för nedladdning

---

## 📋 Vad AI-prompten innehåller:

### 1. **Kontext om uppgiften**
```
Du är en expert på SEO och länkbyggnad med djup förståelse 
för semantisk SEO och topical authority.
```

### 2. **Specifika instruktioner**
- Analysera målsidor
- Generera semantiskt relevanta ankartexter
- Bestäm anchor types
- Säkerställ naturlig distribution
- Bygg topical authority

### 3. **Dina custom instruktioner**
(Om du angav några)

### 4. **Detaljerad data per kund**
```
### Kund: bethard.com (Brand: Bethard)
- Totalt länkar: 15
- Rekommenderad strategi: semantic_foundation
- Historik: 56 länkar totalt
- Vanliga ankartexter i historik:
  - "betting på sport" (12x)
  - "casino odds" (8x)
  
Länkar att planera:
1. 15 länkar på kingsizemag.se
   - Målsida: https://bethard.com/sv/sports
   - Ankartext: "betting på fotboll"
```

### 5. **SEO-principer att följa**
- Natural Distribution
- Semantic Relevance
- Diversity
- Topical Authority
- Avoid Over-Optimization

---

## 💡 Användningsfall:

### **Fall 1: Helt automatisk**
1. Lägg till kunder med endast publiceringssajt
2. Klicka "Generera plan" (utan instruktioner)
3. AI genererar allt automatiskt
4. Granska och ladda ner

### **Fall 2: Med målsidor**
1. Lägg till kunder med publiceringssajt + målsida
2. Klicka "Generera plan"
3. AI genererar ankartexter för målsidorna
4. Granska och ladda ner

### **Fall 3: Med specifika instruktioner**
1. Lägg till kunder
2. Klicka "Generera plan"
3. Skriv instruktioner: "Fokusera på casino-termer, undvik 'betting'"
4. AI följer dina instruktioner
5. Granska och ladda ner

### **Fall 4: Manuell AI-användning**
1. Generera plan som vanligt
2. Kopiera AI-prompten som visas
3. Klistra in i ChatGPT, Claude, eller annan AI
4. Få ännu bättre, skräddarsydda förslag
5. Implementera manuellt

---

## 🎯 AI-prompten kopierad - vad nu?

### Alternativ 1: Använd ChatGPT
1. Gå till https://chat.openai.com/
2. Klistra in prompten
3. ChatGPT genererar förslag
4. Kopiera tillbaka till din planering

### Alternativ 2: Använd Claude
1. Gå till https://claude.ai/
2. Klistra in prompten
3. Claude analyserar och föreslår
4. Implementera förslagen

### Alternativ 3: Använd GitHub Copilot
1. Öppna en fil i VS Code
2. Klistra in prompten som kommentar
3. Copilot föreslår implementering
4. Använd förslagen

---

## 📊 Exempel på AI-prompt:

```markdown
# 🤖 LÄNKPLANERINGSPROMPT

Du är en expert på SEO och länkbyggnad med djup förståelse 
för semantisk SEO och topical authority.

## 📋 UPPGIFT:
Generera en intelligent länkplan baserat på nedanstående data. 
För varje länk ska du:
1. Analysera målsidan (om angiven) eller välj lämplig målsida från historik
2. Generera semantiskt relevant ankartext (om inte angiven)
3. Bestäm anchor type (exact, partial, branded, generic, lsi)
4. Säkerställ naturlig anchor distribution enligt strategin
5. Bygga topical authority där möjligt genom att länka relaterade sidor

## 💡 SPECIELLA INSTRUKTIONER:
Fokusera på casino-relaterade termer och undvik överdrivet 
optimerade ankartexter

## 📊 PLANERINGSDATA:

### Kund: bethard.com (Brand: Bethard)
- **Totalt länkar:** 15
- **Rekommenderad strategi:** semantic_foundation
- **Historik:** 56 länkar totalt
- **Vanliga ankartexter i historik:**
  - "betting på sport" (12x)
  - "casino odds" (8x)
  - "bethard bonus" (7x)

**Länkar att planera:**
1. **15 länkar** på **kingsizemag.se**
   - Målsida: https://bethard.com/sv/sports
   - Ankartext: "betting på fotboll"

## 🎯 OUTPUT-FORMAT:
För varje länk, ange:
- Target URL
- Anchor text
- Anchor type (exact/partial/branded/generic/lsi)
- Reasoning (kort förklaring av valet)

## 📈 SEO-PRINCIPER ATT FÖLJA:
1. **Natural Distribution:** Följ strategins anchor distribution
2. **Semantic Relevance:** Ankartexter ska vara semantiskt relevanta för målsidan
3. **Diversity:** Variera ankartexter även inom samma kategori
4. **Topical Authority:** Länka relaterade sidor för att bygga authority
5. **Avoid Over-Optimization:** Undvik för aggressiva exact match anchors

---

🚀 **BÖRJA PLANERINGEN NU!**
```

---

## ✅ Fördelar med AI-assisterad planering:

### **1. Semantisk förståelse**
AI kan analysera målsidor och generera relevanta ankartexter baserat på innehåll

### **2. Naturlig språkhantering**
AI genererar ankartexter som låter naturliga och varierade

### **3. Strategisk distribution**
AI följer anchor distribution-regler automatiskt

### **4. Topical clustering**
AI kan identifiera relaterade sidor och bygga topic clusters

### **5. Kontextuell anpassning**
Med dina instruktioner kan AI anpassa sig till specifika kampanjer

