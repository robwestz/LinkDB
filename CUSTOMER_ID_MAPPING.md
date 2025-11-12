## 💡 Instruktioner:

### **Uppdatera Google Sheets:**

1. **Öppna din client_index:**
   https://docs.google.com/spreadsheets/d/1mw_P9GqT0MDKb9UdqEZhd610dgb3CYMfDD9M6F-bndg

2. **Lägg till kolumn "customer_id"** (om den inte finns)

3. **Använd VLOOKUP eller kopiera direkt:**
   - Kopiera tabellen ovan
   - Klistra in i Google Sheets
   - Eller använd CSV-filen: `data/customer_id_mapping.csv`

4. **För ej funna kunder:**
   - Ta bort dem från client_index ELLER
   - Lägg till dem i databasen först

---

## 📁 Filer:

- **CSV:** `data/customer_id_mapping.csv`
- **Script:** `get_customer_ids.py`

---

**✅ Nu har du customer_id för alla 69 matchade kunder att uppdatera i Google Sheets!**
# ✅ CUSTOMER_ID MAPPNING - RESULTAT

## 📊 Sammanfattning:

**Matchade:** 69 av 119 kunder
**Ej funna:** 50 kunder

CSV-fil skapad: `data/customer_id_mapping.csv`

---

## ✅ MATCHADE KUNDER (69 st):

Kopiera denna tabell till Google Sheets:

| Kund | customer_id | canonical_root |
|------|-------------|----------------|
| Acnespecialisten | 132 | acnespecialisten.se |
| 4him4her | 193 | 4him4her.com |
| Dryft | 164 | dryft.se |
| Arctic | 12 | arctic.se |
| Bethard | 117 | bethard.com |
| Chattanoogarehab | 140 | chattanoogarehab.com |
| Cherry | 110 | cherry.com |
| comfydence.se | 197 | comfydence.se |
| Distansinstitutet | 36 | distansinstitutet.se |
| Hajper.com | 134 | hajper.com |
| Vardagsfrid | 155 | vardagsfrid.se |
| Himala.ai | 115 | himala.ai |
| Jakt.se | 209 | jakt.se |
| Indoorprofessional | 192 | indoorprofessional.se |
| Kleer | 129 | kleer.se |
| Kungaslottet | 188 | kungaslottet.se |
| KvarnX | 107 | kvarnx.com |
| Lansfast | 18 | lansfast.se |
| Coface | 135 | coface |
| Cateringfabriken.se | 143 | cateringfabriken.se |
| Casinogringo | 151 | casinogringos.se |
| Leaptodigital | 175 | Leaptodigital |
| LSB | 100 | lsb.se |
| Pontech | 24 | pontech |
| Pontonhamnar | 66 | pontonhamnar.se |
| Snuset | 118 | snuset.se |
| Nettotobak | 113 | nettotobak.com |
| Upplevelse.com | 131 | upplevelse.com |
| Megariches | 190 | megariches.com |
| Svenskafonster | 156 | svenskafonster.se |
| Petster.se | 150 | petster.se |
| Ataraxia | 163 | ataraxiavardcentral.se |
| CDG | 68 | cdg.io |
| Merchoteket | 196 | merchoteket.se |
| MrNicco | 94 | mrnicco.com |
| Nodeposit | 123 | nodepositbonus.cc |
| Michaelofrisorerna | 139 | michaelofrisorerna.se |
| Kamux | 72 | kamux.fi |
| Minifinder | 183 | Minifinder.se |
| MrVegas | 189 | mrvegas.com |
| Clearfuze | 153 | clearfuze.com |
| NorthTracker | 200 | northtracker.com |
| Mobot | 98 | mobot.com |
| Bettingsyndikatet | 202 | Bettingsyndikatet |
| Purakliniken | 105 | purakliniken.se |
| Rusta | 114 | rusta.se |
| SvenskIPTV | 157 | svenskiptv.com |
| Sesec | 166 | sesec.se |
| Glassfactory | 168 | glassfactory.fi |
| Spelklubben | 64 | spelklubben.se |
| Startmotor | 90 | startmotor.se |
| Flygbussarna | 167 | flygbussarna.se |
| Bus4You | 170 | bus4you.se |
| Ekonomico | 182 | ekonomico.se |
| Invozio | 181 | Invozio |
| Striveon | 195 | joinstriveon.com |
| Supernormal | 133 | supernormal.health |
| Swedoffice | 13 | swedoffice |
| Tandea | 44 | tandea.se |
| Technobark | 165 | technobark.com |
| Tiotak | 20 | tiotak.se |
| TKW | 161 | tkw.se |
| Tryggbil | 31 | Tryggbil |
| Turner.fi | 194 | turner.fi |
| Videoslots | 116 | videoslots.com |
| Violamilano | 198 | Violamilano.com |
| Wellio | 178 | wellio.se |
| Willabgarden | 177 | willabgarden.de |
| Yourgild | 186 | yourgild.com |

