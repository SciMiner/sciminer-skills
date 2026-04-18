"""Registry for the `virtual-screening` skill."""

LIBRARY_OPTIONS = [
    "Covalent Library",
    "Drug-like Library",
    "Fragment Library",
    "Macrocycle Library",
    "Molecular Glue Library",
    "Natural Product Library",
    "Peptidomimetic Library",
    "PROTAC Library",
]

FILTER_RULE_OPTIONS = ["PAINS", "Ro5", "Ro3"]

INTERACTION_TYPE_OPTIONS = [
    "None",
    "Hydrophobic",
    "HydrogenBond",
    "WeakHydrogenBond",
    "IonicInteraction",
    "PiStacking",
    "Cation-PiInteractions",
    "HalogenBond",
    "MetalCoordination",
]


TOOLS_REGISTRY = {
    "Transformer Virtual Screen": {
        "provider_name": "Transformer-Based Proprietary Library Virtual Screen",
        "description": "Fast proprietary library screening from protein sequence with transformer scoring, clustering, and downstream structure analysis.",
        "category": "Virtual Screening",
        "interfaces": {
            "default": {
                "tool_name": "virtual_screening_virtual-screening-commercial-library-category_post",
                "description": "Screen a proprietary library from protein sequence with filtering, clustering, and Boltz2 follow-up.",
                "parameters": {
                    "library": {"type": "string", "required": False, "description": "Library name", "enum": LIBRARY_OPTIONS},
                    "filter_rules": {"type": "array", "required": False, "description": "Filter rules", "enum": FILTER_RULE_OPTIONS},
                    "Interaction_type": {"type": "string", "required": False, "description": "Interaction type", "enum": INTERACTION_TYPE_OPTIONS},
                    "custom_file": {"type": "file", "required": False, "description": "Custom candidate molecule file"},
                    "protein_sequence": {"type": "string", "required": True, "description": "Protein sequence"},
                    "tCPI_topK": {"type": "integer", "required": True, "description": "Top-K compounds to keep"},
                    "tCPI_num_clusters": {"type": "integer", "required": True, "description": "Number of clusters"},
                    "Boltz2_samples": {"type": "integer", "required": True, "description": "Boltz2 samples"},
                    "Interaction_residue": {"type": "string", "required": False, "description": "Interaction residue constraint"},
                },
                "file_params": ["custom_file"],
            }
        }
    },
    "Docking Virtual Screen": {
        "provider_name": "Docking-Based Proprietary Library Virtual Screen",
        "description": "Docking-based proprietary library screening with receptor structure, docking box, and interaction filtering.",
        "category": "Virtual Screening",
        "interfaces": {
            "default": {
                "tool_name": "virtual_screening_smart_dock-commercial-library-category_post",
                "description": "Screen a proprietary library with explicit docking and interaction analysis.",
                "parameters": {
                    "library": {"type": "string", "required": False, "description": "Library name", "enum": LIBRARY_OPTIONS},
                    "filter_rules": {"type": "array", "required": False, "description": "Filter rules", "enum": FILTER_RULE_OPTIONS},
                    "Interaction_type": {"type": "string", "required": False, "description": "Interaction type", "enum": INTERACTION_TYPE_OPTIONS},
                    "receptor_file": {"type": "file", "required": True, "description": "Receptor structure file"},
                    "reference_ligand": {"type": "file", "required": False, "description": "Reference ligand file"},
                    "custom_file": {"type": "file", "required": False, "description": "Custom candidate molecule file"},
                    "docking_box": {"type": "string", "required": False, "description": "Docking box coordinates or descriptor"},
                    "num_modes": {"type": "integer", "required": True, "description": "Number of docking modes"},
                    "Interaction_residue": {"type": "string", "required": False, "description": "Specific interaction residue constraint"},
                },
                "file_params": ["receptor_file", "reference_ligand", "custom_file"],
            }
        }
    },
    "Get Box": {
        "provider_name": "Get Box",
        "description": "Calculate docking box center and size from a binding-site description and optional structure file.",
        "category": "Virtual Screening Utilities",
        "interfaces": {
            "default": {
                "tool_name": "calculate_box_calculate_post",
                "description": "Calculate docking box parameters.",
                "parameters": {
                    "binding_site": {"type": "string", "required": True, "description": "Natural-language binding-site description"},
                    "pdb_file": {"type": "file", "required": False, "description": "Optional PDB or CIF file"},
                },
                "file_params": ["pdb_file"],
            }
        }
    },
    "Get Protein Sequence": {
        "provider_name": "Get Protein Sequence",
        "description": "Retrieve a reviewed protein accession and sequence from UniProt by query.",
        "category": "Virtual Screening Utilities",
        "interfaces": {
            "default": {
                "tool_name": "uniprotkb_search_get",
                "description": "Search UniProtKB for a protein sequence.",
                "parameters": {
                    "query": {"type": "string", "required": True, "description": "UniProt query string"},
                    "fields": {"type": "string", "required": False, "description": "Fields to return", "default": "accession,sequence"},
                    "format": {"type": "string", "required": False, "description": "Response format", "enum": ["json", "fasta", "tsv"], "default": "json"},
                    "size": {"type": "integer", "required": False, "description": "Number of results to return", "default": 1},
                },
                "file_params": [],
            }
        }
    },
}


KEYWORD_TOOL_MAP = {
    "virtual screening": "Transformer Virtual Screen",
    "transformer screen": "Transformer Virtual Screen",
    "tcpi": "Transformer Virtual Screen",
    "boltz2": "Transformer Virtual Screen",
    "docking screen": "Docking Virtual Screen",
    "gnina": "Docking Virtual Screen",
    "plip": "Docking Virtual Screen",
    "docking box": "Get Box",
    "box center": "Get Box",
    "protein sequence": "Get Protein Sequence",
    "uniprot": "Get Protein Sequence",
}


def find_tool(query: str) -> dict:
    if not query:
        return None
    q = query.lower()

    for name in TOOLS_REGISTRY:
        if name.lower() in q:
            return get_tool_info(name)

    for kw, tool_name in KEYWORD_TOOL_MAP.items():
        if kw in q:
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
