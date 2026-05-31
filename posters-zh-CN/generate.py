#!/usr/bin/env python3
"""Generate standalone Chinese HTML posters for each SciMiner skill."""

import pathlib

OUT = pathlib.Path(__file__).parent

FONT_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Noto+Sans+SC:wght@400;500;600;700;800&'
    'family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />'
)

UI = {
    "capabilities": "核心能力",
    "input": "输入",
    "output": "输出",
    "footer_cta": "药物发现 · AI 智能体",
    "hero_title": "SciMiner · 药物发现 AI 智能体",
    "hero_kicker": "面向药物发现的 AI 智能体",
    "hero_heading": "发现<br/>设计<br/>决策",
    "hero_lead": "从靶点到候选分子，13 项专家级技能覆盖 SciMiner 的完整药物发现流程。可通过以下入口直接安装：",
    "hero_links": [
        ("https://github.com/SciMiner/sciminer-skills", "GitHub: github.com/SciMiner/sciminer-skills"),
        ("https://clawhub.ai/user/sciminer", "Clawhub: clawhub.ai/user/sciminer"),
    ],
    "hero_stats": [("13", "技能"), ("150+", "工具"), ("6", "区域")],
    "hero_stack": "能力栈",
    "hero_footer": "一个智能体 · 端到端",
    "gallery_title": "SciMiner 中文技能海报",
    "gallery_kicker": "SciMiner · 中文海报集",
    "gallery_heading": "药物发现 AI 智能体",
    "gallery_blurb": "适配手机尺寸的 14 张海报，展示 SciMiner 从化学 OCR 到全球医药情报的完整技能栈。点击任意海报即可在手机端全屏查看。",
    "overview_label": "SciMiner · 总览",
    "overview_sub": "从这里开始",
}

