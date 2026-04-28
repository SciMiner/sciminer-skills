import { readFile, writeFile } from 'node:fs/promises';

const replacements = new Map([
  ['<html lang="zh-CN">', '<html lang="en">'],
  ['<title>SciMiner Skills 中文海报</title>', '<title>SciMiner Skills Poster</title>'],
  ['封面', 'Cover'],
  ['能力地图', 'Capability Map'],
  ['小分子', 'Small Molecules'],
  ['生物分子', 'Biomolecules'],
  ['结构与口袋', 'Structure & Pockets'],
  ['抗体工程', 'Antibody'],
  ['闭环流程', 'Workflow'],
  ['安装调用', 'Install & Invoke'],
  ['把药物发现工作流装进 AI Agent', 'Drug Discovery Workflows, Packaged for AI Agents'],
  ['本仓库收录 10 个基于 SciMiner API 的技能，覆盖结构预测、口袋发现、小分子与肽设计、虚拟筛选、合成评估、ADMET/PKPD、抗体工程和化学结构识别。', 'This repository contains 10 SciMiner API skills covering structure prediction, pocket discovery, small-molecule and peptide design, virtual screening, synthesis evaluation, ADMET/PKPD, antibody engineering, and optical chemical structure recognition.'],
  ['个可安装 skill，面向药物发现关键任务', 'installable skills for core drug discovery tasks'],
  ['个 SciMiner 内部工具与模型入口', 'SciMiner tool and model entry points'],
  ['个统一凭证：SCIMINER_API_KEY', 'shared credential: SCIMINER_API_KEY'],
  ['分子、蛋白、肽与抗体候选生成', 'Molecule, protein, peptide, and antibody candidate generation'],
  ['结构、口袋、性质与代谢风险预测', 'Structure, pocket, property, and metabolism-risk prediction'],
  ['商业库筛选、对接评分与聚类', 'Commercial-library screening, docking scores, and clustering'],
  ['Gnina、FoldX、Rosetta 与可开发性分析', 'Gnina, FoldX, Rosetta, and developability analysis'],
  ['每个结果可生成在线 share_url', 'Every result can include an online share_url'],
  ['从图像、序列、结构到候选分子的一张能力地图', 'A Capability Map from Images, Sequences, and Structures to Candidates'],
  ['这些 skill 不是孤立工具，而是可组合的研究链路：先识别和建模，再设计和筛选，随后用性质、合成与可开发性指标做决策。', 'These skills are not isolated tools. They compose into a research chain: identify and model first, design and screen next, then decide using property, synthesis, and developability evidence.'],
  ['结构输入', 'Structural Inputs'],
  ['Chai-1、Boltz-2、Alphafold3 预测蛋白、核酸、配体和复合物。', 'Chai-1, Boltz-2, and Alphafold3 predict proteins, nucleic acids, ligands, and complexes.'],
  ['口袋定位', 'Pocket Localization'],
  ['P2Rank、fpocket、AF2BIND 发现和交叉验证结合位点。', 'P2Rank, fpocket, and AF2BIND discover and cross-check binding sites.'],
  ['分子生成', 'Molecule Generation'],
  ['REINVENT4、PocketXMol、BoltzGen 支持多场景候选设计。', 'REINVENT4, PocketXMol, and BoltzGen support candidate design across scenarios.'],
  ['筛选排序', 'Screening & Ranking'],
  ['TransformerCPI、Docking、Gnina Score 组合产生优先级。', 'TransformerCPI, docking, and Gnina Score combine into ranked priorities.'],
  ['成药判断', 'Drugability Decisions'],
  ['ADMET、SAScore、逆合成、BioPhi 和 SAP 风险检查。', 'ADMET, SAScore, retrosynthesis, BioPhi, and SAP risk checks guide decisions.'],
  ['输入解析', 'Input Parsing'],
  ['化学图像转结构', 'Chemical Images to Structures'],
  ['OCSR 从论文图、截图或幻灯片中提取分子结构与名称，转成后续设计和性质预测可用的分子输入。', 'OCSR extracts molecular structures and names from papers, screenshots, or slides and turns them into downstream-ready inputs.'],
  ['结构理解', 'Structure Context'],
  ['复合物与口袋', 'Complexes and Pockets'],
  ['结构预测与结合位点预测协同，帮助从序列、PDB 或上传结构推断可操作的 docking box 与候选位点。', 'Structure prediction and binding-site prediction work together to infer actionable docking boxes and candidate sites from sequences, PDB IDs, or uploaded structures.'],
  ['候选生成', 'Candidate Generation'],
  ['多模态设计', 'Multimodal Design'],
  ['小分子、肽、蛋白、抗体和纳米抗体设计工具覆盖从头生成、片段连接、骨架设计和序列设计。', 'Design tools cover de novo generation, fragment linking, backbone design, and sequence design for small molecules, peptides, proteins, antibodies, and nanobodies.'],
  ['风险过滤', 'Risk Filtering'],
  ['性质与可合成性', 'Properties and Synthesizability'],
  ['ADMET/PKPD、pKa、溶剂化能、口服生物利用度、SAScore 与逆合成路线支持候选收敛。', 'ADMET/PKPD, pKa, solvation energy, oral bioavailability, SAScore, and retrosynthetic routes help converge candidates.'],
  ['小分子：设计、筛选、合成与 ADMET 决策', 'Small Molecules: Design, Screening, Synthesis, and ADMET Decisions'],
  ['适合先导发现、先导优化、商业库筛选、文献分子提取以及候选分子的早期成药性评估。', 'For hit discovery, lead optimization, commercial-library screening, literature molecule extraction, and early candidate drugability evaluation.'],
  ['小分子生成与优化', 'Small-Molecule Generation and Optimization'],
  ['REINVENT4 负责无结构生成、迁移学习和强化学习优化；PocketXMol 负责基于蛋白口袋的从头设计、片段连接和片段生长。', 'REINVENT4 handles structure-free generation, transfer learning, and reinforcement learning. PocketXMol handles pocket-guided de novo design, fragment linking, and fragment growing.'],
  ['虚拟筛选', 'Virtual Screening'],
  ['有结构时走 docking-based proprietary library screen；无结构时用 Transformer-based screen，并可先从 UniProt 获取蛋白序列。', 'Use docking-based proprietary-library screening when a structure is available. Without a structure, use transformer-based screening and retrieve protein sequence from UniProt when needed.'],
  ['ADMET/PKPD 与性质预测', 'ADMET/PKPD and Property Prediction'],
  ['覆盖 pan-ADMET、溶剂化能、pKa、口服生物利用度、共晶潜力、AOX 代谢位点和分子描述符。', 'Covers pan-ADMET, solvation energy, pKa, oral bioavailability, cocrystal potential, AOX metabolism sites, and molecular descriptors.'],
  ['合成规划与可合成性', 'Synthesis Planning and Synthesizability'],
  ['SynFormer-ED 生成可合成类似物，SAScore 快速判断合成难度，Retrosynthesis Planner 给出候选逆合成路线。', 'SynFormer-ED generates synthesizable analogs, SAScore estimates synthesis difficulty, and Retrosynthesis Planner proposes routes.'],
  ['肽、蛋白与纳米抗体：从骨架到序列再到验证', 'Peptides, Proteins, and Nanobodies: From Backbone to Sequence to Validation'],
  ['面向蛋白靶点结合剂设计，既能做口袋引导的候选生成，也能把骨架设计、序列设计和结构验证串起来。', 'For protein-target binder design, supporting pocket-guided generation and chained backbone design, sequence design, and structural validation.'],
  ['肽与宏环肽设计', 'Peptide and Macrocyclic Peptide Design'],
  ['PocketXMol、BoltzGen、RFpeptides、ProteinMPNN、CyclicMPNN 与 AfCycDesign 支持线性肽、环肽和宏环肽的设计、对接和验证。', 'PocketXMol, BoltzGen, RFpeptides, ProteinMPNN, CyclicMPNN, and AfCycDesign support design, docking, and validation of linear, cyclic, and macrocyclic peptides.'],
  ['蛋白/肽/抗体/纳米抗体设计', 'Protein, Peptide, Antibody, and Nanobody Design'],
  ['BoltzGen 支持针对抗原或小分子的从头设计与定向设计，文件上传后可指定目标链、框架和 CDR 区域约束。', 'BoltzGen supports de novo and targeted design against antigens or small molecules, with uploaded files for target chains, frameworks, and CDR constraints.'],
  ['多组分结构预测', 'Multicomponent Structure Prediction'],
  ['Chai-1、Boltz-2 和 Alphafold3 可预测蛋白、DNA、RNA、配体与混合复合物，为设计与筛选提供结构上下文。', 'Chai-1, Boltz-2, and Alphafold3 predict proteins, DNA, RNA, ligands, and mixed complexes to provide structural context for design and screening.'],
  ['目标结构', 'Target Structure'],
  ['上传 PDB/CIF，或用结构预测工具从序列和配体输入建立复合物模型。', 'Upload PDB/CIF files or build complex models from sequences and ligands using structure-prediction tools.'],
  ['结合区域', 'Binding Region'],
  ['用口袋描述、残基约束或 docking box 限定候选生成空间。', 'Constrain candidate generation using pocket descriptions, residue restraints, or docking boxes.'],
  ['生成肽骨架、蛋白序列、抗体 CDR 变体或纳米抗体方案。', 'Generate peptide backbones, protein sequences, antibody CDR variants, or nanobody designs.'],
  ['结构验证', 'Structural Validation'],
  ['通过 AfCycDesign、IgFold、FoldX 或 Rosetta 检查构象与能量。', 'Check conformation and energetics with AfCycDesign, IgFold, FoldX, or Rosetta.'],
  ['候选收敛', 'Candidate Convergence'],
  ['综合亲和力、稳定性、免疫原性与可开发性风险输出 Top panel。', 'Balance affinity, stability, immunogenicity, and developability risks to produce a top panel.'],
  ['结构预测与结合位点预测，给设计任务确定坐标系', 'Structure and Binding-Site Prediction Set the Coordinate System for Design'],
  ['结构类 skill 的价值在于把自然语言、序列、PDB ID 或上传结构转成可执行的模型、口袋、残基概率和 docking box。', 'Structure-oriented skills turn natural language, sequences, PDB IDs, or uploaded structures into executable models, pockets, residue probabilities, and docking boxes.'],
  ['支持蛋白、核酸、配体与复合物预测；可在需要时带上 MSA、template 或 restraint 输入，用于后续 docking、筛选和结构设计。', 'Supports prediction of proteins, nucleic acids, ligands, and complexes, with optional MSA, template, or restraint inputs for downstream docking, screening, and structure design.'],
  ['P2Rank 做机器学习口袋排名，fpocket 做几何检测，AF2BIND 给出残基级结合概率。多方法一致时更适合作为 docking box 和设计区域。', 'P2Rank ranks pockets with machine learning, fpocket detects geometry, and AF2BIND gives residue-level binding probabilities. Consensus sites are better handoffs for docking boxes and design regions.'],
  ['快速口袋发现', 'Fast Pocket Discovery'],
  ['上传 receptor 后用 P2Rank 或 fpocket 识别可药靶口袋，并输出几何和排名信息。', 'After receptor upload, use P2Rank or fpocket to identify druggable pockets with geometry and ranking outputs.'],
  ['残基级交叉验证', 'Residue-Level Cross-Check'],
  ['结构文件、PDB code 或 UniProt 风格标识可进入 AF2BIND，查看高概率结合残基是否聚集在同一区域。', 'Structure files, PDB codes, or UniProt-style identifiers can go into AF2BIND to see whether high-probability binding residues cluster in the same region.'],
  ['设计前交接', 'Pre-Design Handoff'],
  ['把共识位点交给 Get Box、PocketXMol、虚拟筛选或肽/小分子设计流程，减少无效搜索空间。', 'Pass the consensus site to Get Box, PocketXMol, virtual screening, or peptide/small-molecule design to reduce unproductive search space.'],
  ['抗体工程：编号、人源化、建模、突变扫描与精准重设计', 'Antibody Engineering: Numbering, Humanization, Modeling, Mutation Scanning, and Precision Redesign'],
  ['antibody-engineering skill 把 ANARCI、BioPhi、IgFold、FoldX 和 Rosetta 串成端到端候选优化闭环。', 'The antibody-engineering skill connects ANARCI, BioPhi, IgFold, FoldX, and Rosetta into an end-to-end candidate optimization loop.'],
  ['序列编号', 'Sequence Numbering'],
  ['ANARCI 用 IMGT、Kabat 等体系解析 VH/VL 区域与 CDR 边界。', 'ANARCI parses VH/VL regions and CDR boundaries using IMGT, Kabat, and related schemes.'],
  ['人源化', 'Humanization'],
  ['BioPhi 评估 humanness 与 OASis 风险，生成 Sapiens 或 CDR grafting 变体。', 'BioPhi evaluates humanness and OASis risk, then generates Sapiens or CDR-grafting variants.'],
  ['结构建模', 'Structure Modeling'],
  ['IgFold 预测亲本与候选结构，Rosetta FastRelax 进行局部放松。', 'IgFold predicts parental and candidate structures, while Rosetta FastRelax performs local relaxation.'],
  ['能量扫描', 'Energy Scanning'],
  ['FoldX 对稳定性、AlaScan、PositionScan 和 AnalyseComplex 做高通量初筛。', 'FoldX runs high-throughput first-pass screening for stability, AlaScan, PositionScan, and AnalyseComplex.'],
  ['精准设计', 'Precision Design'],
  ['Rosetta FastDesign 与 InterfaceAnalyzer 复核界面质量，SAP Score 控制聚集风险。', 'Rosetta FastDesign and InterfaceAnalyzer rescore interface quality, while SAP Score controls aggregation risk.'],
  ['先降风险再优化', 'De-Risk Before Optimizing'],
  ['先明确 CDR/FR 边界和免疫原性风险，再决定哪些位置允许突变。', 'Clarify CDR/FR boundaries and immunogenicity risk before deciding which positions can mutate.'],
  ['亲和力与稳定性并行', 'Affinity and Stability in Parallel'],
  ['候选筛选同时关注结合能和折叠稳定性，避免单目标优化带来的开发风险。', 'Screen candidates for binding energy and folding stability together to avoid single-objective development risk.'],
  ['输出 Top 10-20 候选', 'Output Top 10-20 Candidates'],
  ['最终候选综合 FoldX、Rosetta、SAP、IgFold 和 BioPhi 指标，形成可推进 panel。', 'Final candidates balance FoldX, Rosetta, SAP, IgFold, and BioPhi metrics into a panel ready to advance.'],
  ['推荐组合：从资料输入到候选决策的一条可复用路径', 'Recommended Composition: A Reusable Path from Inputs to Candidate Decisions'],
  ['每个 skill 都通过 SciMiner 内部 API 调用，返回统一任务状态和 share_url。把结果链接沉淀下来，就能形成可追踪、可复审的研究记录。', 'Each skill calls the SciMiner internal API and returns unified task status plus a share_url. Preserving result links creates traceable, reviewable research records.'],
  ['提取输入', 'Extract Inputs'],
  ['从图片提取 SMILES，或从 UniProt、序列、PDB、上传文件建立起始材料。', 'Extract SMILES from images, or build starting material from UniProt, sequences, PDB IDs, and uploaded files.'],
  ['建立结构', 'Build Structure'],
  ['结构预测补齐未知复合物，结合位点预测给出口袋与残基概率。', 'Structure prediction fills unknown complexes; binding-site prediction provides pockets and residue probabilities.'],
  ['生成候选', 'Generate Candidates'],
  ['按任务选择小分子、肽、蛋白、抗体或纳米抗体设计工具。', 'Choose small-molecule, peptide, protein, antibody, or nanobody design tools based on the task.'],
  ['筛选评分', 'Screen and Score'],
  ['虚拟筛选、Gnina、FoldX、Rosetta、AfCycDesign 等工具帮助候选排序。', 'Virtual screening, Gnina, FoldX, Rosetta, AfCycDesign, and related tools help rank candidates.'],
  ['成药收敛', 'Drugability Convergence'],
  ['ADMET/PKPD、SAScore、逆合成和可开发性指标决定下一轮实验优先级。', 'ADMET/PKPD, SAScore, retrosynthesis, and developability indicators determine the next experimental priorities.'],
  ['结构驱动路线', 'Structure-Driven Route'],
  ['PDB/结构文件已知', 'PDB or Structure File Available'],
  ['binding-site-prediction → Get Box → small-molecule-design 或 virtual-screening → admet-pkpd → synthesis-evaluation。', 'binding-site-prediction -> Get Box -> small-molecule-design or virtual-screening -> admet-pkpd -> synthesis-evaluation.'],
  ['序列驱动路线', 'Sequence-Driven Route'],
  ['只有靶点名称或序列', 'Only Target Name or Sequence Available'],
  ['Get Protein Sequence / structure-prediction → binding-site-prediction → protein-design / peptide-design → 结构与性质验证。', 'Get Protein Sequence / structure-prediction -> binding-site-prediction -> protein-design / peptide-design -> structure and property validation.'],
  ['统一安装、统一鉴权、统一结果链接', 'Unified Installation, Authentication, and Result Links'],
  ['OpenClaw 可从技能商店安装或添加本仓库；Claude Code 可请求安装 sciminer-skills。所有 skill 都要求 SciMiner API key。', 'OpenClaw can install from the skill marketplace or add this repository. Claude Code can install sciminer-skills on request. Every skill requires a SciMiner API key.'],
  ['环境变量', 'Environment Variable'],
  ['从 SciMiner 获取免费 API key 后，设置 <strong>SCIMINER_API_KEY</strong>。调用时以 <strong>X-Auth-Token</strong> header 发送。', 'Get a free SciMiner API key, then set <strong>SCIMINER_API_KEY</strong>. Calls send it as the <strong>X-Auth-Token</strong> header.'],
  ['任务状态与分享链接', 'Task Status and Share Links'],
  ['内部 API 返回 task_id，轮询 result endpoint 后得到 SUCCESS/FAILURE、result 内容和可在线查看的 share_url。', 'The internal API returns a task_id. Poll the result endpoint to get SUCCESS/FAILURE, result content, and an online share_url.'],
  ['本海报基于仓库 README 与 10 个 SKILL.md 汇总生成，适合网页展示、会议屏幕滚动播放或 A4 竖版分页打印。', 'This poster is generated from the repository README and 10 SKILL.md files, suitable for web display, meeting-screen playback, or A4 portrait page printing.'],
  ['GitHub 仓库二维码', 'GitHub repository QR code'],
  ['SciMiner Skills GitHub 仓库二维码', 'SciMiner Skills GitHub repository QR code'],
  ['提示：浏览器打印可生成多页竖版 PDF', 'Tip: browser print can create a multi-page portrait PDF'],
]);

