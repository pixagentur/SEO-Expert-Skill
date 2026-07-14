# SEO Expert Skill – Claude Plugin Marketplace

Dieses Repo ist eine [Claude Code Plugin-Marketplace](https://docs.claude.com/en/docs/claude-code/plugins), die den Skill **SEO Ranking Experte** bereitstellt.

## Installation

In Claude Code:

```
/plugin marketplace add pixagentur/SEO-Expert-Skill
/plugin install seo-ranking-experte@seo-expert-skill
```

Danach ist der Skill aktiv und wird automatisch getriggert, wenn eine Website/URL SEO-technisch analysiert werden soll (siehe [Skill-Beschreibung](./plugins/seo-ranking-experte/SKILL.md)).

## Updates

Neue Versionen werden hier im Repo veröffentlicht (siehe [CHANGELOG](./plugins/seo-ranking-experte/CHANGELOG.md)). Damit installierte Kopien automatisch aktualisiert werden, muss **Auto-Update für diese Marketplace einmalig aktiviert werden**:

```
/plugin
```
→ Tab **Marketplaces** → `seo-expert-skill` → Auto-Update aktivieren.

Ohne diese Einstellung holt Claude Code Updates nur auf manuellen Befehl:

```
/plugin marketplace update seo-expert-skill
```

## Enthaltene Plugins

| Plugin | Beschreibung |
|---|---|
| [`seo-ranking-experte`](./plugins/seo-ranking-experte/) | SEO-Audit, Score, Handlungsempfehlungen, Text-Swaps, automatischer PDF-Report |
