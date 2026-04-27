"""Registry for the `binding-site-prediction` skill."""

TOOLS_REGISTRY = {
    "P2Rank Binding Site Prediction": {
        "provider_name": "p2rank",
        "description": "Predict ligand-binding pockets from an uploaded protein structure using a machine-learning pocket detector.",
        "category": "Pocket Detection",
        "interfaces": {
            "default": {
                "tool_name": "run_p2rank_run_p2rank_post",
                "description": "Run P2Rank on an uploaded protein structure.",
                "parameters": {
                    "protein_file": {"type": "file", "required": True, "description": "Protein structure file"}
                },
                "file_params": ["protein_file"]
            }
        }
    },
    "AF2BIND Binding Probability": {
        "provider_name": "af2bind",
        "description": "Predict per-residue small-molecule binding probability from a structure file or structure identifier.",
        "category": "Residue-level Scoring",
        "interfaces": {
            "default": {
                "tool_name": "predict_gpu_predict_gpu_post",
                "description": "Run AF2BIND on an uploaded protein structure or a PDB/UniProt identifier.",
                "parameters": {
                    "protein": {"type": "file", "required": False, "description": "Protein structure file in PDB or mmCIF format"},
                    "target_pdb": {"type": "string", "required": False, "description": "PDB code or UniProt ID"},
                    "target_chain": {"type": "string", "required": False, "description": "Target protein chain identifier", "default": "A"},
                    "mask_sidechains": {"type": "boolean", "required": False, "description": "Mask sidechains during inference", "default": True},
                    "mask_sequence": {"type": "boolean", "required": False, "description": "Mask sequence during inference", "default": False}
                },
                "file_params": ["protein"]
            }
        }
    },
    "fpocket Pocket Detection": {
        "provider_name": "fpocket",
        "description": "Detect geometric pockets and inspect size-sensitive pocket candidates from an uploaded receptor structure.",
        "category": "Pocket Detection",
        "interfaces": {
            "default": {
                "tool_name": "run_fpocket_run_fpocket_post",
                "description": "Run fpocket on an uploaded protein structure.",
                "parameters": {
                    "protein_file": {"type": "file", "required": True, "description": "Protein structure file"},
                    "ligand_chain": {"type": "string", "required": False, "description": "Ligand chain identifier in the structure"},
                    "pocket_min_size": {"type": "number", "required": False, "description": "Minimum detectable pocket size", "default": 3.4},
                    "pocket_max_size": {"type": "number", "required": False, "description": "Maximum detectable pocket size", "default": 6.2}
                },
                "file_params": ["protein_file"]
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "p2rank": "P2Rank Binding Site Prediction",
    "machine learning pocket": "P2Rank Binding Site Prediction",
    "binding pocket": "P2Rank Binding Site Prediction",
    "af2bind": "AF2BIND Binding Probability",
    "binding probability": "AF2BIND Binding Probability",
    "per-residue": "AF2BIND Binding Probability",
    "pdb id": "AF2BIND Binding Probability",
    "uniprot": "AF2BIND Binding Probability",
    "fpocket": "fpocket Pocket Detection",
    "geometric pocket": "fpocket Pocket Detection",
    "pocket descriptor": "fpocket Pocket Detection"
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
                    "file_params": iface.get("file_params", [])
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