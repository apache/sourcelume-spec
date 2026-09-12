# Crosswalk: Sourcelume ↔ MLCommons Croissant

> **Status: draft.** Field-level mappings below are a starting proposal, not confirmed against
> the current Croissant release. Discuss on `dev@sourcelume.apache.org` before treating any row
> as final.

Croissant (`http://mlcommons.org/croissant/`) is a schema.org-based JSON-LD vocabulary for
describing ML datasets. Sourcelume records provenance/custody/licensing specifically, so most
Croissant terms (`distribution`, `recordSet`, `field`) have no Sourcelume equivalent — the overlap
is concentrated in dataset identity and licensing metadata, both of which Croissant itself borrows
from schema.org.

| Sourcelume field | Croissant / schema.org term | Notes |
|---|---|---|
| `identifier` | `schema:identifier` (on `cr:Dataset`) | Both typically hold a DOI or persistent URL. |
| `name` | `schema:name` | Direct match. |
| `license` | `schema:license` | Direct match — both expect an IRI or SPDX identifier. |
| `creator` | `schema:creator` | Same schema.org property, but Sourcelume's `creator` is an array of role-tagged (`originator`/`curator`/`distributor`) parties as of 0.0.1, rather than Croissant's single value. |
| `origin` | *(no direct equivalent)* | Croissant doesn't model a provenance narrative; stays Sourcelume-specific. |
| `custodyChain` | *(no direct equivalent)* | Custody-chain modeling is Sourcelume's core addition over Croissant. |

## Open questions

- Should a Sourcelume record be embeddable as a property of a Croissant `cr:Dataset` (e.g. a
  `sourcelume:provenance` extension property), or should the two stay as separate, cross-linked
  documents? Needs dev-list discussion.
