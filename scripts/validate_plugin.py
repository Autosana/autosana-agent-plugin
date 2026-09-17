"""Check this repository's shared plugin packaging without external dependencies."""

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://mcp.autosana.ai/mcp"
REPOSITORY = "https://github.com/Autosana/autosana-agent-plugin"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_path(reference):
    require(isinstance(reference, str), "File references must be strings")
    path = (ROOT / reference).resolve()
    require(not Path(reference).is_absolute(), f"Absolute file reference: {reference}")
    require(
        path.is_relative_to(ROOT), f"File reference escapes repository: {reference}"
    )
    require(path.exists(), f"Missing referenced path: {reference}")
    return path


def read_json(reference):
    return json.loads(local_path(reference).read_text())


def validate():
    versions = set()
    for client in ("claude", "cursor", "codex"):
        filename = f".{client}-plugin/plugin.json"
        manifest = read_json(filename)
        require(manifest["name"] == "autosana", f"Wrong plugin name in {filename}")
        require(manifest["description"].strip(), f"Missing description in {filename}")
        version = manifest["version"]
        require(
            re.fullmatch(r"\d+\.\d+\.\d+", version),
            f"Invalid release version: {version}",
        )
        versions.add(version)
        config = read_json(manifest["mcpServers"])
        expected = {"url": MCP_URL}
        if client != "cursor":
            expected["type"] = "http"
        require(
            config == {"mcpServers": {"autosana": expected}},
            f"Unexpected MCP configuration for {client}; use the production OAuth endpoint without credentials",
        )
        if "logo" in manifest:
            require(
                local_path(manifest["logo"]).is_file(), f"Invalid logo in {filename}"
            )
        if "repository" in manifest:
            require(
                manifest["repository"] == REPOSITORY, f"Wrong repository in {filename}"
            )
        if client == "codex":
            require(
                local_path(manifest["skills"]).is_dir(),
                "Missing Codex skills directory",
            )
            for asset in ("logo", "composerIcon"):
                require(
                    local_path(manifest["interface"][asset]).is_file(),
                    f"Missing Codex {asset}",
                )
    require(len(versions) == 1, "Plugin versions must match across clients")

    marketplace = read_json(".claude-plugin/marketplace.json")
    require(
        marketplace["name"] == "autosana", "Marketplace identity must remain autosana"
    )
    require(len(marketplace["plugins"]) == 1, "Expected one marketplace plugin")
    entry = marketplace["plugins"][0]
    require(entry["name"] == "autosana", "Marketplace plugin name must match")
    require(
        local_path(entry["source"]) == ROOT,
        "Marketplace source must be repository root",
    )
    require(entry["repository"] == REPOSITORY, "Wrong marketplace repository")

    for reference in ("README.md", "LICENSE", "skills/code-managed-flows/SKILL.md"):
        require(local_path(reference).is_file(), f"Missing package file: {reference}")
    print(
        f"Plugin packaging valid for Claude Code, Cursor, and Codex (v{versions.pop()})."
    )


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, KeyError, TypeError, OSError) as error:
        sys.exit(f"Plugin validation failed: {error}")
