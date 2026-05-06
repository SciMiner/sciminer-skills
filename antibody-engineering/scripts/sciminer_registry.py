"""Registry for the `antibody-engineering` skill."""

ANARCI_SCHEMES = ["imgt", "chothia", "kabat", "martin", "wolfguy", "aho"]
BIOPHI_SCHEMES = ["kabat", "chothia", "imgt", "aho"]
BIOPHI_HUMANNESS_CDR = ["kabat", "chothia", "imgt", "north"]
BIOPHI_HUMANIZE_CDR = ["kabat", "kabat_vernier", "chothia", "imgt", "north"]
BIOPHI_HUMANIZE_METHODS = ["sapiens", "cdr_grafting"]
FOLDX_STRUCTURE_OPS = ["RepairPDB", "BuildModel", "Optimize"]
FOLDX_ENERGY_OPS = ["Stability", "AnalyseComplex", "AlaScan", "PositionScan"]
ROSETTA_FASTDESIGN_RELAX_SCRIPTS = ["MonomerDesign2019", "InterfaceDesign2019"]


TOOLS_REGISTRY = {
    "ANARCI Numbering": {
        "provider_name": "ANARCI",
        "description": "Number antibody or TCR sequences to obtain standardized residue coordinates and region boundaries.",
        "category": "Sequence Profiling",
        "interfaces": {
            "default": {
                "tool_name": "predict_predict_post",
                "description": "Number antibody or TCR sequences with ANARCI.",
                "parameters": {
                    "scheme": {"type": "string", "required": False, "description": "Numbering scheme", "enum": ANARCI_SCHEMES, "default": "imgt"},
                    "sequences": {"type": "string", "required": False, "description": "FASTA-formatted sequences or one sequence per line"},
                    "input_file": {"type": "file", "required": False, "description": "Optional FASTA file"}
                },
                "file_params": ["input_file"]
            }
        }
    },
    "BioPhi Humanness Report": {
        "provider_name": "BioPhi",
        "description": "Evaluate antibody humanness with OASis-style 9-mer prevalence analysis.",
        "category": "De-risking and Humanization",
        "interfaces": {
            "default": {
                "tool_name": "humanness_report_humanness_report__post",
                "description": "Run BioPhi humanness evaluation on heavy and light chain sequences.",
                "parameters": {
                    "scheme": {"type": "string", "required": False, "description": "Numbering scheme", "enum": BIOPHI_SCHEMES, "default": "kabat"},
                    "cdr_definition": {"type": "string", "required": False, "description": "CDR definition scheme", "enum": BIOPHI_HUMANNESS_CDR, "default": "kabat"},
                    "heavy_chain": {"type": "array", "required": True, "description": "Heavy chain amino acid sequence(s)"},
                    "light_chain": {"type": "array", "required": True, "description": "Light chain amino acid sequence(s)"},
                    "min_subjects_percent": {"type": "number", "required": False, "description": "OASis prevalence threshold", "default": 10}
                },
                "file_params": []
            }
        }
    },
    "BioPhi Humanize": {
        "provider_name": "BioPhi",
        "description": "Humanize antibody sequences with Sapiens or CDR grafting workflows.",
        "category": "De-risking and Humanization",
        "interfaces": {
            "default": {
                "tool_name": "humanize_humanize__post",
                "description": "Generate humanized antibody sequence candidates.",
                "parameters": {
                    "method": {"type": "string", "required": False, "description": "Humanization method", "enum": BIOPHI_HUMANIZE_METHODS, "default": "sapiens"},
                    "scheme": {"type": "string", "required": False, "description": "Numbering scheme", "enum": BIOPHI_SCHEMES, "default": "kabat"},
                    "cdr_definition": {"type": "string", "required": False, "description": "CDR definition scheme", "enum": BIOPHI_HUMANIZE_CDR, "default": "kabat"},
                    "heavy_v_germline": {"type": "string", "required": False, "description": "Heavy-chain V germline for CDR grafting", "default": "auto"},
                    "light_v_germline": {"type": "string", "required": False, "description": "Light-chain V germline for CDR grafting", "default": "auto"},
                    "heavy_chain": {"type": "array", "required": True, "description": "Heavy chain amino acid sequence(s)"},
                    "light_chain": {"type": "array", "required": True, "description": "Light chain amino acid sequence(s)"},
                    "iterations": {"type": "integer", "required": False, "description": "Sapiens iteration count", "default": 1},
                    "min_subjects_percent": {"type": "number", "required": False, "description": "OASis prevalence threshold", "default": 10}
                },
                "file_params": []
            }
        }
    },
    "BioPhi Designer": {
        "provider_name": "BioPhi",
        "description": "Evaluate designed antibody candidates with OASis-like prevalence scoring.",
        "category": "De-risking and Humanization",
        "interfaces": {
            "default": {
                "tool_name": "designer_designer__post",
                "description": "Assess antibody candidate designs under BioPhi designer evaluation.",
                "parameters": {
                    "scheme": {"type": "string", "required": False, "description": "Numbering scheme", "enum": BIOPHI_SCHEMES, "default": "kabat"},
                    "cdr_definition": {"type": "string", "required": False, "description": "CDR definition scheme", "enum": BIOPHI_HUMANNESS_CDR, "default": "kabat"},
                    "heavy_chain": {"type": "array", "required": True, "description": "Heavy chain amino acid sequence(s)"},
                    "light_chain": {"type": "array", "required": True, "description": "Light chain amino acid sequence(s)"},
                    "min_subjects_percent": {"type": "number", "required": False, "description": "OASis prevalence threshold", "default": 10}
                },
                "file_params": []
            }
        }
    },
    "BioPhi Mutate": {
        "provider_name": "BioPhi",
        "description": "Apply explicit point mutations to humanized antibody sequences and re-evaluate humanness.",
        "category": "De-risking and Humanization",
        "interfaces": {
            "default": {
                "tool_name": "mutate_mutate__post",
                "description": "Apply point mutation sets to antibody heavy and light chains.",
                "parameters": {
                    "scheme": {"type": "string", "required": False, "description": "Numbering scheme", "enum": BIOPHI_SCHEMES, "default": "kabat"},
                    "cdr_definition": {"type": "string", "required": False, "description": "CDR definition scheme", "enum": BIOPHI_HUMANNESS_CDR, "default": "kabat"},
                    "heavy_chain": {"type": "string", "required": True, "description": "Humanized heavy chain sequence"},
                    "light_chain": {"type": "string", "required": True, "description": "Humanized light chain sequence"},
                    "mutation": {"type": "string", "required": True, "description": "Single or multiple point mutations"},
                    "min_subjects_percent": {"type": "number", "required": False, "description": "OASis prevalence threshold", "default": 10}
                },
                "file_params": []
            }
        }
    },
    "IgFold Structure Prediction": {
        "provider_name": "IgFold",
        "description": "Predict antibody 3D structures from heavy and optional light chain sequences.",
        "category": "3D Structural Modeling",
        "interfaces": {
            "default": {
                "tool_name": "predict_predict_post",
                "description": "Predict antibody structures with optional refinement and renumbering.",
                "parameters": {
                    "heavy_sequences": {"type": "array", "required": True, "description": "Heavy chain amino acid sequences"},
                    "light_sequences": {"type": "array", "required": False, "description": "Light chain amino acid sequences"},
                    "do_refine": {"type": "boolean", "required": False, "description": "Perform structural refinement", "default": True},
                    "do_renum": {"type": "boolean", "required": False, "description": "Renumber predicted structure using Chothia scheme", "default": False},
                    "num_models": {"type": "integer", "required": False, "description": "Number of ensemble models", "default": 4}
                },
                "file_params": []
            }
        }
    },
    "Rosetta FastRelax": {
        "provider_name": "Rosetta FastRelax",
        "description": "Relax predicted or modeled antibody structures before developability or energetic analysis.",
        "category": "Modeling and Relaxation",
        "interfaces": {
            "default": {
                "tool_name": "fastrelax_fastrelax_post",
                "description": "Run Rosetta FastRelax on an uploaded PDB structure.",
                "parameters": {
                    "protein": {"type": "file", "required": True, "description": "Protein structure file in PDB format"},
                    "constrain_relax_to_start_coords": {"type": "boolean", "required": False, "description": "Constrain relaxation to starting coordinates", "default": False},
                    "coordinate_constraint_weight": {"type": "number", "required": False, "description": "Coordinate constraint weight when constrained relaxation is enabled"},
                    "num_model": {"type": "integer", "required": False, "description": "Number of relaxed output models", "default": 1}
                },
                "file_params": ["protein"]
            }
        }
    },
    "Rosetta SAP Score": {
        "provider_name": "Rosetta SAP Score",
        "description": "Quantify structure-level aggregation risk through Rosetta surface accessibility profiling.",
        "category": "Developability Profiling",
        "interfaces": {
            "default": {
                "tool_name": "sapscore_sapscore_post",
                "description": "Compute Rosetta SAP score for an uploaded PDB structure.",
                "parameters": {
                    "protein": {"type": "file", "required": True, "description": "Protein structure file in PDB format"}
                },
                "file_params": ["protein"]
            }
        }
    },
    "FoldX Structure Ops": {
        "provider_name": "FoldX",
        "description": "Repair, mutate, or optimize antibody structures before downstream energy analysis.",
        "category": "Affinity and Stability Engineering",
        "interfaces": {
            "default": {
                "tool_name": "structure_ops_structure_ops_post",
                "description": "Run FoldX structure operations such as RepairPDB, BuildModel, or Optimize.",
                "parameters": {
                    "operation": {"type": "string", "required": False, "description": "Structure operation", "enum": FOLDX_STRUCTURE_OPS, "default": "RepairPDB"},
                    "pdb_file": {"type": "file", "required": True, "description": "PDB or mmCIF structure file"},
                    "mutations": {"type": "string", "required": False, "description": "Mutation list for BuildModel"},
                    "temperature": {"type": "number", "required": False, "description": "Temperature in Kelvin", "default": 298},
                    "ph": {"type": "number", "required": False, "description": "pH value", "default": 7},
                    "number_of_runs": {"type": "integer", "required": False, "description": "Number of FoldX runs", "default": 1}
                },
                "file_params": ["pdb_file"]
            }
        }
    },
    "FoldX Energy Ops": {
        "provider_name": "FoldX",
        "description": "Run stability, interface, alanine scan, or position scan energy analyses on antibody structures.",
        "category": "Affinity and Stability Engineering",
        "interfaces": {
            "default": {
                "tool_name": "energy_ops_energy_ops_post",
                "description": "Run FoldX energetic analyses on structures or complexes.",
                "parameters": {
                    "operation": {"type": "string", "required": False, "description": "Energy operation", "enum": FOLDX_ENERGY_OPS, "default": "Stability"},
                    "pdb_file": {"type": "file", "required": True, "description": "PDB or mmCIF structure file"},
                    "residues": {"type": "string", "required": False, "description": "Residue regions for AlaScan"},
                    "temperature": {"type": "number", "required": False, "description": "Temperature in Kelvin", "default": 298},
                    "ph": {"type": "number", "required": False, "description": "pH value", "default": 7}
                },
                "file_params": ["pdb_file"]
            }
        }
    },
    "Rosetta FastDesign": {
        "provider_name": "Rosetta FastDesign",
        "description": "Perform targeted antibody redesign with simultaneous sequence design and structure relaxation.",
        "category": "Precision Design via Rosetta",
        "interfaces": {
            "default": {
                "tool_name": "fastdesign_fastdesign_post",
                "description": "Run Rosetta FastDesign on selected residue ranges.",
                "parameters": {
                    "relax_script": {"type": "string", "required": False, "description": "FastDesign relax script", "enum": ROSETTA_FASTDESIGN_RELAX_SCRIPTS, "default": "MonomerDesign2019"},
                    "protein": {"type": "file", "required": True, "description": "Protein backbone structure file in PDB format"},
                    "resfile": {"type": "string", "required": True, "description": "Residue positions allowed for design"},
                    "num_model": {"type": "integer", "required": False, "description": "Number of design outputs", "default": 1}
                },
                "file_params": ["protein"]
            }
        }
    },
    "Rosetta InterfaceAnalyzer": {
        "provider_name": "Rosetta InterfaceAnalyzer",
        "description": "Evaluate antibody-antigen interface quality for redesigned complexes.",
        "category": "Precision Design via Rosetta",
        "interfaces": {
            "default": {
                "tool_name": "rosetta_interfaceanalyzer_rosetta_interfaceanalyzer_post",
                "description": "Run Rosetta InterfaceAnalyzer on an uploaded complex structure.",
                "parameters": {
                    "protein_file": {"type": "file", "required": True, "description": "Protein complex structure file in PDB or CIF format"},
                    "binder_chain": {"type": "string", "required": True, "description": "Binder chain identifier", "default": "B"}
                },
                "file_params": ["protein_file"]
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "anarci": "ANARCI Numbering",
    "number antibody": "ANARCI Numbering",
    "cdr boundary": "ANARCI Numbering",
    "humanness": "BioPhi Humanness Report",
    "humanize": "BioPhi Humanize",
    "sapiens": "BioPhi Humanize",
    "cdr grafting": "BioPhi Humanize",
    "oasis": "BioPhi Humanness Report",
    "designer": "BioPhi Designer",
    "mutate": "BioPhi Mutate",
    "igfold": "IgFold Structure Prediction",
    "antibody structure": "IgFold Structure Prediction",
    "fastrelax": "Rosetta FastRelax",
    "relax structure": "Rosetta FastRelax",
    "sap": "Rosetta SAP Score",
    "aggregation risk": "Rosetta SAP Score",
    "foldx": "FoldX Energy Ops",
    "repairpdb": "FoldX Structure Ops",
    "buildmodel": "FoldX Structure Ops",
    "positionscan": "FoldX Energy Ops",
    "alascan": "FoldX Energy Ops",
    "analysecomplex": "FoldX Energy Ops",
    "stability": "FoldX Energy Ops",
    "fastdesign": "Rosetta FastDesign",
    "interface design": "Rosetta FastDesign",
    "interfaceanalyzer": "Rosetta InterfaceAnalyzer",
    "interface analyzer": "Rosetta InterfaceAnalyzer"
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
