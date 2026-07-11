#!/usr/bin/env python3
"""Render an interactive, evidence-aware network-pharmacology report from CSV/TSV tables.

Input nodes require: id, type. Optional: label, evidence_tier, score, description.
Input edges require: source, target. Optional: evidence_type, evidence_tier, weight,
direction, source_ref. The script writes network.json and a self-contained HTML page that
loads Cytoscape.js from a public CDN when opened.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


TYPE_COLORS = {
    "herb": "#2f855a", "compound": "#dd6b20", "target": "#2b6cb0",
    "disease": "#c53030", "pathway": "#805ad5", "adverse_effect": "#b83280",
}


def read_table(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        return [dict(row) for row in csv.DictReader(handle, dialect=dialect)]


def require_columns(rows: list[dict[str, str]], columns: tuple[str, ...], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = [column for column in columns if column not in rows[0]]
    if missing:
        raise ValueError(f"{label} is missing required columns: {', '.join(missing)}")


def number(value: str, fallback: float = 1.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def connected_components(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> list[int]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        adjacency[edge["source"]].add(edge["target"])
        adjacency[edge["target"]].add(edge["source"])
    component: dict[str, int] = {}
    next_id = 0
    for node in nodes:
        node_id = node["id"]
        if node_id in component:
            continue
        next_id += 1
        component[node_id] = next_id
        queue: deque[str] = deque([node_id])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in component:
                    component[neighbor] = next_id
                    queue.append(neighbor)
    return [component[node["id"]] for node in nodes]


def build_network(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> tuple[dict, dict]:
    ids = {node["id"] for node in nodes}
    bad_edges = [edge for edge in edges if edge["source"] not in ids or edge["target"] not in ids]
    if bad_edges:
        raise ValueError(f"{len(bad_edges)} edges refer to node IDs absent from nodes table")

    degree: Counter[str] = Counter()
    weighted_degree: Counter[str] = Counter()
    for edge in edges:
        weight = number(edge.get("weight", ""))
        for node_id in (edge["source"], edge["target"]):
            degree[node_id] += 1
            weighted_degree[node_id] += weight

    components = connected_components(nodes, edges)
    elements = []
    for node, component in zip(nodes, components):
        node_type = node.get("type", "other").strip().lower() or "other"
        elements.append({"data": {
            **node, "id": node["id"], "label": node.get("label") or node["id"],
            "type": node_type, "color": TYPE_COLORS.get(node_type, "#4a5568"),
            "degree": degree[node["id"]], "weighted_degree": round(weighted_degree[node["id"]], 4),
            "component": component,
        }})
    for index, edge in enumerate(edges, start=1):
        tier = edge.get("evidence_tier", "unknown") or "unknown"
        elements.append({"data": {**edge, "id": f"e{index}", "weight": number(edge.get("weight", "")), "tier": tier}})

    type_counts = Counter((node.get("type") or "other").lower() for node in nodes)
    tier_counts = Counter((edge.get("evidence_tier") or "unknown") for edge in edges)
    metrics = {
        "nodes": len(nodes), "edges": len(edges), "components": len(set(components)),
        "isolated_nodes": sum(1 for node in nodes if degree[node["id"]] == 0),
        "node_types": dict(sorted(type_counts.items())), "edge_evidence_tiers": dict(sorted(tier_counts.items())),
    }
    return {"elements": elements, "metrics": metrics}, metrics


def render_html(network: dict, title: str) -> str:
    payload = json.dumps(network, ensure_ascii=False).replace("</", "<\\/")
    safe_title = html.escape(title)
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{safe_title}</title><script src=\"https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.4/cytoscape.min.js\"></script>
<style>body{{margin:0;font:14px system-ui,sans-serif;color:#1a202c}}header{{padding:14px 18px;background:#102a43;color:#fff}}#layout{{display:grid;grid-template-columns:310px 1fr;height:calc(100vh - 73px)}}aside{{padding:16px;overflow:auto;border-right:1px solid #d9e2ec}}#cy{{min-width:0;background:#f8fafc}}label{{display:block;margin:12px 0 4px;font-weight:600}}input,select{{width:100%;box-sizing:border-box;padding:7px}}.metric{{background:#edf2f7;padding:7px;margin:5px 0;border-radius:4px}}.hint{{color:#52606d;line-height:1.4}}</style>
</head><body><header><strong>{safe_title}</strong> — interactive evidence network</header><div id=\"layout\"><aside>
<label for=\"search\">Find node</label><input id=\"search\" placeholder=\"name or ID\"><label for=\"type\">Entity type</label><select id=\"type\"><option value=\"\">All types</option></select>
<label for=\"tier\">Minimum edge tier</label><select id=\"tier\"><option value=\"\">All evidence</option><option value=\"1\">Tier 1</option><option value=\"2\">Tier 2</option><option value=\"3\">Tier 3</option></select>
<h3>Network summary</h3><div id=\"metrics\"></div><p class=\"hint\">Node color = entity type. Edge opacity declines from Tier 1 to Tier 3. Click an entity to inspect its attributes. Use this report for exploration; create a filtered static figure for publication.</p><pre id=\"detail\" class=\"hint\"></pre>
</aside><main id=\"cy\"></main></div><script>const network={payload}; const types=[...new Set(network.elements.filter(x=>!x.data.source).map(x=>x.data.type))].sort(); const typeSelect=document.getElementById('type'); types.forEach(t=>typeSelect.add(new Option(t,t)));
const metrics=network.metrics; document.getElementById('metrics').innerHTML=Object.entries(metrics).map(([k,v])=>`<div class=\"metric\"><b>${{k.replaceAll('_',' ')}}:</b> ${{typeof v==='object'?JSON.stringify(v):v}}</div>`).join('');
const cy=cytoscape({{container:document.getElementById('cy'),elements:network.elements,style:[{{selector:'node',style:{{'background-color':'data(color)','label':'data(label)','font-size':10,'text-wrap':'wrap','text-max-width':'80px','width':'mapData(degree,0,20,24,58)','height':'mapData(degree,0,20,24,58)','color':'#1a202c','text-outline-color':'#fff','text-outline-width':2}}}},{{selector:'edge',style:{{'width':'mapData(weight,0,5,1,5)','line-color':'#52606d','curve-style':'bezier','target-arrow-shape':'triangle','target-arrow-color':'#52606d','opacity':0.65}}}},{{selector:'edge[tier = "2"]',style:{{opacity:0.45,'line-style':'dashed'}}}},{{selector:'edge[tier = "3"]',style:{{opacity:0.25,'line-style':'dotted'}}}},{{selector:'.hidden',style:{{display:'none'}}}},{{selector:':selected',style:{{'border-width':4,'border-color':'#f6ad55'}}}}],layout:{{name:'cose',animate:false,padding:30}}}});
function refresh(){{const query=document.getElementById('search').value.toLowerCase(), type=typeSelect.value, tier=document.getElementById('tier').value; cy.elements().removeClass('hidden'); cy.nodes().forEach(n=>{{const ok=(!query||(n.data('label')+' '+n.id()).toLowerCase().includes(query))&&(!type||n.data('type')===type);if(!ok)n.addClass('hidden')}});cy.edges().forEach(e=>{{const edgeTier=String(e.data('tier'));if((tier&&edgeTier>tier)||e.source().hasClass('hidden')||e.target().hasClass('hidden'))e.addClass('hidden')}});}}
document.getElementById('search').oninput=refresh;typeSelect.onchange=refresh;document.getElementById('tier').onchange=refresh;cy.on('tap','node',e=>document.getElementById('detail').textContent=JSON.stringify(e.target.data(),null,2));</script></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", required=True, type=Path)
    parser.add_argument("--edges", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--title", default="Network pharmacology evidence network")
    args = parser.parse_args()
    nodes, edges = read_table(args.nodes), read_table(args.edges)
    require_columns(nodes, ("id", "type"), "nodes table")
    require_columns(edges, ("source", "target"), "edges table")
    network, metrics = build_network(nodes, edges)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "network.json").write_text(json.dumps(network, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.output_dir / "network_report.html").write_text(render_html(network, args.title), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
