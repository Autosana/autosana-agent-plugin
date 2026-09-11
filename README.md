# Autosana agent plugin

A [Claude Code](https://claude.com/claude-code) plugin that helps you author, validate, and export
**[Autosana](https://autosana.ai) code-managed tests** — the `.autosana/` YAML flows, suites, and
hook files that Autosana syncs from your repo via its GitHub App.

The skill teaches Claude the exact file schema, the *validate-before-push* workflow, and the gotchas
that fail a sync, so you can build a valid `.autosana/` tree in one pass. It auto-activates when you
work on files under `.autosana/`, or you can invoke it directly.

## Install

In Claude Code:

```
/plugin marketplace add Autosana/autosana-agent-plugin
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

## OAuth MCP connection

This package also connects to `https://mcp.autosana.ai/mcp`. Complete browser sign-in when your client asks to authenticate. No API key is included or required by the package.

**Release status:** OAuth production rollout and marketplace review are still pending. Do not advertise this release as production-ready until production discovery, login, refresh, revocation, and tool calls pass. Preview testing does not establish production readiness.

## Cursor

The repository includes `.cursor-plugin/plugin.json` and `mcp.json` for Cursor, sharing the existing skills and the same hosted MCP service. The package is prepared for marketplace submission; it is not yet an approved listing. Authenticate in the browser when connecting.

## Claude Desktop

Claude Desktop uses a remote connector, separately from this Claude Code plugin. In Settings, open Connectors, add a custom connector with URL `https://mcp.autosana.ai/mcp`, and complete browser sign-in. Custom connector availability depends on your Claude account. Wait for the production OAuth rollout before using this URL for OAuth.

Official Claude connector directory submission and approval are separate from publishing this repository.

## Package structure

- `.claude-plugin/`: Claude Code plugin and marketplace metadata. The existing `autosana@autosana` identity is unchanged.
- `.cursor-plugin/plugin.json`: Cursor plugin metadata.
- `.codex-plugin/plugin.json`: Codex plugin metadata.
- `.mcp.json` and `mcp.json`: client-specific configuration pointing to the same hosted MCP endpoint.
- `skills/`: shared code-managed flow instructions.

No server implementation or credentials are distributed in this package.
