# Apache Sourcelume — Spec (`sourcelume-spec`)

## Overview

This repository contains our Apache Sourcelume specification.


```
sourcelume-spec/
├── LICENSE                     # Apache 2.0 (code/tooling)
├── README.md
├── NOTICE                      # required for ASF releases
├── CHANGELOG.md
├── context/
│   ├── v0.0.1/
│   │   └── sourcelume.jsonld    # the JSON-LD @context document, pinned
│   └── latest -> v0.0.1/        # symlink or redirect, NOT a moving target for actual releases
├── schema/
│   ├── v0.0.1/
│   │   ├── sourcelume.schema.json   # JSON Schema for structural validation
│   │   └── sourcelume.shacl.ttl     # SHACL shapes for RDF-level validation (optional but common for JSON-LD vocabs)
│   └── ...
├── spec/                         # the prose specification
│   ├── v0.1/
│   │   └── index.md (or .adoc)   # human-readable spec text, versioned alongside schema
├── examples/
│   ├── minimal-record.jsonld
│   ├── full-provenance-card.jsonld
│   └── crosswalk/                # worked examples showing mapping to Croissant / SPDX / OTDI fields
├── mappings/
│   ├── croissant-crosswalk.md
│   ├── spdx-ai-profile-crosswalk.md
│   └── otdi-crosswalk.md
├── tools/
│   ├── validate.py               # or JS — validates examples/ against schema/shacl on every PR
│   └── render-docs.py            # generates human-readable HTML/MD from schema
├── .github/workflows/
│   └── validate.yml              # CI: lint JSON-LD, run schema+SHACL validation, check examples
└── .gitignore
```


## Get involved

- Mailing list: dev@sourcelume.apache.org ([archives](https://lists.apache.org/list.html?dev@sourcelume.apache.org))
- ASF Slack: #sourcelume (Ask to be invited)

## License

This project is licensed under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).