# Bewertungssystem: SEO-Score (0–1000 Punkte)

Ziel: ein einziger, verständlicher Gesamtwert (z. B. "837 von 1.000 Punkten"), der sich aus den
Kategorien der `03-audit-checkliste.md` ableitet – nachvollziehbar, reproduzierbar und über
mehrere Analysen hinweg vergleichbar (z. B. für Vorher-/Nachher-Vergleiche nach Umsetzung der
Empfehlungen).

## Punkteverteilung nach Kategorie (Summe = 1.000)

| Kategorie | Bezug | Max. Punkte |
|---|---|---|
| A. Crawling & Indexierung | Audit-Kategorie A | 150 |
| B. Content & E-E-A-T | Audit-Kategorie B | 300 |
| C. Page Experience & Core Web Vitals | Audit-Kategorie C | 150 |
| D. Strukturierte Daten | Audit-Kategorie D | 100 |
| E. Spam-Freiheit | Audit-Kategorie E | 100 |
| F. KI-Suche/GEO-Fitness | Audit-Kategorie F | 200 |
| **Gesamt** | | **1.000** |

Gewichtung begründet sich aus der Tragweite: Content/E-E-A-T und KI-Suche-Fitness wiegen am
schwersten, weil sie den größten und nachhaltigsten Rankingeinfluss haben; Crawling ist zwar
K.O.-kritisch, aber punktemäßig geringer gewichtet, weil es bei den meisten Websites entweder
ganz erfüllt oder komplett verletzt ist (wenig Graustufen).

## Punktevergabe pro Kategorie

Jede Kategorie enthält mehrere Checklisten-Kriterien (siehe `03-audit-checkliste.md`). Die
Punkte der Kategorie werden gleichmäßig auf ihre Kriterien verteilt. Pro Kriterium:

- 🟢 erfüllt → volle Punktzahl des Kriteriums
- 🟡 teilweise erfüllt → 50 % der Punktzahl des Kriteriums
- 🔴 nicht erfüllt → 0 Punkte

Beispiel: Kategorie D (Strukturierte Daten, 100 Punkte) hat 4 Kriterien → 25 Punkte je Kriterium.
Zwei 🟢, ein 🟡, ein 🔴 → 25 + 25 + 12,5 + 0 = 62,5 → gerundet 63 von 100.

Rohsumme = Summe aller Kategorie-Punkte, danach werden die Deckelungsregeln angewendet.

## Deckelungsregeln (werden NACH der Rohsummen-Berechnung angewendet)

Diese Regeln verhindern, dass ein einzelner K.O.-Mangel durch viele kleine Pluspunkte in anderen
Kategorien "weggemittelt" wird:

1. **Enthält Kategorie A ein 🔴 bei einem K.O.-Kriterium** (Seite nicht erreichbar/indexierbar) →
   Gesamtscore wird auf **maximal 150 Punkte** gedeckelt, unabhängig von der Rohsumme.
   *Begründung: Ohne Indexierung ist jede andere Stärke irrelevant.*
2. **Enthält Kategorie E (Spam-Freiheit) mindestens ein 🔴** → Gesamtscore wird auf **maximal 400
   Punkte** gedeckelt.
   *Begründung: Spam-Verstöße können unabhängig von sonstiger Qualität zu Abwertung/Ausschluss
   führen.*
3. **YMYL-Thema (laut Intake) ohne nachvollziehbare Fachautorenschaft** (R-CONTENT-012 in
   Kategorie B verletzt) → Punkte der Kategorie B werden vor der Gesamtsumme auf **maximal 50 %**
   ihres Rohwerts gedeckelt.
   *Begründung: Bei YMYL wiegt dieser einzelne Mangel besonders schwer.*

Regel 1 und 2 sind exklusiv-priorisiert: Greift Regel 1, wird Regel 2 nicht zusätzlich
angewendet (der niedrigere Deckel gilt ohnehin).

## Einordnung des Gesamtscores

| Punktebereich | Einordnung |
|---|---|
| 900–1.000 | Exzellent – im oberen Wettbewerbssegment |
| 750–899 | Gut – punktuelle Optimierungen sinnvoll |
| 550–749 | Ausbaufähig – spürbares, klar priorisierbares Potenzial |
| 300–549 | Schwach – grundlegende Probleme in mind. einer Kernkategorie |
| 0–299 | Kritisch – Ranking wahrscheinlich stark eingeschränkt |

## Darstellung im PDF-Report

- Ein Gesamt-Score-Diagramm (Halbkreis-/Gauge-Chart mit Farbzonen rot/gelb/grün, aktueller Wert
  groß in der Mitte, z. B. "837 / 1.000").
- Ein Kategorie-Balkendiagramm darunter (je Kategorie erreichte vs. mögliche Punkte), damit auf
  einen Blick sichtbar ist, welche Kategorie den größten Hebel bietet.
- Das Skript `scripts/generate_report_pdf.py` erzeugt beide Diagramme automatisch aus den
  Kategoriewerten.

## Wichtiger Hinweis zur Einordnung des Scores

Der Score ist eine **fachliche Einschätzung auf Basis öffentlich nachvollziehbarer Kriterien**,
keine Vorhersage einer exakten Google-internen Bewertung – Google verwendet ein weit
komplexeres, nicht vollständig offengelegtes System. Der Score dient primär dazu, Fortschritt
über die Zeit sichtbar zu machen (z. B. "beim letzten Audit 640, jetzt 837 nach Umsetzung der
Empfehlungen") und Prioritäten zu verdeutlichen – nicht als exakte Ranking-Prognose.
