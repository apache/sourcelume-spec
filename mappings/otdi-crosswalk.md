# Crosswalk: Sourcelume ↔ Open Trusted Data Initiative (OTDI)

> **Status: draft, lowest confidence of the three crosswalks.** OTDI's public vocabulary is less
> stable/documented than Croissant or SPDX as of this writing — treat every row here as a
> placeholder pending confirmation from the AI Alliance's published OTDI artifacts.

| Sourcelume field | OTDI concept (tentative) | Notes |
|---|---|---|
| `identifier` | dataset identifier | Needs confirmation of OTDI's canonical ID property name. |
| `origin` | provenance narrative / data source description | OTDI is reported to emphasize consent and collection-method disclosure more heavily than Sourcelume's 0.0.1 free-text `origin` field does. |
| `custodyChain` | chain-of-custody / handling event | Likely the strongest conceptual overlap between the two specs, but needs a real OTDI schema reference to map field-by-field. |

## Open questions

- Get a concrete OTDI schema/example on the dev list so this crosswalk can move past
  conceptual-only mapping.