let html = await readFile('poster.html', 'utf8');

for (const [from, to] of replacements) {
  html = html.replaceAll(from, to);
}

const cleanup = new Map([
  ['aria-label="海报分页导航"', 'aria-label="Poster page navigation"'],
  ['aria-label="核心统计"', 'aria-label="Core statistics"'],
  ['aria-label="SciMiner 能力视觉图"', 'aria-label="SciMiner capability visual map"'],
  ['aria-label="SciMiner API 调用示意"', 'aria-label="SciMiner API invocation example"'],
  ['本仓库收录 10 个基于 SciMiner API 的技能，覆盖结构预测、口袋发现、Small Molecules与肽设计、Virtual Screening、合成评估、ADMET/PKPD、Antibody和化学结构识别。', 'This repository contains 10 SciMiner API skills covering structure prediction, pocket discovery, small-molecule and peptide design, virtual screening, synthesis evaluation, ADMET/PKPD, antibody engineering, and optical chemical structure recognition.'],
  ['从图像、序列、结构到候选分子的一张Capability Map', 'A Capability Map from Images, Sequences, and Structures to Candidates'],
  ['Small Molecules、肽、蛋白、抗体和纳米抗体设计工具覆盖从头生成、片段连接、骨架设计和序列设计。', 'Design tools cover de novo generation, fragment linking, backbone design, and sequence design for small molecules, peptides, proteins, antibodies, and nanobodies.'],
  ['Small Molecules、肽 、蛋白、抗体和纳米抗体设计工具覆盖从头生成、片段连接、骨架设计和序列设计。', 'Design tools cover de novo generation, fragment linking, backbone design, and sequence design for small molecules, peptides, proteins, antibodies, and nanobodies.'],
  ['Small Molecules：设计、筛选、合成与 ADMET 决策', 'Small Molecules: Design, Screening, Synthesis, and ADMET Decisions'],
  ['Small Molecules生成与优化', 'Small-Molecule Generation and Optimization'],
  ['面向蛋白靶点结合剂设计，既能做口袋引导的Candidate Generation， 也能把骨架设计、序列设计和Structural Validation串起来。', 'For protein-target binder design, supporting pocket-guided generation and chained backbone design, sequence design, and structural validation.'],
  ['面向蛋白靶点结合剂设计，既能做口袋引导的Candidate Generation，也能把骨架设计、序列设计和Structural Validation串起来。', 'For protein-target binder design, supporting pocket-guided generation and chained backbone design, sequence design, and structural validation.'],
  ['BoltzGen 支持针对抗原或Small Molecules的从头设计与定向设计， 文件上传后可指定目标链、框架和 CDR 区域约束。', 'BoltzGen supports de novo and targeted design against antigens or small molecules, with uploaded files for target chains, frameworks, and CDR constraints.'],
  ['BoltzGen 支持针对抗原或Small Molecules的从头设计与定向设计，文件上传后可指定目标链、框架和 CDR 区域约束。', 'BoltzGen supports de novo and targeted design against antigens or small molecules, with uploaded files for target chains, frameworks, and CDR constraints.'],
  ['用口袋描 述、残基约束或 docking box 限定Candidate Generation空间。', 'Constrain candidate generation using pocket descriptions, residue restraints, or docking boxes.'],
  ['用口袋描述、残基约束或 docking box 限定Candidate Generation空间。', 'Constrain candidate generation using pocket descriptions, residue restraints, or docking boxes.'],
  ['把共识位点交给 Get Box、PocketXMol、Virtual Screening或肽/Small Molecules设计流程，减少无效搜索空间。', 'Pass the consensus site to Get Box, PocketXMol, virtual screening, or peptide/small-molecule design to reduce unproductive search space.'],
  ['Antibody：编号、Humanization、建模、突变扫描与精准重设计', 'Antibody Engineering: Numbering, Humanization, Modeling, Mutation Scanning, and Precision Redesign'],
  ['按任务选择Small Molecules、肽、蛋白、抗体或纳米抗体设计工具。', 'Choose small-molecule, peptide, protein, antibody, or nanobody design tools based on the task.'],
  ['Virtual Screening、Gnina、FoldX、Rosetta、AfCycDesign 等工具帮助候选排序。', 'Virtual screening, Gnina, FoldX, Rosetta, AfCycDesign, and related tools help rank candidates.'],
]);

