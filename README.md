SciMiner Skills

A concise collection of skill definitions built on top of the SciMiner API.

Installation
- OpenClaw: install from the OpenClaw skill marketplace or add this repository.
- Claude Code: in a Claude Code conversation, request installation of "sciminer-skills", or install directly via ClawHub (links are listed with each skill below).

Usage
- Each skill folder contains a SKILL.md with usage details (admet-pkpd, peptide-design, protein-design, structure-prediction).

Skills
- `admet-pkpd`: Pan-ADMET small-molecule property prediction workflows (ADMET, solvation energy, pKa, oral bioavailability, cocrystal, AOX metabolism, molecular descriptors). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/admet-pkpd
- `peptide-design`: Peptide generation and analysis (pocket-guided docking, macrocyclic peptide design, peptide descriptors, extinction coefficient, pI, liabilities). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/xiongzhp/peptide-design
- `protein-design`: BoltzGen protein/peptide/antibody/nanobody design (de novo and targeted designs; supports file uploads for targets and frameworks). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/xiongzhp/protein-design
- `structure-prediction`: Biomolecular structure prediction using Chai-1, Boltz-2, and Alphafold3 for proteins, nucleic acids, ligands, and complexes. Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/xiongzhp/structure-prediction

Notes
- These skills depend on the SciMiner API and may require API credentials.
