# 🎮 Game Design Document (GDD)

**Titel:** (Nog te bepalen)  
**Versie:** 0.5  
**Auteur:** Gerald  
**Engine/Taal:** Python (Pygame)  
**Stijl:** Pixelart (16x16 / 32x32), uniek kleurenpalet per component

---

## 1. 🧠 High-Level Concept

Een uitgebreide, traditionele turn-based RPG in pixelartstijl waarin spelers een open wereld verkennen die elementen combineert van Pokémon (wereldexploratie), Fire Emblem (tactische gevechten) en authentieke spirituele tradities uit verschillende culturen. De game verweeft diepgaande spirituele en mythologische elementen uit culturen wereldwijd in een samenhangende wereld met rijke karakterontwikkeling.

**Kernpunten:**
- **Open wereld** met meerdere cultuurgebieden, elk met eigen identiteit, NPC's en verhaallijnen
- **Niet-lineaire exploratie** met organische progressie en natuurlijke ontgrendeling van gebieden
- **Tri-Sharira klassensysteem** (Fysiek-Mentaal-Spiritueel) voor unieke karakterontwikkeling
- **Culturele & spirituele thema's** geïntegreerd in gameplay-mechanismen
- **Complexe relatieontwikkeling** tussen personages en NPC's
- **Dynamische wereldstructuur** waar spelers terugkeren naar eerdere gebieden voor nieuwe uitdagingen
- **Uitgebreide campaign** (100+ uur) met vaste protagonist
- **Rijke post-game content** voor blijvende ontwikkelingsmogelijkheden
- **Consistente moeilijkheidsgraad** die vanzelf schaalt met spelerprogressie

---

## 2. 🎮 Genre en Doelgroep

- **Genre:** Strategy RPG, Exploration RPG  
- **Stijl:** 2D pixelart  
- **Doelgroep:** RPG-spelers die houden van karakterontwikkeling, spirituele thema's, en gameplay met diepgang

---

## 3. 🌍 Wereld & Setting

In plaats van een "uitverkorene" is de speler een zoekende ziel die groeit door ervaring, leren, en het bouwen van relaties. De wereld is een rijk tapijt van culturen waarin tradities verweven zijn met spirituele dimensies.

### Facties en Regio's

**1. Bharata (Sanatana Dharma)**
- **Omgeving:** Ashrama Valley, heilige rivieren, tempels
- **Thema:** Spirituele traditie, dharma, innerlijke groei
- **NPC's:** Guru's, yogi's, kshatriya krijgers, spirituele zoekers
- **Sterke punten:** Spirituele klassen, uithoudingsvermogen, rituelen

**2. Kemet (Egyptisch geïnspireerd)**
- **Omgeving:** Duat Sands, piramides, oases, tempels
- **Thema:** Dualiteit van leven/dood, rituele magie, hiërarchie
- **NPC's:** Priesters, ontdekkingsreizigers, geesten, farao's wachters
- **Sterke punten:** Balans tussen spiritueel en mentaal, rituele kracht

**3. Nyanza (West-Afrikaanse/Yoruba traditie)**
- **Omgeving:** Weelderige bossen, savannes, dorpen rond heilige rivieren
- **Thema:** Harmonie met voorouders, orale tradities, rituele kracht
- **NPC's:** Babalawo (zieners), griots, Orisha-dienaren, krijgers
- **Sterke punten:** Balansvaardigheid, gemeenschapsmagie, transformaties

**4. Alba (Keltisch/Druidisch)**
- **Omgeving:** Mistige bossen, steencirkels, kustlijnkliffen
- **Thema:** Natuurharminie, voorouderwijsheid, seizoenscycli
- **NPC's:** Druïden, barden, krijgers, stamhoofden
- **Sterke punten:** Natuurmagie, voorspelling, tribale kracht

**5. Anasazi (Noord-Amerikaans inheems)**
- **Omgeving:** Canyons, woestijnen, pueblos
- **Thema:** Verbinding met land, droomwerelden, clan-identiteit
- **NPC's:** Medicijnmannen, droomwandelaars, pottenbakkers, jagers
- **Sterke punten:** Dierlijke verbindingen, bezielde voorwerpen, droommagie

