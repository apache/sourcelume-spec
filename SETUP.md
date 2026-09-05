<!--
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Apache Sourcelume Spec — Development Setup

This document describes how to set up a local development environment for the
Apache Sourcelume specification repository.

This repository is currently in its initial bootstrap phase. Some directories,
validation scripts, examples, schemas, contexts, and generated artifacts
referenced below may not exist yet. They are described here as the intended
development structure for contributors as the specification is built out.

This repository primarily contains versioned specification assets such as
JSON-LD contexts, JSON Schema files, SHACL shapes, examples, mappings, and prose
documentation. Python is the preferred language for local validation and
repository tooling.

Java and Maven are also used to package the versioned schema and context
resources for downstream consumers (ie Sourcelume Registry).

## Prerequisites

Install the following tools before working on this repository:

- Python 3.11 or newer
- `uv`
- Java 17 or newer
- Maven 3.9 or newer
- Git

Python is used for development tooling such as validation scripts.

`uv` is used to create the Python environment, install dependencies, and run
Python-based repository tools.

On macOS, `uv` can be installed with:
```bash
brew install uv
```

Or with the official installer:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

On Windows, `uv` can be installed with:
```bash
winget install astral.sh.uv
```

Java and Maven are used to package specification resources into a Maven artifact.

## Clone the repository

```bash
git clone https://github.com/apache/sourcelume-spec.git
cd sourcelume-spec
```

## Set up Python

Install the project development dependencies using `uv`:

```bash
uv sync --extra dev
```

This creates a local `.venv` directory and installs the development dependencies
declared in `pyproject.toml` (currently `jsonschema`, `pyld`, `rdflib`, and
`pyshacl`).

You normally do not need to activate the virtual environment manually. Prefer
running tools through `uv run`.

If you do want to activate the environment directly:
```bash
source .venv/bin/activate
```

To add a new development dependency, add it to the `dev` optional-dependencies
list in `pyproject.toml`, then re-run:
```bash
uv sync --extra dev
```

## Run Python validation tools

Validation tooling will live under `tools/`.

Once validation scripts are available, run them from the repository root using
`uv run`.

Example:
```bash
uv run python tools/validate.py
```

To test the validation tooling:
```bash
uv run python -m unittest discover -s tests
```


The validation tooling is expected to check things such as:

- JSON-LD example syntax
- JSON Schema validity
- Example conformance to the current schema
- SHACL validation, where applicable
- Cross-version consistency for published contexts and schemas

## Run Maven checks

The Maven build packages the specification resources for downstream use.

Run:
```bash
mvn clean verify
```

This verifies the project and packages the versioned `schema/` and `context/`
resources into the Maven artifact.

## IDE setup

When opening the repository in an IDE:

1. Use the repository root as the project directory.
2. Configure the Python interpreter to use `.venv`.
3. Configure Java 17 or newer for Maven support.
4. Run Python tools from the repository root using `uv run` so relative paths
   resolve correctly.

## Working on specification files

When adding or changing specification assets:

1. Add versioned files under `context/`, `schema/`, or `spec/`.
2. Add or update examples under `examples/`.
3. Update mappings under `mappings/` when fields or semantics change.
4. Run Python validation tools (see "Run Python validation tools" above).
5. Run Maven verification (see "Run Maven checks" above).

## Notes for contributors

- Prefer Python for repository tooling unless there is a strong reason not to.
- Use `uv` for Python environment and dependency management.
- Keep released version directories immutable.
- Add new versioned directories for incompatible or published changes.
- Do not treat `latest` as a stable release target.
- Keep examples small, clear, and valid.
- Keep generated files out of source control unless the project explicitly
  decides otherwise.

## Getting help

Development discussion happens on the Sourcelume developer mailing list:
```text
dev@sourcelume.apache.org
```

The project also uses the ASF Slack `#sourcelume` channel.