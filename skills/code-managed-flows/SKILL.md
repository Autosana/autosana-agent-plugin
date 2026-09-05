---
name: code-managed-flows
description: Use when creating, editing, validating, or exporting Autosana code-managed tests — the `.autosana/` YAML flows, suites, and hook script files that Autosana syncs from a repo via its GitHub App. Covers the exact file schema, the validate-before-push workflow, and the gotchas that fail the sync.
---

# Autosana Code-Managed Flows

Autosana can define test **flows**, **suites**, and **hooks** as files under a repo's `.autosana/`
folder. On a push to the default branch, Autosana's GitHub App syncs those files and materializes
them as dashboard flows/suites (GitOps for tests — the repo is the source of truth, changes go
through PRs). Code-managed definitions are **read-only in the dashboard**; you edit them by
changing the files and pushing.

Use this skill whenever you're authoring or changing files under `.autosana/`, or the user asks
to create / validate / export Autosana code-managed flows.

## The golden rule: validate before you push

The sync applies **all-or-nothing** — one invalid file freezes materialization for the *whole*
`.autosana/` folder until it's fixed. So always validate locally before committing:

```bash
autosana flows validate                              # checks ./.autosana in the current dir
autosana flows validate services/mobile/.autosana    # or a specific path (monorepo)
```

Exit code is non-zero on any error, with the offending file + line. It validates the
flow/suite **YAML** (and `config.yaml`) exactly as the sync does; a few checks run **only** server-side (see
"What the CLI can't check"), so a green local run isn't a full guarantee — but it catches the
mechanical errors behind most sync failures.

## Workflow

1. Author/edit files under `.autosana/` (schema below).
2. `autosana flows validate` — fix every error before committing.
3. Optionally run the uncommitted tests: `autosana run <flow> --local` against a device from
   `autosana up`, or `autosana run --suite <key> --cloud` on Autosana's cloud devices.
4. Commit and open a PR (Autosana previews changed flows + posts an **Autosana - Code-Managed
   Flows** check), or push to the default branch to sync for real.
5. Read the check; it annotates parse errors inline with "Did you mean" hints.

## Repository layout

