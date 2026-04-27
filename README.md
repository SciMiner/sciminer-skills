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
- `virtual-screening`: Virtual screening workflows for small molecules and fragment libraries (docking, scoring, library enumeration, high-throughput screening). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/virtual-screening
- `small-molecule-design`: Small-molecule generative and optimization workflows (de novo design, lead optimization, property-constrained generation). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/small-molecule-design
- `synthesis-evaluation`: Synthesis planning and evaluation tools (retrosynthesis suggestions, route scoring, feasibility and building-block analysis). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/synthesis-evaluation
- `optical-chemical-structure-recognition`: Optical chemical structure recognition (image-to-structure OCR, extract structures from figures or PDFs, image-to-SMILES conversion and parsing). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/optical-chemical-structure-recognition
- `binding-site-prediction`: Binding-site and pocket prediction workflows using P2Rank, AF2BIND, and fpocket (ML-based ranking, geometry-based detection, and per-residue binding probability scoring). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/binding-site-prediction
- `antibody-engineering`: End-to-end antibody engineering combining ANARCI, BioPhi, IgFold, FoldX, and Rosetta (sequence numbering, humanization, structure prediction, developability profiling, affinity maturation, and precision redesign). Requires `SCIMINER_API_KEY`. ClawHub: https://clawhub.ai/sciminer/antibody-engineering

Notes
- These skills rely on the SciMiner API and require an API key, which you can obtain for free at https://sciminer.tech/utility and paste into the input box of OpenClaw or Claude code when prompted.