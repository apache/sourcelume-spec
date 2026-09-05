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

# Versioning
 
This project follows [Semantic Versioning](https://semver.org)
(`MAJOR.MINOR.PATCH`).
 
The `context/`, `schema/`, and `spec/` directories describe one interlocking
data model — the JSON-LD context, the JSON Schema / SHACL shapes, and the
prose specification all describe the same terms and semantics. They
therefore share a single version number rather than versioning
independently. A given version directory, e.g. `0.0.1/`, under `context/`,
`schema/`, and `spec/` always describes the same release of the spec.
 
Version directories are named with the bare semver string (`0.0.1`, not
`v0.0.1`), so that version numbers can be compared and parsed directly by
tooling without stripping a prefix.
 
## What counts as MAJOR, MINOR, or PATCH
 
Because this repository defines a specification rather than an API or
library, semver is applied to the effect a change has on data that
conforms to the spec:
 
- **MAJOR** — a breaking change. Data that validated against the previous
  version may no longer validate, or may now mean something different.
  Examples: removing or renaming a term or field, changing a field's
  required-ness or type, changing the meaning of an existing term.
- **MINOR** — a backward-compatible addition. Existing valid data remains
  valid; new capabilities are added. Examples: adding a new optional
  field or term, adding a new example, adding a new crosswalk mapping.
- **PATCH** — a change with no semantic effect on validation. Examples:
  fixing a typo in prose, clarifying non-normative documentation or
  comments, fixing a bug in tooling (`tools/`) that doesn't change the
  schema or context themselves.
When in doubt about whether a change is MINOR or MAJOR, treat it as
MAJOR. Spec consumers rely on being able to trust that a MINOR or PATCH
bump never breaks their existing data.
 
## Released versions are immutable
 
Once a version directory has been published (tagged and released), its
contents under `context/`, `schema/`, and `spec/` must not be edited.
 
If a mistake is found in a released version, it must be corrected by
publishing a new version directory (at minimum a PATCH bump) rather than
editing the existing one in place. This guarantees that anyone who has
pinned to a specific version, e.g. `context/0.0.1/sourcelume.jsonld`, can
rely on that resource never changing out from under them.
 
## The `latest` pointer
 
`context/latest` is a symlink (or redirect) to the highest published
version directory, provided purely as a convenience for humans browsing
the repository.
 
`latest` is **not** a stable release target:
 
- Tooling, mappings, generated code, and any external references must
  always pin an exact version (e.g. `context/0.0.1/sourcelume.jsonld`),
  never `context/latest`.
- `latest` will move forward silently whenever a new version is
  published, so anything depending on it can break or silently change
  behavior without warning.

## Pre-1.0 versions
 
While the spec is at `0.x.y`, the same MAJOR/MINOR/PATCH rules above
still apply — a breaking change still bumps the leading non-zero
component (i.e. MINOR, since MAJOR is `0`), consistent with how most
semver-following projects treat `0.x` releases. Reaching `1.0.0` signals
that the spec's core terms are considered stable.
