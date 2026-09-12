# Crosswalk: Sourcelume ↔ SPDX AI Profile

> **Status: draft.** Needs review against the current SPDX 3.0 AI profile release before being
> treated as authoritative.

The SPDX AI Profile extends SPDX 3.0 with AI-specific classes (`ai:AIPackage`,
`ai:DatasetPackage`) and already has strong primitives for license expression, which Sourcelume
should reuse rather than duplicate.

| Sourcelume field | SPDX AI Profile term | Notes |
|---|---|---|
| `identifier` | `spdx:SpdxId` / external identifier on `DatasetPackage` | SPDX favors its own ID scheme; mapping needs a stable rule (e.g. always carry the original DOI as an `ExternalIdentifier`). |
| `license` | `spdx:licenseConcluded` / `spdx:licenseDeclared` | SPDX distinguishes *declared* vs. *concluded* license — Sourcelume's single `license` field is closer to `licenseDeclared` since Sourcelume doesn't adjudicate accuracy. |
| `creator` | `spdx:suppliedBy` / `spdx:originatedBy` | SPDX splits "who supplied this copy" from "who originated the data" as distinct relationships; Sourcelume's `creator` is an array of role-tagged parties (`originator`/`curator`/`distributor`) as of 0.0.1, which maps more directly now but still isn't a 1:1 term match. |
| `custodyChain` | *(no direct equivalent)* | Closest SPDX concept is a `Relationship` between elements, but there's no first-class chain-of-custody event type. |

## Open questions

- Should `license` split into `licenseDeclared`/`licenseConcluded` in 0.0.2 to match SPDX more
  closely, or is the ambiguity intentional (Sourcelume publishes claims, not adjudications)?
