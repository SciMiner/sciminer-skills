"""Registry for the `peptide-design` skill."""

TOOLS_REGISTRY = {
    "PocketXMol Dock": {
        "provider_name": "PocketXMol",
        "description": "Dock a small molecule or peptide into a protein binding pocket.",
        "category": "Peptide Design",
        "interfaces": {
            "default": {
                "tool_name": "dock_gpu_dock_gpu_post",
                "description": "Dock a small molecule or peptide into a protein binding pocket using PocketXMol.",
                "parameters": {
                    "noise_mode": {"type": "string", "required": False, "description": "Docking noise mode", "enum": ["gaussian", "flexible"], "default": "gaussian"},
                    "protein": {"type": "file", "required": True, "description": "Protein structure file (pdb)"},
                    "ligand_smiles": {"type": "string", "required": False, "description": "Ligand SMILES string"},
                    "ligand_file": {"type": "file", "required": False, "description": "Ligand structure file (sdf/pdb)"},
                    "peptide_sequence": {"type": "string", "required": False, "description": "Peptide sequence"},
                    "binding_site": {"type": "string", "required": True, "description": "Binding site center and box size"},
                    "num_mols": {"type": "integer", "required": False, "description": "Number of molecules to generate", "default": 10},
                    "num_steps": {"type": "integer", "required": False, "description": "Number of denoising steps", "default": 100},
                    "batch_size": {"type": "integer", "required": False, "description": "Batch size for sampling", "default": 50}
                },
                "file_params": ["protein", "ligand_file"]
            }
        }
    },
    "PocketXMol SBDD": {
        "provider_name": "PocketXMol",
        "description": "Design novel drug-like molecules for a protein binding pocket.",
        "category": "Peptide Design",
        "interfaces": {
            "default": {
                "tool_name": "sbdd_gpu_sbdd_gpu_post",
                "description": "Design drug-like molecules de novo for a protein binding pocket.",
                "parameters": {
                    "mode": {"type": "string", "required": False, "description": "Generation mode", "enum": ["autoregressive", "one_shot"], "default": "autoregressive"},
                    "protein": {"type": "file", "required": True, "description": "Protein structure file (pdb)"},
                    "binding_site": {"type": "string", "required": True, "description": "Binding site center and box size"},
                    "num_atoms": {"type": "integer", "required": False, "description": "Target number of heavy atoms", "default": 28},
                    "num_mols": {"type": "integer", "required": False, "description": "Number of molecules to generate", "default": 10},
                    "num_steps": {"type": "integer", "required": False, "description": "Number of denoising steps", "default": 100},
                    "batch_size": {"type": "integer", "required": False, "description": "Batch size for sampling", "default": 50}
                },
                "file_params": ["protein"]
            }
        }
    },
    "PocketXMol Peptide Design": {
        "provider_name": "PocketXMol",
        "description": "Design peptides for a protein binding pocket.",
        "category": "Peptide Design",
        "interfaces": {
            "default": {
                "tool_name": "pepdesign_gpu_pepdesign_gpu_post",
                "description": "Design peptides with de novo, inverse folding, or side-chain packing modes.",
                "parameters": {
                    "mode": {"type": "string", "required": False, "description": "Peptide design mode", "enum": ["denovo", "inverse_folding", "sc_packing"], "default": "denovo"},
                    "protein": {"type": "file", "required": True, "description": "Protein structure file (pdb)"},
                    "binding_site": {"type": "string", "required": False, "description": "Binding site center and box size"},
                    "peptide_length": {"type": "integer", "required": False, "description": "Target peptide length for de novo mode", "default": 10},
                    "peptide_file": {"type": "file", "required": False, "description": "Input peptide structure file for inverse folding or side-chain packing"},
                    "num_mols": {"type": "integer", "required": False, "description": "Number of peptides to generate", "default": 10},
                    "num_steps": {"type": "integer", "required": False, "description": "Number of denoising steps", "default": 100},
                    "batch_size": {"type": "integer", "required": False, "description": "Batch size for sampling", "default": 50}
                },
                "file_params": ["protein", "peptide_file"]
            }
        }
    },
    "RFpeptides": {
        "provider_name": "RFpeptides",
        "description": "Use RFdiffusion to design macrocyclic peptides binding target proteins.",
        "category": "Peptide Design",
        "interfaces": {
            "default": {
                "tool_name": "get_peptide_design_get_peptide_design_post",
                "description": "Design macrocyclic peptides that bind target proteins.",
                "parameters": {
                    "design_cyclic_peptide": {"type": "string", "required": True, "description": "Whether to design cyclic peptide", "enum": ["True", "False"], "default": "True"},
                    "input_pdb": {"type": "file", "required": False, "description": "Input PDB file"},
                    "target_chains": {"type": "string", "required": False, "description": "Target protein chain IDs"},
                    "hotspot_res": {"type": "string", "required": False, "description": "Hotspot residues on target protein"},
                    "piptide_length": {"type": "string", "required": True, "description": "Length range of designed peptide"},
                    "num_designs": {"type": "integer", "required": True, "description": "Number of designs to generate", "default": 10}
                },
                "file_params": ["input_pdb"]
            }
        }
    },
    "Peptide Molecular Descriptors": {
        "provider_name": "Peptide Molecular Descriptors",
        "description": "Calculate molecular descriptors for SMILES or FASTA sequences.",
        "category": "Peptide Analysis",
        "interfaces": {
            "default": {
                "tool_name": "post_mol_description_mol_description_get",
                "description": "Calculate molecular descriptors.",
                "parameters": {
                    "input_str": {"type": "string", "required": True, "description": "Multi-line SMILES or FASTA input"}
                },
                "file_params": []
            }
        }
    },
    "Peptide Extinction Coefficient": {
        "provider_name": "Peptide Extinction Coefficient",
        "description": "Calculate protein/peptide extinction coefficients.",
        "category": "Peptide Analysis",
        "interfaces": {
            "default": {
                "tool_name": "get_extract_extinction_coefficient_str",
                "description": "Calculate extinction coefficients from FASTA strings.",
                "parameters": {
                    "input_str": {"type": "string", "required": True, "description": "Multi-line FASTA sequence string"}
                },
                "file_params": []
            }
        }
    },
    "Peptide pIChemiSt String": {
        "provider_name": "Peptide pIChemiSt",
        "description": "Calculate isoelectric point (pI) from FASTA or SMILES strings.",
        "category": "Peptide Analysis",
        "interfaces": {
            "default": {
                "tool_name": "post_pichemist_str_pichemist_str_post",
                "description": "Calculate pI from multi-line string input.",
                "parameters": {
                    "input_str": {"type": "string", "required": True, "description": "Multi-line FASTA or SMILES input"}
                },
                "file_params": []
            }
        }
    },
    "Peptide pIChemiSt File": {
        "provider_name": "Peptide pIChemiSt",
        "description": "Calculate isoelectric point (pI) from uploaded molecule files.",
        "category": "Peptide Analysis",
        "interfaces": {
            "default": {
                "tool_name": "post_pichemist_file_pichemist_file_post",
                "description": "Calculate pI from uploaded .smi or .sdf files.",
                "parameters": {
                    "input_file": {"type": "file", "required": True, "description": "Input file in SMILES or SDF format"}
                },
                "file_params": ["input_file"]
            }
        }
    },
    "Peptide Liabilities": {
        "provider_name": "Peptide Liabilities",
        "description": "Detect peptide or molecule liabilities affecting metabolism and toxicity.",
        "category": "Peptide Analysis",
        "interfaces": {
            "default": {
                "tool_name": "post_mol_liabilities_mol_liabilities_post",
                "description": "Detect liabilities from multi-line SMILES input.",
                "parameters": {
                    "input_str": {"type": "string", "required": True, "description": "Multi-line SMILES string"}
                },
                "file_params": []
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "pocketxmol": "PocketXMol Peptide Design",
    "dock peptide": "PocketXMol Dock",
    "peptide docking": "PocketXMol Dock",
    "sbdd": "PocketXMol SBDD",
    "peptide design": "PocketXMol Peptide Design",
    "inverse folding": "PocketXMol Peptide Design",
    "side-chain packing": "PocketXMol Peptide Design",
    "rfpeptides": "RFpeptides",
    "macrocyclic peptide": "RFpeptides",
    "descriptors": "Peptide Molecular Descriptors",
    "extinction coefficient": "Peptide Extinction Coefficient",
    "pichemist": "Peptide pIChemiSt String",
    "isoelectric point": "Peptide pIChemiSt String",
    "liabilities": "Peptide Liabilities",
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
