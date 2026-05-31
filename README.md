# SciMiner Skills

Simplified Chinese: [README.zh-CN.md](./README.zh-CN.md)

This repository collects reusable agent skills for SciMiner-driven scientific
workflows. Each skill lives in its own directory and is packaged as a
`SKILL.md` file that tells an agent when to use the skill, how to choose the
right method, and how to invoke the underlying tools or services.

The current skill set covers:

- ADMET and PK/PD prediction
- antibody engineering
- binding-site prediction
- molecular docking
- optical chemical structure recognition
- peptide design
- global pharma intelligence and biomedical research
- protein design
- general SciMiner tool discovery and invocation
- small-molecule design
- structure prediction
- retrosynthesis and synthesis evaluation
- virtual screening

## Install with an agent

If your coding or research agent supports skill installation from a repository
or hub link, you can ask it to install these skills directly by providing one
of these links:

- GitHub: https://github.com/SciMiner/sciminer-skills
- Clawhub: https://clawhub.ai/user/sciminer

Example prompts:

- `Install the SciMiner skills from https://github.com/SciMiner/sciminer-skills`
- `Install the SciMiner skills from https://clawhub.ai/user/sciminer`

In most agent environments, this is enough for automatic installation. No
manual copying is required if the agent already supports repository- or
hub-based skill import.

## Repository layout

- Each top-level directory is a standalone skill.
- Most skills describe SciMiner-backed workflows and point the agent to the
  authoritative API docs under `https://sciminer.tech/tool_api_files/`.
- `pharma-intelligence/` also includes reference material for regulatory,
  clinical, and literature search workflows.
- `ready-tools-on-sciminer/` is the generic fallback for discovering and using
  published SciMiner tools that are not covered by a more specific skill.

## Notes

Many SciMiner execution skills expect an API key in
`~/.config/sciminer/credentials.json`. See the individual `SKILL.md` files for
workflow-specific requirements, supported tools, and invocation details.