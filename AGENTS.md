<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# AGENTS.md

Guidance for AI coding agents (and the humans running them) working in
this repository. This is the place to record conventions any harness —
Claude Code, Cursor, Copilot, Junie, Codex, a local `pi` setup, whatever
comes next — is expected to follow here. When in doubt, follow the
Apache Sourcelume project conventions over any default the harness
suggests.

## Project overview

This repository, `apache/sourcelume-spec`, holds the **Apache Sourcelume**
provenance metadata specification: the JSON-LD `@context`, the JSON Schema
and SHACL shapes, the normative prose, and the tooling that validates
examples against them. Sourcelume is about AI training-data
**provenance and licensing** — signed, independently verifiable records of
where a dataset came from and what terms it carries — not about training
models on known data.

This repo is early-stage. The `0.0.1` version directories are scaffolding
that is being filled in; do not assume structure described in `README.md`
already exists on disk (the README's tree is partly aspirational). Verify
against the actual tree before referencing paths.

## Build and test commands

Tooling is split by language, on purpose:

- **Python (via `uv`) owns spec validation and repo tooling.**
  - `uv sync --extra dev` — install dev dependencies (`jsonschema[format]`,
    `pyld`, `rdflib`, `pyshacl`).
  - `uv run python tools/validate.py` — validate every `examples/*.jsonld`
    against the corresponding version's schema (jsonschema 2020-12, with
    format assertions enforced) and SHACL shapes (pyshacl). This is the
    real gate: it does not just parse JSON.
  - `uv run python -m unittest discover -s tests` — run the validator's
    own unit tests.
- **Java/Maven owns packaging** of the `context/` and `schema/` resources
  into a JAR for JVM consumers (e.g. the Sourcelume Registry) and runs RAT
  license-header enforcement.
  - `mvn -B verify` — build the artifact and run RAT checks.

Run both before opening or updating a PR. A green `validate.py` plus a
green `mvn -B verify` is the local bar.

## Versioning and immutability

`context/`, `schema/`, and `spec/` describe one interlocking data model and
share a single version number. See `VERSIONING.md` for the full rules; the
short version an agent must internalize:

- Version directories use the **bare semver** string (`0.0.1`, not `v0.0.1`),
  uniformly under `context/`, `schema/`, and `spec/`.
- **Released version directories are immutable.** Once a version is
  tagged/released, do not edit files under that version dir — cut a new
  version instead.
- **Pre-1.0 versions are mutable** while unreleased. Fixable gaps in an
  unreleased `0.0.1` get folded into `0.0.1`; they do not require a `0.0.2`
  unless `0.0.1` has already been tagged.
- `context/latest` is a human-browsing convenience pointer, **not** a
  stable release target. Tooling and external references must pin an
  exact version.
- `spec/<version>/` holds only immutable normative prose for that version.
  Research notes, stress tests, and other non-spec artifacts belong in a
  non-versioned top-level directory (e.g. `notes/`), not under `spec/`.

## Vocabulary reuse

Reuse existing standard terms wherever an equivalent exists
(`dct:`, `schema:`, `spdx:`) rather than inventing Sourcelume-native terms.
The `sourcelume:` namespace stays minimal. This is a deliberate project
decision; do not introduce a new `sourcelume:` term when an established
one will do.

## Commit messages and AI attribution

This is the part every harness must get right. Apache Sourcelume follows
the ASF generative-tooling guidance and the draft convention documented at
<https://rai.apache.org/commit-messages.html>. The established, in-repo
practice (see existing commits by `jgoodyear`) is a three-line trailer
block at the end of the commit message body:

```
Apache-ai: Yes
Generated-by: <tool> (<model>)
Reviewed-by: <human>
```

For example:

```
Apache-ai: Yes
Generated-by: Claude Code (Sonnet 5)
Reviewed-by: anierbeck
```

Rules:

- **`Generated-by:`** — required when an AI tool produced the code, even
  if a human reviewed and edited it. Name the actual tool and model
  (e.g. `Claude Code (Sonnet 5)`, `PyCharm AI Assistant (Claude 4.5 Sonnet)`,
  `Webstorm Junie (Gemini 3 Flash)`), not a generic label.
- **`Assisted-by:`** — use this instead of `Generated-by:` only when the
  human wrote the code and the AI helped in small ways. They are not the
  same action: *Generated* = AI produced, human reviewed; *Assisted* =
  human produced, AI helped. Pick the one that matches what actually
  happened.
- **`Apache-ai: Yes`** — include alongside `Generated-by:` / `Assisted-by:`
  when AI played a significant role, for policy transparency.
- **`Reviewed-by:`** — the human who reviewed the change.
- **`Co-authored-by:`** is for humans only, never for an AI tool.
- The commit message is the committer's representation. Even when AI
  generated the code, the committer is responsible for what's committed.

## Pull requests

- This repository is dual-hosted: authoritative history is on
  `gitbox.apache.org`, mirrored to/from GitHub. Contribute via a GitHub
  pull request against `main` (fork, branch, PR). `main` is treated as
  protected; do not push directly to it.
- Non-trivial or cross-cutting spec changes are normally discussed on the
  dev list first (`dev@sourcelume.apache.org`,
  [archives](https://lists.apache.org/list.html?dev@sourcelume.apache.org)),
  not just via PR. When a discussion has happened on-list, reference it in
  the PR description.
- Apache License 2.0 applies; preserve `LICENSE` and `NOTICE`. RAT
  license-header enforcement runs in `mvn verify`; non-code files
  (`.jsonld`, `.json`, `.ttl`, `.md`) are RAT-excluded by rule, but code
  files are not — add the ASF header to new code files.
- Run `uv run python tools/validate.py` and `mvn -B verify` before pushing.
