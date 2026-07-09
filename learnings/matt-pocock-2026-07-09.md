# Matt Pocock Skills 深度学习

> 来源：github.com/mattpocock/skills | 学习时间：2026-07-09

## 定位

"Skills for real engineers - not vibe coding"

前 Vercel 工程师、TypeScript 社区知名人物（Total TypeScript 作者），60,000+ newsletter 订阅者。他不满于 GSD/BMAD/Spec-Kit 等工具「替你决定一切」的做法，做了一套小而美的 Agent Skill 体系。

## 核心哲学

- **小、可组合、可改造**：每个 skill 只做一件事，你可以随意修改
- **控制权在人**：不替你做决定，不替你写代码——只帮你捋清楚思路
- **任何模型都能用**：不绑定具体 AI
- **Grill 模式是最大创新**：动手之前先审问，解决「AI 没理解你要什么」的失败模式

## 技能体系（17 个，4 大类）

### 工程类
| 技能 | 作用 |
|------|------|
| `/grill-with-docs` | 编码前深度审问 + 自动生成文档 |
| `/triage` | Issue/PR 状态机自动分诊 |
| `/code-review` | 代码审查 |
| `/implement` | 执行实现 |
| `/codebase-design` | 代码库架构设计 |
| `/diagnosing-bugs` | 诊断 Bug |
| `/domain-modeling` | 领域建模（DDD 思路） |
| `/resolving-merge-conflicts` | 解决合并冲突 |
| `/wayfinder` | 导航代码库 |
| `/tdd` | 测试驱动开发 |
| `/to-spec` | 需求转技术规范 |
| `/to-tickets` | 规范拆解为工单 |
| `/ask-matt` | 以 Matt 本人风格回答 |

### 生产力类
| 技能 | 作用 |
|------|------|
| `/grill-me` | 通用版审问（非编码场景） |
| `/teach` | 教 AI 你的领域知识 |
| `/handoff` | Agent 之间交接 |
| `/writing-great-skills` | 怎么写好 Skill |

## 关键创新

### 1. Grill 模式（核心创新）
```
你不要动手，先一个一个问我问题：
- 代码里能找到的事实，你自己查，别问我
- 需要我决策的点，一个一个问，等我回答
- 我没说确认之前，不要执行任何操作
```

这解决的是最高频失败模式：「AI 没理解你要什么」。更像一个资深工程师在开工前跟 PM 对齐需求，而不是直接闷头写。

### 2. 共享语言（DDD 思想）
- 项目维护一份「行话词典」，AI 能读懂你们的术语
- 解决 AI 用 20 个词解释一个概念的问题
- 类似 Eric Evans《领域驱动设计》的「通用语言」

### 3. Triage 状态机
```
issue 进入 → categorise（分类）
          → verify（验证是否可复现）  
          → grill（审问需求细节）
          → agent-ready brief（生成 Agent 可执行的工单）
```
每一步都有明确的角色和转移规则。

### 4. Handoff 模式
- 当前 Agent 把上下文写成结构化文档
- 下一个 Agent 无缝接手
- 解决了「换 Agent 就丢上下文」的问题

## 对我们项目的启示

1. **会前讨论机制应该升级为 Grill 模式**：不是千安和 ZCode 互相聊天，而是 ZCode 开工前先审问千安（或缪艺涵），确保完全理解需求再动手

2. **ClawKit 应该学他的技能粒度**：一个命令做一件事，小而可组合。不是一个大而全的文档

3. **Handoff 正是我们需要的**：千安 ↔ ZCode 交接时，目前用 bridge 发消息 + 行动日志。但缺乏结构化的上下文传递

4. **Triage 状态机**：如果我们有 issue tracker，AI 应该能自动分类 → 验证 → 生成工单
