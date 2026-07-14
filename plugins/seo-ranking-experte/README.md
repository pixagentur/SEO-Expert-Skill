# SEO Ranking Experte – Claude Skill

**Version: 1.1.0** ([Änderungshistorie](./CHANGELOG.md))

Ein Claude-Skill, der wie eine erfahrene SEO-Agentur arbeitet: Man übergibt eine einzelne URL
oder eine ganze Website, und der Skill liefert eine kompakte SEO-Analyse, einen Gesamt-Score
(0–1.000 Punkte), priorisierte Handlungsempfehlungen, fertige Text-Ersetzungsvorschläge im
Originalstil der Seite – und am Ende immer automatisch einen speicherbaren PDF-Report.

## Was der Skill macht

1. Stellt vorab gezielte Fragen (Ziel, Zielgruppe, Umfang, Schreibstil, YMYL-Status).
2. Analysiert die Seite technisch (Crawlbarkeit, Core Web Vitals via PageSpeed-API, Structured
   Data) und inhaltlich (E-E-A-T, Helpful-Content-Kriterien, Spam-Risiken).
3. Liefert einen kurzen Ampel-Report (🟢/🟡/🔴) statt einer ausufernden Analyse.
4. Berechnet einen Gesamt-Score von 0–1.000 Punkten (z. B. "837 von 1.000 Punkten") inklusive
   Kategorie-Aufschlüsselung und Deckelungsregeln für K.O.-Mängel.
5. Priorisiert Handlungsempfehlungen nach Kritisch/Wichtig/Optional.
6. Erstellt eine Text-Swap-Tabelle (Ist-Text ↔ Neu-Text, bzw. "an Stelle XY einfügen" für neue
   Textbausteine), die den bestehenden Schreibstil trifft und sich natürlich/menschlich liest.
7. Erzeugt am Ende **immer automatisch** einen speicherbaren PDF-Report mit Score-Gauge-Chart,
   Kategorie-Balkendiagramm, Empfehlungen und Text-Swap-Liste.

## Grundlage

Die Regeln sind als eigenständiges, versioniertes Fachwissen dieses Skills formuliert
(`references/10`–`13`) – ohne Verweis auf einzelne externe Blogs, Studien oder Autor:innen im
Output. Das Regelwerk verweist nur dort explizit auf offizielle Google-Dokumentation, wo es sich
um verbindliche K.O.-Kriterien handelt (Search Essentials, Spam Policies). Wie das Regelwerk
gepflegt und bei neuen Erkenntnissen erweitert wird, steht in
`references/20-pflege-und-versionierung.md`.

## Installation

1. Repository klonen oder `seo-ranking-experte/` als Ordner herunterladen.
2. Den Ordner (bzw. die gepackte `.skill`-Datei) in Claude als Skill hinzufügen/hochladen.
3. Für den PDF-Report werden `reportlab` und `matplotlib` benötigt (übliche
   Python-Umgebungen haben beides bereits, sonst: `pip install reportlab matplotlib`).
4. Claude ansprechen, z. B.: *"Analysiere https://beispiel.de/produkte und verbessere das
   Ranking."*

## Struktur

```
seo-ranking-experte/
├── SKILL.md                                  # Workflow-Logik (Einstiegspunkt)
├── CHANGELOG.md                              # Versionshistorie (SemVer)
├── scripts/
│   └── generate_report_pdf.py                # Erzeugt den finalen PDF-Report inkl. Diagrammen
└── references/
    ├── 00-intake-fragen.md                   # Fragen vor Analysestart
    ├── 03-audit-checkliste.md                # Konkrete Prüfliste mit Ampel-Logik
    ├── 04-schreibstil-und-natuerlichkeit.md  # Stilanpassung & natürliches Texten
    ├── 05-bewertungssystem.md                # Score-Berechnung 0-1.000 inkl. Deckelungsregeln
    ├── 10-regeln-technik-performance.md      # Regelwerk: Technik/CWV/Structured Data
    ├── 11-regeln-content-eeat.md             # Regelwerk: Content & E-E-A-T
    ├── 12-regeln-ki-suche-geo.md             # Regelwerk: KI-Suche/GEO
    ├── 13-regeln-spam-risiken.md             # Regelwerk: Spam-K.O.-Kriterien
    └── 20-pflege-und-versionierung.md        # Regel-Pflege + Skill-Versionierung (SemVer)
```

## Versionierung

Der Skill folgt [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`). Die aktuelle
Version steht im Frontmatter von `SKILL.md`, direkt im SKILL.md-Text, in `CHANGELOG.md` sowie in
der Fußzeile jedes erzeugten PDF-Reports. Regeln dazu, wann welche Versionsstufe erhöht wird:
`references/20-pflege-und-versionierung.md`.

Ein zusätzlicher `maintenance/`-Ordner existiert lokal für die interne Nachvollziehbarkeit,
woher einzelne Regeln ursprünglich stammen. Er ist **bewusst nicht** Teil dieser
Veröffentlichung und sollte beim Hochladen auf GitHub ausgeschlossen bleiben (z. B. per
`.gitignore`).

## Grenzen & Hinweise

- Keine Ranking-Garantie – Google selbst garantiert nicht, dass regelkonforme Seiten indexiert
  oder top-platziert werden.
- Ohne angebundene Tools (Search Console, GA4, Ahrefs/Semrush/Sistrix-Connector) keine echten
  Rankingpositionen, Backlink- oder Suchvolumendaten – der Skill weist entsprechende Lücken
  explizit aus, statt Zahlen zu erfinden.
- Bei YMYL-Themen (Gesundheit, Recht, Finanzen, Sicherheit) empfiehlt der Skill ausdrücklich
  eine fachliche/juristische Prüfung vor Veröffentlichung.
- Dieser Skill ersetzt keine menschliche SEO-Beratung für strategische Grundsatzentscheidungen,
  sondern unterstützt die operative Umsetzung.

## Lizenz

MIT License – frei nutzbar, veränderbar und weiterverbreitbar. Ohne Gewähr für
Rankingergebnisse; siehe Abschnitt "Grenzen & Hinweise".

## Beitragen / Weiterentwickeln

Pull Requests willkommen, insbesondere für:
- Aktualisierung der destillierten Google-Regeln bei neuen Core-/Spam-Updates
- Ergänzung weiterer geprüfter Fachquellen
- Sprachvarianten (aktuell primär Deutsch ausgelegt)
