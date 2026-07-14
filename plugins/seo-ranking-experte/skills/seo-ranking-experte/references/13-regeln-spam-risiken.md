# Regelwerk: Spam-Risiken

Jeder Treffer in dieser Liste ist ein Alarmsignal – anders als bei den übrigen Regelwerken gibt
es hier keine "teilweise erfüllt"-Zwischenstufe, die akzeptabel wäre.

**R-SPAM-001 | aktiv | K.O.**
Cloaking (unterschiedliche Inhalte für Crawler vs. Besucher:innen) ist in jeder Form
ausgeschlossen – auch dann, wenn die Begründung "nur für KI-Crawler gedacht" lautet.
*Begründung: Explizit gegen geltende Spam-Richtlinien, siehe auch R-GEO-090.*

**R-SPAM-002 | aktiv | K.O.**
Keine Doorway-Seiten (viele nahezu identische Seiten für Keyword-Varianten, die alle auf dieselbe
Zielseite verweisen).

**R-SPAM-003 | aktiv | K.O.**
Kein Keyword-Stuffing, keine versteckten Texte/Links.

**R-SPAM-004 | aktiv | K.O.**
Kein Linkkauf, keine automatisierten Linknetzwerke, keine exzessiven Linktausch-Programme; Links
in Gastbeiträgen/Pressemitteilungen mit `nofollow`/`sponsored` kennzeichnen, wenn sie nicht
redaktionell unabhängig vergeben wurden.

**R-SPAM-005 | aktiv | Hoch**
"Back-Button-Hijacking" (Nutzer:innen am Verlassen der Seite über den Zurück-Button hindern, um
sie auf weiteren Content/Werbung zu halten) als eigenständige, neuere Spam-Kategorie behandeln –
auch wenn technisch elegant umgesetzt.
*Begründung: Wurde als eigene Spam-Policy-Kategorie eingeführt, entsprechend explizit prüfen.*

**R-SPAM-006 | aktiv | Hoch**
Massenhafte, primär zur Rankinggewinnung erzeugte Inhalte ("Scaled Content Abuse") vermeiden –
unabhängig davon, ob manuell oder KI-gestützt produziert; Kriterium ist die fehlende
Mehrwert-Absicht, nicht das Produktionswerkzeug.

**R-SPAM-007 | aktiv | Mittel**
"Site Reputation Abuse" vermeiden: keine themenfremden Drittinhalte auf der eigenen (starken)
Domain hosten, nur um deren Autorität für fremde Zwecke auszunutzen.

**R-SPAM-008 | aktiv | Mittel**
Strukturierte Daten dürfen niemals Inhalte vortäuschen, die auf der Seite nicht sichtbar sind
(z. B. Fake-Bewertungssterne, nicht vorhandene Preise/Verfügbarkeiten).

## Umgang mit Funden

Wird bei einer Analyse eines dieser Muster entdeckt, wird es unabhängig von sonstigen positiven
Befunden **immer** in der Kategorie "🔴 Kritisch" der Handlungsempfehlungen aufgeführt – auch
wenn die Seite ansonsten technisch und inhaltlich stark ist.