for (const [from, to] of cleanup) {
  html = html.replaceAll(from, to);
}

html = html.replace(
  '</style>',
  `
    html[lang="en"] .card p,
    html[lang="en"] .flow-step p,
    html[lang="en"] .tool-row p {
      font-size: 20px;
      line-height: 1.26;
    }

    html[lang="en"] .lead,
    html[lang="en"] .skill-title p {
      line-height: 1.28;
    }

    html[lang="en"] h2 {
      font-size: clamp(40px, 5.5vw, 56px);
      line-height: 1.04;
    }

    html[lang="en"] h3 {
      font-size: 27px;
      line-height: 1.18;
    }

    html[lang="en"] .skill-title {
      display: block;
      margin-bottom: 16px;
    }

    html[lang="en"] .skill-title p {
      max-width: 900px;
      font-size: 22px;
      margin-bottom: 0;
    }

    html[lang="en"] .grid,
    html[lang="en"] .flow,
    html[lang="en"] .tool-list {
      gap: 10px;
    }

    html[lang="en"] .grid {
      margin-top: 0;
    }

    html[lang="en"] .card,
    html[lang="en"] .flow-step,
    html[lang="en"] .tool-row {
      min-height: auto;
      padding: 16px 20px;
    }

    html[lang="en"] .flow {
      margin-top: 14px;
    }

    html[lang="en"] .flow-step b {
      width: 30px;
      height: 30px;
      margin-bottom: 8px;
      font-size: 16px;
    }

    html[lang="en"] .chips {
      gap: 6px;
      margin-top: 10px;
    }

    html[lang="en"] .chip,
    html[lang="en"] .tag {
      font-size: 16px;
    }

    html[lang="en"] .tag {
      min-height: 28px;
      margin-bottom: 10px;
    }

    html[lang="en"] .node {
      width: 210px;
      min-height: 96px;
      padding: 12px 14px;
    }

    html[lang="en"] .node span {
      font-size: 15px;
      line-height: 1.22;
    }

    html[lang="en"] .n1 { top: 8%; left: 8%; }
    html[lang="en"] .n2 { top: 8%; right: 8%; }
    html[lang="en"] .n3 { top: 39%; left: 38%; }
    html[lang="en"] .n4 { bottom: 8%; left: 10%; }
    html[lang="en"] .n5 { bottom: 8%; right: 10%; }
  </style>`
);

await writeFile('poster_en.html', html, 'utf8');
console.log('wrote poster_en.html');