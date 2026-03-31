"""
BoltzGen tools registry for the `protein-design` skill.

Registers Boltzgen design endpoints and parameter definitions so the
shared invocation helper can prepare payloads and upload files.
"""

TOOLS_REGISTRY = {
    "Boltzgen Protein-Anything": {
        "provider_name": "Boltzgen",
        "description": "Design proteins to bind protein/peptide targets",
        "category": "Protein Design",
        "interfaces": {
            "default": {
                "tool_name": "design_protein_anything_design_protein_anything_post",
                "description": "Design Protein Anything -- for designing proteins to bind protein/peptide targets",
                "parameters": {
                    "target_file": {"type": "file", "required": True, "description": "Upload PDB/CIF target file"},
                    "target_chains": {"type": "string", "required": True, "description": "Target chains (e.g., 'A,B')"},
                    "binding_site": {"type": "string", "required": False, "description": "Binding site (e.g., A: 13-14, 56)"},
                    "design_length": {"type": "string", "required": True, "description": "Design length (e.g., '80-140' or '15')"},
                    "bonds_info": {"type": "string", "required": False, "description": "Covalent bonds info"},
                    "secondary_structure": {"type": "string", "required": False, "description": "Secondary structure specification"},
                    "inverse_fold_avoid": {"type": "string", "required": False, "description": "Disallowed residues (e.g., 'KEC')"},
                    "num_designs": {"type": "integer", "required": False, "description": "Number of designs to generate", "default": 5},
                    "budget": {"type": "integer", "required": False, "description": "Final number of designs after filtering", "default": 1}
                },
                "file_params": ["target_file"]
            }
        }
    },

    "Boltzgen Peptide-Anything": {
        "provider_name": "Boltzgen",
        "description": "Design peptides to bind protein targets",
        "category": "Protein Design",
        "interfaces": {
            "default": {
                "tool_name": "design_peptide_anything_design_peptide_anything_post",
                "description": "Design Peptide Anything -- for designing peptides to bind protein targets",
                "parameters": {
                    "target_file": {"type": "file", "required": True, "description": "Upload PDB/CIF target file"},
                    "target_chains": {"type": "string", "required": True, "description": "Target chains (e.g., 'A,B')"},
                    "binding_site": {"type": "string", "required": False, "description": "Binding site (e.g., A: 13-14, 56)"},
                    "design_length": {"type": "string", "required": True, "description": "Design length (e.g., '80-140' or '15')"},
                    "cyclic": {"type": "boolean", "required": False, "description": "Whether the peptide should be cyclic", "default": True},
                    "bonds_info": {"type": "string", "required": False, "description": "Covalent bonds info"},
                    "secondary_structure": {"type": "string", "required": False, "description": "Secondary structure specification"},
                    "inverse_fold_avoid": {"type": "string", "required": False, "description": "Disallowed residues (e.g., 'KEC')"},
                    "num_designs": {"type": "integer", "required": False, "description": "Number of designs to generate", "default": 5},
                    "budget": {"type": "integer", "required": False, "description": "Final number of designs after filtering", "default": 1}
                },
                "file_params": ["target_file"]
            }
        }
    },

    "Boltzgen Protein-Small-Molecule": {
        "provider_name": "Boltzgen",
        "description": "Design proteins to bind small molecules",
        "category": "Protein Design",
        "interfaces": {
            "default": {
                "tool_name": "design_protein_small_molecule_design_protein_small_molecule_post",
                "description": "Design Protein Small Molecule -- for designing proteins to bind small molecules",
                "parameters": {
                    "smiles": {"type": "string", "required": False, "description": "SMILES string for the small molecule"},
                    "ccd": {"type": "string", "required": False, "description": "CCD code"},
                    "design_length": {"type": "string", "required": True, "description": "Design length (e.g., '80-140' or '15')"},
                    "inverse_fold_avoid": {"type": "string", "required": False, "description": "Disallowed residues (e.g., 'KEC')"},
                    "num_designs": {"type": "integer", "required": False, "description": "Number of designs to generate", "default": 5},
                    "budget": {"type": "integer", "required": False, "description": "Final number of designs after filtering", "default": 1}
                },
                "file_params": []
            }
        }
    },

    "Boltzgen Antibody-Anything": {
        "provider_name": "Boltzgen",
        "description": "Design antibodies to bind an antigen",
        "category": "Protein Design",
        "interfaces": {
            "default": {
                "tool_name": "design_antibody_anything_design_antibody_anything_post",
                "description": "Design Antibody Anything -- antibody design",
                "parameters": {
                    "Framework_file": {"type": "file", "required": False, "description": "Antibody framework file (cif/pdb)"},
                    "Target_file": {"type": "file", "required": True, "description": "Antigen pdb to target"},
                    "target_chains": {"type": "string", "required": True, "description": "Target antigen chains"},
                    "heavy_chain_CDR_Regions": {"type": "string", "required": False, "description": "Select heavy CDR regions from Framework_file"},
                    "heavy_chain_insertion_length_range": {"type": "string", "required": False, "description": "Comma-separated ranges for new residues per heavy CDR"},
                    "light_chain_CDR_Regions": {"type": "string", "required": False, "description": "Select light CDR regions from Framework_file"},
                    "light_chain_insertion_length_range": {"type": "string", "required": False, "description": "Comma-separated ranges for new residues per light CDR"},
                    "inverse_fold_avoid": {"type": "string", "required": False, "description": "Disallowed residues (e.g., 'KEC')"},
                    "num_designs": {"type": "integer", "required": False, "description": "Number of designs to generate", "default": 5},
                    "budget": {"type": "integer", "required": False, "description": "Final number of designs after filtering", "default": 1}
                },
                "file_params": ["Framework_file", "Target_file"]
            }
        }
    },

    "Boltzgen Nanobody-Anything": {
        "provider_name": "Boltzgen",
        "description": "Design nanobodies to bind an antigen",
        "category": "Protein Design",
        "interfaces": {
            "default": {
                "tool_name": "design_nanobody_anything_design_nanobody_anything_post",
                "description": "Design Nanobody Anything -- nanobody design",
                "parameters": {
                    "Framework_file": {"type": "file", "required": False, "description": "Antibody framework file (cif/pdb)"},
                    "Target_file": {"type": "file", "required": True, "description": "Antigen pdb to target"},
                    "target_chains": {"type": "string", "required": True, "description": "Target antigen chains"},
                    "heavy_chain_CDR_Regions": {"type": "string", "required": False, "description": "Select heavy CDR regions from Framework_file"},
                    "heavy_chain_insertion_length_range": {"type": "string", "required": False, "description": "Comma-separated ranges for new residues per heavy CDR"},
                    "heavy_chain_anchor_regions": {"type": "string", "required": False, "description": "Comma-separated residue index ranges to retain as anchors"},
                    "inverse_fold_avoid": {"type": "string", "required": False, "description": "Disallowed residues (e.g., 'KEC')"},
                    "num_designs": {"type": "integer", "required": False, "description": "Number of designs to generate", "default": 5},
                    "budget": {"type": "integer", "required": False, "description": "Final number of designs after filtering", "default": 1}
                },
                "file_params": ["Framework_file", "Target_file"]
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "boltzgen": "Boltzgen Protein-Anything",
    "protein design": "Boltzgen Protein-Anything",
    "peptide design": "Boltzgen Peptide-Anything",
    "small molecule": "Boltzgen Protein-Small-Molecule",
    "protein-small": "Boltzgen Protein-Small-Molecule",
    "antibody": "Boltzgen Antibody-Anything",
    "nanobody": "Boltzgen Nanobody-Anything",
}


def find_tool(query: str) -> dict:
    """Find a tool by friendly name or keywords."""
    if not query:
        return None
    q = query.lower()

    # exact friendly name match
    for name in TOOLS_REGISTRY:
        if name.lower() in q:
            return get_tool_info(name)

    # keyword match
    for kw, tool_name in KEYWORD_TOOL_MAP.items():
        if kw in q:
            return get_tool_info(tool_name)

    return None


def get_tool_info(tool_name: str) -> dict:
    """Return tool info by friendly name or internal interface name."""
    if not tool_name:
        return None

    # friendly name
    if tool_name in TOOLS_REGISTRY:
        tool = TOOLS_REGISTRY[tool_name]
        result = {
            "name": tool_name,
            "provider_name": tool.get("provider_name"),
            "description": tool.get("description"),
            "category": tool.get("category"),
            "interfaces": tool.get("interfaces", {})
        }
        if result["interfaces"]:
            first_iface = list(result["interfaces"].values())[0]
            result["tool_name"] = first_iface.get("tool_name")
            result["parameters"] = first_iface.get("parameters", {})
            result["file_params"] = first_iface.get("file_params", [])
        return result

    # internal interface name search
    for friendly_name, tool in TOOLS_REGISTRY.items():
        for iface in tool.get("interfaces", {}).values():
            if iface.get("tool_name") == tool_name:
                result = {
                    "name": friendly_name,
                    "provider_name": tool.get("provider_name"),
                    "description": tool.get("description"),
                    "category": tool.get("category"),
                    "interfaces": tool.get("interfaces", {})
                }
                result["tool_name"] = tool_name
                result["parameters"] = iface.get("parameters", {})
                result["file_params"] = iface.get("file_params", [])
                return result

    return None


def list_categories() -> list:
    cats = set()
    for info in TOOLS_REGISTRY.values():
        c = info.get("category")
        if c:
            cats.add(c)
    return sorted(cats)


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
