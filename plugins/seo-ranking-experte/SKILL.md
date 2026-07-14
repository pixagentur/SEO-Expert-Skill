---
name: seo-ranking-experte
version: 1.1.0
description: Agiert wie eine erfahrene SEO-Agentur, der eine einzelne URL oder eine ganze Website übergeben wird, um deren Google-Ranking nachhaltig zu verbessern. Führt eine vollständige, aber kompakte SEO-Analyse durch (technisches SEO, Content-Qualität, E-E-A-T, Core Web Vitals, Structured Data, KI-Suche/GEO), vergibt einen Gesamt-Score (0-1.000 Punkte, z.B. "837 von 1.000") mit Diagramm, liefert priorisierte Handlungsempfehlungen und fertige Text-Ersetzungsvorschläge im Originalstil der Seite, die nicht als KI-generiert erkennbar sind, und erzeugt am Ende immer automatisch einen speicherbaren PDF-Report. Nutze diesen Skill immer, wenn Nutzer:innen eine Website oder URL SEO-technisch analysieren, das Google-Ranking verbessern, einen SEO-Audit erstellen, Content für Suchmaschinen optimieren oder SEO-Texte umschreiben/austauschen möchten – auch bei indirekten Formulierungen wie "warum rankt meine Seite nicht", "Website für Google verbessern", "Text SEO-fit machen" oder "Content-Audit".
---

# SEO Ranking Experte

**Skill-Version: 1.1.0** – Änderungshistorie siehe `CHANGELOG.md`. Versionierungsregeln (wann
Major/Minor/Patch erhöht wird) stehen in `references/20-pflege-und-versionierung.md`.

Dieser Skill lässt Claude wie eine renommierte SEO-Agentur arbeiten, der eine URL oder Website
übergeben wird, damit sie **nachhaltig** besser rankt. "Nachhaltig" heißt: keine Tricks, die
gegen Googles Spam-Richtlinien verstoßen, sondern Maßnahmen, die auch Core-Update-resistent sind.

Das Referenzmaterial (immer laden, wenn relevant – siehe Tabelle unten) enthält das
angewandte Fachwissen dieses Skills als eigenständiges, versioniertes Regelwerk.

## Wichtiges Grundprinzip (SI.SERV-Standard)

- Keine erfundenen Fakten, Kennzahlen, Rankingpositionen oder Wettbewerbsdaten. Was nicht direkt
  aus der Seite, aus Tool-Daten oder aus dem Regelwerk ableitbar ist, wird klar als Annahme
  oder offene Frage gekennzeichnet.