**6. Pachamama (Zuid-Amerikaans inheems)**
- **Omgeving:** Regenwouden, bergtoppen, oude ruïnes
- **Thema:** Moeder Aarde, sterrenkunde, cyclische tijd
- **NPC's:** Sjamanen, sterrenkundigen, medicijnvrouwen
- **Sterke punten:** Elementaire magie, voorouderconnectie, kosmische timing

**7. Uluru (Australisch Aboriginal)**
- **Omgeving:** Rode woestijnen, heilige rotsen, oases
- **Thema:** Droomtijd, songlines, voorouder-erfgoed
- **NPC's:** Ouderen, verhalenvertellers, dierengidsen
- **Sterke punten:** Droommagie, ancestrale kennis, reizen over grote afstanden

**8. Zhongyuan (Oost-Aziatisch/Taoïstisch)**
- **Omgeving:** Mistige bergen, bamboe wouden, paviljoens
- **Thema:** Balans, qi-energie, natuurlijke filosofie
- **NPC's:** Taoïstische wijzen, krijgskunstmeesters, geleerden
- **Sterke punten:** Balans tussen lichamen, qi-manipulatie, eeuwenoude technieken

### Wereldstructuur en Progressie

- **Gelaagde moeilijkheidsgebieden** binnen elke regio, van beginner tot expert
- **Organische ontgrendeling** van nieuwe gebieden via verhaalgebaseerde obstakels:
  - Natuurlijke barrières (lawines, stormen, ingestorte bruggen)
  - NPC-gerelateerde beperkingen (iemand die toestemming moet geven)
  - Questvereisten die logisch aansluiten bij de wereld
- **Niet-lineaire exploratie** die spelers aanmoedigt om tussen regio's te reizen
- **Terugkerende relevantie** van eerdere gebieden (quests leiden je terug naar bekende plekken)

### Verhaalmechanismen
- Verhalen ontvouwen zich organisch via:
  - Hoofdquestlijn die regio's verbindt
  - Regiospecifieke verhaallijnen
  - Persoonlijke verhalen van teamgenoten
  - Consequenties van spelersbeslissingen

### Thema's
- Balans tussen tradities en nieuwe wegen
- Harmonie tussen de drie lichamen (fysiek, mentaal, spiritueel)
- Zoektocht naar waarheid en zelfkennis
- Gemeenschap versus individualiteit

---

## 4. ⚔️ Tri-Sharira Systeem

De kern van het spel is het Tri-Sharira systeem, gebaseerd op de oude filosofie van de drie lichamen of bestaanslagen. Dit systeem bepaalt klassen, statistieken, vaardigheden en karakterontwikkeling.

### De Drie Lichamen

**1. Fysiek Lichaam (Sthūla Sharīra)**
- Het materiële, tastbare lichaam
- Focus op kracht, beweging, actie, uithoudingsvermogen
- Manifesteert zich via directe aanvallen, fysieke vaardigheden, wapens

**2. Mentaal Lichaam (Sūkshma Sharīra)**
- Het subtiele lichaam van gedachten, emoties, intellect
- Focus op strategie, analyse, controle, perceptie
- Manifesteert zich via tactische beslissingen, illusies, manipulatie

**3. Spiritueel Lichaam (Kārana Sharīra)**
- Het causale lichaam, verbonden met hogere bewustzijnsniveaus
- Focus op energie, intuïtie, verbinding, transformatie
- Manifesteert zich via energiemanipulatie, voorspelling, harmonie

### Klassensysteem

Elke factie heeft unieke implementaties van deze basisklassen, die corresponderen met de drie lichamen:

**Fysiek-gerichte klassen:**
- **Warrior** - Gebalanceerde vechter, wapenmeeesterschap
- **Defender** - Tank, bescherming, controle
- **Archer/Hunter** - Afstandsaanvallen, precisie, mobiliteit
- **Berserker/Martial Artist** - Pure kracht of snelheid, risico/beloning

**Mentaal-gerichte klassen:**
- **Sage** - Kennis, analyse, elementen-manipulatie
- **Enchanter** - Debuffs, statuseffecten, controle
- **Illusionist** - Misleiding, ontwijking
- **Strategist** - Teamondersteuning, tactische buffs

