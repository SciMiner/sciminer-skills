#!/usr/bin/env python3
"""Generate phone-size HTML posters for each SciMiner skill."""
import json
import pathlib

OUT = pathlib.Path(__file__).parent

SKILLS = [
    {
        "key": "admet-pkpd", "theme": "t-admet", "emoji": "💊",
        "category": "ADMET · PK/PD",
        "title": "Drug Property Forecasting",
        "tagline": "Predict ADMET, metabolism & bioavailability — before you synthesize.",
        "summary": "Forecast safety endpoints, pharmacokinetic profiles, and molecular descriptors for any small molecule. The triage layer for drug-likeness, CYP metabolism, BBB penetration, and toxicity.",
        "caps": [
            "ADMET endpoints — hERG, CYP, BBB, Caco-2, AMES",
            "AOX oxidative metabolism & site-of-metabolism",
            "Oral bioavailability at user-specified dose",
            "pKa and ionization-state calculation",
            "Aqueous solvation free-energy prediction",
        ],
        "inputs": "Single SMILES or SDF / CSV library",
        "outputs": "Endpoint table + descriptors, PK summary",
    },
    {
        "key": "antibody-engineering", "theme": "t-antibody", "emoji": "🧪",
        "category": "Antibody Engineering",
        "title": "Antibody Sequence Optimization",
        "tagline": "Humanize, mature, and de-risk antibodies in silico.",
        "summary": "End-to-end mAb optimization combining numbering, humanization, structure prediction, energetic mutation scanning, and developability scoring — built for affinity maturation and candidate panel generation.",
        "caps": [
            "ANARCI numbering & region parsing",
            "Humanness assessment & humanization (BioPhi)",
            "3D structure prediction & relaxation (IgFold, Rosetta)",
            "Affinity & stability mutation scanning (FoldX)",
            "Aggregation risk scoring (SAP)",
        ],
        "inputs": "Heavy & light chain FASTA sequences",
        "outputs": "Optimized variants with ΔΔG, humanness & SAP",
    },
    {
        "key": "binding-site-prediction", "theme": "t-pocket", "emoji": "🎯",
        "category": "Pocket Detection",
        "title": "Protein Binding Pocket Finder",
        "tagline": "Find druggable pockets before docking ever begins.",
        "summary": "Detect ligand-binding pockets with ML- and geometry-based methods. The first step before docking or virtual screening — turn a bare structure into a ranked pocket list with docking-ready coordinates.",
        "caps": [
            "ML pocket ranking with P2Rank",
            "Geometric detection & descriptors (fpocket)",
            "Per-residue probability via AF2BIND",
            "Cross-method consensus validation",
            "Pocket centroids ready for docking-box setup",
        ],
        "inputs": "Protein structure (PDB ID or file upload)",
        "outputs": "Ranked pockets, confidence scores, residue lists",
    },
    {
        "key": "molecular-docking", "theme": "t-docking", "emoji": "🔗",
        "category": "Molecular Docking",
        "title": "Multi-Engine Docking Suite",
        "tagline": "Five docking engines, one consistent interface.",
        "summary": "Score ligand–protein complexes through deep-learning, force-field, flexible-receptor, surface-aware, and diffusion-based engines. Pick the right method for the right task — or run them in concert.",
        "caps": [
            "Gnina — deep-learning pocket-guided docking",
            "AutoDock Vina — classical force-field",
            "PackDock — flexible side-chain repacking",
            "SurfDock — surface-geometry-aware",
            "DiffDock — diffusion-model docking",
        ],
        "inputs": "Ligand (SMILES/SDF/MOL2) + protein PDB",
        "outputs": "Docked poses, binding scores, RMSD metrics",
    },
    {
        "key": "optical-chemical-structure-recognition", "theme": "t-ocsr", "emoji": "📸",
        "category": "Chemistry OCR",
        "title": "Optical Structure Recognition",
        "tagline": "Turn any chemistry figure into machine-readable SMILES.",
        "summary": "Convert drawn, photographed, or screenshotted chemical structures into SMILES and names. Digitize paper figures, patents, slides, and handwritten chemistry in seconds.",
        "caps": [
            "Multi-structure extraction from one image",
            "Molecule name recovery from image text",
            "Figure → SMILES conversion at scale",
            "Drawing interpretation & validation",
            "Batch image processing",
        ],
        "inputs": "Chemistry image (PNG / JPG / PDF page)",
        "outputs": "SMILES strings, structure data, molecule names",
    },
    {
        "key": "peptide-design", "theme": "t-peptide", "emoji": "🧬",
        "category": "Peptide Design",
        "title": "Peptide & Macrocycle Design",
        "tagline": "Design cyclic, linear, and macrocyclic binders.",
        "summary": "Generate and optimize peptide binders against a protein target — cyclic backbones included. Couple docking, sequence design, structure validation, and property prediction into a single workflow.",
        "caps": [
            "Pocket-guided peptide docking (PocketXMol)",
            "Cyclic & macrocyclic backbone generation",
            "Sequence design (ProteinMPNN / CyclicMPNN)",
            "Structure validation (AfCycDesign)",
            "Physico-chemical props & extinction coefficient",
        ],
        "inputs": "Target protein structure or peptide FASTA",
        "outputs": "Designed sequences, 3D structures, properties",
    },
    {
        "key": "pharma-intelligence", "theme": "t-pharma", "emoji": "🌍",
        "category": "Pharma Intelligence",
        "title": "Global Drug & Trial Intelligence",
        "tagline": "Trials, approvals, patents, targets — worldwide, instantly.",
        "summary": "Search regulatory, clinical-trial, patent, and academic databases across the US, EU, China, Japan, Korea, and Australia. The competitive-landscape and drug-repurposing engine for biomedical research.",
        "caps": [
            "Multi-region trial search (CT.gov, NMPA, ChiCTR, jRCT, CRIS)",
            "Approval status (FDA, EMA, PMDA, MFDS, TGA)",
            "Patent & exclusivity expiry lookup",
            "Adverse-event & safety profiling",
            "Target discovery & drug-repurposing analysis",
        ],
        "inputs": "Drug, target, indication, company, or gene",
        "outputs": "Trials, approvals, patents, competitive views",
    },
    {
        "key": "protein-design", "theme": "t-protein", "emoji": "🧬",
        "category": "Protein Design",
        "title": "De Novo Protein & Binder Design",
        "tagline": "Design proteins, nanobodies, and binders against any target.",
        "summary": "De novo design of proteins, antibodies, and nanobodies against antigen or small-molecule targets via BoltzGen. Generate ensemble candidate panels ready for downstream screening.",
        "caps": [
            "Protein-to-protein binder design",
            "Peptide & linear binder design",
            "Antibody and nanobody generation",
            "Small-molecule binding-protein design",
            "Ensemble-based candidate generation",
        ],
        "inputs": "Target antigen structure or SMILES",
        "outputs": "Designed sequences and 3D structures",
    },
    {
        "key": "ready-tools-on-sciminer", "theme": "t-ready", "emoji": "🛠️",
        "category": "Universal Access",
        "title": "Any SciMiner Tool, On Demand",
        "tagline": "Call any published SciMiner tool — auto-documented.",
        "summary": "Dynamically discover and invoke any published SciMiner tool by name. The universal fallback when a specific tool is needed but no dedicated skill covers it — with automatic payload generation and result polling.",
        "caps": [
            "Dynamic discovery from the published index",
            "Automatic API documentation retrieval",
            "Payload generation from the tool registry",
            "File upload & async result polling",
            "Shareable result URLs",
        ],
        "inputs": "Tool name + user parameters",
        "outputs": "Results JSON & SciMiner share URLs",
    },
    {
        "key": "small-molecule-design", "theme": "t-smol", "emoji": "🧫",
        "category": "Small-Molecule Design",
        "title": "Generative Small-Molecule Design",
        "tagline": "Structure-free or pocket-guided — generate druglike chemistry.",
        "summary": "De novo generation with REINVENT4 (structure-free) or PocketXMol (pocket-guided). Hit-to-lead optimization, scaffold hopping, fragment growing, and post-generation scoring in one flow.",
        "caps": [
            "RL molecule generation (REINVENT4)",
            "Transfer learning & scaffold hopping",
            "Pocket-guided design (PocketXMol)",
            "Fragment linking & growing",
            "Post-generation scoring (Gnina)",
        ],
        "inputs": "Pocket coordinates and/or target protein",
        "outputs": "SMILES with docking scores & desirability",
    },
    {
        "key": "structure-prediction", "theme": "t-structure", "emoji": "🏗️",
        "category": "Structure Prediction",
        "title": "Multimodal Complex Prediction",
        "tagline": "Predict proteins, DNA, RNA, ligands — together.",
        "summary": "Predict biomolecular structures including proteins, nucleic acids, ligands, and mixed assemblies with Chai-1, Boltz-2, or AlphaFold3. The modeling engine for complex assemblies and interactions.",
        "caps": [
            "Protein & protein-complex prediction",
            "Protein–DNA and protein–RNA complexes",
            "Ligand-bound and covalent modeling",
            "MSA, template, and restraint inputs",
            "Multi-chain assemblies with confidence",
        ],
        "inputs": "Sequences + ligand SMILES + optional MSA",
        "outputs": "3D coordinates with per-residue confidence",
    },
    {
        "key": "synthesis-evaluation", "theme": "t-synthesis", "emoji": "⚗️",
        "category": "Synthesis Evaluation",
        "title": "Retrosynthesis & Accessibility",
        "tagline": "Score synthetic feasibility before you commit to chemistry.",
        "summary": "Generate synthesizable analogs, propose retrosynthetic routes, and score synthetic accessibility. Use to triage candidates before procurement or synthesis.",
        "caps": [
            "Synthesizable analog generation (SynFormer)",
            "Retrosynthetic route recommendation",
            "Synthetic-accessibility scoring (SAScore)",
            "Batch molecule processing",
            "Chemical reaction pathway exploration",
        ],
        "inputs": "Target molecule SMILES or SDF file",
        "outputs": "Analogs, routes, and SAScore values",
    },
    {
        "key": "virtual-screening", "theme": "t-screening", "emoji": "🔍",
        "category": "Virtual Screening",
        "title": "High-Throughput Library Screening",
        "tagline": "Find binding hits across massive compound libraries.",
        "summary": "Screen proprietary or commercial libraries against a protein target via transformer-based CPI or docking-based methods. The hit-discovery engine for early drug discovery.",
        "caps": [
            "Transformer-based CPI library screening",
            "Docking-based library screening",
            "Automatic docking-box calculation",
            "Protein sequence retrieval from UniProt",
            "Hit ranking and clustering",
        ],
        "inputs": "Target protein sequence or structure",
        "outputs": "Ranked hits with scoring & binding predictions",
    },
]