---

## ❌ EJ FUNNA KUNDER (50 st):

Dessa kunder finns INTE i databasen och måste antingen:
1. Läggas till i databasen
2. Korrigeras i Google Sheets (felstavning?)
3. Tas bort från client_index

| Kund |
|------|
| Aerius Ventilation |
| Cdbilvård |
| A Retro Tale |
| Ekström & Garay |
| Bergets-Ro |
| OptiOne |
| Optitech Sverige |
| Seniorabatt |
| Crystal Beverage Company |
| D-Bet |
| Discountsover60 |
| Epidemic Sounds |
| Fair Investments |
| Flax Casino |
| Happy Casino |
| Kelleher International |
| Jour Eliten |
| Låsjouren |
| Rörjour247 |
| Leovegas |
| Lilla-Världen |
| Oljedroppen.se |
| Lucky Casino |
| Mäklarringen |
| Tiger Of Sweden |
| Mockfjärds |
| Racha Organics, Inc |
| MyNicco (US) |
| Nbi Nordic Beauty Import Oy |
| Nordic Knots |
| Socialcatfish |
| Säkra rör AB |
| Tandea (Haninge) |
| Standupsverige |
| Sthlm Physique |
| Stockholm Rör & VVS |
| Sweden Longstay |
| Tandlakare.se |
| Zmarta Finland |
| Bokahandyman |
| Flyttgaranti |
| Snickare.online |
| Technomeow |
| Villasandudden.se |
| Zmarta Sverige |
| T2H Rakkenus |
| Lessworries.com |
| Vera&John |
| Florister I Sverige |
| Mynt.com |

---

## 📋 För Google Sheets:

### **Enkel kopia (tab-separerad):**

```
Kund	customer_id
Acnespecialisten	132
4him4her	193
Dryft	164
Arctic	12
Bethard	117
Chattanoogarehab	140
Cherry	110
comfydence.se	197
Distansinstitutet	36
Hajper.com	134
Vardagsfrid	155
Himala.ai	115
Jakt.se	209
Indoorprofessional	192
Kleer	129
Kungaslottet	188
KvarnX	107
Lansfast	18
Coface	135
Cateringfabriken.se	143
Casinogringo	151
Leaptodigital	175
LSB	100
Pontech	24
Pontonhamnar	66
Snuset	118
Nettotobak	113
Upplevelse.com	131
Megariches	190
Svenskafonster	156
Petster.se	150
Ataraxia	163
CDG	68
Merchoteket	196
MrNicco	94
Nodeposit	123
Michaelofrisorerna	139
Kamux	72
Minifinder	183
MrVegas	189
Clearfuze	153
NorthTracker	200
Mobot	98
Bettingsyndikatet	202
Purakliniken	105
Rusta	114
SvenskIPTV	157
Sesec	166
Glassfactory	168
Spelklubben	64
Startmotor	90
Flygbussarna	167
Bus4You	170
Ekonomico	182
Invozio	181
Striveon	195
Supernormal	133
Swedoffice	13
Tandea	44
Technobark	165
Tiotak	20
TKW	161
Tryggbil	31
Turner.fi	194
Videoslots	116
Violamilano	198
Wellio	178
Willabgarden	177
Yourgild	186
```

---


