# Regelwerk: Technik & Performance

Format je Regel: **ID | Status | Priorität | Regel | Kurzbegründung**
Status: `aktiv` (wird angewendet) oder `veraltet` (bewusst ausgemustert, Grund vermerkt).
Priorität: `K.O.` (blockiert Ranking) / `Hoch` / `Mittel` / `Niedrig`.

## Crawling & Indexierung

**R-TECH-001 | aktiv | K.O.**
Seiten müssen crawlbar und indexierbar sein (HTTP 200, kein versehentliches `noindex`/Blockieren
wichtiger Bereiche über robots.txt).
*Begründung: Ohne Indexierung ist jede weitere Optimierung wirkungslos.*

**R-TECH-002 | aktiv | Hoch**
XML-Sitemap vorhanden, aktuell und in robots.txt referenziert; interne Verlinkung sorgt dafür,
dass wichtige Seiten max. 3–4 Klicks von der Startseite entfernt sind.
*Begründung: Beschleunigt Auffindbarkeit neuer/aktualisierter Inhalte.*

**R-TECH-003 | aktiv | Hoch**
Kanonische URLs korrekt setzen; Duplicate Content und Keyword-Kannibalisierung zwischen
mehreren eigenen Seiten zum selben Thema vermeiden.
*Begründung: Verhindert, dass die eigene Seite gegen die eigene Seite konkurriert und Signale
verwässert werden.*

**R-TECH-004 | aktiv | Mittel**
Nach Canonical-/Konsolidierungs-Fixes 1–2 Wochen Vorlaufzeit einplanen, bevor man Ergebnisse
bewertet – Indexanpassungen sind nicht sofort sichtbar.
*Begründung: Realistische Erwartungssteuerung, verhindert vorschnelle Fehldiagnosen.*

**R-TECH-005 | aktiv | Mittel**
Cookie-/Consent-Banner dürfen weder das Rendering des Hauptinhalts verzögern noch dessen
Crawling blockieren; technische Umsetzung des Banners immer mitprüfen, nicht nur rechtliche.
*Begründung: Ein häufig unterschätzter, aber real wirksamer Rankingkiller bei modernen
Consent-Lösungen.*

## Core Web Vitals & Page Experience

**R-TECH-010 | aktiv | Hoch**
Zielwerte: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1 (75. Perzentil, mobil und Desktop separat
prüfen).
*Begründung: Offizieller Schwellenwert-Standard; INP hat FID 2024 abgelöst.*

**R-TECH-011 | aktiv | Mittel**
Gute Core-Web-Vitals-Werte sind Voraussetzung, kein eigenständiger Rankingbooster – ein
technisch perfekter, aber inhaltlich schwacher Auftritt gewinnt dadurch keine Top-Position.
*Begründung: Verhindert Fehlinvestition in Perfektionierung der Ladezeit auf Kosten von Content.*

**R-TECH-012 | aktiv | Mittel**
Seitengeschwindigkeit wirkt sich zusätzlich auf die Wahrscheinlichkeit aus, von KI-Systemen
(Chatbots/Answer Engines) gecrawlt und zitiert zu werden – schnelle Seiten werden von
KI-Crawlern zuverlässiger vollständig erfasst.
*Begründung: Page Speed ist nicht mehr nur ein klassisches Ranking-, sondern auch ein
KI-Sichtbarkeitsthema.*

**R-TECH-013 | aktiv | Mittel**
Technische Mängel priorisiert vor neuem Content beheben, wenn beides um Ressourcen konkurriert:
ungelöste kritische technische Probleme "bluten" jeden Monat Sichtbarkeit, auch wenn der Effekt
unsichtbar bleibt (man sieht nicht, was man dadurch nicht verliert).
*Begründung: Technische Schulden sind ein unterschätzter, aber messbar wirksamer Hebel –
sichtbarer Content-Fortschritt verdrängt in der Praxis oft unsichtbare, aber wichtigere Fixes.*

## Strukturierte Daten

**R-TECH-020 | aktiv | Hoch**
Strukturierte Daten (JSON-LD bevorzugt) müssen wahrheitsgemäß dem sichtbaren Inhalt entsprechen;
alle Pflichtfelder ausfüllen, lieber wenige Felder korrekt als viele unvollständig/fehlerhaft.
*Begründung: Fehlerhafte/irreführende Markup führt zu Rich-Result-Verlust bis Manual Action.*

**R-TECH-021 | aktiv | Niedrig**
`llms.txt` als optionales, noch nicht standardisiertes Signal für KI-Systeme betrachten – kein
Pflichtkriterium, aber unschädliche Ergänzung, wenn ohnehin Ressourcen vorhanden sind.
*Begründung: Kein offizieller Ranking- oder Zitier-Standard, aber wachsende Praxisverbreitung.*

## Crawler-Zugänglichkeit für KI-Systeme

**R-TECH-030 | aktiv | Mittel**
Bewusst entscheiden (nicht per Default blockieren), ob KI-Crawler (u. a. GPTBot und vergleichbare
User-Agents) Zugriff erhalten – abhängig vom Geschäftsmodell (Sichtbarkeit in KI-Antworten vs.
Schutz vor Content-Abgriff).
*Begründung: Pauschales Blockieren aus Reflex verhindert Sichtbarkeit in einem wachsenden
Suchkanal; pauschales Erlauben ignoriert mögliche Content-Schutz-Interessen. Eine bewusste,
im Intake abgefragte Entscheidung ist besser als ein Default.*