POSTER_TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title} · SciMiner</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="styles.css" />
</head>
<body class="stage">
  <section class="poster {theme}">
    <div class="brandbar">
      <span class="brand"><span class="dot"></span>SciMiner</span>
      <span class="index">{idx:02d} / 13</span>
    </div>

    <div class="hero">
      <span class="emoji">{emoji}</span>
      <span class="category">{category}</span>
      <h1>{title}</h1>
      <p class="tagline">{tagline}</p>
      <p class="summary">{summary}</p>
    </div>

    <div class="section-label">Capabilities</div>
    <div class="caps">
{caps_html}
    </div>

    <div class="io">
      <div class="box">
        <div class="label">Input</div>
        <div class="value">{inputs}</div>
      </div>
      <div class="box">
        <div class="label">Output</div>
        <div class="value">{outputs}</div>
      </div>
    </div>

    <div class="footer">
      <span class="url">sciminer.tech</span>
      <span class="cta">Drug Discovery · AI Agent</span>
    </div>
  </section>
</body>
</html>
"""

CAP_TPL = '      <div class="cap"><span class="bullet">{n:02d}</span><span>{txt}</span></div>'

def render_poster(idx: int, s: dict) -> str:
    caps_html = "\n".join(CAP_TPL.format(n=i + 1, txt=c) for i, c in enumerate(s["caps"]))
    return POSTER_TPL.format(
        idx=idx, theme=s["theme"], emoji=s["emoji"], category=s["category"],
        title=s["title"], tagline=s["tagline"], summary=s["summary"],
        caps_html=caps_html, inputs=s["inputs"], outputs=s["outputs"],
    )

HERO_TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>SciMiner · Drug Discovery AI Agent</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="styles.css" />
</head>
<body class="stage">
  <section class="poster overview">
    <div class="brandbar">
      <span class="brand"><span class="dot"></span>SciMiner</span>
      <span class="index">00 / 13</span>
    </div>

    <div class="hero">
      <span class="kicker">AI Agent for Drug Discovery</span>
      <h1 class="big">Discover.<br/>Design.<br/>Decide.</h1>
      <p class="lead">From target to candidate — 13 expert skills powering the SciMiner agent across the entire drug-discovery stack.</p>
    </div>

    <div class="stats">
      <div class="stat"><div class="num">13</div><div class="lbl">Skills</div></div>
      <div class="stat"><div class="num">25+</div><div class="lbl">Tools</div></div>
      <div class="stat"><div class="num">6</div><div class="lbl">Regions</div></div>
    </div>

    <div class="section-label">The Stack</div>
    <div class="skill-grid">
{tiles}
    </div>

    <div class="footer">
      <span class="url">sciminer.tech</span>
      <span class="cta">One Agent · End to End</span>
    </div>
  </section>
</body>
</html>
"""

