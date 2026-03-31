"""Registry for the `structure-prediction` skill."""

TOOLS_REGISTRY = {
    "Chai-1": {
        "provider_name": "Chai-1",
        "description": "Multimodal foundation model for biomolecular structure prediction across proteins, ligands, DNA, RNA, glycans, and more.",
        "category": "Structure Prediction",
        "interfaces": {
            "default": {
                "tool_name": "get_chai_info_from_params_api_get_chai_info_from_params_api_post",
                "description": "Run Chai-1 structure prediction from sequence, ligand, restraint, and optional MSA/template inputs.",
                "parameters": {
                    "MSA_method": {"type": "string", "required": True, "description": "Protein MSA method", "enum": ["Search MSA", "Upload File", "No MSA"], "default": "No MSA"},
                    "Template_method": {"type": "string", "required": True, "description": "Protein template method", "enum": ["Default Search Template", "No Template"], "default": "No Template"},
                    "MSA_file": {"type": "file", "required": False, "description": "MSA file", "suffix": ["A3M", "pqt"]},
                    "protein": {"type": "array", "required": False, "description": "Protein sequences"},
                    "dna": {"type": "array", "required": False, "description": "DNA sequences"},
                    "rna": {"type": "array", "required": False, "description": "RNA sequences"},
                    "ligand_smiles": {"type": "array", "required": False, "description": "Ligand SMILES strings"},
                    "glycan": {"type": "array", "required": False, "description": "Glycan inputs"},
                    "covalent_bonds": {"type": "array", "required": False, "description": "Covalent bond definitions"},
                    "contact_restraints": {"type": "array", "required": False, "description": "Contact restraints"},
                    "pocket_restraints": {"type": "array", "required": False, "description": "Pocket restraints"},
                    "num_diffn_samples": {"type": "integer", "required": True, "description": "Number of diffusion samples", "default": 5}
                },
                "file_params": ["MSA_file"]
            }
        }
    },
    "Boltz-2": {
        "provider_name": "Boltz-2",
        "description": "Next-generation biomolecular foundation model for complex structure prediction and binding affinity modeling.",
        "category": "Structure Prediction",
        "interfaces": {
            "default": {
                "tool_name": "get_boltz_info_from_params2_get_boltz_info_from_params2_post",
                "description": "Run Boltz-2 structure prediction with optional MSA, templates, restraints, ligands, and affinity binder settings.",
                "parameters": {
                    "protein_MSA_method": {"type": "string", "required": True, "description": "Protein MSA method", "enum": ["Default Search", "Upload File", "No MSA"], "default": "No MSA"},
                    "protein": {"type": "array", "required": False, "description": "Protein sequences"},
                    "protein_MSA_file": {"type": "file", "required": False, "description": "Protein MSA file", "suffix": ["A3M"]},
                    "rna": {"type": "array", "required": False, "description": "RNA sequences"},
                    "dna": {"type": "array", "required": False, "description": "DNA sequences"},
                    "modifications": {"type": "array", "required": False, "description": "Post-translational or nucleotide modifications"},
                    "ligand_smiles": {"type": "array", "required": False, "description": "Ligand SMILES strings"},
                    "ligand_ccd": {"type": "array", "required": False, "description": "Ligand CCD codes"},
                    "covalent_bonds": {"type": "array", "required": False, "description": "Covalent bond definitions"},
                    "pocket_restraints": {"type": "array", "required": False, "description": "Pocket restraints"},
                    "contact_restraints": {"type": "array", "required": False, "description": "Contact restraints"},
                    "template_file": {"type": "file[]", "required": False, "description": "Template CIF files", "suffix": ["cif"]},
                    "template_info": {"type": "array", "required": False, "description": "Template mapping info"},
                    "affinity_binder": {"type": "string", "required": False, "description": "Affinity binder chain ID"},
                    "diffusion_samples": {"type": "integer", "required": True, "description": "Number of diffusion samples", "default": 1}
                },
                "file_params": ["protein_MSA_file", "template_file"]
            }
        }
    },
    "Alphafold3": {
        "provider_name": "Alphafold3",
        "description": "High-accuracy multimodal structure prediction with global docking analysis for diverse molecular interactions.",
        "category": "Structure Prediction",
        "interfaces": {
            "default": {
                "tool_name": "get_alphafold3_info_from_params_api_get_alphafold3_info_from_params_api_post",
                "description": "Run Alphafold3 prediction with optional MSA files, template files, ligands, and bonded restraints.",
                "parameters": {
                    "protein_MSA_method": {"type": "string", "required": True, "description": "Protein MSA method", "enum": ["Jackhmmer/Nhmmer", "MMseqs2", "Upload File", "No MSA"], "default": "No MSA"},
                    "protein_template_method": {"type": "string", "required": True, "description": "Protein template method", "enum": ["Jackhmmer/Nhmmer", "Upload File", "No Template"], "default": "No Template"},
                    "protein": {"type": "array", "required": False, "description": "Protein sequences"},
                    "protein_unpaired_MSA_file": {"type": "file", "required": False, "description": "Protein unpaired MSA file", "suffix": ["A3M"]},
                    "protein_paired_MSA_file": {"type": "file", "required": False, "description": "Protein paired MSA file", "suffix": ["A3M"]},
                    "protein_template_file": {"type": "file[]", "required": False, "description": "Protein template CIF files", "suffix": ["cif"]},
                    "rna": {"type": "array", "required": False, "description": "RNA sequences"},
                    "dna": {"type": "array", "required": False, "description": "DNA sequences"},
                    "modifications": {"type": "array", "required": False, "description": "Modifications"},
                    "ligand_smiles": {"type": "array", "required": False, "description": "Ligand SMILES strings"},
                    "ligand_ccd": {"type": "array", "required": False, "description": "Ligand CCD codes"},
                    "userCCD_mmcif": {"type": "file", "required": False, "description": "User CCD mmCIF file", "suffix": ["cif"]},
                    "bondedAtomPairs": {"type": "array", "required": False, "description": "Bonded atom pair definitions"},
                    "num_diffusion_samples": {"type": "integer", "required": True, "description": "Number of diffusion samples", "default": 5}
                },
                "file_params": ["protein_unpaired_MSA_file", "protein_paired_MSA_file", "protein_template_file", "userCCD_mmcif"]
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "chai": "Chai-1",
    "chai-1": "Chai-1",
    "boltz-2": "Boltz-2",
    "boltz2": "Boltz-2",
    "alphafold3": "Alphafold3",
    "alphafold3": "Alphafold3",
    "structure prediction": "Chai-1",
    "protein complex": "Alphafold3",
    "binding affinity": "Boltz-2",
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
