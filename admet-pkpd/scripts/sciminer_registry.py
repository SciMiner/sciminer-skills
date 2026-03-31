"""Registry for the `admet-prediction` skill."""

ADMET_FEATURE_OPTIONS = [
    "A", "D", "M", "E", "T",
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
    "ADMET Predictor (SMILES)": {
        "provider_name": "ADMET Predictor",
        "description": "Predict ADMET properties from one or more SMILES strings.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "smiles_admet_post",
                "description": "Input one or more SMILES strings to predict ADMET properties.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings"},
                    "features": {"type": "array", "required": False, "description": "Feature groups or detailed ADMET endpoints", "enum": ADMET_FEATURE_OPTIONS},
                },
                "file_params": [],
            }
        }
    },
    "ADMET Predictor (File)": {
        "provider_name": "ADMET Predictor",
        "description": "Predict ADMET properties from uploaded files.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "admet_post",
                "description": "Upload a file containing one or more SMILES for batch ADMET prediction.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "Input file containing SMILES"},
                    "features": {"type": "array", "required": False, "description": "Feature groups or detailed ADMET endpoints", "enum": ADMET_FEATURE_OPTIONS},
                },
                "file_params": ["file"],
            }
        }
    },
    "DeepEsol (SMILES)": {
        "provider_name": "DeepEsol API",
        "description": "Predict solvation energy from SMILES strings.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "start_esol_task_smiles_start_esol_task_smiles_post",
                "description": "Input one or more SMILES strings to predict solvation energy.",
                "parameters": {
                    "smiles": {"type": "array", "required": True, "description": "One or more SMILES strings"},
                },
                "file_params": [],
            }
        }
    },
    "DeepEsol (CSV)": {
        "provider_name": "DeepEsol API",
        "description": "Predict solvation energy from uploaded CSV input.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "start_esol_task_start_esol_task_post",
                "description": "Upload a CSV file containing mol_id and smiles columns.",
                "parameters": {
                    "input_csv": {"type": "file", "required": True, "description": "Input CSV file"},
                },
                "file_params": ["input_csv"],
            }
        }
    },
    "Graph-pKa": {
        "provider_name": "Graph-pKa",
        "description": "Predict pKa values for small molecules from SMILES strings.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "pluginspka-smiles_post",
                "description": "Input one or more SMILES strings to predict pKa values.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings"},
                },
                "file_params": [],
            }
        }
    },
    "OBA": {
        "provider_name": "OBA",
        "description": "Predict oral bioavailability from molecular structure and dose.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "pluginsoba_post",
                "description": "Predict oral bioavailability from SMILES and dose.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "SMILES string"},
                    "dose": {"type": "integer", "required": True, "description": "Dose value"},
                },
                "file_params": [],
            }
        }
    },
    "CoCrystal (SMILES)": {
        "provider_name": "CoCrystal",
        "description": "Perform cocrystal prediction from SMILES strings.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "pluginscocrystal_smiles_post",
                "description": "Input one or more SMILES strings to perform cocrystal prediction.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings"},
                },
                "file_params": [],
            }
        }
    },
    "CoCrystal (File)": {
        "provider_name": "CoCrystal",
        "description": "Perform batch cocrystal prediction from uploaded files.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "pluginscocrystal_post",
                "description": "Upload a structure file for batch cocrystal prediction.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "Input structure file"},
                },
                "file_params": ["file"],
            }
        }
    },
    "AOMP (SMILES)": {
        "provider_name": "AOMP",
        "description": "Predict AOX-mediated oxidative metabolism and site of metabolism from SMILES.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "pluginsaomp_smiles_post",
                "description": "Input one or more SMILES strings to predict AOX-mediated metabolism.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "One or more SMILES strings"},
                },
                "file_params": [],
            }
        }
    },
    "AOMP (File)": {
        "provider_name": "AOMP",
        "description": "Predict AOX-mediated metabolism from uploaded files.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "pluginsaomp_post",
                "description": "Upload a file containing multiple SMILES entries for batch AOX metabolism prediction.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "Input file"},
                },
                "file_params": ["file"],
            }
        }
    },
    "Molecular Descriptors (SMILES)": {
        "provider_name": "Molecular Descriptors",
        "description": "Calculate molecular descriptors from SMILES strings.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "mol_description_cal_mol_des_get",
                "description": "Calculate descriptors from a SMILES string.",
                "parameters": {
                    "smiles": {"type": "string", "required": True, "description": "SMILES string"},
                },
                "file_params": [],
            }
        }
    },
    "Molecular Descriptors (File)": {
        "provider_name": "Molecular Descriptors",
        "description": "Calculate molecular descriptors from uploaded files.",
        "category": "ADMET Prediction",
        "interfaces": {
            "default": {
                "tool_name": "file_descriptors_calc_file_descriptors_post",
                "description": "Upload a file to compute molecular descriptors for each entry.",
                "parameters": {
                    "file": {"type": "file", "required": True, "description": "Input file"},
                },
                "file_params": ["file"],
            }
        }
    },
}


KEYWORD_TOOL_MAP = {
    "admet": "ADMET Predictor (SMILES)",
    "toxicity": "ADMET Predictor (SMILES)",
    "solvation energy": "DeepEsol (SMILES)",
    "esol": "DeepEsol (SMILES)",
    "pka": "Graph-pKa",
    "oral bioavailability": "OBA",
    "oba": "OBA",
    "cocrystal": "CoCrystal (SMILES)",
    "aomp": "AOMP (SMILES)",
    "aox": "AOMP (SMILES)",
    "descriptor": "Molecular Descriptors (SMILES)",
    "molecular descriptors": "Molecular Descriptors (SMILES)",
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
