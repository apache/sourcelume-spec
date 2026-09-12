# Stress test: OLMo / Dolma (Allen Institute for AI)

## What we stress-tested

The fourth stress test of the 0.0.1 ProvenanceRecord shape, complementary to the DFM Mímir,
Pleias Common Corpus, and BLOOM/ROOTS tests:

- **DFM Mímir** stresses per-dataset licensing at small scale (12 datasets, one license each,
  one language).
- **Pleias Common Corpus** stresses per-document licensing at large scale and
  jurisdiction-scoped public-domain status.
- **BLOOM/ROOTS** stresses distributed community sourcing, agreement-supplied access at scale,
  and a use-restricted model license (RAIL).
- **OLMo / Dolma** stresses a **truly open** model release (Apache 2.0 weights + data + code +
  evaluation + checkpoints), a **risk-based dataset license that was later relaxed** (ImpACT
  medium-risk → ODC-BY), and a **code component with per-document permissive licenses tracked
  in metadata** (The Stack).

Dolma is the training corpus (3T tokens, 6 sources: Common Crawl, C4, peS2o, The Stack,
Project Gutenberg, Wikipedia/Wikibooks); OLMo is the 7B-parameter model trained on a 2T-token
sample of Dolma. Sources: Soldaini et al., "Dolma: An Open Corpus of Three Trillion Tokens for
Language Model Pretraining Research", arXiv 2402.00159 (datasheet). Groeneveld et al., "OLMo:
Accelerating the Science of Language Models", arXiv 2402.00838. AI2 license-change blog post:
"Making a switch — Dolma moves to ODC-BY" (allenai.org/blog).

Five records authored, covering four distinct Dolma source categories plus the OLMo base
model:

- `olmo-dolma-common-crawl.jsonld` — Common Crawl subset (24 shards, 2020-05 to 2023-06)
- `olmo-dolma-the-stack-code.jsonld` — The Stack (permissively-licensed GitHub code)
- `olmo-dolma-pes2o-academic.jsonld` — peS2o v2 (academic papers, derived from S2ORC, ODC-By)
- `olmo-dolma-project-gutenberg-books.jsonld` — Project Gutenberg (public-domain books)
- `olmo-7b-model.jsonld` — the OLMo-7B model itself (Apache 2.0, truly open)

## What worked

- The `licenseScope` field (folded into 0.0.1 after the Common Corpus stress test) generalized
  cleanly to the Gutenberg record — the same copyright-expiration jurisdiction clause pattern
  as the Pleias Gutenberg record, now applied to a second corpus. This confirms the field is
  correctly shaped and not Common-Corpus-specific.
- The `agreement-supplied` interim license IRI was reused for The Stack (whose per-document
  permissive licenses are tracked in The Stack's metadata but whose dataset-level license is
  ODC-By covering the curation, not the underlying code). The same convention Mímir established
  for `dbc` now covers four distinct cases (Mímir dbc, BLOOM S2ORC, BLOOM pseudo-crawled
  websites, OLMo The Stack).
- The `custodyChain[]` array captured the multi-hop Dolma pipeline (Common Crawl → cc_net →
  AI2 filters → ImpACT release → ODC-By relicensing) as a readable ordered chain, including the
  license-change event as a custody hop with its own `action`.
- The OLMo base-model record carries a clean Apache 2.0 license IRI — the canonical Apache 2.0
  URL — which is classifiable at a glance. This is the cleanest licensing model we've modeled
  and a useful baseline for the `licenseCategory` proposal (Gap G): it would classify as
  `open-source` vs. BLOOM's `use-restricted`.

## What the schema could not represent

One new gap surfaced; existing gaps A, B, and G were re-surfaced and strengthened.

