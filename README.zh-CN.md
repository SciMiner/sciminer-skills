# SciMiner Skills

English: [README.md](./README.md)

本仓库收录了面向 SciMiner 科学工作流的可复用 agent skills。每个 skill
都位于独立目录中，并通过一个 `SKILL.md` 文件定义何时触发、如何选择合适
的方法，以及如何调用对应的工具或服务。

当前技能覆盖的方向包括：

- ADMET 与 PK/PD 预测
- 抗体工程
- 结合位点预测
- 分子对接
- 光学化学结构识别
- 肽设计
- 全球医药情报与生物医学研究
- 蛋白设计
- 通用 SciMiner 工具发现与调用
- 小分子设计
- 结构预测
- 逆合成与合成可行性评估
- 虚拟筛选

## 通过 agent 安装

如果你的编程 agent 或科研 agent 支持从仓库链接或 hub 链接安装 skills，
你可以直接把以下任一链接提供给 agent，让它自动安装这些 skills：

- GitHub: https://github.com/SciMiner/sciminer-skills
- Clawhub: https://clawhub.ai/user/sciminer

示例提示词：

- `Install the SciMiner skills from https://github.com/SciMiner/sciminer-skills`
- `Install the SciMiner skills from https://clawhub.ai/user/sciminer`
- `请从 https://github.com/SciMiner/sciminer-skills 安装 SciMiner skills`
- `请从 https://clawhub.ai/user/sciminer 安装 SciMiner skills`

在大多数支持该能力的 agent 环境中，仅提供上述链接即可完成自动安装，无需
手动复制文件。

## 仓库结构

- 每个顶层目录对应一个独立 skill。
- 大多数 skills 描述的是基于 SciMiner 的工作流，并会引导 agent 使用
  `https://sciminer.simm.ac.cn/tool_api_files/` 下的权威 API 文档。
- `pharma-intelligence/` 额外包含监管、临床和文献检索相关的参考资料。
- `ready-tools-on-sciminer/` 是一个通用兜底 skill，用于发现和调用那些尚未
  被更具体 skill 覆盖的已发布 SciMiner 工具。

## 说明

许多 SciMiner 执行类 skills 依赖位于
`~/.config/sciminer/credentials.json` 的 API key。具体的工作流要求、支持
的工具以及调用细节，请查看各目录中的 `SKILL.md` 文件。