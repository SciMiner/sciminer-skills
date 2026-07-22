"""Write a standalone, presentation-focused HTML patent trends report."""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title><style>
:root{--primary:#2563eb;--primary-light:#dbeafe;--success:#059669;--success-light:#d1fae5;--warning:#d97706;--warning-light:#fef3c7;--danger:#dc2626;--danger-light:#fee2e2;--gray-50:#f8fafc;--gray-100:#f1f5f9;--gray-200:#e2e8f0;--gray-600:#475569;--gray-800:#1e293b;--gray-900:#0f172a}*{box-sizing:border-box}body{margin:0;background:var(--gray-50);color:var(--gray-800);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif}.container{max-width:1400px;margin:0 auto;padding:2rem}header{background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 100%);color:#fff;padding:3rem 2rem;border-radius:16px;margin-bottom:2rem;box-shadow:0 10px 40px rgba(37,99,235,.2)}header h1{font-size:2rem;font-weight:700;line-height:1.25;margin:0 0 .5rem}header .subtitle{opacity:.9;font-size:1.05rem;margin:0}header .meta{margin-top:1rem;display:flex;gap:.6rem 2rem;flex-wrap:wrap;font-size:.9rem;opacity:.85}.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem;margin-bottom:2rem}.stat-card{background:#fff;padding:1.5rem;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1);border-left:4px solid var(--primary);transition:transform .2s}.stat-card:hover{transform:translateY(-3px)}.stat-card .number{font-size:2.5rem;font-weight:700;color:var(--primary);line-height:1}.stat-card .label{color:var(--gray-600);font-size:.9rem;margin-top:.5rem}.stat-card.success{border-left-color:var(--success)}.stat-card.success .number{color:var(--success)}.stat-card.warning{border-left-color:var(--warning)}.stat-card.warning .number{color:var(--warning)}.stat-card.danger{border-left-color:var(--danger)}.stat-card.danger .number{color:var(--danger)}.section{background:#fff;border-radius:12px;padding:2rem;margin-bottom:2rem;box-shadow:0 1px 3px rgba(0,0,0,.1)}.section-title{font-size:1.4rem;font-weight:700;color:var(--gray-900);margin:0 0 1.5rem;display:flex;align-items:center;gap:.5rem}.section-title:before{content:"";display:inline-block;width:4px;height:24px;background:var(--primary);border-radius:2px}.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:2rem}.chart-heading{margin:0 0 1rem;color:var(--gray-600);font-size:1rem}.chart-container{position:relative;height:350px}.chart-caption{font-size:.8rem;color:var(--gray-600);margin:.75rem 0 0}.empty-state{background:var(--gray-50);border:1px dashed var(--gray-200);border-radius:8px;color:var(--gray-600);padding:1.25rem}.observation-list{list-style:none;margin:0;padding:0}.observation-list li{padding:1rem 0;border-bottom:1px solid var(--gray-100);display:flex;gap:1rem;align-items:flex-start}.observation-list li:last-child{border-bottom:none}.obs-badge{background:var(--primary-light);color:var(--primary);font-weight:700;padding:.25rem .75rem;border-radius:6px;font-size:.85rem;white-space:nowrap;margin-top:.1rem}.obs-content h3{font-size:1.05rem;margin:0 0 .25rem;color:var(--gray-900)}.obs-content p{color:var(--gray-600);font-size:.95rem;margin:0}.focus-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem}.focus-card{background:var(--gray-50);padding:1rem;border-radius:8px}.focus-card strong{color:var(--primary)}.focus-card p{font-size:.85rem;color:var(--gray-600);margin:.25rem 0 0}.risk-box{background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:1.25rem}.risk-box h3{color:#92400e;margin:0 0 .5rem;font-size:1rem}.risk-box ul{margin:0 0 0 1.2rem;padding:0;color:#78350f}.risk-box li{margin:.3rem 0}footer{text-align:center;padding:0 2rem 2rem;color:var(--gray-600);font-size:.85rem}@media(max-width:768px){.container{padding:1rem}header h1{font-size:1.5rem}.chart-grid{grid-template-columns:1fr}.stats-grid{grid-template-columns:repeat(2,1fr)}.section{padding:1.3rem}}@media(max-width:430px){.stats-grid{grid-template-columns:1fr}}
</style></head><body><main class="container"><header><h1 id="title"></h1><p class="subtitle" id="subtitle"></p><div class="meta" id="meta"></div></header><section class="stats-grid" id="metrics"></section><section class="section" id="visuals"><h2 class="section-title">Visual analysis</h2><div class="chart-grid" id="primary-charts"></div><div id="secondary-chart" hidden><h3 class="chart-heading" id="secondary-title"></h3><div class="chart-container" style="height:400px"><canvas id="termsChart"></canvas></div><p class="chart-caption" id="secondary-caption"></p></div></section><section class="section" id="inventors"><h2 class="section-title">Inventor distribution</h2><div class="chart-container" id="inventor-chart-box" style="height:400px"><canvas id="inventorChart"></canvas></div><p class="empty-state" id="inventor-empty" hidden></p><p class="chart-caption" id="inventor-caption"></p></section><section class="section" id="findings"><h2 class="section-title">Key observations</h2><ul class="observation-list" id="insights"></ul></section><section class="section" id="focus"><h2 class="section-title">Other noteworthy themes</h2><div class="focus-grid" id="focus-cards"></div></section><section class="section" id="limits"><h2 class="section-title">Major risks and uncertainties</h2><div class="risk-box"><h3>Analysis limitations</h3><ul id="limitations"></ul></div></section><footer id="source"></footer></main><script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script><script>
const report=__PAYLOAD__,palette=['#2563eb','#059669','#d97706','#dc2626','#7c3aed','#0891b2'];
const add=(parent,tag,text,cls)=>{const e=document.createElement(tag);if(cls)e.className=cls;e.textContent=text;parent.append(e);return e};
document.title=report.title;add(document.getElementById('title'),'span',report.title);document.getElementById('subtitle').textContent=report.subtitle||'Biomedical patent trends report';(report.metadata||[]).forEach(item=>add(document.getElementById('meta'),'span',`${item.label}: ${item.value}`));
(report.metrics||[]).forEach((metric,index)=>{const card=document.createElement('article');card.className=`stat-card ${['','success','warning','danger','success'][index%5]}`;add(card,'div',metric.value,'number');add(card,'div',metric.label,'label');document.getElementById('metrics').append(card)});
const items=chart=>(chart.items||[]).filter(item=>Number.isFinite(Number(item.count)));const chartOptions={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>`${ctx.raw} mentions`}}},scales:{y:{beginAtZero:true,grid:{color:'#f1f5f9'}},x:{grid:{display:false}}}};
function makeChart(chart,index){const wrap=document.createElement('div'),heading=add(wrap,'h3',chart.title,'chart-heading'),box=document.createElement('div'),canvas=document.createElement('canvas'),caption=add(wrap,'p',chart.note||'Source: local derived report data.','chart-caption');box.className='chart-container';box.append(canvas);wrap.append(box);document.getElementById('primary-charts').append(wrap);const data=items(chart);new Chart(canvas,{type:index===1?'doughnut':'bar',data:{labels:data.map(x=>x.label),datasets:[{label:'Count',data:data.map(x=>x.count),backgroundColor:index===1?data.map((_,i)=>palette[i%palette.length]):palette[index%palette.length],borderWidth:index===1?0:0,borderRadius:index===1?0:6,barPercentage:.6}]},options:index===1?{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{padding:16,usePointStyle:true}},tooltip:{callbacks:{label:ctx=>`${ctx.label}: ${ctx.raw}`}}}}:chartOptions});}
const charts=report.charts||[];charts.slice(0,2).forEach(makeChart);if(!charts.length)document.getElementById('visuals').hidden=true;if(charts[2]){const chart=charts[2],data=items(chart),section=document.getElementById('secondary-chart');section.hidden=false;document.getElementById('secondary-title').textContent=chart.title;document.getElementById('secondary-caption').textContent=chart.note||'Source: local derived report data.';new Chart(document.getElementById('termsChart'),{type:'bar',data:{labels:data.map(x=>x.label),datasets:[{label:'Frequency',data:data.map(x=>x.count),backgroundColor:'#2563eb',borderRadius:4,barPercentage:.5}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{beginAtZero:true,grid:{color:'#f1f5f9'}},y:{grid:{display:false}}}}});}
const inventorData=items({items:report.inventor_items||[]}).slice(0,15),inventorNote=report.inventor_note||'Source: inventor metadata in local Patent-Mol-Wiki index.md.';document.getElementById('inventor-caption').textContent=inventorNote;if(inventorData.length){new Chart(document.getElementById('inventorChart'),{type:'bar',data:{labels:inventorData.map(x=>x.label),datasets:[{label:'Patents',data:inventorData.map(x=>x.count),backgroundColor:'#7c3aed',borderRadius:4,barPercentage:.55}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>`${ctx.raw} patents`}}},scales:{x:{beginAtZero:true,grid:{color:'#f1f5f9'}},y:{grid:{display:false}}}}});}else{document.getElementById('inventor-chart-box').hidden=true;const empty=document.getElementById('inventor-empty');empty.hidden=false;empty.textContent='Inventor metadata was not available in the analyzed indexes, so no inventor distribution was calculated.';}
const insights=document.getElementById('insights');(report.insights||[]).forEach((item,index)=>{const li=document.createElement('li'),badge=add(li,'span',`Observation ${index+1}`,'obs-badge'),content=document.createElement('div');content.className='obs-content';add(content,'h3',item.title);add(content,'p',item.text);li.append(content);insights.append(li)});if(!(report.insights||[]).length)document.getElementById('findings').hidden=true;
const focus=document.getElementById('focus-cards');(report.focus_items||[]).forEach(item=>{const card=document.createElement('article');card.className='focus-card';add(card,'strong',item.title);add(card,'p',item.text);focus.append(card)});if(!(report.focus_items||[]).length)document.getElementById('focus').hidden=true;
const limits=document.getElementById('limitations');(report.limitations||[]).forEach(item=>add(limits,'li',item));if(!(report.limitations||[]).length)document.getElementById('limits').hidden=true;document.getElementById('source').textContent=report.source_note||'';
</script></body></html>"""


def write_dashboard(
    out: Path,
    *,
    title: str,
    metrics: list[dict[str, Any]],
    charts: list[dict[str, Any]],
    source_note: str,
    subtitle: str = "",
    metadata: list[dict[str, Any]] | None = None,
    insights: list[dict[str, str]] | None = None,
    focus_items: list[dict[str, str]] | None = None,
    limitations: list[str] | None = None,
    inventor_items: list[dict[str, Any]] | None = None,
    inventor_note: str = "",
) -> None:
    """Create a report-style visualization without patent lookup or search controls."""
    payload = json.dumps(
        {
            "title": title,
            "subtitle": subtitle,
            "metadata": metadata or [],
            "metrics": metrics,
            "charts": charts,
            "insights": insights or [],
            "focus_items": focus_items or [],
            "limitations": limitations or [],
            "inventor_items": inventor_items or [],
            "inventor_note": inventor_note,
            "source_note": source_note,
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    out.write_text(
        PAGE.replace("__TITLE__", html.escape(title)).replace("__PAYLOAD__", payload),
        encoding="utf-8",
    )