SKILLS = [
    {
        "key": "admet-pkpd",
        "theme": "t-admet",
        "emoji": "💊",
        "category": "ADMET · PK/PD",
        "title": "药物性质预测",
        "tagline": "在合成之前，先预测 ADMET、代谢与生物利用度。",
        "summary": "面向任意小分子预测安全性终点、药代动力学特征和分子描述符，用作药物相似性、CYP 代谢、BBB 穿透和毒性分层筛选的首道关口。",
        "caps": [
            "ADMET 端点：hERG、CYP、BBB、Caco-2、AMES",
            "AOX 氧化代谢与代谢位点预测",
            "指定给药剂量下的口服生物利用度",
            "pKa 与电离状态计算",
            "水相溶剂化自由能预测",
        ],
        "inputs": "单个 SMILES 或 SDF / CSV 分子库",
        "outputs": "终点表 + 描述符，PK 摘要",
    },
    {
        "key": "antibody-engineering",
        "theme": "t-antibody",
        "emoji": "🧪",
        "category": "抗体工程",
        "title": "抗体序列优化",
        "tagline": "在计算机中完成人源化、成熟化与可开发性降风险。",
        "summary": "面向单抗的端到端优化流程，结合编号、人源化、结构预测、能量突变扫描与可开发性评分，用于亲和力成熟和候选抗体面板生成。",
        "caps": [
            "ANARCI 编号与区域解析",
            "人源性评估与人源化（BioPhi）",
            "3D 结构预测与弛豫（IgFold、Rosetta）",
            "亲和力与稳定性突变扫描（FoldX）",
            "聚集风险评分（SAP）",
        ],
        "inputs": "重链与轻链 FASTA 序列",
        "outputs": "含 ΔΔG、人源性与 SAP 的优化变体",
    },
    {
        "key": "binding-site-prediction",
        "theme": "t-pocket",
        "emoji": "🎯",
        "category": "口袋检测",
        "title": "蛋白结合口袋发现",
        "tagline": "在开始对接之前，先找到可成药口袋。",
        "summary": "结合机器学习和几何方法检测配体结合口袋，是分子对接和虚拟筛选前的第一步。将裸蛋白结构转化为带排序、可直接用于对接框设置的口袋列表。",
        "caps": [
            "P2Rank 机器学习口袋排序",
            "几何口袋检测与描述符分析（fpocket）",
            "AF2BIND 残基级结合概率",
            "多方法共识验证",
            "可直接用于 docking box 设置的口袋中心",
        ],
        "inputs": "蛋白结构（PDB ID 或上传文件）",
        "outputs": "排序口袋、置信度分数与残基列表",
    },
    {
        "key": "molecular-docking",
        "theme": "t-docking",
        "emoji": "🔗",
        "category": "分子对接",
        "title": "多引擎分子对接套件",
        "tagline": "五种对接引擎，一个一致接口。",
        "summary": "通过深度学习、力场、柔性受体、表面感知和扩散模型等多类引擎评估配体-蛋白复合物。按任务选择最佳方法，或并行综合运行。",
        "caps": [
            "Gnina：深度学习口袋引导对接",
            "AutoDock Vina：经典力场对接",
            "PackDock：柔性侧链接触重排",
            "SurfDock：表面几何感知对接",
            "DiffDock：扩散模型对接",
        ],
        "inputs": "配体（SMILES/SDF/MOL2）+ 蛋白 PDB",
        "outputs": "对接构象、结合评分与 RMSD 指标",
    },
    {
        "key": "optical-chemical-structure-recognition",
        "theme": "t-ocsr",
        "emoji": "📸",
        "category": "化学 OCR",
        "title": "化学结构光学识别",
        "tagline": "把任意化学结构图转成机器可读的 SMILES。",
        "summary": "将绘制、拍摄或截图得到的化学结构图转换为 SMILES 和名称。论文图、专利、幻灯片和手写化学式都能快速数字化。",
        "caps": [
            "单张图片多结构提取",
            "从图中文字恢复分子名称",
            "批量图像到 SMILES 转换",
            "手绘结构解释与校验",
            "批量图片处理",
        ],
        "inputs": "化学结构图（PNG / JPG / PDF 页面）",
        "outputs": "SMILES、结构数据与分子名称",
    },
    {
        "key": "peptide-design",
        "theme": "t-peptide",
        "emoji": "🧬",
        "category": "多肽设计",
        "title": "多肽与大环设计",
        "tagline": "设计环肽、线性肽与大环结合物。",
        "summary": "围绕蛋白靶点生成并优化多肽结合物，支持环状骨架。将对接、序列设计、结构验证和性质预测串联为一体化流程。",
        "caps": [
            "口袋引导多肽对接（PocketXMol）",
            "环肽与大环骨架生成",
            "序列设计（ProteinMPNN / CyclicMPNN）",
            "结构验证（AfCycDesign）",
            "理化性质与消光系数预测",
        ],
        "inputs": "靶蛋白结构或多肽 FASTA",
        "outputs": "设计序列、3D 结构与性质",
    },
    {
        "key": "pharma-intelligence",
        "theme": "t-pharma",
        "emoji": "🌍",
        "category": "医药情报",
        "title": "全球药物与临床试验情报",
        "tagline": "试验、上市、专利、靶点，一次覆盖全球。",
        "summary": "检索美国、欧盟、中国、日本、韩国和澳大利亚的监管、临床试验、专利及学术数据库，用于竞争格局分析和药物再利用研究。",
        "caps": [
            "多地区试验检索（CT.gov、NMPA、ChiCTR、jRCT、CRIS）",
            "上市审批状态（FDA、EMA、PMDA、MFDS、TGA）",
            "专利与市场独占期到期查询",
            "不良事件与安全性画像",
            "靶点发现与药物再定位分析",
        ],
        "inputs": "药物、靶点、适应症、公司或基因",
        "outputs": "试验、审批、专利与竞争态势视图",
    },
    {
        "key": "protein-design",
        "theme": "t-protein",
        "emoji": "🧬",
        "category": "蛋白设计",
        "title": "从头蛋白与结合体设计",
        "tagline": "针对任意靶点设计蛋白、纳米抗体与结合体。",
        "summary": "借助 BoltzGen，面向抗原或小分子靶点从头设计蛋白、抗体和纳米抗体，并生成可供下游筛选的候选面板。",
        "caps": [
            "蛋白-蛋白结合体设计",
            "多肽与线性结合体设计",
            "抗体与纳米抗体生成",
            "小分子结合蛋白设计",
            "基于集成采样的候选生成",
        ],
        "inputs": "目标抗原结构或 SMILES",
        "outputs": "设计序列与 3D 结构",
    },
    {
        "key": "ready-tools-on-sciminer",
        "theme": "t-ready",
        "emoji": "🛠️",
        "category": "通用调用",
        "title": "按需调用任意 SciMiner 工具",
        "tagline": "调用已发布的任意 SciMiner 工具，并自动补全文档。",
        "summary": "按工具名动态发现并调用任意已发布的 SciMiner 工具。当需要特定能力但尚无专用 skill 时，可作为通用兜底方案，并自动生成请求载荷和轮询结果。",
        "caps": [
            "从公开索引动态发现工具",
            "自动拉取 API 文档",
            "依据工具注册信息生成请求参数",
            "文件上传与异步结果轮询",
            "可分享的结果链接",
        ],
        "inputs": "工具名 + 用户参数",
        "outputs": "结果 JSON 与 SciMiner 分享链接",
    },
    {
        "key": "small-molecule-design",
        "theme": "t-smol",
        "emoji": "🧫",
        "category": "小分子设计",
        "title": "生成式小分子设计",
        "tagline": "无结构先验或口袋引导，都能生成成药化学空间。",
        "summary": "使用 REINVENT4 进行无结构先验生成，或用 PocketXMol 进行口袋引导设计。命中到先导优化、骨架跃迁、片段生长和后评分在同一流程中完成。",
        "caps": [
            "强化学习分子生成（REINVENT4）",
            "迁移学习与骨架跃迁",
            "口袋引导设计（PocketXMol）",
            "片段连接与生长",
            "后生成评分（Gnina）",
        ],
        "inputs": "口袋坐标和/或目标蛋白",
        "outputs": "带对接评分与期望度的 SMILES",
    },
    {
        "key": "structure-prediction",
        "theme": "t-structure",
        "emoji": "🏗️",
        "category": "结构预测",
        "title": "多模态复合体预测",
        "tagline": "蛋白、DNA、RNA、配体，可联合预测。",
        "summary": "使用 Chai-1、Boltz-2 或 AlphaFold3 预测蛋白、核酸、配体及其混合装配体结构，是复杂复合物建模与相互作用分析的核心引擎。",
        "caps": [
            "蛋白与蛋白复合体预测",
            "蛋白-DNA 与蛋白-RNA 复合体",
            "配体结合与共价建模",
            "支持 MSA、模板与约束输入",
            "多链装配及置信度评估",
        ],
        "inputs": "序列 + 配体 SMILES + 可选 MSA",
        "outputs": "含残基级置信度的 3D 坐标",
    },
    {
        "key": "synthesis-evaluation",
        "theme": "t-synthesis",
        "emoji": "⚗️",
        "category": "合成评估",
        "title": "逆合成与可及性评估",
        "tagline": "在投入化学实验之前，先评估合成可行性。",
        "summary": "生成可合成类似物、提出逆合成路线并给出合成可及性评分，用于采购或合成前的候选分流。",
        "caps": [
            "可合成类似物生成（SynFormer）",
            "逆合成路线推荐",
            "合成可及性评分（SAScore）",
            "批量分子处理",
            "化学反应路径探索",
        ],
        "inputs": "目标分子 SMILES 或 SDF 文件",
        "outputs": "类似物、路线与 SAScore 值",
    },
    {
        "key": "virtual-screening",
        "theme": "t-screening",
        "emoji": "🔍",
        "category": "虚拟筛选",
        "title": "高通量分子库筛选",
        "tagline": "在海量化合物库中发现潜在命中。",
        "summary": "使用基于 Transformer 的 CPI 或基于对接的方法，将自有或商业化分子库针对蛋白靶点进行筛选，是早期药物发现阶段的命中发现引擎。",
        "caps": [
            "基于 Transformer 的 CPI 分子库筛选",
            "基于对接的分子库筛选",
            "自动计算 docking box",
            "从 UniProt 自动获取蛋白序列",
            "命中排序与聚类",
        ],
        "inputs": "靶蛋白序列或结构",
        "outputs": "带评分与结合预测的排序结果",
    },
]

