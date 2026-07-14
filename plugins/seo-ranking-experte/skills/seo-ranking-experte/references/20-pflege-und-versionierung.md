# Pflege & Versionierung

Diese Datei regelt zwei Ebenen der Versionierung:
1. Die **Skill-Gesamtversion** (SemVer, `MAJOR.MINOR.PATCH`) – für Weiterentwicklungen des
   kompletten Skills.
2. Die **Regelwerk-Ebene** (`10-regeln-technik-performance.md`, `11-regeln-content-eeat.md`,
   `12-regeln-ki-suche-geo.md`, `13-regeln-spam-risiken.md`) – einzelne Regeln mit eigener ID,
   die unabhängig von der Skill-Gesamtversion ergänzt/veraltet werden.

## Grundprinzip: Ergänzen statt Überschreiben

- Neue Erkenntnisse werden als **neue Regel mit neuer ID** ergänzt, nicht in bestehende Regeln
  hineingeschrieben. So bleibt nachvollziehbar, was sich wann geändert hat.
- Veraltete Regeln werden nicht gelöscht, sondern auf `Status: veraltet` gesetzt und bekommen
  einen Hinweis, warum (z. B. "durch R-TECH-0xx abgelöst" oder "Google-Richtlinie hat sich
  geändert am [Datum]").
- ID-Schema: `R-<KATEGORIE>-<Nummer>`, Kategorien: `TECH`, `CONTENT`, `GEO`, `SPAM`. Neue
  Kategorien nur anlegen, wenn eine neue Datei sie rechtfertigt (z. B. `R-LOCAL-...` für ein
  künftiges Local-SEO-Regelwerk).
- Nummern in 10er-Schritten vergeben (001, 002, 010, 011 ...), damit später Regeln thematisch
  dazwischen einsortiert werden können, ohne alles umzunummerieren.

## Skill-Versionierung (SemVer) – getrennt von den Regel-IDs

Die Regel-IDs (`R-TECH-001` usw.) versionieren einzelne Regeln. Zusätzlich hat der **gesamte
Skill** eine eigene Versionsnummer nach dem Schema `MAJOR.MINOR.PATCH`
([Semantic Versioning](https://semver.org/)), sichtbar in:
- dem Feld `version:` im YAML-Frontmatter von `SKILL.md`,
- dem Hinweis direkt unter der Überschrift in `SKILL.md`,
- `CHANGELOG.md` (Änderungshistorie),
- der Fußzeile jedes erzeugten PDF-Reports (`SKILL_VERSION` in `scripts/generate_report_pdf.py`).

Bei jeder Weiterentwicklung müssen **alle vier Stellen konsistent aktualisiert** werden.

### Wann welche Stelle erhöht wird

- **PATCH** (z. B. 1.0.0 → 1.0.1): Kleine Korrekturen ohne Verhaltensänderung – Tippfehler,
  Formulierungsschliff einer bestehenden Regel, kleine Bugfixes im PDF-Skript, die das
  Ausgabeformat nicht ändern.
- **MINOR** (z. B. 1.0.0 → 1.1.0): Neue, abwärtskompatible Funktionalität – neue Regeln ergänzt,
  neue Kategorie im Regelwerk, zusätzliche Intake-Frage, neues optionales Feld im
  PDF-Datenschema. Bestehende Nutzung des Skills funktioniert unverändert weiter.
- **MAJOR** (z. B. 1.1.0 → 2.0.0): Breaking Changes – Workflow-Schritte grundlegend umgebaut oder
  entfernt, Datenschema von `build_report()` inkompatibel geändert (bestehende Aufrufe würden
  fehlschlagen), Punkteverteilung des Bewertungssystems grundlegend neu gewichtet (macht alte
  Scores nicht mehr vergleichbar mit neuen).

### Ablauf bei einer neuen Version

1. Änderung wie gewohnt umsetzen (Regel ergänzen, Skript anpassen etc.).
2. Passende Versionsstufe nach obigem Schema bestimmen.
3. `version:` im Frontmatter von `SKILL.md` UND den Versionshinweis im Fließtext aktualisieren.
4. `SKILL_VERSION` in `scripts/generate_report_pdf.py` aktualisieren.
5. Neuen Eintrag oben in `CHANGELOG.md` ergänzen (Datum + Kategorien "Hinzugefügt/Geändert/
   Behoben/Entfernt", nur die zutreffenden).
6. Bei MAJOR-Änderungen zusätzlich in der Changelog-Zeile kurz vermerken, was konkret nicht mehr
   kompatibel ist, damit bestehende Nutzer:innen des Skills wissen, worauf sie achten müssen.

## Pflege des Regelwerks (Rule-Level)

### Ablauf bei neuen Erkenntnissen (z. B. nach einem Core Update)

1. Erkenntnis kurz auf Faktentreue prüfen: Ist es eine bestätigte, dauerhafte Änderung oder nur
   eine Einzelbeobachtung/Vermutung? Nur ersteres wird als Regel aufgenommen.
2. Passende Kategorie-Datei wählen, neue Regel mit nächster freier ID anlegen.
3. Format beibehalten: `ID | Status | Priorität` als Kopfzeile, dann Regel-Satz, dann
   `*Begründung: ...*` in einem Satz – ohne Nennung, aus welcher externen Quelle die Erkenntnis
   stammt (siehe Prinzip unten).
4. Prüfen, ob die neue Regel eine bestehende Regel widerspricht. Falls ja: die ältere Regel auf
   `veraltet` setzen und in der Begründung auf die neue ID verweisen, statt beide unkommentiert
   nebeneinander stehen zu lassen.
5. Bei Bedarf `03-audit-checkliste.md` ergänzen, falls die neue Regel ein neues, konkret
   prüfbares Kriterium liefert.

## Prinzip: Keine Quellenattribution im Regelwerk

Die Regeln werden bewusst als eigenständiges, angewandtes Fachwissen formuliert – ohne Verweis
auf einzelne Blogs, Studien oder Autor:innen. Das hat zwei Gründe:
1. Der Skill soll wie eine erfahrene Agentur mit eigener Expertise wirken, nicht wie eine
   Link-Sammlung.
2. Regeln sollen nach Plausibilität und Konsistenz mit den offiziellen Google-Grundlagen bewertet
   werden – nicht danach, wer sie zuerst aufgeschrieben hat.

Das bedeutet nicht, dass Herkunft für die Pflege irrelevant ist – nur, dass sie nicht Teil des
öffentlichen Regelwerks ist. Wer intern nachvollziehen möchte, aus welchem Themenfeld eine
ursprüngliche Erkenntnis kam, kann dafür eine eigene, nicht veröffentlichte Arbeitsnotiz führen
(außerhalb dieses Skill-Ordners, z. B. lokal beim Verfasser/bei der Verfasserin des Updates).

## Konflikte zwischen neuen und alten Erkenntnissen auflösen

Wenn zwei Erkenntnisse sich widersprechen (z. B. eine Taktik wird an einer Stelle empfohlen, an
anderer Stelle als riskant eingestuft):
- Die offiziellen Google-Grundprinzipien (Search Essentials, Spam Policies, Helpful Content) sind
  immer das Tie-Breaker-Kriterium – eine Praxis-Taktik, die diesen widerspricht, wird nicht
  übernommen (Beispiel: R-GEO-090).
- Bei zwei plausiblen, aber unterschiedlichen Praxis-Einschätzungen ohne klaren
  Google-Grundsatzbezug: die vorsichtigere, geringeres Risiko bergende Einschätzung übernehmen
  und ggf. beide Perspektiven in der Begründung kurz spiegeln.

## Regelmäßige Review-Empfehlung

- Nach jedem bestätigten Google Core Update: Regelwerk sichten, ob etwas veraltet oder ergänzt
  werden muss.
- Mindestens einmal pro Quartal unabhängig davon eine allgemeine Durchsicht, insbesondere der
  `12-regeln-ki-suche-geo.md` (Bereich mit der höchsten Veränderungsgeschwindigkeit).
