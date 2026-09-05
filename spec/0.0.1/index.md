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

# Apache Sourcelume Specification — v0.0.1

> **Status:** Draft / skeleton. This version is a starting point for
> development and has not been released. Content will be filled in as the
> specification develops. See `VERSIONING.md` for how this version number
> relates to changes in `context/` and `schema/`.

## 1. Introduction

Sourcelume defines a vocabulary and data model for describing
[fill in: what Sourcelume records represent, and the problem the spec
solves].

## 2. Terminology

This section defines terms used throughout the specification.

- **Record** — [definition]

## 3. Data model

This section describes the structure of a Sourcelume record.

Normative field definitions live in the corresponding JSON Schema
(`schema/0.0.1/sourcelume.schema.json`) and SHACL shapes
(`schema/0.0.1/sourcelume.shacl.ttl`). This document should describe the
*meaning* and intended usage of each field; the schema/shapes describe the
*constraints*.

| Field         | Type     | Required | Description                          |
|---------------|----------|----------|---------------------------------------|
| `id`          | IRI      | Yes      | Unique identifier for the record.     |
| `type`        | string   | Yes      | The record type.                      |
| `name`        | string   | No       | Human-readable name.                  |
| `description` | string   | No       | Free-text description.                |
| `version`     | string   | No       | Version of the record content.        |
| `createdAt`   | datetime | No       | Creation timestamp (ISO 8601).        |

## 4. JSON-LD context

Sourcelume records are expressed as JSON-LD using the context published at
`context/0.0.1/sourcelume.jsonld`.

## 5. Examples

See `examples/` for sample records conforming to this version of the
specification.

## 6. Conformance

[fill in: what it means for a document/tool to conform to this version of
the spec]

## 7. Changes from previous versions

This is the first version of the specification; there is no prior version
to compare against.