**Status of 0.0.1.** As of this stress test, the 0.0.1 schema on `main` is only a minimal
skeleton; the concrete `ProvenanceRecord` shape lives on the `minimal-mimir` and
`common-corpus-stress-test` branches. Because 0.0.1 has neither been released nor landed as a
concrete schema on `main`, it is still fluid: gaps can be folded in without breaking a released
or main-resident form. The distinction that matters is **additive vs. breaking** (see the Common
Corpus notes for the full framing). The new gap here is additive (an optional field), so it is
a candidate for 0.0.1 if the list takes it up.

### Gap H — A dataset whose license changed over time has no way to record both licenses with their dates  *(additive — candidate for 0.0.1)*

Dolma was initially released (August 2023) under the **AI2 ImpACT license as a medium-risk
artifact** — a risk-based license with use restrictions and derivative-impact-report
requirements. Later, AI2 **switched Dolma's license to ODC-BY** (a more permissive Open Data
Commons attribution license) based on community feedback that the ImpACT license was too
restrictive for the creative uses researchers were making of Dolma. AI2's license-change blog
post states the ODC-BY license applies retroactively to copies downloaded under the ImpACT
license; there is no requirement to redownload.

The `olmo-dolma-common-crawl.jsonld` (and the other three Dolma source records) carries
`license: https://commoncrawl.org/terms-of-use/` (the source's terms) and documents the ImpACT
→ ODC-By switch in the `origin` prose, with the two release events as separate custodyChain
hops. But the 0.0.1 schema has no structured way to record that a dataset's *own dataset-level
license* changed over time: which license applied during which period, and which is current.
The `license` field is a single IRI; the `custodyChain` can record the events as hops but has
no license-IRI field per hop; the `origin` prose is free text an auditor must read.

**How this model surfaced it.** OLMo/Dolma is the first corpus we've modeled whose license was
publicly changed after release. Mímir, Common Corpus, and BLOOM/ROOTS all have stable licenses
(no post-release change documented). Dolma's ImpACT → ODC-By switch is well-documented by AI2
and material to downstream users: a derivative created under the ImpACT license has different
flow-down restrictions than one created under ODC-By.

**Why this justifies a change.** For a provenance system, the license-that-applied-when-a-
derivative-was-created is a checkable claim that matters (different flow-down obligations). An
optional, additive `licenseHistory` (or `licenseChanges`) field — an array of
`{ iri, effectiveDate, supersededBy }` entries — would let a record record both the original
ImpACT license and the current ODC-By license with their dates, so a downstream consumer can
determine which license applied when. This is additive and non-breaking: records with a stable
license (the common case) omit the field and keep validating; records with a license change
(like Dolma) can now make the change checkable rather than burying it in prose. The single
`license` field remains the *current* license; `licenseHistory` records the prior ones.

**Proposed direction:** an optional `licenseHistory` array of `{ iri, effectiveDate }` entries
(earliest first) recording prior licenses the dataset was distributed under, with the current
license still in the `license` field. Additive, non-breaking, candidate for 0.0.1.

### Re-surfaced and strengthened: Gaps A, B, G

- **Gap A (jurisdiction-scoped public-domain status)** is re-surfaced by the Gutenberg record,
  which carries the `licenseScope` field with the same copyright-expiration jurisdiction clause
  as the Pleias Gutenberg record. This confirms `licenseScope` generalizes across corpora and
  is correctly optional (the other four OLMo records omit it cleanly).
- **Gap B (per-document multi-license aggregate)** is re-surfaced and strengthened by three
  records: Common Crawl (web pages, heterogeneous licenses), The Stack (permissively-licensed
  code with per-document licenses tracked in The Stack's metadata — the clearest case yet,
  because the per-document licenses are *known and recorded* in the source's metadata but
  cannot be lifted to the dataset-level record), and peS2o (papers from many publishers under
  many licenses). OLMo/Dolma confirms Gap B is universal across all four stress-tested corpora.
- **Gap G (license IRI cannot express use-restricted license category)** is sharpened by the
  OLMo-vs-BLOOM contrast: OLMo is Apache 2.0 (open-source, no use restrictions), BLOOM is RAIL
  (use-restricted). Both are "open" model releases but with materially different licensing
  models. The proposed `licenseCategory` field would classify OLMo as `open-source` and BLOOM
  as `use-restricted`, making the distinction checkable at a glance. Additionally, Dolma's
  initial ImpACT license was a *risk-based* license (medium-risk artifact with derivative-impact
  reports) — a third category distinct from both open-source and RAIL — further motivating the
  controlled vocabulary.

## Summary table

| Gap | Title | First surfaced by | OLMo evidence | Resolution status |
|---|---|---|---|---|
| A | Jurisdiction-scoped public-domain status | Common Corpus | Re-surfaced by Gutenberg record (licenseScope generalizes) | **Folded into 0.0.1** (`licenseScope`) |
| B | Per-document multi-license aggregate | Common Corpus | Re-surfaced by Common Crawl, The Stack (clearest case), peS2o | Open (breaking); prototypes built |
| C | Large distributed creator/source population | Common Corpus | Not applicable (Dolma sources are institutional, not distributed) | Open (additive); prototype built |
| D | Transformative LLM custody-hop action vocabulary | Common Corpus | Not applicable (Dolma curation is rule-based, not LLM-based) | Open (vocabulary) |
| E | Training-phase (pretrain/SFT/RAG) not distinguishable | Mímir / Common Corpus | Not applicable (OLMo is pretrain-only; adaptation via Tülu is separate) | Open (scope) |
| F | `license` reflects processing artifact not intended selection | BLOOM (GitHub code) | Not applicable (no documented processing artifact in Dolma) | Open (additive — candidate for 0.0.1) |
| G | `license` IRI cannot express use-restricted license category | BLOOM (RAIL License) | Sharpened by OLMo (Apache 2.0) vs. BLOOM (RAIL) vs. Dolma ImpACT (risk-based) contrast | Open (additive — candidate for 0.0.1) |
| H | License changed over time has no structured record | OLMo/Dolma (ImpACT → ODC-By) | New | Open (additive — candidate for 0.0.1) |

Gap H is additive and a candidate for 0.0.1 (0.0.1 is not yet on `main` as a concrete schema).
Gaps F, G, and H are now a coherent cluster of additive license-field refinements
(licenseNote + licenseCategory + licenseHistory) that together would make the `license` field
much more faithfully checkable without breaking the single-IRI structure. None breaks existing
records. 0.0.1 is not yet on `main` as a concrete schema, so additive changes can still be
folded in without breaking a released form when the open questions settle.

## Inputs used

- Soldaini et al., "Dolma: An Open Corpus of Three Trillion Tokens for Language Model
  Pretraining Research", arXiv 2402.00159 — Dolma datasheet (source taxonomy Table 1, per-source
  licensing, ImpACT license as medium-risk artifact, representativeness discussion).
  https://arxiv.org/abs/2402.00159
- Groeneveld et al., "OLMo: Accelerating the Science of Language Models", arXiv 2402.00838 —
  OLMo framework, Apache 2.0 release, Dolma as pretraining data, evaluation (Catwalk, Paloma).
  https://arxiv.org/abs/2402.00838
- AI2 blog, "Making a switch — Dolma moves to ODC-BY" — documents the ImpACT → ODC-By license
  change and its retroactive application. https://allenai.org/blog/making-a-switch-dolma-moves-to-odc-by-8f0e73852f44
- Dolma dataset on HuggingFace — https://huggingface.co/datasets/allenai/dolma (current
  license: ODC-BY per the dataset card).
- OLMo-7B model on HuggingFace — https://huggingface.co/allenai/OLMo-7B (Apache 2.0).
- The Stack dataset on HuggingFace — https://huggingface.co/datasets/bigcode/the-stack
  (permissively-licensed code, per-document license metadata).
- peS2o dataset on HuggingFace — https://huggingface.co/datasets/allenai/peS2o (ODC-By,
  derived from S2ORC).
- Dolma toolkit and documentation — https://github.com/allenai/dolma
- OLMo model and training code — https://github.com/allenai/OLMo
