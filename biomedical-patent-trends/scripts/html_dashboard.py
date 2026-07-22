"""Write a self-contained interactive HTML dashboard for local patent analyses."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_dashboard(
    out: Path,
    *,
    title: str,
    metrics: list[dict[str, Any]],
    charts: list[dict[str, Any]],
    source_note: str,
) -> None:
    """Create an offline HTML file; values are embedded and never fetched remotely."""
    payload = json.dumps(
        {"metrics": metrics, "charts": charts, "source_note": source_note},
        ensure_ascii=False,
    ).replace("</", "<\\/")
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>
:root{{color-scheme:light;font-family:Inter,Segoe UI,Arial,sans-serif;color:#172033;background:#f5f7fb}}
body{{margin:0}}main{{max-width:1180px;margin:auto;padding:32px 24px 48px}}h1{{margin:0;font-size:30px}}.subtitle,.source{{color:#56637a;line-height:1.5}}.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:24px 0}}.metric,.panel{{background:#fff;border:1px solid #e3e8f0;border-radius:12px;box-shadow:0 2px 7px #1b2b4a0a}}.metric{{padding:17px}}.metric b{{display:block;font-size:27px;color:#155eef;margin-bottom:3px}}.metric span{{font-size:14px;color:#56637a}}.panel{{padding:20px}}.controls{{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 18px}}button{{appearance:none;border:1px solid #cdd5df;background:white;border-radius:7px;padding:8px 11px;color:#344054;cursor:pointer}}button.active{{background:#155eef;color:white;border-color:#155eef}}#chart-title{{margin:0 0 4px;font-size:20px}}#chart-note{{min-height:20px;color:#667085;font-size:14px}}svg{{width:100%;height:auto;overflow:visible;margin-top:10px}}.label{{font-size:14px;fill:#344054}}.value{{font-size:14px;fill:#172033;font-weight:600}}.axis{{stroke:#d0d5dd;stroke-width:1}}.bar{{fill:#2563eb}}footer{{font-size:13px;margin-top:22px;color:#667085}}@media(max-width:600px){{main{{padding:22px 14px}}h1{{font-size:25px}}}}
</style></head><body><main><h1>{title}</h1><p class="subtitle">Interactive local analysis dashboard</p><section class="metrics" id="metrics"></section><section class="panel"><nav class="controls" id="controls" aria-label="Chart selection"></nav><h2 id="chart-title"></h2><p id="chart-note"></p><svg id="chart" role="img"></svg></section><footer id="source"></footer></main>
<script>const data={payload};const ns='http://www.w3.org/2000/svg';const el=(n,a={{}},t='')=>{{const x=document.createElementNS(ns,n);Object.entries(a).forEach(([k,v])=>x.setAttribute(k,v));x.textContent=t;return x}};
document.getElementById('metrics').replaceChildren(...data.metrics.map(m=>{{const d=document.createElement('div');d.className='metric';d.innerHTML=`<b>${{m.value}}</b><span>${{m.label}}</span>`;return d}}));document.getElementById('source').textContent=data.source_note;
const controls=document.getElementById('controls');function draw(index){{const c=data.charts[index],svg=document.getElementById('chart');document.getElementById('chart-title').textContent=c.title;document.getElementById('chart-note').textContent=c.note||'';[...controls.children].forEach((b,i)=>b.classList.toggle('active',i===index));const items=c.items.slice(0,15),w=1080,left=305,right=85,row=39,h=Math.max(170,76+items.length*row+35),max=Math.max(1,...items.map(x=>x.count));svg.setAttribute('viewBox',`0 0 ${{w}} ${{h}}`);svg.replaceChildren(el('line',{{x1:left,y1:52,x2:left,y2:h-28,class:'axis'}}));items.forEach((item,i)=>{{const y=58+i*row,bw=Math.round((w-left-right)*item.count/max);svg.append(el('text',{{x:left-12,y:y+18,'text-anchor':'end',class:'label'}},item.label),el('rect',{{x:left,y:y,width:bw,height:23,rx:4,class:'bar'}}),el('text',{{x:left+bw+8,y:y+18,class:'value'}},String(item.count)))}});if(!items.length)svg.append(el('text',{{x:24,y:80,class:'label'}},'No chartable data was detected.'));}}data.charts.forEach((c,i)=>{{const b=document.createElement('button');b.textContent=c.title;b.addEventListener('click',()=>draw(i));controls.append(b)}});draw(0);</script></body></html>"""
    out.write_text(document, encoding="utf-8")
