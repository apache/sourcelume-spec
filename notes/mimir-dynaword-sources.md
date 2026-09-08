# Mímir (DFM) training corpus — dynaword source manifest

This is a working manifest of the constituent datasets that make up the
Danish Dynaword corpus, against which the DFM Mímir model is trained. It is
used to track authoring of `ProvenanceRecord` examples in this repository.

Source: <https://huggingface.co/datasets/danish-foundation-models/danish-dynaword>
(version 1.2.23 at time of writing). Dynaword is continually developed; sizes
and even membership change over time. Pin a revision for reproducibility.

The corpus totals 9.81B tokens (Llama 3) across 48 sources. The license below
is applied to the constituent text; the collection (metadata, quality
control) is CC-0. Each row's datasheet lives at
`data/<source>/<source>.md` under the dynaword repo — that datasheet is the
authoritative source for originator/curator/custody detail when authoring a
`ProvenanceRecord` for that source.

## License families and representative picks

Eight license classes appear across the 48 sources. We author one
representative `ProvenanceRecord` per class first, to prove the 0.0.1 schema
handles every license dynaword uses. The other 40 sources are authored in a
follow-on pass using the same conventions.

| License class                           | IRI / note                                      | Picked source            | Tokens   | Domain | Datasheet |
|-----------------------------------------|-------------------------------------------------|--------------------------|----------|--------|----------|
| CC-0 (public domain dedication)         | https://creativecommons.org/publicdomain/zero/1.0/legalcode.en | adl                      | 58.49M   | Books  | data/adl/adl.md |
| CC-BY 4.0                                | https://creativecommons.org/licenses/by/4.0/deed.en | folketingets-dokumenter  | 2.81B    | Other  | data/folketingets-dokumenter/folketingets-dokumenter.md |
| CC-BY-SA 4.0                             | https://creativecommons.org/licenses/by-sa/4.0/deed.en | wikipedia                | 173.33M  | Encyclopedic | data/wikipedia/wikipedia.md |
| Public domain (by expiration, not CC-0) | CC Public Domain Mark — see spec prose convention | kalliope                 | 14.01M   | Books  | data/kalliope/kalliope.md |
| Danish Copyright Law (state edict)      | No standard IRI — documented convention          | retsinformationdk       | 818.25M  | Legal  | data/retsinformationdk/retsinformationdk.md |
| NLOD 2.0 (Norwegian Licence for Open Government Data) | https://data.norge.no/nlod/en/2.0 | ncc_parliament           | 338.87M  | Other  | data/ncc_parliament/ncc_parliament.md |
| Apache 2.0                               | https://www.apache.org/licenses/LICENSE-2.0      | ai-aktindsigt            | 139.23M  | Web    | data/ai-aktindsigt/ai-aktindsigt.md |
| MIT                                      | https://opensource.org/license/mit              | dakultur                 | 5.49K    | Conversation | data/dakultur/dakultur.md |

danish-pd (already authored, CC Public Domain Mark) overlaps the "Public
domain" row; kalliope is a second PD source but by a different mechanism
(explicit PD release of poetry), so it still serves as the representative
for the PD-by-means-other-than-CC-0 case.

## Full source list (48)

Token counts are Llama-3 tokens. "Datasheet" column is the relative path
within the dynaword repo.

### Other (domain) — 3.22B

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| ncc_parliament | 338.87M | NLOD 2.0 | data/ncc_parliament/ncc_parliament.md |
| dannet | 1.48M | DanNet 1.0 (custom) | data/dannet/dannet.md |
| depbank | 185.45K | CC-BY-SA 4.0 | data/depbank/depbank.md |
| synne | 52.02K | CC-0 | data/synne/synne.md |
| historical-danish-handwriting | 5.20M | CC-BY 4.0 | data/historical-danish-handwriting/historical-danish-handwriting.md |
| kb_historical_letters | 14.75M | CC-0 | data/kb_historical_letters/kb_historical_letters.md |
| tidsskrift-dk | 50.03M | CC-BY 4.0 | data/tidsskrift-dk/tidsskrift-dk.md |
| folketingets-dokumenter | 2.81B | CC-BY 4.0 | data/folketingets-dokumenter/folketingets-dokumenter.md |

