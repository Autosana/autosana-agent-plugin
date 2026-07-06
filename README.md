# Autosana — Claude Code plugin

A [Claude Code](https://claude.com/claude-code) plugin that helps you author, validate, and export
**[Autosana](https://autosana.ai) code-managed tests** — the `.autosana/` YAML flows, suites, and
hook files that Autosana syncs from your repo via its GitHub App.

The skill teaches Claude the exact file schema, the *validate-before-push* workflow, and the gotchas
that fail a sync, so you can build a valid `.autosana/` tree in one pass. It auto-activates when you
work on files under `.autosana/`, or you can invoke it directly.

## Install

In Claude Code:

```
/plugin marketplace add Autosana/claude-code-plugin
/plugin install autosana@autosana
```

Then invoke it explicitly with `/autosana:code-managed-flows`, or just start editing files under
`.autosana/` and Claude will pull the skill in automatically.

## What's inside

| Skill | Purpose |
| --- | --- |
| `code-managed-flows` | Author/validate/export `.autosana/` flows, suites, and hooks |

The skill pairs with the `autosana` CLI (`pip install "autosana>=0.8.0"`), which provides
`autosana flows validate` and `autosana flows export`.

## Learn more

- **Code-Managed Flows docs:** https://docs.autosana.ai/code-managed-flows
- **Install the CLI:** https://docs.autosana.ai/install-cli
- **Autosana:** https://autosana.ai