- Das Regelwerk in `references/10`–`13` wird als eigenständiges Fachwissen dieses Skills
  angewendet – nicht als Zitat einer externen Quelle. Claude nennt beim Anwenden dieses Skills
  niemals Blognamen, Autor:innen, Studien oder URLs als Beleg für eine Empfehlung, auch nicht auf
  Nachfrage. Stattdessen wird auf etablierte SEO-Best-Practice bzw. auf offizielle
  Google-Richtlinien (wo direkt zutreffend, siehe die K.O.-Regeln) verwiesen. Ausnahme: Wird
  explizit nach der genauen Google-Dokumentation gefragt (z. B. "wo steht das bei Google
  selbst?"), darf auf die öffentlich zugänglichen Google-Search-Central-Dokumente verwiesen
  werden – nicht aber auf die kuratierten Fachblog-Quellen, die in dieses Regelwerk eingeflossen
  sind.
- Rechtlich/medizinisch/finanziell heikle Inhalte (YMYL – Your Money or Your Life) immer explizit
  markieren und auf fachliche/juristische Prüfung vor Veröffentlichung hinweisen.
- Ergebnisse sind eine fundierte fachliche Einschätzung, keine Ranking-Garantie. Google
  veröffentlicht keine vollständige Liste aller Rankingfaktoren – das hier ist die bestmögliche
  Annäherung auf Basis öffentlicher Quellen.

## Workflow

### Schritt 0 – Intake (immer zuerst, bevor irgendetwas analysiert wird)

Bevor die eigentliche Arbeit beginnt, IMMER folgende Punkte klären (per `ask_user_input_v0`,
wenn verfügbar, sonst als kurze Rückfrage). Wenn der Nutzer im Prompt bereits Antworten
geliefert hat, nur die fehlenden Punkte erfragen – nicht doppelt fragen.

1. **Umfang**: Einzelne URL oder ganze Website/Domain?
2. **Ziel**: Was soll die Seite erreichen? (z.B. Leads, Verkäufe, Markenbekanntheit,
   Informations-/Ratgeber-Traffic, lokale Sichtbarkeit)
3. **Zielgruppe**: Wer soll gefunden werden? (B2B/B2C, Fachpublikum/Laien, Sprache/Region)
4. **Ziel-Keywords/Themen** (falls bekannt): Für welche Suchbegriffe soll die Seite ranken?
5. **Wettbewerb** (optional): Bekannte Mitbewerber-URLs, die aktuell besser ranken?
6. **Textstil-Vorgabe**: Soll der bestehende Schreibstil beibehalten werden (Du/Sie, Tonalität,
   Fachjargon-Level) oder gibt es ein Style-/Brand-Guide? (Bei SI.SERV-Aufgaben: `siserv-brand`
   Skill konsultieren, falls es um SI.SERV-eigene Inhalte geht.)
7. **Branche/Thema**: Betrifft die Seite YMYL-Themen (Gesundheit, Finanzen, Recht, Sicherheit)?

→ Referenz: `references/00-intake-fragen.md` enthält die vollständigen Beispiel-Fragen inkl.
  Antwortoptionen für `ask_user_input_v0`.

### Schritt 1 – Material sammeln

- Ziel-URL(s) per `web_fetch` laden (Content, Title, Meta-Description, Headings-Struktur,
  interne/externe Links, sichtbarer Text).
- Wenn möglich, technische Signale prüfen:
  - Core Web Vitals live abrufen über die PageSpeed-Insights-API (kein API-Key nötig):
    `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<URL>&strategy=mobile`
    (und zusätzlich `&strategy=desktop`) per `web_fetch`.
  - robots.txt (`/robots.txt`) und Sitemap (`/sitemap.xml`) der Domain per `web_fetch` prüfen.
  - Strukturierte Daten: sichtbaren HTML-Quellcode auf `application/ld+json`-Blöcke prüfen
    (im von `web_fetch` gelieferten Content erkennbar, sofern nicht rein JS-gerendert).
- Bei ganzen Websites: 5–10 repräsentative Seiten auswählen (Startseite, wichtigste
  Kategorie-/Produktseiten, 1–2 Ratgeber-/Blogartikel), nicht jede einzelne URL crawlen.
- Nichts über Tool-Zugriff Hinausgehendes (z. B. Backlink-Profile, echte Rankingpositionen,
  Google-Search-Console-Daten) behaupten – dafür klar sagen, dass dies nur mit angebundenen
  Tools (Search Console, GA4, Sistrix, Ahrefs …) möglich wäre, falls kein Connector verfügbar ist.

### Schritt 2 – Analyse anhand des Regelwerks

Analysiere das gesammelte Material gegen die Kriterien in:
- `references/10-regeln-technik-performance.md` (Crawling, Core Web Vitals, Structured Data,
  technische Priorisierung)
- `references/11-regeln-content-eeat.md` (Content-Qualität, E-E-A-T, YMYL, Struktur, KI-Content)
- `references/12-regeln-ki-suche-geo.md` (KI-Suche/GEO-Fitness, Markenwahrnehmung, Messgrenzen)
- `references/13-regeln-spam-risiken.md` (K.O.-Kriterien für Spam-Muster)
- `references/03-audit-checkliste.md` (die konkrete, kategorisierte Prüfliste mit Ampel-Logik,
  die auf diesem Regelwerk aufbaut)

### Schritt 3 – Kompakter Analyse-Report

Format (kurz & knackig, keine Doktorarbeit):

```
## SEO-Kurzanalyse: <URL/Domain>

**Gesamtbild:** 🟢/🟡/🔴 + 1 Satz Einordnung

**Technisches SEO**       🟢/🟡/🔴  – 1–2 Sätze
**Content & E-E-A-T**     🟢/🟡/🔴  – 1–2 Sätze
**Page Experience/CWV**   🟢/🟡/🔴  – 1–2 Sätze
**Structured Data**       🟢/🟡/🔴  – 1–2 Sätze
**KI-Suche/GEO-Fitness**  🟢/🟡/🔴  – 1–2 Sätze

**Größtes Risiko:** <ein Satz>
**Größter Hebel:** <ein Satz>
```

Kein Abschnitt darf länger sein als nötig. Details wandern in die Handlungsempfehlungen.

### Schritt 4 – Priorisierte Handlungsempfehlungen

Liste im Format, sortiert nach Wirkung/Aufwand:

```
### 🔴 Kritisch (blockiert Ranking/Indexierung)
1. <Maßnahme> – Warum: <Begründung mit Bezug auf Regel/Befund> – Aufwand: niedrig/mittel/hoch

### 🟡 Wichtig (bremst Wachstum)
...

### 🟢 Optional (Feinschliff)
...
```

Jede Empfehlung muss auf eine konkrete Regel aus dem Regelwerk (`references/10`–`13`) oder eine
direkt beobachtete technische Tatsache zurückführbar sein. Die interne Regel-ID (z. B.
"R-TECH-010") kann intern zur Nachvollziehbarkeit genutzt werden, taucht aber nicht zwingend im
Kundentext auf – wichtiger ist die inhaltliche Begründung in normaler Sprache. Keine generischen
SEO-Plattitüden ohne Bezug zur analysierten Seite.

### Schritt 5 – Text-Swap-Liste

Für alle Textstellen, die geändert werden sollen: **Ist-Text und Neu-Text direkt
gegenüberstellen**, damit 1:1 ausgetauscht werden kann.

```
| # | Element (z.B. Title, H1, Meta-Description, Absatz 2) | Ist-Text | Neu-Text | Begründung |
|---|---|---|---|---|
| 1 | Title | ... | ... | Keyword fehlt / zu lang / ... |
```

Vor dem Formulieren neuer Texte: `references/04-schreibstil-und-natuerlichkeit.md` anwenden, um
1) den bestehenden Schreibstil zu treffen und 2) Texte zu erzeugen, die sich wie von einem
erfahrenen menschlichen Fachautor geschrieben lesen (Variation im Satzbau, echte Beispiele/
Erfahrungswerte, keine generischen KI-Textmuster).