### Legal (domain) — 3.18B

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| cellar | 1.15B | CC-BY-SA 4.0 | data/cellar/cellar.md |
| eur-lex-sum-da | 31.37M | CC-BY-SA 4.0 | data/eur-lex-sum-da/eur-lex-sum-da.md |
| fm-udgivelser | 50.34M | CC-BY-SA 4.0 | data/fm-udgivelser/fm-udgivelser.md |
| retsinformationdk | 818.25M | Danish Copyright Law | data/retsinformationdk/retsinformationdk.md |
| skat | 122.11M | CC-0 | data/skat/skat.md |
| retspraksis | 56.26M | CC-0 | data/retspraksis/retspraksis.md |
| domsdatabasen | 86.35M | Danish Copyright Law | data/domsdatabasen/domsdatabasen.md |
| kb_administrative_publication | 844.58M | CC-0 | data/kb_administrative_publication/kb_administrative_publication.md |
| municipality_meetings | 22.64M | CC-0 | data/municipality_meetings/municipality_meetings.md |

### News (domain) — 1.09B

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| enevaeldens_nyheder | 1.03B | CC-BY-SA 4.0 | data/enevaeldens_nyheder/enevaeldens_nyheder.md |
| ncc_newspaper | 1.05M | CC-0 | data/ncc_newspaper/ncc_newspaper.md |
| tv2r | 21.67M | CC-BY-SA 4.0 | data/tv2r/tv2r.md |
| nordjyllandnews | 37.90M | CC-0 | data/nordjyllandnews/nordjyllandnews.md |

### Books (domain) — 747.93M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| grundtvig | 10.53M | CC-0 | data/grundtvig/grundtvig.md |
| ncc_books | 531.97M | CC-0 | data/ncc_books/ncc_books.md |
| memo | 113.74M | CC-BY-SA 4.0 | data/memo/memo.md |
| adl | 58.49M | CC-0 | data/adl/adl.md |
| wikibooks | 7.63M | CC-BY-SA 4.0 | data/wikibooks/wikibooks.md |
| jvj | 3.55M | CC-BY-SA 4.0 | data/jvj/jvj.md |
| gutenberg | 6.76M | Gutenberg (custom) | data/gutenberg/gutenberg.md |
| relig | 1.24M | CC-0 | data/relig/relig.md |
| kalliope | 14.01M | Public domain | data/kalliope/kalliope.md |

### Conversation (domain) — 497.11M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| danske-taler | 8.72M | CC-0 | data/danske-taler/danske-taler.md |
| opensubtitles | 271.60M | CC-0 | data/opensubtitles/opensubtitles.md |
| ep | 100.84M | CC-0 | data/ep/ep.md |
| ft | 114.09M | CC-0 | data/ft/ft.md |
| spont | 1.56M | CC-0 | data/spont/spont.md |
| naat | 286.68K | CC-0 | data/naat/naat.md |
| dakultur | 5.49K | MIT | data/dakultur/dakultur.md |
| mosel_youtubecommons | 7.09K | CC-BY 4.0 | data/mosel_youtubecommons/mosel_youtubecommons.md |

### Social Media (domain) — 389.32M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| hest | 389.32M | CC-0 | data/hest/hest.md |

### Web (domain) — 295.93M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| ai-aktindsigt | 139.23M | Apache 2.0 | data/ai-aktindsigt/ai-aktindsigt.md |
| ncc_maalfrid | 29.26M | NLOD 2.0 | data/ncc_maalfrid/ncc_maalfrid.md |
| miljoeportalen | 127.38M | CC-0 | data/miljoeportalen/miljoeportalen.md |
| hvadvilduhelst | 57.22K | CC-BY 4.0 | data/hvadvilduhelst/hvadvilduhelst.md |

### Encyclopedic (domain) — 185.75M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| wikisource | 6.28M | CC-BY-SA 4.0 | data/wikisource/wikisource.md |
| wikipedia | 173.33M | CC-BY-SA 4.0 | data/wikipedia/wikipedia.md |
| wiki-comments | 6.14M | CC-BY-SA 4.0 | data/wiki-comments/wiki-comments.md |

### Speeches (domain) — 161.33M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| mosel_voxpopuli | 161.33M | CC-BY 4.0 | data/mosel_voxpopuli/mosel_voxpopuli.md |

### Medical (domain) — 27.07M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| health_hovedstaden | 27.07M | CC-0 | data/health_hovedstaden/health_hovedstaden.md |

### Readaloud (domain) — 7.30M

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| nota | 7.30M | CC-0 | data/nota/nota.md |

### Dialect (domain) — 847.97K

| Source | Tokens | License | Datasheet |
|---|---|---|---|
| botxt | 847.97K | CC-0 | data/botxt/botxt.md |

## Note on danish-pd

`examples/dfm-mimir-danish-pd-best-effort.jsonld` is already authored. It
is not itself a dynaword source — it is the upstream corpus that PleIAs
aggregated and that DFM drew from for the public-domain portion of
dynaword. It is included here as the reference record shape and as the
Public-Domain-Mark representative.
