# Evidence model

Apply this model before merging networks or ranking targets.

## Entity evidence tiers

| Entity or edge | Tier | Meaning |
|---|---:|---|
| Compound | 1 | Measured in the material, preparation, or biological sample with traceable analytical evidence. |
| Compound | 2 | Literature- or curated-database supported constituent. |
| Compound | 3 | Database-listed or computational candidate only. |
| Compound–target | 1 | Quantitative experimental bioactivity or a directly curated mechanism. |
| Compound–target | 2 | Curated interaction without usable quantitative context. |
| Compound–target | 3 | Algorithmic prediction, including SciMiner prediction. |
| Target–disease | 1 | Human genetics or strongly supported causal/functional evidence. |
| Target–disease | 2 | Disease-relevant functional, expression, pathway, or clinical-context evidence. |
| Target–disease | 3 | Text-mined, co-occurrence, or weak indirect association. |

Keep tiers separate. A composite score may rank records within a project, but it must be explainable, preserve source fields, and never upgrade the underlying tier.

## Interpretation checks

- Treat a predicted target as a testable candidate, not an observed interaction.
- Treat PPI links as functional or physical associations according to the source; do not assume direct binding.
- Treat enrichment as annotation over-representation, not pathway activation or inhibition.
- Require an explicit direction source before claiming activation, inhibition, up-regulation, or down-regulation.
- Treat docking as structural plausibility only unless independent activity/engagement evidence exists.

## Reproducibility checklist

Record source URLs, versions/releases, access date, species, identifier namespace, mapping losses, filtering thresholds, background universe, statistical test, multiple-testing method, SciMiner tool document URL, task ID, and share URL.
