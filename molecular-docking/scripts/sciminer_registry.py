"""Registry for the `molecular-docking` skill."""

COMPARISON_KEYWORDS = [
    "compare",
    "comparison",
    "benchmark",
    "versus",
    "vs",
    "multi-engine",
    "multiple engines",
]

TOOLS_REGISTRY = {
    "Gnina": {
        "provider_name": "Gnina",
        "description": "Default docking engine for pocket-guided protein-ligand docking.",
        "category": "Molecular Docking",
        "interfaces": {
            "default": {
                "tool_name": "get_gnina_result_from_pocket_center_picker_get_gnina_result_from_pocket_center_picker_post",
                "description": "Run Gnina docking with optional reference ligand and pocket information.",
                "parameters": {
                    "receptor": {"type": "file", "required": True, "description": "Receptor structure file (pdb/cif)"},
                    "ligand_to_dock": {"type": "file", "required": True, "description": "Ligand file to dock (sdf/pdb/smi/txt)"},
                    "reference_ligand": {"type": "file", "required": False, "description": "Reference ligand file for pocket guidance (sdf)"},
                    "pocket_info": {"type": "string", "required": False, "description": "Pocket details from pocket-center-picker"},
                    "num_modes": {"type": "integer", "required": True, "description": "Number of docking modes to generate"},
                },
                "file_params": ["receptor", "ligand_to_dock", "reference_ligand"],
            }
        },
    },
    "AutoDock Vina": {
        "provider_name": "AutoDock Vina",
        "description": "Classical and fast open-source docking with explicit mode controls.",
        "category": "Molecular Docking",
        "interfaces": {
            "default": {
                "tool_name": "vina_docking_from_pocket_center_picker_vina_docking_from_pocket_center_picker_post",
                "description": "Run AutoDock Vina docking from pocket center information.",
                "parameters": {
                    "receptor": {"type": "file", "required": True, "description": "Receptor file (pdb/pdbqt)"},
                    "ligand_to_dock": {"type": "file", "required": True, "description": "Ligand file (pdb/pdbqt/sdf)"},
                    "reference_ligand": {"type": "file", "required": False, "description": "Reference ligand to define pocket center (sdf/pdb)"},
                    "pocket_info": {"type": "string", "required": False, "description": "Pocket information from pocket-center-picker"},
                    "num_modes": {"type": "integer", "required": True, "description": "Number of binding modes to generate"},
                },
                "file_params": ["receptor", "ligand_to_dock", "reference_ligand"],
            }
        },
    },
    "PackDock": {
        "provider_name": "PackDock",
        "description": "Flexible docking with apo/holo conformer optimization and Vina sampling.",
        "category": "Molecular Docking",
        "interfaces": {
            "default": {
                "tool_name": "dock_from_pocket_center_picker_dock_from_pocket_center_picker_post",
                "description": "Run flexible PackDock docking from protein, ligand, and optional pocket-center inputs.",
                "parameters": {
                    "receptor": {"type": "file", "required": True, "description": "Complete protein file (pdb/cif)"},
                    "ligand_to_dock": {"type": "file", "required": True, "description": "Ligand file to dock (sdf/mol2/pdb)"},
                    "reference_ligand": {"type": "file", "required": False, "description": "Reference ligand file (sdf/pdb)"},
                    "pocket_info": {"type": "string", "required": False, "description": "Pocket information from pocket-center-picker"},
                    "num_apo_conformers": {"type": "integer", "required": False, "description": "Number of apo conformers", "default": 1},
                    "num_holo_conformers": {"type": "integer", "required": False, "description": "Number of holo conformers", "default": 5},
                    "vina_sample": {"type": "integer", "required": False, "description": "Number of Vina poses kept", "default": 9},
                },
                "file_params": ["receptor", "ligand_to_dock", "reference_ligand"],
            }
        },
    },
    "SurfDock": {
        "provider_name": "SurfDock",
        "description": "AI-driven docking that integrates protein sequence, residue structure, and surface geometry.",
        "category": "Molecular Docking",
        "interfaces": {
            "default": {
                "tool_name": "run_surfdock_process_from_pocket_center_picker_run_surfdock_process_from_pocket_center_picker_post",
                "description": "Run SurfDock with optional pocket guidance and sampling control.",
                "parameters": {
                    "protein": {"type": "file", "required": True, "description": "Protein file (pdb)"},
                    "ligand_to_dock": {"type": "file", "required": True, "description": "Ligand file (sdf/mol2/csv/txt/smi)"},
                    "reference_ligand": {"type": "file", "required": False, "description": "Reference ligand file (sdf)"},
                    "pocket_info": {"type": "string", "required": False, "description": "Pocket information from pocket-center-picker"},
                    "samples_per_complex": {"type": "integer", "required": False, "description": "Samples per complex", "default": 10},
                },
                "file_params": ["protein", "ligand_to_dock", "reference_ligand"],
            }
        },
    },
    "DiffDock": {
        "provider_name": "DiffDock",
        "description": "Diffusion-model docking for protein-ligand complex pose prediction.",
        "category": "Molecular Docking",
        "interfaces": {
            "default": {
                "tool_name": "diffdock_get_diffdock_info_post",
                "description": "Run DiffDock to predict 3D complex poses.",
                "parameters": {
                    "protein_file": {"type": "file", "required": True, "description": "Protein file (pdb/fasta/txt)"},
                    "ligand_file": {"type": "file", "required": True, "description": "Ligand file (sdf/mol2/txt/smi)"},
                    "samples_per_complex": {"type": "integer", "required": False, "description": "Samples per complex", "default": 10},
                },
                "file_params": ["protein_file", "ligand_file"],
            }
        },
    },
    "Get Box": {
        "provider_name": "Get Box",
        "description": "Obtain native ligand binding-site box parameters from natural-language site descriptions and optional structures.",
        "category": "Binding Site Utilities",
        "interfaces": {
            "default": {
                "tool_name": "calculate_box_calculate_post",
                "description": "Calculate docking box center and size for a native ligand binding site.",
                "parameters": {
                    "binding_site": {"type": "string", "required": True, "description": "Natural-language binding-site description; can include PDB ID"},
                    "pdb_file": {"type": "file", "required": False, "description": "Optional protein structure file (pdb/cif)"},
                },
                "file_params": ["pdb_file"],
            }
        },
    },
    "fpocket": {
        "provider_name": "fpocket",
        "description": "Predict binding pockets from protein structures when native pocket annotations are unavailable.",
        "category": "Binding Site Utilities",
        "interfaces": {
            "default": {
                "tool_name": "run_fpocket_run_fpocket_post",
                "description": "Run fpocket to detect and score predicted pockets.",
                "parameters": {
                    "protein_file": {"type": "file", "required": True, "description": "Protein structure file for pocket detection"},
                    "ligand_chain": {"type": "string", "required": False, "description": "Optional ligand chain ID"},
                    "pocket_min_size": {"type": "number", "required": False, "description": "Minimum detectable pocket size", "default": 3.4},
                    "pocket_max_size": {"type": "number", "required": False, "description": "Maximum detectable pocket size", "default": 6.2},
                },
                "file_params": ["protein_file"],
            }
        },
    },
}