TILE_TPL = '      <a class="skill-tile" href="{key}.html" style="text-decoration:none;color:inherit"><span class="ic">{emoji}</span><span>{label}</span></a>'

INDEX_TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>SciMiner Skill Posters</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="styles.css" />
</head>
<body>
  <main class="gallery">
    <header>
      <div class="kicker">SciMiner · Skill Gallery</div>
      <h1>The Drug-Discovery AI Agent, in 14 Posters</h1>
      <p>Phone-size posters showing the SciMiner agent's full skill stack — from chemistry OCR to global pharma intelligence. Tap any poster to open it full screen on a phone.</p>
    </header>

    <section class="shelf">
{thumbs}
    </section>
  </main>
</body>
</html>
"""

THUMB_TPL = """      <a class="thumb" href="{href}" target="_blank" rel="noopener">
        <div class="frame"><iframe src="{href}" loading="lazy" title="{label}"></iframe></div>
        <div class="caption">{label}<span class="sub">{sub}</span></div>
      </a>"""

def main():
    # per-skill posters
    for i, s in enumerate(SKILLS, start=1):
        (OUT / f"{s['key']}.html").write_text(render_poster(i, s), encoding="utf-8")

    # overview hero poster
    tiles = "\n".join(
        TILE_TPL.format(key=s["key"], emoji=s["emoji"], label=s["category"])
        for s in SKILLS
    )
    (OUT / "hero.html").write_text(HERO_TPL.format(tiles=tiles), encoding="utf-8")

    # index gallery
    thumbs = [THUMB_TPL.format(href="hero.html", label="SciMiner · Overview", sub="Start here")]
    for s in SKILLS:
        thumbs.append(THUMB_TPL.format(href=f"{s['key']}.html", label=s["title"], sub=s["category"]))
    (OUT / "index.html").write_text(INDEX_TPL.format(thumbs="\n".join(thumbs)), encoding="utf-8")

    print(f"Wrote {len(SKILLS) + 2} files to {OUT}")

if __name__ == "__main__":
    main()
