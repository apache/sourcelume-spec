# DFM Mímir v1 — direct training-input manifest

This is a working manifest of the datasets that the DFM Mímir v1 model is
*directly* trained on, against which we author `ProvenanceRecord` examples in
this repository.

**Corrected understanding (2026-09-08).** An earlier version of this manifest
described the 48 constituent sources of the
[`danish-foundation-models/danish-dynaword`](https://huggingface.co/datasets/danish-foundation-models/danish-dynaword)
corpus as if they were Mímir's training data. That was wrong. Mímir does **not**
train on raw dynaword. Per the Mímir v1 technical report (arXiv 2608.13517,
Appendix A, Table 10), Mímir is trained on **161 datasets**; dynaword enters
the corpus only indirectly, through four synthetic derivatives published under
`schneiderkamplab/danish-dynaword-*` (denoising, span-filling,
prefix-continuation, paragraph-reordering), which are derived from dynaword
text and judge-filtered with `google/gemma-4-31B-it`.

Dynaword itself (9.81B Llama-3 tokens across 48 sources, v1.2.23) remains a
useful upstream-of-Mímir corpus, but its 48 sub-sources are **not** direct
Mímir training inputs and are out of scope for this branch's example records.

## The 12 authored direct-input records

Each row below has a corresponding `examples/dfm-mimir-*.jsonld` record in this
repository. Token counts and shares are sampled tokens per epoch, from Table 10
of the technical report.

| # | Dataset (HF id) | Form | Tokens/epoch | Share | Record |
|---|---|---|---|---|---|
| 1 | `sapientinc/HRM-Text-data-io-cleaned-20260515` | Curated + reformatted | 11.92B | 16.91% | `dfm-mimir-hrm-text-data-io-cleaned.jsonld` |
| 2 | `danish-foundation-models/laerebogen` | Reformatted | 8.32B | 11.81% | `dfm-mimir-laerebogen.jsonld` |
| 5 | `danish-foundation-models/dfm-dyna-instruct` | Reformatted | 3.54B | 5.03% | `dfm-mimir-dfm-dyna-instruct.jsonld` |
| 7 | `schneiderkamplab/opus-da-en-permissive` | Reformatted | 2.90B | 4.12% | `dfm-mimir-opus-da-en-permissive.jsonld` |
| 16 | `synquid/wiki-instruct-da` | Reformatted | 988M | 1.40% | `dfm-mimir-wiki-instruct-da.jsonld` |
| 17 | `schneiderkamplab/dfm8-openhermes-da` | Translated + audited | 922M | 1.31% | `dfm-mimir-dfm8-openhermes-da.jsonld` |
| 34 | DBC (agreement-supplied) | Agreement-supplied | 356M | 0.505% | `dfm-mimir-dbc.jsonld` |
| 35 | `schneiderkamplab/danish-dynaword-denoising` | Synthetic + audited | 323M | 0.459% | `dfm-mimir-danish-dynaword-denoising.jsonld` |
| 36 | Lex.dk articles (agreement-supplied) | Agreement-supplied | 313M | 0.445% | `dfm-mimir-lexdk-articles.jsonld` |
| 38 | `schneiderkamplab/danish-dynaword-prefix-continuation` | Synthetic + audited | 252M | 0.357% | `dfm-mimir-danish-dynaword-prefix-continuation.jsonld` |
| 39 | `schneiderkamplab/danish-dynaword-span-filling` | Synthetic + audited | 251M | 0.356% | `dfm-mimir-danish-dynaword-span-filling.jsonld` |
| 49 | `schneiderkamplab/danish-dynaword-paragraph-reordering` | Synthetic + audited | 160M | 0.228% | `dfm-mimir-danish-dynaword-paragraph-reordering.jsonld` |

These 12 cover: the English pretraining core (sapientinc), the three largest
Danish instruction sources (laerebogen, dfm-dyna-instruct, opus), the
Danish-Wikipedia-derived instruction set, the translated OpenHermes derivative,
both agreement-supplied sources, and all four dynaword-derived synthetic task
datasets. Together they represent ~41% of the Mímir corpus by sampled tokens
and span every "form" category the report uses for Danish-relevant data.

## The remaining 149 datasets

The other 149 entries in Table 10 are predominantly English
instruction/reasoning/tool-use corpora (OpenMathInstruct, Nemotron, Dolci,
Tulu, etc.) and a long tail of small `schneiderkamplab/sapient-synth-*` and
`oliverkinch/*` Danish datasets. They are not authored as records in this pass.
The full 161-entry table is reproduced in Appendix A of the Mímir v1 technical
report (arXiv 2608.13517) and is the authoritative source for any future
record authoring.

## Dynaword's sub-sources (out of scope, kept for reference)

The 48 constituent sources of `danish-foundation-models/danish-dynaword`
(adl, folketingets-dokumenter, wikipedia, kalliope, retsinformationdk, ncc_parliament,
ai-aktindsigt, dakultur, and 40 others) are upstream of dynaword and therefore
*upstream-of-upstream* of Mímir. They are not direct Mímir training inputs.
Their per-source datasheets live at `data/<source>/<source>.md` under the
dynaword repo. If a future crosswalk or registry query needs to trace Mímir's
Danish text back to its ultimate origin, those sub-sources would each warrant
their own `ProvenanceRecord` linked from the four `danish-dynaword-*`
derivative records' `custodyChain` entries — but that is a larger, separate
effort, not part of this 0.0.1 teaching artifact.

## License vocabulary used across the 12 records

| License | IRI | Records |
|---|---|---|
| Apache 2.0 | https://www.apache.org/licenses/LICENSE-2.0 | laerebogen, 4x danish-dynaword-* derivatives, dfm8-openhermes-da |
| ODC-By 1.0 | https://opendatacommons.org/licenses/by/1-0/ | hrm-text-data-io-cleaned, dfm-dyna-instruct (dominant sub-source) |
| CC-BY-SA 4.0 (Wikipedia) | https://creativecommons.org/licenses/by-sa/4.0/deed.en | wiki-instruct-da (underlying text) |
| OPUS aggregated (mixed permissive) | https://opus.nlpl.eu/ | opus-da-en-permissive |
| Agreement-supplied (interim convention) | https://sourcelume.apache.org/ns#agreement-supplied | DBC, Lex.dk articles |
