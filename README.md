# Autosana agent plugin

A plugin for Claude Code, Cursor, and Codex that connects your assistant to
[Autosana](https://autosana.ai) for web, iOS, and Android testing. It also helps you author,
validate, and export code-managed tests: the `.autosana/` YAML flows, suites, and hook
files that Autosana syncs from your repo via its GitHub App.

The skill teaches your assistant the exact file schema, the *validate-before-push* workflow, and the gotchas
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

Browser sign-in is available on the production MCP endpoint. Official marketplace listings remain subject to each marketplace's review.

## Cursor

Once the plugin is listed in the Cursor Marketplace, open **Cursor Settings → Plugins**, search for **Autosana**, and click **Install**. You can also run `/add-plugin autosana` in chat. Complete the browser sign-in when Cursor connects. There's no API key to configure.

To try the plugin before it's listed, clone this repository to `~/.cursor/plugins/local/autosana` and reload Cursor.

The Cursor plugin uses `.cursor-plugin/plugin.json` and `mcp.json`, and shares the skills and the hosted MCP service with the other clients.

## Codex

Install from the repository using the Codex CLI:

```sh
codex plugin marketplace add Autosana/autosana-agent-plugin
codex plugin add autosana@autosana
```

Start a new session and complete browser sign-in when prompted. The plugin includes the MCP connection and the shared code-managed flow skill.

## Claude Desktop

Claude Desktop uses a remote connector, separately from this Claude Code plugin. In Settings, open Connectors, add a custom connector with URL `https://mcp.autosana.ai/mcp`, and complete browser sign-in. Custom connector availability depends on your Claude account.

Official Claude connector directory submission and approval are separate from publishing this repository.

## Package structure

- `.claude-plugin/`: Claude Code plugin and marketplace metadata. The existing `autosana@autosana` identity is unchanged.
- `.cursor-plugin/plugin.json`: Cursor plugin metadata.
- `.codex-plugin/plugin.json`: Codex plugin metadata.
- `.mcp.json` and `mcp.json`: client-specific configuration pointing to the same hosted MCP endpoint.
- `skills/`: shared code-managed flow instructions.

No server implementation or credentials are distributed in this package.