POSTER_TPL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title} · SciMiner</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
{font_link}
<link rel="stylesheet" href="styles.css" />
</head>
<body class="stage lang-zh">
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

    <div class="section-label">{capabilities}</div>
    <div class="caps">
{caps_html}
    </div>

    <div class="io">
      <div class="box">
        <div class="label">{input_label}</div>
        <div class="value">{inputs}</div>
      </div>
      <div class="box">
        <div class="label">{output_label}</div>
        <div class="value">{outputs}</div>
      </div>
    </div>

    <div class="footer">
      <span class="url">www.sciminer.tech</span>
      <span class="cta">{footer_cta}</span>
    </div>
  </section>
</body>
</html>
"""

CAP_TPL = '      <div class="cap"><span class="bullet">{n:02d}</span><span>{txt}</span></div>'

HERO_TPL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{hero_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
{font_link}
<link rel="stylesheet" href="styles.css" />
</head>
<body class="stage lang-zh">
  <section class="poster overview">
    <div class="brandbar">
      <span class="brand"><span class="dot"></span>SciMiner</span>
      <span class="index">00 / 13</span>
    </div>

    <div class="hero">
      <span class="kicker">{hero_kicker}</span>
      <h1 class="big">{hero_heading}</h1>
      <p class="lead">{hero_lead}</p>
      <div class="link-list">
{hero_links}
      </div>
    </div>

    <div class="stats">
{hero_stats}
    </div>

    <div class="section-label">{hero_stack}</div>
    <div class="skill-grid">
{tiles}
    </div>

    <div class="footer">
      <span class="url">www.sciminer.tech</span>
      <span class="cta">{hero_footer}</span>
    </div>
  </section>
</body>
</html>
"""

