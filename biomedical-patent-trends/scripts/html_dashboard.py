"""Write a flexible, standalone HTML patent-trends report."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


DEFAULT_SECTION_LABELS = {
    "visual_analysis": "Visual analysis",
    "applicant_distribution": "Applicant distribution",
    "key_observations": "Key observations",
    "noteworthy_themes": "Other noteworthy themes",
    "risks_uncertainties": "Major risks and uncertainties",
    "analysis_limitations": "Analysis limitations",
    "observation": "Observation",
    "count": "Count",
    "frequency": "Frequency",
    "patents": "patents",
    "mentions": "mentions",
    "default_subtitle": "Biomedical patent trends report",
    "source_fallback": "Source: local derived report data.",
    "applicant_unavailable": (
        "Applicant metadata was not available in the analyzed indexes, "
        "so no applicant distribution was calculated."
    ),
}


PAGE = r"""<!doctype html>
<html lang="__LANG__"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title><style>
:root{--primary:#2563eb;--primary-light:#dbeafe;--success:#059669;--warning:#d97706;--danger:#dc2626;--surface:#fff;--bg:#f8fafc;--line:#e2e8f0;--muted:#475569;--text:#1e293b;--heading:#0f172a}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif}.container{max-width:1400px;margin:0 auto;padding:2rem}header{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;padding:3rem 2rem;border-radius:16px;margin-bottom:2rem;box-shadow:0 10px 40px rgba(37,99,235,.2)}header h1{font-size:2rem;line-height:1.25;margin:0 0 .5rem}.subtitle{opacity:.9;font-size:1.05rem;margin:0}.meta{margin-top:1rem;display:flex;gap:.6rem 2rem;flex-wrap:wrap;font-size:.9rem;opacity:.85}.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1.5rem;margin-bottom:2rem}.stat-card,.section{background:var(--surface);border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.1)}.stat-card{padding:1.5rem;border-left:4px solid var(--primary)}.stat-card .number{font-size:2.25rem;font-weight:700;color:var(--primary);line-height:1}.stat-card .label{color:var(--muted);font-size:.9rem;margin-top:.5rem}.stat-card.success{border-left-color:var(--success)}.stat-card.success .number{color:var(--success)}.stat-card.warning{border-left-color:var(--warning)}.stat-card.warning .number{color:var(--warning)}.stat-card.danger{border-left-color:var(--danger)}.stat-card.danger .number{color:var(--danger)}.section{padding:2rem;margin-bottom:2rem}.section-title{font-size:1.4rem;color:var(--heading);margin:0 0 1.5rem;display:flex;align-items:center;gap:.5rem}.section-title:before{content:"";width:4px;height:24px;background:var(--primary);border-radius:2px}.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:2rem}.chart-block.wide{grid-column:1/-1}.chart-heading{margin:0 0 1rem;color:var(--muted);font-size:1rem}.chart-container{position:relative;height:350px}.chart-caption{font-size:.8rem;color:var(--muted);margin:.75rem 0 0}.empty-state{background:var(--bg);border:1px dashed var(--line);border-radius:8px;color:var(--muted);padding:1.25rem}.observation-list{list-style:none;margin:0;padding:0}.observation-list li{padding:1rem 0;border-bottom:1px solid var(--line);display:flex;gap:1rem;align-items:flex-start}.observation-list li:last-child{border-bottom:0}.obs-badge{background:var(--primary-light);color:var(--primary);font-weight:700;padding:.25rem .75rem;border-radius:6px;font-size:.85rem;white-space:nowrap}.obs-content h3{font-size:1.05rem;margin:0 0 .25rem;color:var(--heading)}.obs-content p{color:var(--muted);font-size:.95rem;margin:0}.focus-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem}.focus-card{background:var(--bg);padding:1rem;border-radius:8px}.focus-card strong{color:var(--primary)}.focus-card p{font-size:.85rem;color:var(--muted);margin:.25rem 0 0}.risk-box{background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:1.25rem}.risk-box h3{color:#92400e;margin:0 0 .5rem;font-size:1rem}.risk-box ul{margin:0 0 0 1.2rem;padding:0;color:#78350f}footer{text-align:center;padding:0 2rem 2rem;color:var(--muted);font-size:.85rem}@media(max-width:768px){.container{padding:1rem}header{padding:2rem 1.3rem}header h1{font-size:1.5rem}.chart-grid{grid-template-columns:1fr}.section{padding:1.3rem}}@media(max-width:430px){.stats-grid{grid-template-columns:1fr}}
__CUSTOM_CSS__
</style></head><body><main class="container">
<header><h1 id="title"></h1><p class="subtitle" id="subtitle"></p><div class="meta" id="meta"></div></header>
<section class="stats-grid" id="metrics"></section>
<section class="section" id="visuals"><h2 class="section-title" data-label="visual_analysis"></h2><div class="chart-grid" id="charts"></div></section>
<section class="section" id="applicants"><h2 class="section-title" data-label="applicant_distribution"></h2><div class="chart-container" id="applicant-chart-box" style="height:400px"><canvas id="applicantChart"></canvas></div><p class="empty-state" id="applicant-empty" hidden></p><p class="chart-caption" id="applicant-caption"></p></section>
<section class="section" id="findings"><h2 class="section-title" data-label="key_observations"></h2><ul class="observation-list" id="insights"></ul></section>
<section class="section" id="focus"><h2 class="section-title" data-label="noteworthy_themes"></h2><div class="focus-grid" id="focus-cards"></div></section>
<section class="section" id="limits"><h2 class="section-title" data-label="risks_uncertainties"></h2><div class="risk-box"><h3 data-label="analysis_limitations"></h3><ul id="limitations"></ul></div></section>
<footer id="source"></footer></main>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script><script>
const report=__PAYLOAD__,labels=report.section_labels,palette=['#2563eb','#059669','#d97706','#dc2626','#7c3aed','#0891b2'];
const add=(parent,tag,text,cls)=>{const e=document.createElement(tag);if(cls)e.className=cls;e.textContent=text;parent.append(e);return e};
document.querySelectorAll('[data-label]').forEach(node=>node.textContent=labels[node.dataset.label]||node.dataset.label);
document.title=report.title;add(document.getElementById('title'),'span',report.title);
document.getElementById('subtitle').textContent=report.subtitle||labels.default_subtitle;
(report.metadata||[]).forEach(item=>add(document.getElementById('meta'),'span',`${item.label}: ${item.value}`));
(report.metrics||[]).forEach((metric,index)=>{const card=document.createElement('article');card.className=`stat-card ${['','success','warning','danger','success'][index%5]}`;add(card,'div',metric.value,'number');add(card,'div',metric.label,'label');document.getElementById('metrics').append(card)});
const validItems=items=>(items||[]).filter(item=>Number.isFinite(Number(item.count)));
function makeChart(chart,index){const data=validItems(chart.items),wrap=document.createElement('article');wrap.className=`chart-block ${index>1?'wide':''}`;add(wrap,'h3',chart.title,'chart-heading');const box=document.createElement('div');box.className='chart-container';const canvas=document.createElement('canvas');box.append(canvas);wrap.append(box);add(wrap,'p',chart.note||labels.source_fallback,'chart-caption');document.getElementById('charts').append(wrap);if(!data.length){box.hidden=true;add(wrap,'p',chart.empty_text||chart.note||labels.source_fallback,'empty-state');return}const doughnut=chart.type==='doughnut';new Chart(canvas,{type:doughnut?'doughnut':'bar',data:{labels:data.map(x=>x.label),datasets:[{label:labels.count,data:data.map(x=>x.count),backgroundColor:doughnut?data.map((_,i)=>palette[i%palette.length]):palette[index%palette.length],borderWidth:0,borderRadius:doughnut?0:6,barPercentage:.6}]},options:doughnut?{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{padding:16,usePointStyle:true}},tooltip:{callbacks:{label:ctx=>`${ctx.label}: ${ctx.raw}`}}}}:{indexAxis:chart.horizontal?'y':'x',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>`${ctx.raw} ${labels.mentions}`}}},scales:{x:{beginAtZero:Boolean(chart.horizontal),grid:{display:!chart.horizontal}},y:{beginAtZero:!chart.horizontal,grid:{display:Boolean(chart.horizontal)}}}}})}
(report.charts||[]).forEach(makeChart);if(!(report.charts||[]).length)document.getElementById('visuals').hidden=true;
const applicantData=validItems(report.applicant_items).slice(0,15);document.getElementById('applicant-caption').textContent=report.applicant_note||labels.source_fallback;
if(applicantData.length){new Chart(document.getElementById('applicantChart'),{type:'bar',data:{labels:applicantData.map(x=>x.label),datasets:[{label:labels.patents,data:applicantData.map(x=>x.count),backgroundColor:'#7c3aed',borderRadius:4,barPercentage:.55}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>`${ctx.raw} ${labels.patents}`}}},scales:{x:{beginAtZero:true},y:{grid:{display:false}}}}})}else{document.getElementById('applicant-chart-box').hidden=true;const empty=document.getElementById('applicant-empty');empty.hidden=false;empty.textContent=labels.applicant_unavailable}
const insights=document.getElementById('insights');(report.insights||[]).forEach((item,index)=>{const li=document.createElement('li');add(li,'span',`${labels.observation} ${index+1}`,'obs-badge');const content=document.createElement('div');content.className='obs-content';add(content,'h3',item.title);add(content,'p',item.text);li.append(content);insights.append(li)});if(!(report.insights||[]).length)document.getElementById('findings').hidden=true;
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
    applicant_items: list[dict[str, Any]] | None = None,
    applicant_note: str = "",
    language: str = "en",
    section_labels: dict[str, str] | None = None,
    custom_css: str = "",
) -> None:
    """Create a localized report whose content, composition, and styling may vary."""
    if not language.lower().startswith("en"):
        missing_labels = sorted(DEFAULT_SECTION_LABELS.keys() - (section_labels or {}).keys())
        if missing_labels:
            raise ValueError(
                "Non-English reports must localize every section label: "
                + ", ".join(missing_labels)
            )
    labels = {**DEFAULT_SECTION_LABELS, **(section_labels or {})}
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
            "applicant_items": applicant_items or [],
            "applicant_note": applicant_note,
            "source_note": source_note,
            "section_labels": labels,
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    rendered = (
        PAGE.replace("__LANG__", html.escape(language, quote=True))
        .replace("__TITLE__", html.escape(title))
        .replace("__CUSTOM_CSS__", custom_css.replace("</style", r"<\/style"))
        .replace("__PAYLOAD__", payload)
    )
    out.write_text(rendered, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a localized patent-trends payload as standalone HTML."
    )
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--language", required=True)
    parser.add_argument("--custom-css", type=Path)
    args = parser.parse_args()
    report = json.loads(args.payload.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise SystemExit("The report payload must be a JSON object.")
    report["language"] = args.language
    if args.custom_css:
        report["custom_css"] = args.custom_css.read_text(encoding="utf-8")
    try:
        write_dashboard(args.out, **report)
    except TypeError as exc:
        raise SystemExit(f"Invalid report payload: {exc}") from exc


if __name__ == "__main__":
    main()
