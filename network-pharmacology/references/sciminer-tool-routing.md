# SciMiner routing

Resolve each tool dynamically from the live index. Tool availability and exact payload schemas can change; never copy a provider name, tool name, enum, or parameter from this file into an API request without rereading that tool's live Markdown document.

| Analysis need | Candidate live SciMiner document | Use only when |
|---|---|---|
| Candidate on-target interactions | `Target Predictor_api_doc.md`, `TransformerCPI_api_doc.md` | A canonical ligand structure is available and the output will be labelled predicted. |
| Safety and promiscuity | `Off-Target Predictor_api_doc.md` | The question includes selectivity, adverse effects, or unintended targets. |
| Existing experimental activity | `Get Bioactivity_api_doc.md` | A compound or chemical series needs activity context. |
| Drug-likeness and exposure hypotheses | `ADMET Predictor_api_doc.md`, `Check Lipinski_api_doc.md`, `Check PAINS_api_doc.md`, `Graph-pKa_api_doc.md` | The study explicitly needs developability, exposure, or artifact-risk context. |
| Protein structure or binding site | `AlphaFold*_api_doc.md`, `fpocket_api_doc.md`, `p2rank_api_doc.md` | A target passes evidence prioritization and structure is needed for a specified follow-up. |
| Docking and rescoring | `AutoDock Vina_api_doc.md`, `DiffDock_api_doc.md`, `Gnina_api_doc.md`, `Smina_api_doc.md` | A pre-specified compound–target pair has structure/site rationale. |
| Interaction inspection | `Mol Interactions_api_doc.md`, `PoseView_api_doc.md`, `PLIP Filter_api_doc.md` | A docked or experimental complex needs pose-level inspection. |
| Chemical tables and figures | `CSV Visualizer_api_doc.md`, `SMILES 2 Image_api_doc.md` | A SciMiner-generated table or molecular depiction adds value to the report. |

## Invocation protocol

1. Read `https://sciminer.simm.ac.cn/tool_api_files/` and resolve the actual link by case-insensitive exact tool-name match where possible.
2. Read the complete selected document.
3. Read the API key from `~/.config/sciminer/credentials.json`; send it only as the documented authentication header.
4. Upload required files using the documented upload field, then place returned `file_id` values in documented parameters.
5. Submit exactly the documented payload and poll exactly as documented.
6. Save only non-secret task metadata, result summary, source-doc URL, `task_id`, and `share_url` in the project manifest.

If the tool is absent, ambiguous, or requires a parameter the user did not supply, stop that lane and state the missing requirement. Do not substitute a different platform or invent values.
