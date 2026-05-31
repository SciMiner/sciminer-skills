SciMiner 技能集

一套基于 SciMiner API 构建的精简技能集合。

安装
- OpenClaw：在 OpenClaw 技能商店中安装或将本仓库添加为技能源。
- Claude Code：在 Claude Code 对话中请求安装 "sciminer-skills"，或通过 ClawHub 安装（链接见技能条目）。

使用
- 每个技能子文件夹包含 SKILL.md，详见 admet-pkpd、peptide-design、protein-design、structure-prediction。

统一 SciMiner 凭证
- 从 https://sciminer.tech/utility 免费获取 SciMiner API key。
- 将凭证保存在仓库外的 `~/.config/sciminer/credentials.json`：

```bash
mkdir -p ~/.config/sciminer
chmod 700 ~/.config/sciminer
printf '{"api_key":"your_api_key_here"}\n' > ~/.config/sciminer/credentials.json
chmod 600 ~/.config/sciminer/credentials.json
```

- Agent 应记住凭证文件路径，而不是凭证值：调用 SciMiner 时，从 `~/.config/sciminer/credentials.json` 读取 API key；不要在 prompt、日志或仓库文件中打印或存储 API key。
- 如果 `~/.config/sciminer/credentials.json` 不存在，或其中没有 `api_key` 字段，应停止并提示用户从 https://sciminer.tech/utility 获取免费 API key 并写入该文件。不要改用其他工具或服务来继续任务。

技能简介
- `admet-pkpd`：小分子性质预测工作流（ADMET、溶剂化能、pKa、口服生物利用度、共晶、AOX 代谢位点、分子描述符）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/admet-pkpd
- `peptide-design`：肽设计与分析（口袋引导对接、宏环肽设计、肽描述符、消光系数、等电点、毒性/不利特性检测）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/xiongzhp/peptide-design
- `protein-design`：BoltzGen 蛋白/肽/抗体/纳米抗体设计（支持从目标或框架文件进行设计）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/xiongzhp/protein-design
- `structure-prediction`：生物分子结构预测（Chai-1、Boltz-2、Alphafold3），支持蛋白、核酸、配体及复合体。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/xiongzhp/structure-prediction
- `virtual-screening`：虚拟筛选工作流（小分子与片段库的对接、评分、库生成与高通量筛选）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/virtual-screening
- `small-molecule-design`：小分子生成与优化工作流（从头设计、先导优化、性质约束生成）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/small-molecule-design
- `synthesis-evaluation`：合成规划与评估（逆合成建议、路线评分、可行性与构建块分析）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/synthesis-evaluation
- `optical-chemical-structure-recognition`：光学化学结构识别（从图像或文献图中提取化学结构、图像转 SMILES、结构解析）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/optical-chemical-structure-recognition
- `binding-site-prediction`：蛋白结合位点与口袋预测工作流（P2Rank 机器学习口袋排名、fpocket 几何检测、AF2BIND 残基级结合概率评分）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/binding-site-prediction
- `pharma-intelligence`：全球医药情报与生物医学研究工作流（覆盖多地区监管状态、临床试验、安全性、专利、竞品格局、文献与靶点发现）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/pharma-intelligence
- `antibody-engineering`：端到端抗体工程工作流，整合 ANARCI、BioPhi、IgFold、FoldX 和 Rosetta（序列编号、人源化、结构预测、可开发性分析、亲和力优化与精准重设计）。需要 `~/.config/sciminer/credentials.json`。ClawHub: https://clawhub.ai/sciminer/antibody-engineering

备注
- 依赖 SciMiner 的技能会从 `~/.config/sciminer/credentials.json` 读取 API key，并通过 `X-Auth-Token` header 发送。
- 不要在 prompt、日志或仓库文件中粘贴或保存 API key。
