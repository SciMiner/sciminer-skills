"""Registry for the `small-molecule-design` skill."""

REINVENT4_MODEL_TYPES = [
    "reinvent",
    "libinvent",
    "linkinvent",
    "mol2mol",
    "pepinvent",
]

REINVENT4_SAMPLE_STRATEGIES = ["multinomial", "beamsearch"]

REINVENT4_TRANSFER_MODEL_TYPES = ["reinvent", "mol2mol"]

REINVENT4_COMPONENTS = [
    "QED",
    "MolecularWeight",
    "TPSA",
    "SlogP",
    "Csp3",
    "HBondAcceptors",
    "HBondDonors",
    "NumRotBond",
    "NumHeavyAtoms",
    "NumRings",
    "NumAromaticRings",
    "NumHeteroAtoms",
    "SAScore",
    "TanimotoSimilarity",
    "CustomAlerts",
    "Docking:gnina",
]

POCKETXMOL_TASK_TYPES = ["sbdd", "linking", "growing"]
POCKETXMOL_MODES = ["autoregressive", "one_shot"]
POCKETXMOL_FRAGMENT_POSE_MODES = ["fixed", "free", "small"]


TOOLS_REGISTRY = {
    "REINVENT4 Sampling": {
        "provider_name": "REINVENT4",
        "description": "Generate molecules with REINVENT4 using de novo, linker, transformation, or peptide-aware generative models.",
        "category": "Generative Molecule Design",
        "interfaces": {
            "default": {
                "tool_name": "sampling_sampling_post",
                "description": "Sample molecules with REINVENT4 from default or uploaded trained models.",
                "parameters": {
                    "model_type": {"type": "string", "required": False, "description": "REINVENT4 model type", "enum": REINVENT4_MODEL_TYPES, "default": "reinvent"},
                    "sample_strategy": {"type": "string", "required": False, "description": "Sampling strategy for Mol2Mol or PepInvent", "enum": REINVENT4_SAMPLE_STRATEGIES, "default": "multinomial"},
                    "num_smiles": {"type": "integer", "required": False, "description": "Number of SMILES to sample", "default": 100},
                    "unique_molecules": {"type": "boolean", "required": False, "description": "Remove duplicate molecules", "default": True},
                    "randomize_smiles": {"type": "boolean", "required": False, "description": "Randomize SMILES atom order", "default": True},
                    "smiles_file": {"type": "file", "required": False, "description": "Optional SMILES file for LibInvent, LinkInvent, Mol2Mol, or PepInvent"},
                    "model_file": {"type": "file", "required": False, "description": "Optional trained model file from transfer-learning output"},
                    "temperature": {"type": "number", "required": False, "description": "Sampling temperature", "default": 2},
                },
                "file_params": ["smiles_file", "model_file"],
            }
        }
    },
    "REINVENT4 Transfer Learning": {
        "provider_name": "REINVENT4",
        "description": "Fine-tune supported REINVENT4 models from custom SMILES data.",
        "category": "Generative Molecule Design",
        "interfaces": {
            "default": {
                "tool_name": "transfer_learning_transfer_learning_post",
                "description": "Run transfer learning on REINVENT4 priors with custom molecular examples.",
                "parameters": {
                    "model_type": {"type": "string", "required": False, "description": "Transfer-learning model type", "enum": REINVENT4_TRANSFER_MODEL_TYPES, "default": "reinvent"},
                    "transfer_smiles_file": {"type": "file", "required": True, "description": "Training SMILES file for fine-tuning"},
                    "input_model_file": {"type": "file", "required": False, "description": "Optional starting model file"},
                    "num_epochs": {"type": "integer", "required": False, "description": "Number of training epochs", "default": 10},
                    "batch_size": {"type": "integer", "required": False, "description": "Training batch size", "default": 64},
                    "learning_rate": {"type": "number", "required": False, "description": "Training learning rate", "default": 0.0001},
                },
                "file_params": ["transfer_smiles_file", "input_model_file"],
            }
        }
    },
    "REINVENT4 Staged Learning": {
        "provider_name": "REINVENT4",
        "description": "Optimize molecular generation with reinforcement learning and configurable scoring components.",
        "category": "Generative Molecule Design",
        "interfaces": {
            "default": {
                "tool_name": "staged_learning_staged_learning_post",
                "description": "Run staged reinforcement learning for molecule optimization with optional docking-aware objectives.",
                "parameters": {
                    "model_type": {"type": "string", "required": False, "description": "REINVENT4 model type", "enum": REINVENT4_MODEL_TYPES, "default": "reinvent"},
                    "components": {"type": "array", "required": False, "description": "Optimization scoring components", "enum": REINVENT4_COMPONENTS},
                    "seed_smiles_file": {"type": "file", "required": False, "description": "Seed molecules for RL optimization"},
                    "ref_smiles_file": {"type": "file", "required": False, "description": "Reference molecules for TanimotoSimilarity"},
                    "input_model_file": {"type": "file", "required": False, "description": "Optional starting model file"},
                    "smarts_filters": {"type": "string", "required": False, "description": "SMARTS filters for CustomAlerts"},
                    "protein_file": {"type": "file", "required": False, "description": "Protein structure file when docking-aware scoring is used"},
                    "binding_site": {"type": "string", "required": False, "description": "Binding site center and grid box for docking-aware scoring"},
                    "flexible_residues": {"type": "string", "required": False, "description": "Flexible receptor residues for docking-aware scoring"},
                    "max_steps": {"type": "integer", "required": False, "description": "Training steps", "default": 20},
                    "batch_size": {"type": "integer", "required": False, "description": "Batch size", "default": 64},
                    "learning_rate": {"type": "number", "required": False, "description": "Learning rate", "default": 0.0001},
                },
                "file_params": ["seed_smiles_file", "ref_smiles_file", "input_model_file", "protein_file"],
            }
        }
    },
    "PocketXMol SBDD": {
        "provider_name": "PocketXMol",
        "description": "Design small molecules from receptor-pocket context, including de novo design, fragment linking, and fragment growing.",
        "category": "Structure-Based Molecule Design",
        "interfaces": {
            "default": {
                "tool_name": "sbdd_gpu_sbdd_gpu_post",
                "description": "Run PocketXMol structure-based molecule design against a protein pocket.",
                "parameters": {
                    "task_type": {"type": "string", "required": False, "description": "Small-molecule generation task", "enum": POCKETXMOL_TASK_TYPES, "default": "sbdd"},
                    "mode": {"type": "string", "required": False, "description": "Generation mode", "enum": POCKETXMOL_MODES, "default": "autoregressive"},
                    "fragment_pose_mode": {"type": "string", "required": False, "description": "Fragment pose treatment for linking or growing", "enum": POCKETXMOL_FRAGMENT_POSE_MODES, "default": "fixed"},
                    "protein": {"type": "file", "required": True, "description": "Protein structure file"},
                    "ligand_file": {"type": "file", "required": False, "description": "Input ligand or fragment file for linking or growing"},
                    "binding_site": {"type": "string", "required": False, "description": "Binding site center and box size"},
                    "fragment_groups": {"type": "string", "required": False, "description": "Grouped fragment atom indices for linking or growing"},
                    "anchor_groups": {"type": "string", "required": False, "description": "Optional grouped anchor atom indices for linking"},
                    "use_input_pose": {"type": "boolean", "required": False, "description": "Whether to start from the uploaded fragment pose", "default": False},
                    "part1_level_min": {"type": "number", "required": False, "description": "Minimum denoising level for fragment part1", "default": 0},
                    "init_step": {"type": "number", "required": False, "description": "Initial noise level", "default": 1},
                    "num_atoms": {"type": "integer", "required": False, "description": "Target number of heavy atoms", "default": 28},
                    "num_mols": {"type": "integer", "required": False, "description": "Number of molecules to generate", "default": 10},
                    "num_steps": {"type": "integer", "required": False, "description": "Number of denoising steps", "default": 100},
                    "batch_size": {"type": "integer", "required": False, "description": "Batch size for sampling", "default": 50},
                },
                "file_params": ["protein", "ligand_file"],
            }
        }
    },
    "Get Box": {
        "provider_name": "Get Box",
        "description": "Calculate a docking box from a binding-site description and optional structure input.",
        "category": "Design Utilities",
        "interfaces": {
            "default": {
                "tool_name": "calculate_box_calculate_post",
                "description": "Calculate pocket center and box size for downstream structure-based design.",
                "parameters": {
                    "binding_site": {"type": "string", "required": True, "description": "Natural-language binding-site description"},
                    "pdb_file": {"type": "file", "required": False, "description": "Optional PDB or CIF structure file"},
                },
                "file_params": ["pdb_file"],
            }
        }
    },
    "Gnina Score Single": {
        "provider_name": "Gnina Score",
        "description": "Score generated ligands against a receptor using separate protein and ligand files.",
        "category": "Design Validation",
        "interfaces": {
            "default": {
                "tool_name": "get_gnina_score_api_single_get_gnina_score_api_single_post",
                "description": "Score one or more generated ligands with Gnina using separate receptor and ligand inputs.",
                "parameters": {
                    "protein_file": {"type": "file", "required": True, "description": "Protein structure file in PDB format"},
                    "ligand_file": {"type": "file", "required": True, "description": "Ligand structure file in SDF format"},
                },
                "file_params": ["protein_file", "ligand_file"],
            }
        }
    },
    "Gnina Score Complex": {
        "provider_name": "Gnina Score",
        "description": "Score a prepared protein-ligand complex structure with Gnina.",
        "category": "Design Validation",
        "interfaces": {
            "default": {
                "tool_name": "get_gnina_score_api_complex_get_gnina_score_api_complex_post",
                "description": "Score a pre-docked complex structure directly.",
                "parameters": {
                    "complex_file": {"type": "file", "required": True, "description": "Protein-ligand complex file"},
                },
                "file_params": ["complex_file"],
            }
        }
    },
}


