# Apache Sourcelume Provenance Record — 0.0.1

## Status

Draft. Describes the `ProvenanceRecord` type defined by schema/context version `0.0.1`. This is
the minimal viable shape: enough to publish a checkable claim about one dataset's identity, one
or more role-tagged creators, its license, its origin, and an ordered custody chain. It
intentionally leaves out cryptographic attestation and downstream usage/audit metadata — those
are planned for later, once Sourcelume Attest exists and once the dataset-vs-model-usage scope
question is settled.

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
| `license` | yes | IRI | License under which the dataset is claimed to be distributed (e.g. an SPDX license URL). See [License IRI conventions](#license-iri-conventions) below for public-domain and agreement-supplied cases. |
| `licenseScope` | no | string | Jurisdiction or scope in which the claimed `license` applies, for cases where a license (especially a public-domain claim) is jurisdiction-scoped rather than global. For example: `US` for US judicial-work-product public domain, or a longer clause for a copyright-expiration public-domain claim whose term depends on jurisdiction. Omit for licenses that apply globally (e.g. CC0, MIT). |
| `licenseNote` | no | string | Free-text qualifier for the claimed `license` IRI, for cases where the IRI alone is materially misleading. The classic case is a `license` IRI that reflects a processing artifact rather than an intended selection (e.g. a code subset that filters to a copyleft license by a bug, so the license IRI reads copyleft even though the intent was permissively-licensed code). Omit when the IRI faithfully represents the licensing situation. |
| `licenseCategory` | no | enum | Category of the claimed `license`, so its licensing *model* is checkable at a glance rather than only by reading the IRI. Values: `open-source` (standard permissive OSS, e.g. Apache 2.0, MIT), `open-data` (standard permissive data license, e.g. ODC-By, CC0), `public-domain` (CC Public Domain Mark or equivalent), `agreement-supplied` (data shared under a bilateral agreement whose terms do not permit public sharing), `use-restricted` (open IP grants but with use-based restrictions), `risk-based` (tiered access by risk band), `other`. Omit when the IRI is a well-known standard license whose category is obvious. |
| `licenseHistory` | no | array (min 1) | Prior licenses the dataset was distributed under, earliest first, when the dataset's own dataset-level license changed over time. The current license remains in the `license` field; this array records the superseded ones. Each entry: `iri` (prior license IRI) and `effectiveDate` (xsd:dateTime). Omit for datasets whose license has been stable since release. |
| `creator` | yes | array (min 1) | One or more parties involved in producing this dataset — each a `schema:Organization` or `schema:Person` with a `name`, and an optional `role` (`originator`, `curator`, or `distributor`) to distinguish who made the underlying data from who aggregated or redistributed it. Omit `role` for a single, undifferentiated creator. |
| `created` | yes | xsd:dateTime | When this provenance record was authored (record metadata, not content provenance). Distinct from `added` and `contentCreated` below. |
| `added` | yes | xsd:dateTime | When the dataset was added to the collection being described (e.g. when a source was incorporated into an aggregator corpus). Mirrors the `added` field commonly found in dataset datasheets. |
| `contentCreated` | yes | xsd:dateTime | When the dataset's underlying documents/content were originally created (e.g. the historical date of the texts). Mirrors the `created` field commonly found in dataset datasheets; use the start of the range if a range applies. |
| `origin` | yes | string | Free-text description of where the dataset's underlying data came from. |
| `custodyChain` | yes | array (min 1) | Ordered chain of custody events, earliest first. Each entry: `agent` (IRI), `action` (string, e.g. `"collected"`, `"ingested"`, `"transformed"`), `startTime` (xsd:dateTime). A single-hop dataset has exactly one entry. |

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
- **No usage/audit metadata.** `ProvenanceRecord` is deliberately dataset-centric. A model
  producer's downstream usage claims about a dataset (e.g. a memorisation audit) belong to a
  separate, later record type, not to this one — this is a scope decision worth raising on the
  dev list rather than a settled fact.

## See also

- [`context/0.0.1/sourcelume.jsonld`](../../context/0.0.1/sourcelume.jsonld) — the JSON-LD context.
- [`schema/0.0.1/sourcelume.schema.json`](../../schema/0.0.1/sourcelume.schema.json) — structural validation.
- [`schema/0.0.1/sourcelume.shacl.ttl`](../../schema/0.0.1/sourcelume.shacl.ttl) — RDF-level validation.
- `mappings/` — crosswalks to Croissant, the SPDX AI Profile, and OTDI (draft).
