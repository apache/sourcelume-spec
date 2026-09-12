# Stress test: Pleias Common Corpus vs. Sourcelume 0.0.1 schema

Companion to `notes/stress-test-dfm-mimir.md`; same methodology (take a well-documented
open model with granular training-data provenance, map a few representative sub-datasets to
`ProvenanceRecord`, record what the schema cannot represent).

## What we stress-tested

[Common Corpus](https://huggingface.co/datasets/PleIAs/common_corpus) is a 2.27-trillion-token
text dataset created by Pleias and partners. It is the training corpus of
[PleIAs/Pleias-1.2b-Preview](https://huggingface.co/PleIAs/Pleias-1.2b-Preview) (1.21B-parameter
base model) and related Pleias models. Common Corpus differs from existing open datasets in that
it contains *only* data that is either uncopyrighted or freely licensed, and records
**per-document licensing and contextual metadata** (the dataset has 635 distinct `license`
values across 69.9k+ rows in the Hugging Face viewer). It is organized into six collections:
OpenCulture, OpenGovernment, OpenScience, OpenSource, OpenWeb, OpenSemantic.

This is a deliberate **contrast case** to the DFM Mímir stress test: Mímir's provenance is
*dataset-level* (161 datasets, each with one license); Common Corpus's provenance is
*document-level* (one dataset, thousands of documents, many different licenses). The two tests
are complementary — Mímir stresses per-dataset licensing and multi-hop custody of synthetic
derivatives; Common Corpus stresses per-document licensing, jurisdiction-scoped public-domain
status, and large distributed creator populations.

We took representative sub-collections from all six Common Corpus collections, plus a
separate downstream model's SFT/RAG dataset, and attempted to express each as a Sourcelume
`ProvenanceRecord` under the current 0.0.1 schema:

1. [`examples/pleias-common-corpus-caselaw-access-project.jsonld`](../examples/pleias-common-corpus-caselaw-access-project.jsonld)
   — OpenGovernment / Legal Commons (Harvard Caselaw Access Project)
2. [`examples/pleias-common-corpus-github-opensource.jsonld`](../examples/pleias-common-corpus-github-opensource.jsonld)
   — OpenSource (GitHub, ArmoRM-filtered)
3. [`examples/pleias-common-corpus-openculture-gutenberg-wikisource.jsonld`](../examples/pleias-common-corpus-openculture-gutenberg-wikisource.jsonld)
   — OpenCulture (Project Gutenberg + Wikisource, Pleias OCR-corrected)
4. [`examples/pleias-common-corpus-youtube-commons.jsonld`](../examples/pleias-common-corpus-youtube-commons.jsonld)
   — OpenWeb (YouTube-Commons, CC-BY transcripts)
5. [`examples/pleias-common-corpus-openscience-openalex.jsonld`](../examples/pleias-common-corpus-openscience-openalex.jsonld)
   — OpenScience (OpenAlex, CC0)
6. [`examples/pleias-common-corpus-opensemantic-wikidata.jsonld`](../examples/pleias-common-corpus-opensemantic-wikidata.jsonld)
   — OpenSemantic (Wikidata, CC0, triplet-to-natural-language transcription)
7. [`examples/pleias-rag-1b-synth-sft.jsonld`](../examples/pleias-rag-1b-synth-sft.jsonld)
   — Downstream: PleIAs/SYNTH, the synthetic SFT/RAG dataset for Pleias-RAG-1B (a different
     training phase than the Common-Corpus-pretrained base model)

Two additional records are forward-looking **prototypes** that intentionally do NOT validate
against the current 0.0.1 schema, because they demonstrate proposed solutions to Gaps B and C:

- [`examples/prototypes/pleias-common-corpus-github-opensource-with-license-distribution.jsonld`](../examples/prototypes/pleias-common-corpus-github-opensource-with-license-distribution.jsonld)
  — Gap B prototype: `license` as an array of `{ iri, count, proportion }` entries
- [`examples/prototypes/pleias-common-corpus-youtube-commons-with-manifest.jsonld`](../examples/prototypes/pleias-common-corpus-youtube-commons-with-manifest.jsonld)
  — Gap C prototype: a `creator` entry with a `manifest` field pointing at a separate roster
  ([`examples/prototypes/pleias-common-corpus-youtube-commons-creator-manifest.jsonld`](../examples/prototypes/pleias-common-corpus-youtube-commons-creator-manifest.jsonld))

## What worked

All seven conforming records are structurally valid under 0.0.1 (JSON Schema + SHACL, verified
with `jsonschema` 4.26.0 + `pyshacl` 0.40.1). The role-tagged `creator[]` array and ordered
`custodyChain[]` array — both folded into 0.0.1 after the Mímir stress test — carry over cleanly
to Common Corpus: each sub-collection has distinguishable originator/curator/distributor roles
and a multi-hop custody chain. No schema change was needed for these four records to be produced.

## What the schema could not represent

Five concrete gaps surfaced. Gaps A and B generalize Mímir's Gap 1 (license vocabulary); Gap E
generalizes Mímir's Gap 4 (usage/audit scope); Gap C is new; Gap D is a vocabulary/precision gap,
not a structural one.

**Status of 0.0.1.** As of this stress test, the 0.0.1 schema on `main` is only a minimal
skeleton — the concrete `ProvenanceRecord` shape (required fields, `creator[]` array with role
enum, `custodyChain[]` ordered array) lives on the `minimal-mimir` and `common-corpus-stress-test`
branches, not yet on `main`. Because 0.0.1 has neither been released nor landed as a concrete
schema on `main`, it is still fluid: gaps can be folded in without breaking a released or
main-resident form. The distinction that matters is **additive vs. breaking**: non-breaking
additions (an optional `licenseScope` field, an optional `manifest` field) can be folded into
0.0.1 directly; changes that would alter a required field's shape (making `license` an array) or
add required usage/audit metadata are larger and should wait for the license-vocabulary and
usage-scope discussions that are still open. Each gap below is labeled with which kind it is.

### Gap A — Jurisdiction-scoped public-domain status has no single IRI  *(folded into 0.0.1)*

Two of the four records (Caselaw Access Project, OpenCulture/Gutenberg-Wikisource) carry
`"license": "https://creativecommons.org/publicdomain/mark/1.0/"` — the CC Public Domain Mark.
But the underlying public-domain status is **jurisdiction-scoped**, not global:

- US federal and state judicial opinions are public domain because *no copyright subsists in
  judicial work product* under US law. A French court decision, by contrast, is public domain
  under a different French-law doctrine; Chinese case law under yet another.
- A Project Gutenberg book that is public domain by copyright expiration in the US may still be
  in copyright in another country whose copyright term is longer.

A single `license` IRI cannot say "public domain, *specifically under US judicial-work-product
doctrine*" or "public domain *in jurisdictions with a life+70 term where the author died before
1954*." The CC Public Domain Mark is itself a *claim* ("the work is in the public domain
worldwide"), which is exactly the over-broad claim the data doesn't support. This generalizes
Mímir's Gap 1: the interim convention documented in `spec/0.0.1/index.md` works as a placeholder
but cannot express *why* a work is public domain or *where*.

**How this model surfaced it.** Common Corpus makes the jurisdiction question concrete because it
explicitly aggregates *public-domain-by-different-doctrines* sources into one corpus: US case law
(PD by US judicial-work-product doctrine), Chinese case law (PD by PRC judicial doctrine), French
court decisions (PD under French law), and Gutenberg books (PD by copyright expiration, with the
expiration date depending on the jurisdiction's term). The Caselaw and Gutenberg records both
end up with the *same* `license` IRI (the CC PD Mark) despite deriving their public-domain status
from *different legal bases in different jurisdictions*. Mímir never surfaced this because its
datasets were a single-jurisdiction corpus (Danish), so every PD-ish claim sat under one doctrine.

**Why this justifies a change.** Sourcelume's purpose is to make license/provenance claims
*checkable by someone else*. A `license` IRI that silently overclaims (worldwide PD when the
basis is jurisdiction-scoped) is not a checkable claim — an auditor cannot verify "worldwide PD"
against a US-judicial-doctrine source, because the claim is false outside the US. An optional,
additive `licenseScope` (jurisdiction) and/or `licenseBasis` (the legal doctrine or expiration
rule) field would let a record say "public domain, *under US judicial-work-product doctrine,
US jurisdiction*" — a claim an auditor *can* verify — without changing the existing `license` IRI
for any record that doesn't need the qualification. This is additive and non-breaking: records
that omit the new field keep validating, and records that need it (like Caselaw, Gutenberg) can
now make a faithful claim instead of an over-broad one.

**Resolution (folded into 0.0.1):** added the optional, non-breaking `licenseScope` field —
schema, SHACL, context, spec prose, and the two affected records (Caselaw carries
`"licenseScope": "US"`; Gutenberg carries a copyright-expiration jurisdiction clause). A record
can now qualify *where* and *on what legal basis* a license (public-domain or otherwise) applies,
without changing the existing `license` IRI. The richer license-object shape (`{ iri, scope,
basis }` instead of a bare IRI + side fields) remains the cleaner long-term design but is a
breaking change for the `license` field itself; deferred in favor of the additive side-field
approach for 0.0.1. This field was added rather than only documented because 0.0.1 is not yet
on `main` as a concrete schema and the change is additive (no existing record breaks).

### Gap B — A single `license` IRI cannot represent a per-document multi-license aggregate  *(breaking — defer)*

The OpenSource collection is scraped from GitHub repositories carrying *different* permissive
licenses (MIT, Apache-2.0, BSD, ISC, CC0, … — 635 distinct license values appear across Common
Corpus overall). `ProvenanceRecord.license` is a single IRI. The record
(`pleias-common-corpus-github-opensource.jsonld`) carries a representative SPDX IRI (MIT) plus a
prose note in `origin` explaining the collection is not uniformly MIT — but this is a workaround,
not a faithful representation. The same problem recurs at smaller scale for OpenWeb (CC-BY but
with different CC-BY versions across sources) and would recur for any aggregate dataset whose
documents carry heterogeneous licenses.

This is the strongest new gap this stress test surfaces and is specific to document-level-licensed
corpora like Common Corpus. A dataset-level license field is simply the wrong granularity for
this class of dataset.

**Proposed direction:** either (a) allow `license` to be an array of `{ iri,
proportion }` or `{ iri, count }` entries for aggregate datasets, (b) add a companion
`licenseDistribution` field, or (c) require each document to be its own `ProvenanceRecord`
(infeasible at 69.9k+ documents for one collection). Not yet resolved — and it interacts with
Gap A (each entry in the distribution may itself be jurisdiction-scoped).

### Gap C — A large distributed creator population cannot be enumerated in `creator[]`  *(additive — candidate for 0.0.1)*

YouTube-Commons has **721,136 individual channels** as originators. `creator[]` requires
`min 1` entries but has no way to point at a *manifest* or *roster* of creators rather than
enumerating each. The record (`pleias-common-corpus-youtube-commons.jsonld`) uses a single
`originator` entry that summarizes the population ("Individual YouTube video creators
(721,136 distinct channels)…"), but this is not a complete attribution — and CC-BY's
attribution requirement is satisfied by per-channel credit in the dataset metadata, not by
this summary. The Mímir records had the same problem at much smaller scale (a handful of named
creators per dataset) and could enumerate them; Common Corpus makes the problem concrete at
~721k scale.

**Proposed direction:** allow a `creator` entry of shape
`{ type, name, role, manifest: <IRI to a creator roster> }` for distributed-creator cases, so
the record points at a separate, checkable manifest rather than compressing 721k creators into
one prose name. Not yet resolved.

### Gap D — Transformative LLM-based custody hops have no action vocabulary  *(vocabulary — defer)*

Three of the four records include custody hops performed by an LLM-based pipeline: OCR
correction (PleIAs/OCRonos), toxicity filtering (PleIAs/celadon), and quality scoring
(ArmoRM). `custodyChain[].action` is a free string, so these can be recorded as prose
(`machine-ocr-corrected-digitized-texts`, `quality-scored-and-filtered-to-top-80-percent`), but
there is no shared vocabulary — two record authors describing the same ArmoRM step would write
different action strings, and a downstream consumer cannot filter on "all records whose custody
chain includes an LLM-judge step."

This is a vocabulary/precision gap, not a structural one (the chain structure works). Mímir's
custody hops already included an LLM judge (`gemma-4-31B-it` judging generated rows), so this gap
was latently present in the Mímir test too; Common Corpus just makes it starker because 3 of 4
records rely on LLM-based transformative hops.

**Proposed direction:** a small controlled vocabulary for `custodyChain[].action`
(covering at least: `digitized`, `ocr-corrected`, `quality-filtered`, `toxicity-filtered`,
`pii-scrubbed`, `synthesized`, `judge-accepted`, `translated`, `aggregated`, `redistributed`),
optionally with a `transformedBy` model IRI on the hop. Not yet resolved.

### Gap E — Training-phase (pretrain / SFT / RAG) is not distinguishable in a record  *(scope — defer)*

The `pleias-rag-1b-synth-sft.jsonld` record describes PleIAs/SYNTH, the synthetic SFT/RAG dataset
used to train Pleias-RAG-1B. This is a **different training phase** than the Common-Corpus
pretraining of Pleias-1.2b-Preview: SYNTH is itself *derived from* Common Corpus sources (it
emulates RAG retrieval over them, with Qwen-3-8B generating synthetic rows). ProvenanceRecord
has no field to record *which training phase* a dataset was used in (pretrain vs. SFT vs.
RAG-grounding vs. evaluation). This generalizes Mímir Gap 4 (usage/audit scope): the question of
how a specific model consumed a dataset is currently out of scope for a dataset-centric record,
but the stress test shows the boundary is reached as soon as one models a downstream model's
fine-tuning data rather than just its pretraining corpus.

**Proposed direction:** keep `ProvenanceRecord` dataset-centric (per the 0.0.1 non-goals) and
introduce a *separate* model-usage/audit record type that links a model to the datasets it
consumed in each phase. Not yet resolved.

## Prototypes (forward-looking, do not validate against 0.0.1)

Two records intentionally break the current schema to demonstrate proposed solutions:

- **Gap B prototype** (`pleias-common-corpus-github-opensource-with-license-distribution.jsonld`):
  `license` is an array of `{ iri, count, proportion, note }` entries, one per SPDX license present
  in the OpenSource collection. This faithfully represents the multi-license aggregate. The
  `count`/`proportion` values are placeholders (0.0) because exact per-license counts are not
  published per-collection in Common Corpus metadata; a real entry would carry true counts.
- **Gap C prototype** (`pleias-common-corpus-youtube-commons-with-manifest.jsonld` +
  `pleias-common-corpus-youtube-commons-creator-manifest.jsonld`): a `creator` entry carries a
  `manifest` field pointing at a separate `CreatorManifest` document that lists/excerpts the
  721,136 individual YouTube channels. This lets the record point at a checkable roster rather
  than compressing 721k creators into one prose name. The manifest document uses a prototype
  `CreatorManifest` type (not in 0.0.1).

Both prototypes are marked `[PROTOTYPE]` in their `name` and explained in their `origin`; they
are excluded from the validating-record set but kept in `examples/` to make the proposed
directions concrete and reviewable.

## Summary table

| Gap | Title | Mímir precedent | Resolution status |
|---|---|---|---|
| A | Jurisdiction-scoped public-domain status | Generalizes Mímir Gap 1 (license vocabulary) | **Folded into 0.0.1** (optional `licenseScope` field) |
| B | Per-document multi-license aggregate | New (Common Corpus-specific granularity) | Open; prototype built |
| C | Large distributed creator population | Latent in Mímir (small scale) | Open; prototype built |
| D | Transformative LLM custody-hop action vocabulary | Latent in Mímir (gemma-4-31B-it judge) | Open |
| E | Training-phase (pretrain/SFT/RAG) not distinguishable | Generalizes Mímir Gap 4 (usage/audit scope) | Open |

Gap A has been folded into 0.0.1 as the optional, non-breaking `licenseScope` field
(schema, SHACL, context, spec prose, and the two affected records). Gaps B–E remain open: B and
E are breaking changes (they alter a required field's shape or add usage/audit metadata) and
wait for the license-vocabulary and usage-scope discussions that are still open; C is additive
but introduces a new `CreatorManifest` document type and is deferred; D is a vocabulary
question (free string vs. controlled enum) and is deferred. 0.0.1 is not yet on `main` as a
concrete schema, so these can still be folded in without breaking a released form when the
open questions settle.

## Inputs used

- `examples/pleias-common-corpus-caselaw-access-project.jsonld`
- `examples/pleias-common-corpus-github-opensource.jsonld`
- `examples/pleias-common-corpus-openculture-gutenberg-wikisource.jsonld`
- `examples/pleias-common-corpus-youtube-commons.jsonld`
- `examples/pleias-common-corpus-openscience-openalex.jsonld`
- `examples/pleias-common-corpus-opensemantic-wikidata.jsonld`
- `examples/pleias-rag-1b-synth-sft.jsonld`
- `examples/prototypes/pleias-common-corpus-github-opensource-with-license-distribution.jsonld` (Gap B prototype)
- `examples/prototypes/pleias-common-corpus-youtube-commons-with-manifest.jsonld` (Gap C prototype)
- `examples/prototypes/pleias-common-corpus-youtube-commons-creator-manifest.jsonld` (Gap C prototype manifest)
- Pleias Common Corpus dataset card, https://huggingface.co/datasets/PleIAs/common_corpus
- PleIAs/Pleias-1.2b-Preview model card, https://huggingface.co/PleIAs/Pleias-1.2b-Preview
- Common Corpus technical report, arXiv 2506.01732 (ICLR 2026 oral)
- Harvard LIL blog: "Transitions for the Caselaw Access Project",
  https://lil.law.harvard.edu/blog/2024/03/26/transitions-for-the-caselaw-access-project/
- Caselaw Access Project, https://case.law/
- BigCode — The Stack, https://www.bigcode-project.org/docs/about/the-stack/
- PleIAs/YouTube-Commons dataset card, https://huggingface.co/datasets/PleIAs/YouTube-Commons
- PleIAs/OCRonos model card, https://huggingface.co/PleIAs/OCRonos
- PleIAs/Post-OCR-Correction dataset card, https://huggingface.co/datasets/PleIAs/Post-OCR-Correction
- Project Gutenberg, https://www.gutenberg.org/ ; Wikisource, https://www.wikisource.org/
- OpenAlex license documentation, https://github.com/ourresearch/openalex-docs/blob/main/license.md
- Wikidata licensing, https://www.wikidata.org/wiki/Wikidata:Licensing
- PleIAs/Pleias-RAG-1B model card, https://huggingface.co/PleIAs/Pleias-RAG-1B
- PleIAs/SYNTH dataset, https://huggingface.co/datasets/PleIAs/SYNTH
