# Stress test: DFM Mímir v1 training data vs. Sourcelume 0.0.1 schema

Findings from a stress test of the DFM Mímir v1 training data against the
Sourcelume 0.0.1 schema. Gaps 1–3 below were folded directly into `0.0.1` (which had not yet been
released, so nothing needed a version bump) rather than deferred — see the resolution notes on
each. Gap 4 remains an open scope question.

## What we stress-tested

[DFM Mímir v1](https://huggingface.co/danish-foundation-models/DFM-Mimir) is a 1B-parameter
Danish/English Hierarchical Reasoning Model (HRM-Text) trained from scratch on **161 datasets**
that the project states are "permissible and openly licensed, made available by agreement, or
allowed by the EU text-and-data-mining exception for research institutions" (Mímir v1 technical
report, arXiv 2608.13517). Mímir is an unusually good fit for Sourcelume's purpose: its entire
value proposition is *verifiable, ethically-sourced training data*, yet today all of that
provenance and licensing information lives as human-readable prose — in the arXiv report's
Appendix A (Table 10, the full 161-dataset manifest), the Hugging Face model card, and per-dataset
datasheets. None of it is machine-checkable.

We took a real source dataset from Mímir's training corpus —
[`schneiderkamplab/danish-dynaword-denoising`](https://huggingface.co/datasets/schneiderkamplab/danish-dynaword-denoising)
(323M sampled tokens/epoch, 0.46% of the corpus) — and attempted to express it as a Sourcelume
`ProvenanceRecord` under the current 0.0.1 schema. This dataset is one of four synthetic
derivatives that the Mímir project derives from the
[`danish-foundation-models/danish-dynaword`](https://huggingface.co/datasets/danish-foundation-models/danish-dynaword)
raw text corpus (the others being `-span-filling`, `-prefix-continuation`, and
`-paragraph-reordering`); Mímir trains on the derivatives, not on raw dynaword directly.

## What worked

A structurally valid 0.0.1 record can be produced
([`examples/dfm-mimir-danish-dynaword-denoising.jsonld`](../examples/dfm-mimir-danish-dynaword-denoising.jsonld)).
It passes both JSON Schema and SHACL validation, and, after the fixes below, records the
identifiable custody hops (dynaword source-corpus provision, Gemma-4 judging of generated rows,
schneiderkamplab publication of accepted rows) and role-tagged creators (DFM/dynaword as
`originator`, Peter Schneider-Kamp as `curator`, schneiderkamplab as `distributor`).

## What the schema could not represent

Four concrete gaps surfaced against this one real dataset. Each would have been hypothetical if
we had only inspected the 0.0.1 field list; mapping a real datasheet made them immediate.

1. **"Agreement-supplied" has no clean license IRI.** Two of the 161 Mímir datasets — "DBC
   (agreement-supplied)" and "Lex.dk articles" — are provided to the Danish Foundation Models
   project under agreements whose licensing does not permit public sharing. SPDX has no term
   for *agreement-bound, non-redistributable data*. Our best-effort records use an interim
   Sourcelume convention IRI (`https://sourcelume.apache.org/ns#agreement-supplied`) as a
   placeholder, which is pragmatic but not a precise license term.
   **Resolved for 0.0.1:** documented this as the interim convention in `spec/0.0.1/index.md`'s
   `license` field description, pending a more precise term if/when the list takes it up — not a
   schema change, since inventing a `sourcelume:`-native license term without list consensus would
   be exactly the kind of thing to raise there first.

2. **Single `custodyEvent` collapses a multi-hop chain.** This dataset actually has at least three
   custodians: the original text sources aggregated by dynaword (e.g. ADL, ai-aktindsigt, botxt,
   cellar — each a separate corpus), the DFM dynaword corpus (which aggregated them), and
   schneiderkamplab (which generated the synthetic denoising task and judged rows with
   Gemma-4-31B-it before publishing accepted rows). The single-`custodyEvent` shape could record
   only the most recent hop and silently dropped the earlier ones.
   **Resolved for 0.0.1:** `custodyEvent` (object) replaced with `custodyChain` (array, min 1).
   The updated example now records the dynaword-provision and schneiderkamplab-publication hops;
   the underlying original authors/rightsholders (per dynaword sub-source) still can't be recorded
   as a hop within *this* derivative's record since they have no single identifiable agent or
   timestamp at this scale — a data-availability limit, not a schema one. Those sub-sources, if
   needed, would each warrant their own `ProvenanceRecord` linked from this one's `custodyChain`.

3. **`creator` conflates originator and curator.** `creator` was a single object. For
   `danish-dynaword-denoising` there are at least three distinct roles: DFM/dynaword (the original
   corpus originator), Peter Schneider-Kamp/schneiderkamplab (the curator who derived and
   audited the synthetic task), and schneiderkamplab (the distributor on Hugging Face). The
   single-object shape could not distinguish these roles.
   **Resolved for 0.0.1:** `creator` is now an array (min 1) of parties, each with an optional
   `role` (`originator`/`curator`/`distributor`). The updated example tags DFM/dynaword as
   `originator`, Peter Schneider-Kamp as `curator`, and schneiderkamplab as `distributor`. Full
   alignment with a richer provenance vocabulary (PROV) was considered and deferred — the
   three-value enum covers this dataset's needs without committing to PROV's larger model.

4. **No place for downstream usage or audit metadata.** Mímir's technical report documents a
   formal memorisation audit across four data risk categories (agreement-backed synthetic,
   opt-out-uncertain, high-confidence-no-opt-out, low-risk synthetic/reasoning). This is exactly
   the kind of claim Sourcelume should make checkable, but it belongs to the *model producer's*
   view of the dataset, not the *dataset producer's* record. The 0.0.1 schema has no field for
   it. This raises a scope question: should `ProvenanceRecord` stay dataset-centric
   (and let model usage/audits live in a separate, later type), or should it grow a `usage: [...]`
   block recording how specific models consumed and audited the dataset?

## Bug found in our own validator

While building the stress-test records, we discovered that the JSON Schema validator
(NetworkNT `json-schema-validator`, used in an earlier Java-based validator) was **not enforcing
`format: uri`** on the `license` field by default — JSON Schema 2020-12 treats `format` as
annotation-only unless assertion mode is explicitly enabled. A record with
`"license": "Agreement-supplied"` (a plain string, not a URI) silently passed validation. Fix
applied at the time in `ValidateExamplesTest.java`:
`SchemaValidatorsConfig.builder().formatAssertionsEnabled(true)`. With the fix, the invalid
record correctly failed with `/license: does not match the uri pattern`.

Validation tooling has since moved to Python (`tools/validate.py`, see `SETUP.md`), which has
the analogous gap: the `jsonschema` library also treats `format` as non-enforcing unless a
format checker is supplied. `tools/validate.py` passes
`format_checker=Draft202012Validator.FORMAT_CHECKER` and `pyproject.toml` depends on
`jsonschema[format]` (which pulls in `rfc3987`) specifically to keep this check active — verified
by re-running the same broken-license case against the Python validator.

A separate, deeper issue remains: even with format assertions on, JSON-LD's `@type: @id`
coercion resolves *any* non-absolute string as a relative IRI against the document base, so a
plain string like `"Agreement-supplied"` still becomes *some* absolute IRI at the RDF level.
SHACL's `sh:nodeKind sh:IRI` therefore cannot catch "the author typed words instead of a URI."
Real license validation likely needs an enum/pattern against a known vocabulary (e.g. the SPDX
license list), not just a URI-shape check.

## Open questions

- **Usage/audit scope decision** — decide whether `ProvenanceRecord` stays dataset-centric or
  grows a `usage` block; if the former (current default in `spec/0.0.1/index.md`'s non-goals),
  schedule a separate model-audit record type for a later version.
- **License vocabulary beyond the interim convention** — the agreement-supplied and
  public-domain conventions above are stopgaps; consider a proper enum/pattern against a known
  license list (e.g. SPDX) so `format: uri` isn't the only check, per the deeper JSON-LD coercion
  issue noted below.

## Inputs used

- `examples/dfm-mimir-danish-dynaword-denoising.jsonld` — the conformant best-effort record.
- Mímir v1 technical report, arXiv 2608.13517 (Appendix A, Table 10 — the 161-dataset manifest).
- `schneiderkamplab/danish-dynaword-denoising` README on Hugging Face (license, row counts,
  source files, judge model).
- DFM-Mimir Hugging Face model card.