TILE_TPL = '      <a class="skill-tile" href="{key}.html" style="text-decoration:none;color:inherit"><span class="ic">{emoji}</span><span>{label}</span></a>'
HERO_LINK_TPL = '        <a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'
HERO_STAT_TPL = '      <div class="stat"><div class="num">{num}</div><div class="lbl">{label}</div></div>'

INDEX_TPL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{gallery_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
{font_link}
<link rel="stylesheet" href="styles.css" />
</head>
<body class="lang-zh">
  <main class="gallery">
    <header>
      <div class="kicker">{gallery_kicker}</div>
      <h1>{gallery_heading}</h1>
      <p>{gallery_blurb}</p>
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


def render_poster(idx: int, skill: dict) -> str:
    caps_html = "\n".join(CAP_TPL.format(n=i + 1, txt=cap) for i, cap in enumerate(skill["caps"]))
    return POSTER_TPL.format(
        idx=idx,
        theme=skill["theme"],
        emoji=skill["emoji"],
        category=skill["category"],
        title=skill["title"],
        tagline=skill["tagline"],
        summary=skill["summary"],
        caps_html=caps_html,
        capabilities=UI["capabilities"],
        input_label=UI["input"],
        output_label=UI["output"],
        inputs=skill["inputs"],
        outputs=skill["outputs"],
        footer_cta=UI["footer_cta"],
        font_link=FONT_LINK,
    )


def render_hero() -> str:
    hero_links = "\n".join(HERO_LINK_TPL.format(href=href, label=label) for href, label in UI["hero_links"])
    hero_stats = "\n".join(HERO_STAT_TPL.format(num=num, label=label) for num, label in UI["hero_stats"])
    tiles = "\n".join(TILE_TPL.format(key=skill["key"], emoji=skill["emoji"], label=skill["category"]) for skill in SKILLS)
    return HERO_TPL.format(
        hero_title=UI["hero_title"],
        hero_kicker=UI["hero_kicker"],
        hero_heading=UI["hero_heading"],
        hero_lead=UI["hero_lead"],
        hero_links=hero_links,
        hero_stats=hero_stats,
        hero_stack=UI["hero_stack"],
        tiles=tiles,
        hero_footer=UI["hero_footer"],
        font_link=FONT_LINK,
    )


def render_index() -> str:
    thumbs = [
        THUMB_TPL.format(
            href="hero.html",
            label=UI["overview_label"],
            sub=UI["overview_sub"],
        )
    ]
    for skill in SKILLS:
        thumbs.append(THUMB_TPL.format(href=f"{skill['key']}.html", label=skill["title"], sub=skill["category"]))
    return INDEX_TPL.format(
        gallery_title=UI["gallery_title"],
        gallery_kicker=UI["gallery_kicker"],
        gallery_heading=UI["gallery_heading"],
        gallery_blurb=UI["gallery_blurb"],
        thumbs="\n".join(thumbs),
        font_link=FONT_LINK,
    )


def main() -> None:
    for idx, skill in enumerate(SKILLS, start=1):
        (OUT / f"{skill['key']}.html").write_text(render_poster(idx, skill), encoding="utf-8")

    (OUT / "hero.html").write_text(render_hero(), encoding="utf-8")
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")

    print(f"Wrote {len(SKILLS) + 2} files to {OUT}")


if __name__ == "__main__":
    main()