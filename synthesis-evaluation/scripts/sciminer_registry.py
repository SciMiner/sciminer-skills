"""Registry for the `synthesis-evaluation` skill."""

TOOLS_REGISTRY = {
    "SynFormer-ED": {
        "provider_name": "SynFormer",
        "description": "Generate synthesizable analogs from target molecules with SynFormer-ED.",
        "category": "Synthesizable Molecule Generation",
        "interfaces": {
            "default": {
                "tool_name": "synformer_ed_synformer_ed_post",
                "description": "Generate synthesizable analogs from SMILES strings or uploaded molecule files.",
                "parameters": {
                    "smiles": {"type": "string", "required": False, "description": "Input molecule SMILES string(s), one per line"},
                    "input_file": {"type": "file", "required": False, "description": "Input molecule file in CSV, SDF, SMI, or TXT format"}
                },
                "file_params": ["input_file"]
            }
        }
    },
    "Retrosynthesis Planner": {
        "provider_name": "Retrosynthesis Planner",
        "description": "Generate retrosynthetic route recommendations from target molecule SMILES strings.",
        "category": "Retrosynthesis Planning",
        "interfaces": {
            "default": {
                "tool_name": "get_syntheseus_info_get_syntheseus_info_post",
                "description": "Generate retrosynthetic route recommendations for one or more target molecules.",
                "parameters": {
                    "smiles_list": {"type": "string", "required": True, "description": "One or more target SMILES strings separated by line breaks"},
                    "num_routes": {"type": "integer", "required": False, "description": "Number of retrosynthetic routes to design for each molecule", "default": 2}
                },
                "file_params": []
            }
        }
    },
    "SAScore from SMILES": {
        "provider_name": "SAScore",
        "description": "Calculate synthetic accessibility scores directly from SMILES strings.",
        "category": "Synthesizability Evaluation",
        "interfaces": {
            "default": {
                "tool_name": "calculatesascore_calculate_sascore_get",
                "description": "Calculate SAScore for one or more SMILES strings.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings"}
                },
                "file_params": []
            }
        }
    },
    "SAScore from File": {
        "provider_name": "SAScore",
        "description": "Calculate synthetic accessibility scores in batch from uploaded files.",
        "category": "Synthesizability Evaluation",
        "interfaces": {
            "default": {
                "tool_name": "calculate_file_calculate_file_post",
                "description": "Calculate SAScore for molecules provided in an uploaded file.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "Input molecule file in SDF or TXT format"}
                },
                "file_params": ["file"]
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "synformer": "SynFormer-ED",
    "synformer-ed": "SynFormer-ED",
    "synthesizable analog": "SynFormer-ED",
    "retrosynthesis": "Retrosynthesis Planner",
    "route planning": "Retrosynthesis Planner",
    "synthesis route": "Retrosynthesis Planner",
    "sascore": "SAScore from SMILES",
    "synthetic accessibility": "SAScore from SMILES",
    "synthesizability": "SAScore from SMILES",
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