KEYWORD_TOOL_MAP = {
    "reinvent4": "REINVENT4 Sampling",
    "de novo design": "REINVENT4 Sampling",
    "scaffold hopping": "REINVENT4 Sampling",
    "linker design": "REINVENT4 Sampling",
    "transfer learning": "REINVENT4 Transfer Learning",
    "reinforcement learning": "REINVENT4 Staged Learning",
    "molecule optimization": "REINVENT4 Staged Learning",
    "pocketxmol": "PocketXMol SBDD",
    "protein structure": "PocketXMol SBDD",
    "pdb id": "PocketXMol SBDD",
    "binding pocket": "PocketXMol SBDD",
    "fragment linking": "PocketXMol SBDD",
    "fragment growing": "PocketXMol SBDD",
    "get box": "Get Box",
    "binding site": "Get Box",
    "docking box": "Get Box",
    "gnina": "Gnina Score Single",
    "score molecules": "Gnina Score Single",
    "validate molecules": "Gnina Score Single",
    "complex score": "Gnina Score Complex",
}


def find_tool(query: str) -> dict:
    if not query:
        return None
    q = query.lower()

    for name in TOOLS_REGISTRY:
        if name.lower() in q:
            return get_tool_info(name)

    for keyword, tool_name in KEYWORD_TOOL_MAP.items():
        if keyword in q:
            return get_tool_info(tool_name)

    return None