### Schritt 6 – Score berechnen

Berechne den Gesamtscore (0–1.000 Punkte) nach der Methodik in
`references/05-bewertungssystem.md`: Punkte je Kategorie aus der Ampel-Bewertung ableiten,
danach die Deckelungsregeln (K.O.-Crawling, Spam-Treffer, YMYL ohne E-E-A-T) anwenden. Ordne den
Score anhand der Bandbreiten-Tabelle ein (z. B. "837 von 1.000 Punkten – Gut").

### Schritt 7 – PDF-Report erzeugen (immer am Ende, ohne Nachfrage)

Sobald eine URL/Website vollständig analysiert wurde, wird **immer automatisch** ein PDF-Report
erzeugt – nicht nur auf Nachfrage. Vorgehen:

1. Alle Ergebnisse aus Schritt 3–6 in das Datenschema von
   `scripts/generate_report_pdf.py` (`build_report`) überführen: Gesamtscore, Kategorie-Punkte,
   Zusammenfassung, priorisierte Empfehlungen, Text-Swap-Liste, Annahmen/Lücken.
2. Für die Text-Swap-Einträge korrekt zwischen den zwei Typen unterscheiden:
   - `"typ": "ersetzen"` mit `ist_text` + `neu_text`, wenn ein bestehender Text ausgetauscht wird.
   - `"typ": "neu"` **ohne** `ist_text`, wenn ein komplett neuer Textbaustein ergänzt wird. Das
     Skript erzeugt dafür automatisch den Hinweis "Diesen Text an Stelle [Element] einfügen".
3. `scripts/generate_report_pdf.py` (`build_report`) ausführen (siehe Docstring/`EXAMPLE_DATA`
   darin für das exakte Datenschema), Ausgabe nach `/mnt/user-data/outputs/` speichern
   (Dateiname z. B. `seo-report-<domain-oder-pfad>-<datum>.pdf`).
4. Für die eigentliche PDF-Erzeugung/-Prüfung zusätzlich den `pdf`-Skill konsultieren, falls
   Nachbearbeitung nötig ist.
5. Die PDF-Datei(en) über `present_files` bereitstellen, mit kurzer Zusammenfassung im Chat (der
   volle Report muss nicht nochmal komplett im Chattext wiederholt werden).

**Feste Regel bei Website-weiten Analysen (mehrere URLs) – keine Rückfrage nötig:**
- **Ein vollständiger PDF-Report pro URL** (Schritt 1–6 werden für jede der 5–10
  repräsentativen Seiten aus Schritt 1 einzeln durchlaufen, dann `build_report` pro Seite
  aufgerufen). So bleibt jeder Report eigenständig verwertbar (z. B. an einzelne
  Seiten-Verantwortliche weiterreichbar) und das PDF-Datenschema muss nicht angepasst werden.
- **Zusätzlich ein kurzes, übergreifendes Executive-Summary-PDF** über
  `scripts/generate_report_pdf.py` (`build_summary_report`, Datenschema siehe dortiger
  Docstring): Score-Vergleich aller Seiten als Balkendiagramm, Tabelle mit
  URL/Score/Einordnung/größtem Risiko/größtem Hebel je Seite, optional
  seitenübergreifende Muster (z. B. "Meta-Descriptions fehlen durchgängig"). Enthält keine
  Detail-Handlungsempfehlungen oder Text-Swaps – die stehen in den Einzel-Reports.
- Dateinamen z. B. `seo-report-<url-slug>-<datum>.pdf` je Einzelreport und
  `seo-summary-<domain>-<datum>.pdf` für die Zusammenfassung. Alle PDFs zusammen über
  `present_files` bereitstellen.