Everything lives under one `.autosana/` folder (repo root by default, or a subdirectory set via the
repo's **Root directory** setting for monorepos). Keys stay relative to `.autosana/` regardless.

```text
.autosana/
├── config.yaml              # run defaults for the CLI — not a test, never synced
├── login.flow.yaml          # a root flow (key "login")
├── hooks/
│   └── seed-db.py           # a hook — slug "seed-db"
└── smoke/                   # a suite folder (suite key "smoke")
    ├── _suite.yaml          # the suite manifest
    ├── checkout.flow.yaml   # a flow in the suite (key "smoke/checkout")
    └── hooks/
        └── reset-test-env.sh  # a hook — slug "reset-test-env"
```

A file is recognized only if it ends in `.flow.yaml`, is named exactly `_suite.yaml`, or sits
**directly** inside a `hooks/` folder with a supported extension. Everything else is ignored.

## Flow files — `*.flow.yaml`

Required keys are **`name`** and **`instructions`**. `instructions` is either a single multiline
prompt (a string → `single-prompt`) or a YAML list of step strings (a list → `step-by-step`).

```yaml
key: checkout
name: Checkout happy path
description: Buys one item as a logged-in user
caching: false
setup_hooks: [seed-db]
teardown_hooks: [reset-test-env]
instructions:
  - From the home screen, tap the cart icon
  - Tap "Checkout"
  - Verify the order confirmation screen appears
```

| Key | Required | Notes |
| --- | --- | --- |
| `name` | **Yes** | Non-empty string. |
| `instructions` | **Yes** | A YAML list of non-empty step strings, **or** a single non-empty prompt string. It's always `instructions`, never `steps`. |
| `type` | No | `step-by-step` or `single-prompt`. Inferred from `instructions`; set only to override. |
| `key` | No | Unique flow key. Defaults to the path minus `.autosana/` and `.flow.yaml` (`smoke/checkout`). Set it explicitly so run history follows a rename/move. |
| `description` | No | Free text. |
| `app` | Sometimes | Linked app name. Optional with 0–1 linked apps; **required on every flow once the repo links >1 app**. An unknown name fails the sync. |
| `caching` | No | Boolean, default `true`. |
| `setup_hooks` / `teardown_hooks` | No | Ordered lists of hook **slugs** (see Hooks). |

**Any top-level key not in this table is a hard error** (with a "Did you mean" suggestion).

## Suites — `_suite.yaml`

A suite is a folder with a `_suite.yaml`; the suite key is the folder path (`smoke/` → `smoke`).
`_suite.yaml` cannot sit at the `.autosana/` root — a suite *is* a folder. Only `name` is required.

```yaml
name: Smoke Tests
description: Critical-path checks
setup_flow: login
instructions: |
  Test account is qa+smoke@example.com.
flows: [login, smoke/checkout]
```

| Key | Required | Notes |
| --- | --- | --- |
| `name` | **Yes** | Non-empty string. |
| `flows` | No | Ordered list of flow-key references. Omit to include every flow **directly in this folder** (not subfolders), filename-alphabetical. |
| `setup_flow` | No | One flow-key reference to run first. |
| `description` | No | Free text. |
| `instructions` | No | Suite-level shared context. |
| `setup_hooks` / `teardown_hooks` | No | Ordered lists of hook slugs. |

References resolve **sibling-first** (a flow in the suite's own folder wins), else against every flow
in the repo. Flow keys and suite keys must each be **unique across the whole repo**.

## Hooks — script files under `hooks/`

The extension sets the hook type; the filename becomes the **slug** (final extension removed,
lowercased, runs of non-alphanumerics → `-`). `Seed DB.sh` → slug `seed-db`. The file content **is**
the script, stored verbatim (empty/whitespace-only is rejected).

| Extension | Hook type |
| --- | --- |
| `.py` | Python |
| `.js` | JavaScript |
| `.ts` | TypeScript |
| `.sh` | Bash |
| `.json` | Launch args (must be valid JSON) |

Reference hooks from a flow/suite via `setup_hooks` / `teardown_hooks` (ordered lists of slugs). A
slug resolves against **every active hook in your org** — repo files *and* dashboard hooks — so you
can reference dashboard-only **cURL** hooks by slug too (cURL has no file form). Duplicate slugs in
one list are rejected; the same slug in both setup and teardown is fine.

- Script hooks read env vars **natively** (`os.environ`, `process.env`, `$VAR`).
- Launch-args (`.json`) and cURL hooks use the `${env:KEY}` token instead.

## Run defaults — `config.yaml`

Which app a run targets normally comes from `--bundle-id`/`--platform` (mobile) or `--app-id` (web)
on every `autosana run`. Commit `.autosana/config.yaml` and those become defaults:

```yaml
apps:
  ios:
    bundle_id: com.example.app.dev
  android:
    bundle_id: com.example.app
  web:
    app_id: my-web-app
default_platform: ios
environment: staging   # optional
```

- **Only these keys.** `apps` (keyed `ios` / `android` / `web`; mobile entries take `bundle_id`, web
  takes `app_id`), `default_platform`, `environment`. Anything else is an error, and
  `autosana flows validate` reports it.
- **Precedence.** A flag beats `AUTOSANA_BUNDLE_ID`, which beats the file. `--platform <p>` picks
  that entry; with no `--platform`, `default_platform` does (or the sole entry when there is one).
  A `--local` run picks the entry for the live session's platform.
- **Not a test.** It is never uploaded by `--cloud` and never read by the sync — it only sets
  defaults for commands you run yourself.

## Referencing variables

Inside `instructions`, reference dashboard variables with `${env:VAR_NAME}` — **reference only**.
There is no `env:` block; values stay in the dashboard and resolve at run time. To invoke a hook by
display name mid-run, use `${hooks:Hook Name}` in the instructions text.

## Critical gotchas (these fail the sync)

- **Unknown top-level key = hard error.** Only the keys in the tables above are allowed.
- **`instructions`, never `steps`.** A list of steps still goes under `instructions:`.
- **Norway problem.** YAML reads bare `no`/`yes`/`on`/`off` as booleans. String fields like
  `setup_flow: no` or `name: on` fail — **quote them** (`"no"`).
- **Keys are unique repo-wide.** Duplicate flow keys or suite keys fail. Two hook files that slugify
  the same collide.
- **Hook slug scope is the whole org.** A slug matching a **dashboard** hook is *adopted* (its run
  history preserved) — not an error. A slug matching a **different repository's** hook *is* a
  blocking error → rename.
- **`app:` becomes required** on every flow once the repo links more than one app.
- **One broken file freezes everything.** Apply runs only at zero issues across all of `.autosana/`.
- **Deleting a hook still referenced** by any flow/suite fails — remove the `setup_hooks` /
  `teardown_hooks` reference in the same commit.

### What the CLI can't check (server-side only)

`app:` name resolution, hook-slug references + conflicts, and hook-file contents (empty scripts,
invalid launch-args JSON) need your org's data, so they run only on the server and surface on the
**Autosana - Code-Managed Flows** check after you push — not in `autosana flows validate`.

## Migrating existing dashboard flows

To move flows already defined in the dashboard into code, export them (writes flows, suites, **and**
their setup/teardown hook files, with `setup_hooks`/`teardown_hooks` wired up):

```bash
autosana flows export --all                 # every flow, suite, and their hooks → ./.autosana
autosana flows export --suite "Smoke Tests" # one suite and its flows
```

On the first sync after you commit + enable Code-Managed Testing, each exported flow/suite is
**adopted** by exact name (hooks by slug), preserving run history and becoming read-only. Review the
generated files (especially names) before enabling — adoption claims any single exact match, even an
unrelated one. cURL hooks are exported as slug references only (no file), staying dashboard-authored.

## References

- Full docs: https://docs.autosana.ai/code-managed-flows
- Hooks model: https://docs.autosana.ai/hooks · Variables: https://docs.autosana.ai/variables
