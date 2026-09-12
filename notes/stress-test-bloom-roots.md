# Stress test: BLOOM / ROOTS (BigScience workshop)

## What we stress-tested

The third stress test of the 0.0.1 ProvenanceRecord shape, complementary to the DFM Mímir
and Pleias Common Corpus tests:

- **DFM Mímir** stresses per-dataset licensing at small scale (12 datasets, one license each,
  one language).
- **Pleias Common Corpus** stresses per-document licensing at large scale (one dataset, 635
  distinct license values, ~6 collections) and jurisdiction-scoped public-domain status.
- **BLOOM / ROOTS** stresses **distributed community sourcing** (498 datasets, 59 languages,
  1000+ participants across 50+ institutions), **agreement-supplied access** at scale (gated
  release subject to the BigScience ethical charter; data-host-provider-agreements for partner
  data), and a **model license with use-based restrictions** (BigScience RAIL License v1.0).

ROOTS is the training corpus (1.6TB, 59 languages, 498 datasets); BLOOM is the 176B-parameter
model trained on it. Source: Laurençon et al., "The BigScience ROOTS Corpus", NeurIPS 2022
Datasets and Benchmarks Track (arXiv 2303.03915). The BLOOM model license is the BigScience RAIL
License v1.0 (https://huggingface.co/spaces/bigscience/license).

Five records authored, one per distinct ROOTS source category plus the BLOOM model:

- `bloom-roots-oscar-web-crawl.jsonld` — OSCAR v21.09 (38% of ROOTS, web-crawl component)
- `bloom-roots-github-code-gpl-only.jsonld` — GitHub code (BigQuery, GPL-family only)
- `bloom-roots-s2orc-academic-papers.jsonld` — S2ORC (Semantic Scholar academic papers)
- `bloom-roots-pseudo-crawled-websites.jsonld` — 539 community-identified domains
- `bloom-176b-model.jsonld` — the BLOOM 176B model itself (RAIL License v1.0)

## What worked

- The `creator[]` array with roles handled the multi-party BigScience structure cleanly:
  BigScience workshop + Hugging Face + Allen Institute for AI + Google BigQuery + Common Crawl
  Foundation + partner communities (Masakhane, Machine Learning Tokyo, LatinX in AI) all fit
  into originator / curator / distributor roles without strain.
- The `agreement-supplied` interim license IRI (documented in `spec/0.0.1/index.md`) was
  reused directly for S2ORC and pseudo-crawled websites — the same convention Mímir established
  for `dbc`, now validated at much larger scale (539 domains + a major academic corpus).
- The `licenseScope` field (added after the Common Corpus stress test) was not needed here
  because BLOOM/ROOTS sources are not jurisdiction-scoped public-domain claims; this confirms
  the field is correctly optional (records that don't need it omit it cleanly).
- The `custodyChain[]` array captured the multi-hop sourcing (e.g. GitHub → BigQuery →
  BigScience filter → gated release) as a readable ordered chain.

## What the schema could not represent

Two new gaps surfaced; both BLOOM-specific. Existing gaps B and C were re-surfaced and
strengthened by new evidence.

**Status of 0.0.1.** As of this stress test, the 0.0.1 schema on `main` is only a minimal
skeleton; the concrete `ProvenanceRecord` shape lives on the `minimal-mimir` and
`common-corpus-stress-test` branches. Because 0.0.1 has neither been released nor landed as a
concrete schema on `main`, it is still fluid: gaps can be folded in without breaking a released
or main-resident form. The distinction that matters is **additive vs. breaking** (see the Common
Corpus notes for the full framing). Both new gaps here are additive (optional fields), so both
are candidates for 0.0.1 if the list takes them up.

### Gap F — The `license` field can reflect a processing artifact rather than the intended selection  *(additive — candidate for 0.0.1)*

The GitHub code component of ROOTS was *intended* to include code under a range of permissive
and copyleft licenses (the same language selection as AlphaCode). Due to a bug in the
pre-processing pipeline, the dataset was *actually* filtered for GPL-family licenses only. The
ROOTS paper documents this honestly (Section 2.1, "GitHub Code") as an unintended restriction.

The `bloom-roots-github-code-gpl-only.jsonld` record carries `license: GPL-3.0-only` — which is
*accurate* to the files that survived the buggy filter, but *inaccurate* to what BigScience
intended to select. A consumer reading this record cannot tell from the `license` field alone
that it reflects a processing artifact rather than a deliberate selection. This is a
provenance-honesty / data-quality problem distinct from the license-vocabulary gaps (A, B):
the license IRI is not wrong, but the *reason* it has that value is not "the dataset is
GPL-licensed" but "the filter had a bug."

**How this model surfaced it.** BLOOM/ROOTS is the first corpus we've modeled that documents a
processing artifact in its own datasheet. Mímir and Common Corpus records carry licenses that
reflect deliberate choices; the GitHub-code record carries a license that reflects an
unintended filter. An auditor comparing the record to the ROOTS paper would find the
discrepancy, but the record itself gives no signal.

**Why this justifies a change.** Sourcelume's purpose is to make claims *checkable by someone
else*. A `license` field whose value reflects a processing artifact rather than the intended
selection is technically accurate but misleading without context. An optional, additive
`licenseNote` or `selectionBasis` field would let a record say "this license reflects the
intended selection" vs. "this license reflects a processing artifact (see origin / ROOTS paper
§2.1)" — turning a silent inaccuracy into a checkable, honest claim. This is additive and
non-breaking: records that don't need the field omit it.

**Proposed direction:** an optional `licenseNote` (or `selectionBasis`) free-text field to
qualify *why* the `license` field has its value (deliberate selection vs. processing artifact
vs. representative-IRI-for-a-heterogeneous-aggregate). Distinct from `licenseScope` (which
qualifies *where* a license applies) and from the multi-license-array proposal (Gap B, which
would replace the single IRI). Because this is additive and 0.0.1 is not yet on `main` as a
concrete schema, it can be folded in without breaking a released form.

### Gap G — A single `license` IRI cannot express a use-restricted (RAIL) license category  *(additive — candidate for 0.0.1)*

BLOOM is released under the BigScience RAIL License v1.0 — a Responsible AI License that is
open and permissive in its copyright/patent grants (similar to Apache 2.0 in the IP section) but
carries use-based restrictions (Attachment A) prohibiting specific harmful uses (exploiting
minors, generating verifiably false information to harm others, fully automated decision-making
adversely impacting legal rights, discrimination against protected groups, providing medical
advice, use in law-enforcement/immigration/asylum processes).

The `bloom-176b-model.jsonld` record carries `license` pointing at the RAIL License text URL.
This is *checkable* — an auditor following the IRI finds the full license text including the
use-restriction clauses. But the 0.0.1 schema has no way to signal, at the record level, that
this license is a **use-restricted** license (RAIL) rather than a pure open-source (Apache 2.0)
or pure open-data (CC0/CC-BY) license. A consumer who only inspects the license IRI's domain
(`huggingface.co/spaces/bigscience/license`) cannot classify it without fetching and reading
the full text.

**How this model surfaced it.** BLOOM is the first model we've modeled whose license is neither
pure open-source nor a pure data license. Mímir and Pleias-RAG-1B are trained on data under
various licenses, but the *models'* own licenses (where we recorded them) are standard
open-source-ish. BLOOM's RAIL License is a distinct category: open-access weights with
use-based restrictions. This is increasingly common for "open" AI model releases (RAIL,
OpenRAIL, BigScience RAIL, LLaMA's community license, etc.).

**Why this justifies a change.** For a provenance system, the distinction between "open-source
license" and "use-restricted model license" is material: a downstream user deciding whether
they can use a model for a given purpose needs to know the license *category*, not just
fetch-and-read every license text. An optional, additive `licenseCategory` (or `licenseType`)
field with a small controlled vocabulary (e.g. `open-source`, `open-data`,
`use-restricted-model-license`, `public-domain`, `agreement-supplied`, `proprietary`) would
let a record classify its license at a glance while the `license` IRI remains the
authoritative full text. This is additive and non-breaking.

**Proposed direction:** an optional `licenseCategory` field with a small controlled vocabulary
classifying the *kind* of license (open-source / open-data / use-restricted / public-domain /
agreement-supplied / proprietary). The `license` IRI remains the authoritative full text; the
category is a convenience classifier for downstream consumers. Additive, non-breaking, candidate
for 0.0.1.

### Re-surfaced and strengthened: Gaps B and C

- **Gap B (per-document multi-license aggregate)** is re-surfaced by three of the five BLOOM
  records: OSCAR (web pages under heterogeneous licenses), GitHub code (multiple GPL-family
  licenses + the processing artifact), and S2ORC (papers from many publishers under many
  licenses). BLOOM/ROOTS confirms Gap B is not Common-Corpus-specific — it recurs for any
  large web-crawl or multi-publisher academic corpus.
- **Gap C (large distributed creator/source population)** is re-surfaced by the pseudo-crawled
  websites record: 539 community-identified domains, each with its own terms, aggregated into
  one dataset. This is the same structural problem as Common Corpus's 721k YouTube channels,
  but at smaller scale (539 vs. 721k) and with a different sourcing model (community-identified
  domains vs. platform-hosted channels).

## Summary table

| Gap | Title | First surfaced by | BLOOM evidence | Resolution status |
|---|---|---|---|---|
| A | Jurisdiction-scoped public-domain status | Common Corpus | Not applicable (BLOOM/ROOTS sources not jurisdiction-scoped PD) | **Folded into 0.0.1** (`licenseScope`) |
| B | Per-document multi-license aggregate | Common Corpus | Re-surfaced by OSCAR, GitHub code, S2ORC | Open (breaking); prototypes built |
| C | Large distributed creator/source population | Common Corpus | Re-surfaced by 539 pseudo-crawled domains | Open (additive); prototype built |
| D | Transformative LLM custody-hop action vocabulary | Common Corpus | Not applicable (BLOOM/ROOTS curation is human/rule-based, not LLM-based) | Open (vocabulary) |
| E | Training-phase (pretrain/SFT/RAG) not distinguishable | Mímir / Common Corpus | Not applicable (BLOOM is pretrain-only) | Open (scope) |
| F | `license` reflects processing artifact not intended selection | BLOOM (GitHub code GPL-only bug) | New | Open (additive — candidate for 0.0.1) |
| G | `license` IRI cannot express use-restricted (RAIL) license category | BLOOM (RAIL License v1.0) | New | Open (additive — candidate for 0.0.1) |

Gaps F and G are additive and candidates for 0.0.1 if the list takes them up; they do not break
existing records. Gap B remains the strongest breaking candidate (waits for the
license-vocabulary discussion). 0.0.1 is not yet on `main` as a concrete schema, so additive
changes can still be folded in without breaking a released form when the open questions settle.

## Inputs used

- Laurençon et al., "The BigScience ROOTS Corpus: A 1.6TB Composite Multilingual Dataset",
  NeurIPS 2022 Datasets and Benchmarks Track — arXiv 2303.03915
  (https://arxiv.org/abs/2303.03915). Source taxonomy (Section 2), OSCAR processing
  (Section 3), GitHub code GPL-only bug (Section 2.1), Data Sources appendix (Appendix E).
- BigScience RAIL License v1.0 — https://huggingface.co/spaces/bigscience/license
  (copyright/patent grants + use-based restrictions in Attachment A).
- BigScience ethical charter — https://hf.co/spaces/bigscience/ethical-charter (the gated
  release of ROOTS is subject to committing to this charter).
- BigScience data-host-provider-agreement —
  https://huggingface.co/spaces/bigscience/data-host-provider-agreement (the data governance
  framework for partner-contributed data).
- BigScience data-preparation tools — https://github.com/bigscience-workshop/data-preparation
- BLOOM model card — https://huggingface.co/bigscience/bloom
- Jernite et al. 2022, data governance paper —
  https://doi.org/10.1145/3531146.3534637 (the BigScience data-governance approach).