**Spiritueel-gerichte klassen:**
- **Yogi** - Innerlijke kracht, zelfbuffs, ademcontrole
- **Guru** - Mentorschap, teamversterking, wijsheid
- **Oracle** - Voorspelling, verborgen paden, intuïtie
- **Shaman** - Elementaire krachten, natuurverbinding, transformatie

**Hybride klassen** (voorbeelden):
- **Battle Monk** (Fysiek + Spiritueel)
- **Mystic Scholar** (Mentaal + Spiritueel)
- **Tactical Warrior** (Fysiek + Mentaal)

### Vaardigheden per Lichaam

**Fysieke Vaardigheden:**
- **Vajra Strike** - Krachtige directe aanval
- **Precision Cut** - Gerichte aanval op zwakke plekken
- **Immovable Mountain** - Verdedigingsstance
- **Thunderous Charge** - Dash-aanval

**Mentale Vaardigheden:**
- **Mind Spike** - Directe mentale schade
- **Confusion Web** - Brengt tegenstanders in verwarring
- **Mental Barrier** - Bescherming tegen mentale aanvallen
- **Tactical Deception** - Illusoire kopieën

**Spirituele Vaardigheden:**
- **Prāṇa Beam** - Energiestraal
- **Astral Projection** - Aanval vanuit spirituele dimensie
- **Aura Shield** - Beschermende barrière
- **Karmic Reflection** - Weerkaatst schade naar aanvaller

---

## 5. 🧑‍🤝‍🧑 Personages en Progressie

### Hoofdkarakter
- Eén vast hoofdpersonage voor alle spelers
- Diepgaande karakterontwikkeling door verhaal en speelerskeuzes
- Kan in verschillende richtingen evolueren afhankelijk van speelstijl

### Partijleden en NPC's
- Diverse recruiteerbare partijleden uit alle wereldregio's
- Elke factie heeft zowel "good guys" als "bad guys"
- Non-combat karakters die de wereld verrijken en side-quests aanbieden

### Progressiesysteem
- Natuurlijke groei door gedrag en gebruik
- Vaardigheden evolueren bij veelvuldig gebruik
- Doorbraakmomenten bij mijlpalen die vaardigheden transformeren
- Promotiesysteem met twee evolutiefasen:
  - Eerste promotie (~niveau 20)
  - Tweede promotie (~niveau 40)

### Relatiesystemen
- Vertrouwensniveaus tussen teamleden
- Mentor-leerling relaties voor kennisoverdracht
- Combo-aanvallen tussen karakters met sterke banden
- Reputatiesysteem met verschillende facties

---

## 6. 📊 Statistiekensysteem

Elke karakter heeft stats in alle drie de lichamen, maar hun klasse bepaalt waar de nadruk ligt. Stats zijn gegroepeerd per lichaam:

### Universele Statistieken
- **Levenspunten (HP)** - Gezondheid
- **Beweging (MOV)** - Tegels verplaatsing per beurt

### Fysiek Lichaam
- **Kracht (STR)** - Fysieke aanvalskracht
- **Uithoudingsvermogen (END)** - Stamina voor acties
- **Verdediging (DEF)** - Bescherming tegen fysieke aanvallen
- **Snelheid (SPD)** - Ontwijking en extra aanvallen
- **Lichaamsbeheersing** - Balans en precisie

### Mentaal Lichaam
- **Nauwkeurigheid (ACC)** - Trefkans voor aanvallen
- **Focus (FOC)** - Concentratie voor complexe acties
- **Inzicht (INS)** - Vermogen zwakheden te vinden
- **Wilskracht (WILL)** - Weerstand tegen statuseffecten
- **Geheugen (MEM)** - Patroonherkenning en leren

### Spiritueel Lichaam
- **Magiekracht (MAG)** - Kracht van spirituele aanvallen
- **Prāṇa (PRA)** - Spirituele energie voor vaardigheden
- **Spirituele Weerstand (RES)** - Bescherming tegen magie
- **Intuïtie (INT)** - Voorspellend vermogen
- **Devotie (DEV)** - Versterkt helende en ondersteunende krachten
- **Karma (KAR)** - Geluksfactor en NPC-reacties

