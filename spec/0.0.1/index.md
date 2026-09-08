# Apache Sourcelume Provenance Record — 0.0.1

## Status

Draft. Describes the `ProvenanceRecord` type defined by schema/context version `0.0.1`. This is
the minimal viable shape: enough to publish a checkable claim about one dataset's identity, one
or more role-tagged creators, its license, its origin, and an ordered custody chain. It
intentionally leaves out cryptographic attestation and downstream usage/audit metadata — those
are planned for later, once Sourcelume Attest exists and once the dataset-vs-model-usage scope
question is settled on the dev list (see `notes/stress-test-dfm-mimir.md`).

## Purpose

A `ProvenanceRecord` is a structured, machine-readable claim of the form: *this dataset, with
this identity, was produced/curated/distributed by these parties, is licensed under these terms,
came from this origin, and passed through this chain of custody.* Sourcelume does not verify the
claim's accuracy — it gives the claim a consistent shape so it *can* be verified by someone else.

## Fields

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | yes | IRI | Identifier for this provenance record itself (not necessarily the dataset). |
| `type` | yes | `"ProvenanceRecord"` | Fixed type discriminator. |
| `identifier` | yes | string (IRI or DOI) | Identifier for the dataset being described. |
| `name` | yes | string | Human-readable dataset name. |
| `version` | no | string | Dataset version, if versioned. |
| `license` | yes | IRI | License under which the dataset is claimed to be distributed (e.g. an SPDX license URL). For a public-domain-by-copyright-expiration claim, for which SPDX has no direct term, use the CC Public Domain Mark IRI (`https://creativecommons.org/publicdomain/mark/1.0/`) as the current best-effort convention pending a more precise term. |
| `creator` | yes | array (min 1) | One or more parties involved in producing this dataset — each a `schema:Organization` or `schema:Person` with a `name`, and an optional `role` (`originator`, `curator`, or `distributor`) to distinguish who made the underlying data from who aggregated or redistributed it. Omit `role` for a single, undifferentiated creator. |
| `created` | yes | xsd:dateTime | When this provenance record was authored (record metadata, not content provenance). Distinct from `added` and `contentCreated` below. |
| `added` | yes | xsd:dateTime | When the dataset was added to the collection being described (e.g. when a source was incorporated into dynaword). Mirrors the `added` field in dynaword datasheets. |
| `contentCreated` | yes | xsd:dateTime | When the dataset's underlying documents/content were originally created (e.g. the historical date of the texts). Mirrors the `created` field in dynaword datasheets; use the start of the range if a range applies. |
| `origin` | yes | string | Free-text description of where the dataset's underlying data came from. |
| `custodyChain` | yes | array (min 1) | Ordered chain of custody events, earliest first. Each entry: `agent` (IRI), `action` (string, e.g. `"collected"`, `"ingested"`, `"transformed"`), `startTime` (xsd:dateTime). A single-hop dataset has exactly one entry. |

## Non-goals for 0.0.1

- **No signature block.** Cryptographic signing is Sourcelume Attest's responsibility; this
  version defines the record's shape, not how it gets signed.
- **No adjudication fields.** There is no field for "verified: true/false" — Sourcelume publishes
  claims, and verification is a downstream concern for registries/auditors, not the record itself.
- **No usage/audit metadata.** `ProvenanceRecord` is deliberately dataset-centric. A model
  producer's downstream usage claims about a dataset (e.g. a memorisation audit) belong to a
  separate, later record type, not to this one — this is a scope decision worth defending on the
  dev list rather than a settled fact, see `notes/stress-test-dfm-mimir.md`.

## See also

- [`context/0.0.1/sourcelume.jsonld`](../../context/0.0.1/sourcelume.jsonld) — the JSON-LD context.
- [`schema/0.0.1/sourcelume.schema.json`](../../schema/0.0.1/sourcelume.schema.json) — structural validation.
- [`schema/0.0.1/sourcelume.shacl.ttl`](../../schema/0.0.1/sourcelume.shacl.ttl) — RDF-level validation.
- [`examples/minimal-record.jsonld`](../../examples/minimal-record.jsonld) — a conformant example.
- `mappings/` — crosswalks to Croissant, the SPDX AI Profile, and OTDI (draft).
- [`notes/stress-test-dfm-mimir.md`](../../notes/stress-test-dfm-mimir.md) — real-dataset stress
  test that motivated the `creator`/`custodyChain` shape above and raises the still-open
  usage/audit scope question.