KEYWORD_TOOL_MAP = {
    "docking": "Gnina",
    "dock": "Gnina",
    "pocket docking": "Gnina",
    "default docking": "Gnina",
    "gnina": "Gnina",
    "vina": "AutoDock Vina",
    "autodock": "AutoDock Vina",
    "autodock vina": "AutoDock Vina",
    "packdock": "PackDock",
    "flexible docking": "PackDock",
    "flex docking": "PackDock",
    "surfdock": "SurfDock",
    "diffdock": "DiffDock",
    "get box": "Get Box",
    "native ligand binding site": "Get Box",
    "native binding site": "Get Box",
    "fpocket": "fpocket",
    "predicted binding site": "fpocket",
    "pocket prediction": "fpocket",
}


def is_comparison_request(query: str) -> bool:
    if not query:
        return False
    q = query.lower()
    return any(keyword in q for keyword in COMPARISON_KEYWORDS)


def select_tools_for_query(query: str) -> list:
    if not query:
        return ["Gnina"]

    q = query.lower()

    if is_comparison_request(q):
        return ["Gnina", "AutoDock Vina", "PackDock", "SurfDock", "DiffDock"]

    selected = []
    for tool_name in TOOLS_REGISTRY:
        if tool_name.lower() in q:
            selected.append(tool_name)

    for kw, tool_name in KEYWORD_TOOL_MAP.items():
        if kw in q and tool_name not in selected:
            selected.append(tool_name)

    return selected or ["Gnina"]


def find_tool(query: str) -> dict:
    selected = select_tools_for_query(query)
    if not selected:
        return None
    return get_tool_info(selected[0])


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
