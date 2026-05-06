"""Registry for the `admet-pkpd` skill."""

ADMET_FEATURES = [
    "A",
    "D",
    "M",
    "E",
    "T",
    "A_Human Intestinal Absorption",
    "A_Caco-2 Permeability",
    "A_P-glycoprotein Inhibitor",
    "A_P-glycoprotein Substrate",
    "D_Blood-Brain Barrier",
    "M_CYP450 1A2 Inhibitor",
    "M_CYP450 2C19 Inhibitor",
    "M_CYP450 2C9 Inhibitor",
    "M_CYP450 2C9 Substrate",
    "M_CYP450 2D6 Inhibitor",
    "M_CYP450 2D6 Substrate",
    "M_CYP450 3A4 Inhibitor",
    "M_CYP450 3A4 Substrate",
    "M_CYP Inhibitory Promiscuity",
    "M_Biodegradation",
    "E_Renal Organic Cation Transporter",
    "T_AMES Toxicity",
    "T_Carcinogens",
    "T_hERG inhibition",
    "T_Honey Bee Toxicity",
    "T_Tetrahymena Pyriformis Toxicity",
    "T_Fish Toxicity",
]


TOOLS_REGISTRY = {
    "ADMET Predictor SMILES": {
        "provider_name": "ADMET Predictor",
        "description": "Predict ADMET properties (absorption, distribution, metabolism, excretion, toxicity) from SMILES strings.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "ADMET_smiles_admet_post",
                "description": "Input one or more SMILES strings to predict ADMET properties. Optionally select specific property categories or endpoints.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings, one per line"},
                    "features": {"type": "array", "required": False, "description": "ADMET property categories or endpoints to compute", "enum": ADMET_FEATURES},
                },
                "file_params": [],
            }
        },
    },
    "ADMET Predictor File": {
        "provider_name": "ADMET Predictor",
        "description": "Batch-predict ADMET properties from an uploaded SMILES file.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "ADMET_admet_post",
                "description": "Upload a TXT file of SMILES strings for batch ADMET prediction. Optionally select specific property categories or endpoints.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "TXT file containing SMILES strings, one per line"},
                    "features": {"type": "array", "required": False, "description": "ADMET property categories or endpoints to compute", "enum": ADMET_FEATURES},
                },
                "file_params": ["file"],
            }
        },
    },
    "AOMP SMILES": {
        "provider_name": "AOMP",
        "description": "Predict AOX-mediated oxidative metabolism substrate classification and site of metabolism from SMILES strings.",
        "category": "Metabolism Prediction",
        "interfaces": {
            "default": {
                "tool_name": "AOMP_plugins-aomp-smiles_post",
                "description": "Input one or more SMILES strings to predict whether the molecule is an AOX metabolic substrate and identify potential sites of metabolism.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings, one per line"},
                },
                "file_params": [],
            }
        },
    },
    "AOMP File": {
        "provider_name": "AOMP",
        "description": "Batch-predict AOX-mediated oxidative metabolism from an uploaded file.",
        "category": "Metabolism Prediction",
        "interfaces": {
            "default": {
                "tool_name": "AOMP_plugins-aomp_post",
                "description": "Upload a TXT or SDF file for batch prediction of AOX-mediated metabolism and metabolic sites.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "TXT or SDF file containing molecules"},
                },
                "file_params": ["file"],
            }
        },
    },
    "OBA": {
        "provider_name": "OBA",
        "description": "Predict oral bioavailability of a small molecule using the Attentive FP graph neural network.",
        "category": "Pharmacokinetics",
        "interfaces": {
            "default": {
                "tool_name": "oba_plugins-oba_post",
                "description": "Input a SMILES string and dose (mg) to predict oral bioavailability.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "SMILES string of the molecule"},
                    "dose": {"type": "integer", "required": True, "description": "Administered dose in milligrams"},
                },
                "file_params": [],
            }
        },
    },
    "Graph-pKa": {
        "provider_name": "Graph-pKa",
        "description": "Predict pKa values of ionizable groups in small molecules.",
        "category": "Physicochemical Properties",
        "interfaces": {
            "default": {
                "tool_name": "pka_plugins-pka-smiles_post",
                "description": "Input one or more SMILES strings to predict pKa values.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings, one per line"},
                },
                "file_params": [],
            }
        },
    },
    "DeepEsol SMILES": {
        "provider_name": "DeepEsol",
        "description": "Predict aqueous solvation free energy (ΔG_solv) from SMILES strings using physics-based sampling and an ML force field.",
        "category": "Physicochemical Properties",
        "interfaces": {
            "default": {
                "tool_name": "start_esol_task_smiles_start_esol_task_smiles_post",
                "description": "Input one or more SMILES strings to predict solvation energy.",
                "parameters": {
                    "smiles": {"type": "array", "required": True, "description": "List of SMILES strings"},
                },
                "file_params": [],
            }
        },
    },
    "DeepEsol File": {
        "provider_name": "DeepEsol",
        "description": "Batch-predict solvation free energy from a CSV file with mol_id and smiles columns.",
        "category": "Physicochemical Properties",
        "interfaces": {
            "default": {
                "tool_name": "start_esol_task_start_esol_task_post",
                "description": "Upload a CSV file with 'mol_id' and 'smiles' columns to batch-predict solvation energy.",
                "parameters": {
                    "input_csv": {"type": "file", "required": True, "description": "CSV file with 'mol_id' and 'smiles' columns"},
                },
                "file_params": ["input_csv"],
            }
        },
    },
    "Molecular Descriptors SMILES": {
        "provider_name": "Molecular Descriptors",
        "description": "Calculate physicochemical molecular descriptors from a SMILES string.",
        "category": "Physicochemical Properties",
        "interfaces": {
            "default": {
                "tool_name": "mol_description_cal_mol_des_get",
                "description": "Input a SMILES string to compute a full set of molecular descriptors.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "SMILES string of the molecule"},
                },
                "file_params": [],
            }
        },
    },
    "Molecular Descriptors File": {
        "provider_name": "Molecular Descriptors",
        "description": "Batch-calculate molecular descriptors from an uploaded SDF or TXT file.",
        "category": "Physicochemical Properties",
        "interfaces": {
            "default": {
                "tool_name": "file_descriptors_calc_file_descriptors_post",
                "description": "Upload an SDF or TXT file to compute molecular descriptors for each molecule.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "SDF or TXT file containing molecules"},
                },
                "file_params": ["file"],
            }
        },
    },
}


