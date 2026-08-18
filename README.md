# SciMiner Skills

Reusable, evidence-aware skills for life-science research workflows powered by SciMiner and related public resources.

## Included skills

The repository covers workflows for:

- ADMET/PK-PD, molecular docking, virtual screening, FEP alternatives, and synthesis evaluation
- Protein, peptide, antibody, and small-molecule design
- Structure prediction, binding-site prediction, and optical chemical-structure recognition
- Network pharmacology, SAR analysis, pharmaceutical intelligence, and biomedical patent trends
- Life-science database queries and SciMiner tool discovery

Each skill is self-contained in its own directory and includes a `SKILL.md` with its scope, workflow, requirements, and safety boundaries. Some skills also provide references and helper scripts.

## Usage

Use the skill directory as the source of truth for its workflow. Read the relevant `SKILL.md` before starting an analysis and provide the required inputs and environment variables listed there. SciMiner API credentials must be supplied through the runtime environment; do not commit secrets to this repository.

## Evidence and reproducibility

These skills are designed to separate experimental, curated, literature, predicted, and computational evidence. Computational results are hypotheses or supporting evidence, not proof of binding, efficacy, causality, or clinical benefit. Preserve source URLs, tool versions, parameters, exclusions, and generated reports for reproducibility.

## License

See the repository or organization-level license and contribution policies before redistributing or modifying these materials.
