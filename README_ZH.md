SciMiner 技能集

一套基于 SciMiner API 构建的精简技能集合。

安装
- OpenClaw：在 OpenClaw 技能商店中安装或将本仓库添加为技能源。
- Claude Code：在 Claude Code 对话中请求安装 "sciminer-skills"，或通过 ClawHub 安装（链接见技能条目）。

使用
- 每个技能子文件夹包含 SKILL.md，详见 admet-pkpd、peptide-design、protein-design、structure-prediction。

技能简介
- `admet-pkpd`：小分子性质预测工作流（ADMET、溶剂化能、pKa、口服生物利用度、共晶、AOX 代谢位点、分子描述符）。需要环境变量 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/sciminer/admet-pkpd
- `peptide-design`：肽设计与分析（口袋引导对接、宏环肽设计、肽描述符、消光系数、等电点、毒性/不利特性检测）。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/xiongzhp/peptide-design
- `protein-design`：BoltzGen 蛋白/肽/抗体/纳米抗体设计（支持从目标或框架文件进行设计）。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/xiongzhp/protein-design
- `structure-prediction`：生物分子结构预测（Chai-1、Boltz-2、Alphafold3），支持蛋白、核酸、配体及复合体。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/xiongzhp/structure-prediction
- `virtual-screening`：虚拟筛选工作流（小分子与片段库的对接、评分、库生成与高通量筛选）。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/sciminer/virtual-screening
- `small-molecule-design`：小分子生成与优化工作流（从头设计、先导优化、性质约束生成）。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/sciminer/small-molecule-design
- `synthesis-evaluation`：合成规划与评估（逆合成建议、路线评分、可行性与构建块分析）。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/sciminer/synthesis-evaluation
- `optical-chemical-structure-recognition`：光学化学结构识别（从图像或文献图中提取化学结构、图像转 SMILES、结构解析）。需要 `SCIMINER_API_KEY`。ClawHub: https://clawhub.ai/sciminer/optical-chemical-structure-recognition

备注
- 这些技能依赖 SciMiner API，需要 API key，可以从 https://sciminer.tech/utility 免费获取，在需要时直接粘贴进入OpenClaw或Claude Code的对话框即可。
