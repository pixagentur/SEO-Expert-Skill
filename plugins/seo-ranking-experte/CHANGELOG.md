# Changelog

Alle nennenswerten Änderungen an diesem Skill werden hier dokumentiert. Format orientiert sich an
[Keep a Changelog](https://keepachangelog.com/), Versionierung folgt
[Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

Die genauen Regeln, wann welche Stelle der Versionsnummer erhöht wird, stehen in
`references/20-pflege-und-versionierung.md` (Abschnitt "Skill-Versionierung").

## [1.1.0] – 2026-07-14

### Hinzugefügt
- Feste Standardregel für Website-weite Analysen (mehrere URLs): immer ein vollständiger
  PDF-Report pro URL plus ein zusätzliches, übergreifendes Executive-Summary-PDF – keine
  Rückfrage beim Intake mehr nötig (`SKILL.md` Schritt 7).
- `build_summary_report()` in `scripts/generate_report_pdf.py`: neues, eigenständiges PDF mit
  Score-Vergleich (Balkendiagramm), Seiten-Übersichtstabelle und optionalen
  seitenübergreifenden Erkenntnissen.

### Geändert
- Referenz auf den `pdf`-Skill in Schritt 7 präzisiert (nur noch für optionale
  Nachbearbeitung, nicht mehr für das Zusammenführen mehrerer Reports – das übernimmt jetzt
  `build_summary_report`).

## [1.0.0] – 2026-07-14

Erste vollständige Fassung mit allen Kernfunktionen. Erstveröffentlichungsstand für GitHub
Marketplace.

### Hinzugefügt
- Bewertungssystem: Gesamt-Score von 0–1.000 Punkten mit Kategorien-Gewichtung und
  Deckelungsregeln für K.O.-Mängel (`references/05-bewertungssystem.md`).
- Automatische PDF-Report-Erzeugung am Ende jeder Analyse, inkl. Score-Gauge-Chart und
  Kategorie-Balkendiagramm (`scripts/generate_report_pdf.py`).
- Klare Unterscheidung in der Text-Swap-Liste zwischen "Text ersetzen" (Ist-Text/Neu-Text) und
  "neuen Text einfügen" (mit Stellenangabe).
- Skill-Versionierung inkl. dieser Changelog-Datei.

### Geändert
- Regelwerk vollständig auf Basis aller 13 vom Auftraggeber vorgegebenen Fachquellen plus
  offizieller Google-Dokumentation synthetisiert und in vier Themendateien strukturiert
  (`references/10`–`13`), mit eindeutigen Regel-IDs statt Fließtext.
- Keine Quellen-/Autor:innen-Nennung mehr im Skill-Output – das Regelwerk wird als eigenständiges
  angewandtes Fachwissen dargestellt (siehe `references/20-pflege-und-versionierung.md`).

### Entfernt
- Frühere Dateien `01-google-regeln.md`, `02-blog-insights.md`, `05-quellenverzeichnis.md`
  (ersetzt durch das konsolidierte, quellenfreie Regelwerk `10`–`13`).

## [0.2.0] – 2026-07-14 (nicht veröffentlicht, interner Zwischenstand)

### Hinzugefügt
- Intake-Fragen (`00-intake-fragen.md`) und Audit-Checkliste mit Ampel-Logik
  (`03-audit-checkliste.md`).
- Schreibstil- und Natürlichkeits-Leitfaden (`04-schreibstil-und-natuerlichkeit.md`).
- Erster Regel-Entwurf auf Basis offizieller Google-Quellen, plus grobe Einordnung der
  vorgegebenen Fachblog-Liste (mit Quellenangaben – später in 1.0.0 entfernt).

## [0.1.0] – 2026-07-14 (nicht veröffentlicht, erster Entwurf)

### Hinzugefügt
- Grundgerüst des Skills: SKILL.md mit Workflow-Skizze, README, LICENSE (MIT).
- Erste, noch unvollständige Quellenrecherche zu offiziellen Google-Ranking-Kriterien.

---

## Format für zukünftige Einträge

```
## [MAJOR.MINOR.PATCH] – JJJJ-MM-TT

### Hinzugefügt
- ...

### Geändert
- ...

### Behoben
- ...

### Entfernt
- ...
```

Nur die tatsächlich zutreffenden Unterabschnitte verwenden, leere Abschnitte weglassen.
