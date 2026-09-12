# Changelog
 
All notable changes to the Apache Sourcelume specification will be
documented in this file.
 
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org) as
described in `VERSIONING.md`.
 
## [Unreleased]
 
### Added

- Unit tests for the validation tooling (`tests/test_validate.py`), covering
  successful validation of minimal valid ProvenanceRecords and proper rejection
  of incomplete records that fail JSON Schema validation.
- `ProvenanceRecord` as the schema's `type` discriminator, with a documented minimal
  viable field set covering dataset identity, license, creators, origin, and custody chain.
- `creator`: array of one or more role-tagged parties (`schema:Organization` /
  `schema:Person`), with an optional `role` (`originator`, `curator`, `distributor`) to
  distinguish who produced the underlying data from who curated or redistributed it.
- `custodyChain`: ordered array of custody events (`agent`, `action`, `startTime`),
  so a multi-hop dataset's provenance can be represented without dropping earlier hops.
- License nuance fields: `licenseScope`, `licenseNote`, `licenseCategory` (enum), and
  `licenseHistory`, covering jurisdiction-scoped licenses, IRI-misleading edge cases,
  at-a-glance license categorization, and historical license changes.
- Two interim license IRI conventions, documented in `spec/0.0.1/index.md`: the CC
  Public Domain Mark for copyright-expiration/public-domain claims, and a
  Sourcelume-native `agreement-supplied` IRI for bilaterally-agreed data that cannot
  be redistributed publicly. Both are flagged as placeholders pending dev-list input,
  not settled conventions.
- `mappings/` crosswalks to Croissant, the SPDX AI Profile, and OTDI.
- SHACL shapes (`schema/0.0.1/sourcelume.shacl.ttl`) covering all fields above.
- Add maven resources plugin for API jar construction. 
- Initial content for context, schema, and specification. Initial tooling for validation.
- Initial project scaffold: repository structure, development setup, pom.mxl, pyproject.toml, 
  (`SETUP.md`), and versioning policy (`VERSIONING.md`).

 
### Changed

- JSON-LD context now grounds terms in established external vocabularies (`dct:`,
  `schema.org`, `spdx:`, `xsd:`) rather than a private namespace alone, so the spec
  interoperates with DPI/OTDI/Croissant/SPDX rather than reinventing them. Only
  genuinely Sourcelume-native terms remain under `sl:`.
- Schema `title`/`description` updated to describe the `ProvenanceRecord` shape
  specifically, replacing the earlier generic placeholder text.
- `spec/0.0.1/index.md` rewritten from a skeleton with `[fill in: ...]` markers to a
  complete field-by-field description of the current shape, including a "Non-goals
  for 0.0.1" section (no signature block, no adjudication fields, no usage/audit
  metadata) so this version's scope limits are explicit rather than implicit.

### Fixed

- `tools/validate.py` now enables JSON Schema format assertions
  (`Draft202012Validator.FORMAT_CHECKER`) and depends on `jsonschema[format]`.
  Without this, `format: uri` constraints (e.g. on `license`) are treated as
  annotation-only under JSON Schema 2020-12 and silently do not reject invalid data.

### Notes

- This update generalizes findings from stress-testing the previous skeleton
  against a real, published dataset's provenance information. Only the fixes found
  to be broadly applicable were carried forward; the usage/audit-metadata scope
  question and the two interim license conventions above remain open items for
  dev@ discussion rather than settled decisions.