def get_tool_info(tool_name: str) -> dict:
    if not tool_name:
        return None

    if tool_name in TOOLS_REGISTRY:
        tool = TOOLS_REGISTRY[tool_name]
        result = {
            "name": tool_name,
            "provider_name": tool.get("provider_name"),
            "description": tool.get("description"),
            "category": tool.get("category"),
            "interfaces": tool.get("interfaces", {}),
        }
        if result["interfaces"]:
            first_iface = list(result["interfaces"].values())[0]
            result["tool_name"] = first_iface.get("tool_name")
            result["parameters"] = first_iface.get("parameters", {})
            result["file_params"] = first_iface.get("file_params", [])
        return result

    for friendly_name, tool in TOOLS_REGISTRY.items():
        for iface in tool.get("interfaces", {}).values():
            if iface.get("tool_name") == tool_name:
                return {
                    "name": friendly_name,
                    "provider_name": tool.get("provider_name"),
                    "description": tool.get("description"),
                    "category": tool.get("category"),
                    "interfaces": tool.get("interfaces", {}),
                    "tool_name": iface.get("tool_name"),
                    "parameters": iface.get("parameters", {}),
                    "file_params": iface.get("file_params", []),
                }

    return None


def list_categories() -> list:
    return sorted({info.get("category") for info in TOOLS_REGISTRY.values() if info.get("category")})


def list_tools(category: str = None) -> list:
    if category:
        return [
            {"name": name, "category": info.get("category")}
            for name, info in TOOLS_REGISTRY.items()
            if info.get("category") and category.lower() in info.get("category", "").lower()
        ]
    return [
        {"name": name, "category": info.get("category"), "description": info.get("description")}
        for name, info in TOOLS_REGISTRY.items()
    ]
