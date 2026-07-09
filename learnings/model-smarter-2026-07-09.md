# 让模型变聪明的 GitHub 项目深度研究

> 作者：千安 | 2026-07-09


> 学习时间：2026-07-09

## 核心发现：让 AI 变聪明的三条路径

### 路径 1：Skill 化（给模型装「技能包」）
**代表项目**：anthropics/skills (159K⭐)、danielmiessler/fabric (43K⭐)、Matt Pocock/skills

**原理**：把人类的知识、流程、判断标准打包成模块，加载到 AI 的上下文中

**anthropics/skills** —— 官方技能库
- 17 个官方技能：frontend-design、pptx、pdf、docx、xlsx、mcp-builder
- skill-creator 教你写自己的 Skill
- 每个 Skill 由 SKILL.md + scripts/ + references/ 组成
- 本质：用 Markdown 写「给 AI 的操作手册」

**fabric** —— AI 增强人类的框架
- 核心概念：Pattern（模式）
- 把人类的各种任务抽象为可复用的 AI Pattern
- extract_wisdom、summarize、analyze_claims、create_quiz 等 200+ Pattern
- 通过 CLI 调用：`fabric --pattern extract_wisdom < input.txt`
- 不绑定特定模型，任何 LLM 都能用
- 社区贡献模式，持续增长

**学到什么**：
- AI 的能力上限 = 你给它的指令质量
- Skill = 结构化知识 + 可执行代码
- Pattern = 人类智慧的模板化

### 路径 2：知识增强（让模型「有记性」）
**代表项目**：microsoft/graphrag (34K⭐)

**graphrag** —— 图增强 RAG
- 传统 RAG：向量搜索 → 找到相似文本 → 喂给 LLM
- GraphRAG：先建知识图谱（实体+关系）→ 基于图的全局理解
- 不是「找到相关段落」，而是「理解整个知识体系」
- Azure 级别工程化，模块化设计
- 适合：大型文档库、企业知识管理、多文档综合分析

**学到什么**：
- 向量搜索只能找「相似的」，不能找「相关的但表达不同的」
- 知识图谱让 AI 理解「A 和 B 什么关系」，而不是只看表面词频
- 我们的知识管家可以升级为 GraphRAG 架构

### 路径 3：Agent 协作（让模型「会合作」）
**代表项目**：microsoft/autogen (60K⭐)、google/A2A (25K⭐)、modelcontextprotocol/servers (88K⭐)

**autogen** —— 多 Agent 对话框架
- 定义 Agent 角色 + 对话规则
- Agent 之间自动对话，不需要人干预
- 适用：代码审查自动化、数据分析流水线、多视角决策

**A2A (Agent2Agent)** —— Google 的 Agent 通信协议
- 解决不同 Agent 之间的通信标准
- 类似 HTTP 之于 Web 的意义
- 你的 Agent 可以调用任何人的 Agent

**MCP (Model Context Protocol)** —— Anthropic 的工具调用协议
- 标准化模型如何访问外部工具和数据
- 88K ⭐ 的 servers 仓库提供各种 MCP 服务器
- 类似 USB 接口：任何模型插上就能用

**学到什么**：
- 单个 Agent 聪明程度有限，但多个 Agent 协作可以指数级提升
- 我们千安+ZCode+GLM 三 Agent 协作已经是这个方向
- 但缺少标准协议（A2A）和工具接口（MCP）

## 三者交汇：模型变聪明的终极公式

```
AI 能力 = Skill（结构化指令）
        × 知识（图谱化存储）
        × 协作（标准化通信）
```

- **Skill** 决定 AI「会不会做」
- **知识** 决定 AI「懂不懂」
- **协作** 决定 AI「做不做得好」

## 对千安体系的行动建议

| 项目 | 做什么 |
|------|--------|
| Skill | 把 jm-pdf 进一步细化，加错误处理、进度提示 |
| 知识 | 知识管家考虑引入 GraphRAG，从向量搜索升级为图谱理解 |
| 协作 | 千安↔ZCode bridge 参考 A2A 协议规范化 |
| MCP | 研究 MCP servers，给千安加工具调用标准接口 |
