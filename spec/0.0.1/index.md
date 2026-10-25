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

# Apache Sourcelume Provenance Records — 0.0.1

## Status

Draft. Describes the two record types defined by schema/context version `0.0.1`:

- `ProvenanceRecord`: the minimal viable shape for a checkable claim about one dataset's identity,
  one or more role-tagged creators, its license, its origin, and an ordered custody chain.
- `TrainingProvenanceRecord`: a model producer's claim of which datasets a model was trained on,
  referencing dataset records by IRI. See [TrainingProvenanceRecord](#trainingprovenancerecord).

It intentionally leaves out cryptographic attestation, which is planned for later, once Sourcelume
Attest exists.

## Purpose

A `ProvenanceRecord` is a structured, machine-readable claim of the form: *this dataset, with
this identity, was produced/curated/distributed by these parties, is licensed under these terms,
came from this origin, and passed through this chain of custody.* Sourcelume does not verify the
claim's accuracy — it gives the claim a consistent shape so it *can* be verified by someone else.

## JSON-LD context

Records reference the context with the canonical IRI
`https://sourcelume.apache.org/context/0.0.1/sourcelume.jsonld` and no other `@context` value.
The context is published at that address by the release process and is not modified after release. Its namespace is the
stable `https://sourcelume.apache.org/ns#`, so term IRIs stay the same across versions. Inline
`@context` objects and other context IRIs are rejected.

## Fields

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | yes | IRI | Identifier for this provenance record itself (not necessarily the dataset). |
| `type` | yes | `"ProvenanceRecord"` | Fixed type discriminator. |
| `identifier` | yes | string (IRI or DOI) | Identifier for the dataset being described. |
| `name` | yes | string | Human-readable dataset name. |
| `version` | no | string | Dataset version, if versioned. |
| `license` | yes | IRI | License under which the dataset is claimed to be distributed (e.g. an SPDX license URL). See [License IRI conventions](#license-iri-conventions) below for public-domain and agreement-supplied cases. |
| `licenseScope` | no | string | Jurisdiction or scope in which the claimed `license` applies, for cases where a license (especially a public-domain claim) is jurisdiction-scoped rather than global. For example: `US` for US judicial-work-product public domain, or a longer clause for a copyright-expiration public-domain claim whose term depends on jurisdiction. Omit for licenses that apply globally (e.g. CC0, MIT). |
| `licenseNote` | no | string | Free-text qualifier for the claimed `license` IRI, for cases where the IRI alone is materially misleading. The classic case is a `license` IRI that reflects a processing artifact rather than an intended selection (e.g. a code subset that filters to a copyleft license by a bug, so the license IRI reads copyleft even though the intent was permissively-licensed code). Omit when the IRI faithfully represents the licensing situation. |
| `licenseCategory` | no | enum | Category of the claimed `license`, so its licensing *model* is checkable at a glance rather than only by reading the IRI. Values: `open-source` (standard permissive OSS, e.g. Apache 2.0, MIT), `open-data` (standard permissive data license, e.g. ODC-By, CC0), `public-domain` (CC Public Domain Mark or equivalent), `agreement-supplied` (data shared under a bilateral agreement whose terms do not permit public sharing), `use-restricted` (open IP grants but with use-based restrictions), `risk-based` (tiered access by risk band), `other`. Omit when the IRI is a well-known standard license whose category is obvious. |
| `licenseHistory` | no | array (min 1) | Prior licenses the dataset was distributed under, earliest first, when the dataset's own dataset-level license changed over time. The current license remains in the `license` field; this array records the superseded ones. Each entry: `iri` (prior license IRI) and `effectiveDate` (xsd:dateTime). Omit for datasets whose license has been stable since release. |
| `creator` | yes | array (min 1) | One or more parties involved in producing this dataset — each a `schema:Organization` or `schema:Person` with a `name`, and an optional `role` (`originator`, `curator`, or `distributor`) to distinguish who made the underlying data from who aggregated or redistributed it. Omit `role` for a single, undifferentiated creator. |
| `created` | yes | xsd:dateTime | When this provenance record was authored (record metadata, not content provenance). Distinct from `added` and `contentCreated` below. |
| `added` | yes | xsd:dateTime | When the dataset was added to the collection being described (e.g. when a source was incorporated into an aggregator corpus). Mirrors the `added` field commonly found in dataset datasheets. |
| `contentCreated` | yes | xsd:dateTime | When the dataset's underlying documents/content were originally created (e.g. the historical date of the texts). Mirrors the `created` field commonly found in dataset datasheets. For content created over a period this is the start of the period; see `contentCreatedEnd`. |
| `contentCreatedEnd` | no | xsd:dateTime | End of the period in which the underlying content was created. Omit for content created at a single point in time. Must not be earlier than `contentCreated`. |
| `origin` | yes | string | Free-text description of where the dataset's underlying data came from. |
| `custodyChain` | yes | array (min 1) | Ordered chain of custody events, earliest first. Each entry: `agent` (IRI), `action` (string, e.g. `"collected"`, `"ingested"`, `"transformed"`), `startTime` (xsd:dateTime). A single-hop dataset has exactly one entry. |

### `custodyChain` entries as a graph, not a nested tree

Each `custodyChain` entry's `agent` is an IRI. That IRI may point to either:

- an opaque external identifier with no corresponding Sourcelume record (e.g. a
  organization's homepage, a DOI, a repository URL), or
- the `id` of another Sourcelume record: a `ProvenanceRecord`, or a
  `TrainingProvenanceRecord` when the agent is a model that processed the data
  (for example, one that rewrote it).

When `agent` refers to another Sourcelume record, that upstream record's own
provenance is **not** nested or embedded inside the current record. A consumer
who wants to trace further back resolves `agent` as a reference — for example,
via the Registry's query API — to a separately-signed record of its own.

This is a deliberate choice, not an omission: `custodyChain` is not recursive,
and implementations should not expect (or produce) a custody event containing
an embedded sub-chain. Provenance beyond one hop is represented as a **graph of
linked, independently-signed records**, not as nesting within one record. This
matters for three reasons:

1. **Signing.** A record is signed as one unit. Embedding an upstream record's
   data inside a custody event would leave it unclear whose signature covers
   that embedded content — the embedding party's, or the original asserting
   party's. A reference by `id` avoids this ambiguity: each record is signed
   once, by whoever actually asserts it.
2. **Immutability.** Records are treated as append-only once signed. If an
   upstream record is later corrected, a reference by `id` means downstream
   consumers see the correction automatically; an embedded copy would not.
3. **Consistency with how the reference Registry stores records.** Provenance
   as a graph of linked entities, rather than nested documents, is the native
   shape for graph-backed storage — the schema and the storage model agree on
   what the data looks like.

Producers who want a self-contained document for a specific purpose (for
example, an offline audit bundle) may still choose to inline the referenced
node's full data using standard JSON-LD node inlining, rather than a bare
`@id` reference. This is a serialization choice available to any JSON-LD
consumer already, and does not require any change to this schema.

### One IRI, one record

An IRI denotes exactly one record, of one type, for the whole life of that record. The `id` names
the record, not the thing the record describes: an `agent` that is the `id` of a
`TrainingProvenanceRecord` refers to that record, not to the model itself.

References between records (`custodyChain[].agent`, `trainingData[].dataset`) are by IRI alone
and resolve across record types. A Registry reports the current state of the record a reference
names when the referencing record is read: one hop, status only, nothing stored in either record.

## TrainingProvenanceRecord

A `ProvenanceRecord` says where a dataset came from. It says nothing about which models were
trained on it, and it should not: that is a claim by the model's producer, not by the dataset's.
A `TrainingProvenanceRecord` is that second claim: *this model was trained on these datasets*. It
is the training-data inventory of a model, a bill of materials, and it is asserted by whoever
produced the model.

The record describes the model, using the same terms `ProvenanceRecord` uses for a dataset
(`identifier`, `name`, `version`, `creator`). The datasets are not described again. Each entry of
`trainingData` refers to a dataset by IRI, normally the `id` of a `ProvenanceRecord`, so that the
dataset's own provenance and license claims are found by following the reference, in the same
way as an `agent` in a `custodyChain` (see above). A dataset record never points back to the
models trained on it.

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | yes | IRI | Identifier for this record itself. |
| `type` | yes | `"TrainingProvenanceRecord"` | Fixed type discriminator. |
| `identifier` | yes | string (IRI or DOI) | Identifier for the model being described. |
| `name` | yes | string | Human-readable model name. |
| `version` | no | string | Model version or checkpoint, if versioned. |
| `creator` | yes | array (min 1) | The party or parties that produced the model and make this claim. Same shape as in `ProvenanceRecord`. |
| `created` | yes | xsd:dateTime | When this record was authored (record metadata, not a training date). |
| `disclosure` | yes | enum | How much of the training data the producer discloses: `complete` (every training dataset is listed), `partial` (only some are listed), or `undisclosed` (the producer does not disclose it). This is the producer's own statement. |
| `trainingData` | yes, unless `disclosure` is `undisclosed` | array (min 1) | The datasets the model was trained on, in no particular order. Entries are described below. |
| `note` | no | string | Free-text qualifier, e.g. where the full list is published or whether `tokens` are per epoch or in total. |

Each `trainingData` entry:

| Field | Required | Type | Description |
|---|---|---|---|
| `dataset` | yes | IRI | The dataset. Normally the `id` of a `ProvenanceRecord`; any other dataset IRI is allowed when no record exists. |
| `phase` | no | enum | Training phase in which the dataset was used: `pretraining`, `fine-tuning` (instruction, SFT and retrieval-grounding stages), `alignment`, or `evaluation` (held-out sets the model was tested on). Omit when the producer does not distinguish phases. |
| `tokens` | no | integer ≥ 0 | Number of tokens drawn from the dataset. |
| `share` | no | number, 0 to 1 | Fraction of the phase's training tokens that came from this dataset. Shares are not required to add up to 1, because a record may list only some of the datasets. |

### Resolving the references

The schema checks that `dataset` is an IRI, not that a record exists behind it. Whether a
referenced record exists, and what state the registry holds it in, is looked up when the
`TrainingProvenanceRecord` is read; it is not stored in the record or on the dataset record. A
model record therefore never carries an "approved" or "verified" flag, in line with the
non-goals below.

### Example

[`examples/dfm-mimir-v1-training.jsonld`](../../examples/dfm-mimir-v1-training.jsonld) describes
DFM Mímir v1 from Table 10 of its technical report. It references the 12 dataset records
among the `dfm-mimir-*.jsonld` examples and is marked `partial`, because the report lists 161 datasets and
only these 12 have a record. [`examples/acme-undisclosed-model.jsonld`](../../examples/acme-undisclosed-model.jsonld)
shows the `undisclosed` case, which needs no `trainingData`.

## License IRI conventions

Two interim conventions for cases SPDX has no direct term. Both are best-effort placeholders
pending a more precise term if/when the dev list takes it up.

(a) **Public domain by copyright expiration.** Use the CC Public Domain Mark IRI,
`https://creativecommons.org/publicdomain/mark/1.0/`. Pair with `licenseScope` when the PD
status is jurisdiction-scoped (e.g. judicial-work-product public domain in a specific country,
or works whose copyright-expiration term depends on jurisdiction) rather than a worldwide claim.

(b) **Agreement-supplied data.** For data shared under a bilateral agreement whose terms do
not permit public sharing (e.g. a data donation gated by a usage agreement), use
`https://sourcelume.apache.org/ns#agreement-supplied`.

## Non-goals for 0.0.1

- **No signature block.** Cryptographic signing is Sourcelume Attest's responsibility; this
  version defines the record's shape, not how it gets signed.
- **No adjudication fields.** There is no field for "verified: true/false" — Sourcelume publishes
  claims, and verification is a downstream concern for registries/auditors, not the record itself.
- **No audit metadata.** `ProvenanceRecord` stays dataset-centric, and `TrainingProvenanceRecord`
  only says which datasets a model was trained on. Results of auditing a model against its data
  (e.g. a memorisation audit) are a further, later record type.
- **No weight-level lineage.** `TrainingProvenanceRecord` does not describe what happened to a
  model's weights after training (merging, quantisation, editing). It names the training data,
  not the history of the artifact.

## See also

- [`context/0.0.1/sourcelume.jsonld`](../../context/0.0.1/sourcelume.jsonld) — the JSON-LD context.
- [`schema/0.0.1/sourcelume.schema.json`](../../schema/0.0.1/sourcelume.schema.json) — structural validation of a `ProvenanceRecord`.
- [`schema/0.0.1/sourcelume-training.schema.json`](../../schema/0.0.1/sourcelume-training.schema.json) — structural validation of a `TrainingProvenanceRecord`.
- [`schema/0.0.1/sourcelume.shacl.ttl`](../../schema/0.0.1/sourcelume.shacl.ttl) — RDF-level validation of both record types.
- `mappings/` — crosswalks to Croissant, the SPDX AI Profile, and OTDI (draft).