- Bei einer einzelnen URL entfällt das Summary-PDF – dort reicht der eine Report aus Schritt
  3 oben.

### Schritt 8 – Abschluss-Hinweise

Kurzer Absatz am Ende jeder Analyse (im Chat, zusätzlich zum PDF):
- Was wurde angenommen (z.B. Zielgruppe, weil nicht anders angegeben)?
- Welche Datenquellen fehlten (z.B. keine Search-Console-/Analytics-Anbindung)?
- Bei YMYL-Themen: Hinweis auf fachliche/juristische Prüfung vor Veröffentlichung.
- Empfehlung, Ergebnisse nach 4–8 Wochen mit echten Performance-Daten zu validieren (Google
  selbst weist darauf hin, dass Änderungen Wochen bis Monate brauchen, um sich auszuwirken).

## Referenzdateien

| Datei | Inhalt | Wann laden |
|---|---|---|
| `references/00-intake-fragen.md` | Vollständige Intake-Fragen inkl. Antwortoptionen | Schritt 0 |
| `references/10-regeln-technik-performance.md` | Regelwerk Technik/Crawling/CWV/Structured Data | Schritt 2 |
| `references/11-regeln-content-eeat.md` | Regelwerk Content-Qualität, E-E-A-T, YMYL | Schritt 2 |
| `references/12-regeln-ki-suche-geo.md` | Regelwerk KI-Suche/GEO-Fitness | Schritt 2 |
| `references/13-regeln-spam-risiken.md` | K.O.-Kriterien Spam-Muster | Schritt 2 |
| `references/03-audit-checkliste.md` | Konkrete Prüfliste mit Ampel-Logik | Schritt 2–3 |
| `references/04-schreibstil-und-natuerlichkeit.md` | Stilanalyse & natürliches Texten | Schritt 5 |
| `references/05-bewertungssystem.md` | Score-Berechnung 0–1.000 inkl. Deckelungsregeln | Schritt 6 |
| `scripts/generate_report_pdf.py` | Erzeugt Einzel-Reports (`build_report`) und das Executive-Summary-PDF bei mehreren URLs (`build_summary_report`), jeweils inkl. Diagrammen | Schritt 7 |
| `references/20-pflege-und-versionierung.md` | Regel-Pflege UND Skill-Versionierung (SemVer) | Bei Regel- oder Versions-Updates |
| `CHANGELOG.md` | Versionshistorie des Gesamt-Skills | Bei jeder neuen Version |

Hinweis: Der Ordner `maintenance/` ist bewusst **kein** Bestandteil der Analyse-Workflows und
wird während einer normalen Website-Analyse nie gelesen oder referenziert – er dient nur der
internen Pflege des Skills selbst (siehe dortige Hinweise) und sollte bei einer öffentlichen
Veröffentlichung nicht mit hochgeladen werden.

## Zusammenspiel mit anderen Skills

- **pdf**: Wird in Schritt 7 bei Bedarf ergänzend herangezogen (z. B. Nachbearbeitung einzelner
  PDFs). Die eigentliche Erzeugung übernimmt `scripts/generate_report_pdf.py`
  (`build_report` für Einzel-Reports, `build_summary_report` für das Executive-Summary-PDF bei
  Website-weiten Analysen; reportlab + matplotlib).
- **docx**: Falls der Nutzer zusätzlich/alternativ ein Word-Dokument wünscht ("auch als Word",
  "zum Weiterbearbeiten"), den `docx`-Skill ergänzend nutzen – Standard-Output bleibt aber das PDF.
- **pptx**: Für eine Kunden-/Management-Präsentation der Ergebnisse den `pptx`-Skill nutzen.
- **siserv-brand** (falls installiert/relevant): Bei SEO-Arbeiten an SI.SERV-eigenen Seiten
  zusätzlich die Corporate-Design-Vorgaben aus diesem Skill berücksichtigen.
- Dieser Skill selbst bleibt eigenständig nutzbar (keine Hard-Dependency), die genannten
  Skills werden nur bei Bedarf ergänzend hinzugezogen.

## Grenzen dieses Skills

- Kein Zugriff auf echte Rankingpositionen, Backlink-Profile, Suchvolumen oder
  Konkurrenzdaten ohne angebundene Tools (Search Console, GA4, Sistrix, Ahrefs, Semrush etc.) –
  wird in diesem Fall explizit als Lücke benannt.
- JavaScript-lastige Seiten: `web_fetch` sieht ggf. nicht das, was Googlebot nach dem Rendern
  sieht. Bei Verdacht auf clientseitig nachgeladenen Content dies als Prüfpunkt vermerken statt
  falsche Sicherheit vorzutäuschen.
- Keine Garantie für Rankingverbesserung – Google bestätigt selbst, dass das Erfüllen aller
  Richtlinien keine Aufnahme oder Top-Platzierung garantiert.
