"""Registry for the `ocsr` skill."""

TOOLS_REGISTRY = {
    "AlphaExtractor": {
        "provider_name": "AlphaExtractor",
        "description": "Extract molecules and names from chemistry images, including images containing multiple molecules.",
        "category": "Optical Chemical Structure Recognition",
        "interfaces": {
            "default": {
                "tool_name": "file_descriptors_calc_images_descriptors_post",
                "description": "Extract molecular structures and names from an uploaded image.",
                "parameters": {
                    "image": {
                        "type": "file",
                        "required": True,
                        "description": "Chemistry image file",
                        "suffix": ["png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "gif", "ico"]
                    }
                },
                "file_params": ["image"]
            }
        }
    }
}


KEYWORD_TOOL_MAP = {
    "ocsr": "AlphaExtractor",
    "alphaextractor": "AlphaExtractor",
    "extract molecule from image": "AlphaExtractor",
    "chemical image": "AlphaExtractor",
    "structure recognition": "AlphaExtractor",
    "extract names from image": "AlphaExtractor",
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