### Statverhouding per Klasse
Elke klasse legt nadruk op bepaalde statistieken:
- **Fysieke klassen:** Hoge fysieke stats, gemiddelde mentale stats, lage spirituele stats
- **Mentale klassen:** Hoge mentale stats, gemiddelde spirituele stats, lage fysieke stats
- **Spirituele klassen:** Hoge spirituele stats, gemiddelde fysieke stats, lage mentale stats
- **Hybride klassen:** Hoge stats in twee lichamen, lage in het derde

---

## 7. 🎨 Kunst en Audio

- Volledige pixelartstijl: 16x16 of 32x32 sprites
- Uniek kleurenpalet per type element (regio, karakter, object)
- UI stijlvol en spiritueel-modern
- Muziek: Ambient + per regio

---

## 8. 🧰 Interface en Controls

- Toetsenbord (pijltjes + actietoetsen), mogelijk gamepad later
- HUD: HP/MP of equivalent, skills, cooldowns, teamstatus
- UI: Questlog, inventaris, relaties, statoverzicht, skills

---

## 9. 🧪 Techniek

- Python 3.x + Pygame
- Tilemap-based werelden (Tiled integratie mogelijk)
- Structuur: `main.py`, `assets/`, `entities/`, `ui/`, `data/`, `scenes/`
- Save/load systeem

---

## 10. 🗺️ Wereld & Kalender

- **Dag/nacht-cyclus** met veranderende NPC-routines en unieke gebeurtenissen
- **Kalendersysteem** met seizoenen en speciale dagen
- **Astrologische gebeurtenissen** die spirituele krachten beïnvloeden
- **Tijdgevoelige content** zoals festivals en speciale quests
- **Weersysteem** dat gameplay en beschikbare resources beïnvloedt

### Wereldprogressie

- **Natuurlijke barrières** voor gebiedsontgrendeling:
  - Geografische obstakels (ravijnen, rivieren, bergen)
  - Weersomstandigheden (stormen, mist, sneeuw)
  - Beschadigde infrastructuur (ingestorte bruggen, geblokkeerde paden)

- **NPC-gestuurde ontgrendeling**:
  - Karakters die toestemming moeten geven voor toegang
  - Gidsen die ontbreken maar later gevonden kunnen worden
  - Missende sleutels of voorwerpen die nodig zijn voor toegang

- **Quest-gerelateerde ontgrendeling**:
  - Lokale problemen die moeten worden opgelost
  - Vertrouwen winnen van lokale gemeenschappen
  - Vaardigheden leren die nodig zijn om obstakels te overwinnen

- **Gelaagde gebieden** binnen elke regio:
  - Beginnersgebieden die vanaf het begin toegankelijk zijn
  - Middelmatige zones die ontgrendeld worden tijdens het verhaal
  - Expertgebieden die alleen toegankelijk zijn in latere fases

Deze progressiemechanismen zorgen voor een natuurlijke, geloofwaardige ontdekking van de wereld zonder artificiële barrières, terwijl ze de speler een duidelijk pad voorwaarts bieden.

---

## 11. 💰 Economie & Resources

### Materiële Economie
- **Basisvaluta:** Goud of equivalent voor standaard transacties
- **Speciale materialen:** Zeldzame crafting-items, wapenmaterialen
- **Standaard items:** Verbruiksartikelen, equipment, accessoires

### Spirituele Economie
- **Kennis:** Voor nieuwe vaardigheden en verborgen informatie
- **Karma:** Beïnvloedt NPC-reacties en toegang tot quests
- **Wijsheid:** Voor krachtige upgrades en mentorrelaties
- **Prāṇa:** Spirituele energie voor speciale vaardigheden

---

## 12. 🧩 Openstaande Discussiepunten

1. **Gevechtssysteem specifics** - Precieze implementatie van turn-based gevechten
2. **Energieherstelmechanieken** - Verschillende methoden voor verschillende klassen
3. **UI voor drie-lichamen-systeem** - Visuele representatie van complex statsysteem
4. **Kalendersysteem details** - Specifieke astrologische gebeurtenissen en effecten
5. **Verhaalstructuur** - Hoofdlijn en vertakkingen
6. **Balansmechanismen** - Hoe moeilijkheidsgraad natuurlijk schaalt met spelerprogressie
7. **Partijsamenstelling** - Hoeveel karakters actief in gevecht, wisselmechanismen