KEYWORD_TOOL_MAP = {
    # ADMET
    "admet": "ADMET Predictor SMILES",
    "absorption": "ADMET Predictor SMILES",
    "distribution": "ADMET Predictor SMILES",
    "metabolism": "ADMET Predictor SMILES",
    "excretion": "ADMET Predictor SMILES",
    "toxicity": "ADMET Predictor SMILES",
    "herg": "ADMET Predictor SMILES",
    "ames": "ADMET Predictor SMILES",
    "cyp": "ADMET Predictor SMILES",
    "bbb": "ADMET Predictor SMILES",
    "blood-brain barrier": "ADMET Predictor SMILES",
    "p-glycoprotein": "ADMET Predictor SMILES",
    "caco-2": "ADMET Predictor SMILES",
    "intestinal absorption": "ADMET Predictor SMILES",
    # AOMP
    "aomp": "AOMP SMILES",
    "aox": "AOMP SMILES",
    "site of metabolism": "AOMP SMILES",
    "oxidative metabolism": "AOMP SMILES",
    "aldehyde oxidase": "AOMP SMILES",
    # OBA
    "oba": "OBA",
    "oral bioavailability": "OBA",
    "bioavailability": "OBA",
    # pKa
    "pka": "Graph-pKa",
    "ionization": "Graph-pKa",
    "protonation": "Graph-pKa",
    # DeepEsol
    "esol": "DeepEsol SMILES",
    "solvation": "DeepEsol SMILES",
    "solubility": "DeepEsol SMILES",
    "aqueous": "DeepEsol SMILES",
    "delta g solv": "DeepEsol SMILES",
    # Molecular Descriptors
    "descriptors": "Molecular Descriptors SMILES",
    "molecular descriptors": "Molecular Descriptors SMILES",
    "physicochemical": "Molecular Descriptors SMILES",
    "mw": "Molecular Descriptors SMILES",
    "molecular weight": "Molecular Descriptors SMILES",
    "tpsa": "Molecular Descriptors SMILES",
    "logp": "Molecular Descriptors SMILES",
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
        interfaces = result["interfaces"] or {}
        if interfaces:
            first_iface = interfaces.get("default") or list(interfaces.values())[0]
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


def get_default_interface(tool_name: str) -> dict:
    """Return the default interface metadata for a tool."""
    info = get_tool_info(tool_name)
    if not info:
        return None
    interfaces = info.get("interfaces") or {}
    if not interfaces:
        return None
    return interfaces.get("default") or list(interfaces.values())[0]


def build_payload_from_registry(tool_name: str, user_parameters: dict) -> dict:
    """Build a SciMiner invoke payload strictly from registry-defined metadata.

    - provider_name and tool_name come from the registry, never from caller input.
    - user_parameters are filtered against the registry's allowed parameter keys.
    - Required parameters are validated; missing ones raise ValueError.
    """
    info = get_tool_info(tool_name)
    if not info:
        raise ValueError(f"Unknown tool: {tool_name}")

    interface = get_default_interface(tool_name)
    if not interface:
        raise ValueError(f"No interface found for tool: {tool_name}")

    allowed_params = interface.get("parameters", {})
    filtered_parameters = {
        key: value
        for key, value in (user_parameters or {}).items()
        if key in allowed_params and value is not None
    }

    missing_required = [
        key for key, meta in allowed_params.items()
        if meta.get("required") and key not in filtered_parameters
    ]
    if missing_required:
        raise ValueError(f"Missing required parameters: {sorted(missing_required)}")

    return {
        "provider_name": info["provider_name"],
        "tool_name": interface["tool_name"],
        "parameters": filtered_parameters,
    }
