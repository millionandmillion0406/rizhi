# 开源项目深度学习 — Paul Bakaus 

> 来源：github.com/pbakaus | 学习时间：2026-07-09

## impeccable（45,000+ ⭐）

**定位**：AI 编码 Agent 的设计指南——1 个 skill、23 条命令、45 条确定性检测规则。

**不做什么**：不是 UI 框架，不是组件库。不写一行 CSS。

**做什么**：给 AI 一套「设计语法」，告诉它什么是好的设计。AI 自己生成代码。

**核心架构**：
- `npx impeccable install` 一键安装
- `/impeccable init` 初始化项目设计上下文
- 分 brand 模式（营销/落地页/作品集）和 product 模式（应用/后台/工具）
- 23 个命令形成人机共享词汇：craft/critique/polish/audit/shape/animate/bolder/quieter/distill/harden/onboard
- 45 条确定性规则（纯算法，不用 LLM，零 API 调用）
- LLM 只负责主观判断（"这个设计有情感共鸣吗？"）

**设计哲学**：
- 互联网上所有 SaaS 模板都一样（Inter 字体、紫蓝渐变、卡片套卡片）
- AI 模型训练在这些模板上，输出也千篇一律
- impeccable 通过设计约束打破这种同质化

**学到的**：
1. **语法 > 代码**：定义设计语法比写代码效率高 10 倍
2. **确定性优先**：能写规则的不要用 LLM，省 token 且结果一致
3. **共享词汇**：人和 AI 用同一套命令语言沟通
4. **分模式设计**：营销和工具的设计标准完全不同

---

## agent-reviews（207 ⭐）

**定位**：从终端和 AI Agent 管理 GitHub PR review 评论。

**解决的真实痛点**：
- Bot review 产生评论 → 你修复 → push → 新评论出现 → 无限循环
- gh CLI 对 Agent 不友好（语法易错、分页失败、无法判断回复状态）
- 云端环境无法使用本地工具

**架构亮点**：
- 三条命名路径解析认证：GITHUB_TOKEN → GH_TOKEN → .env.local → gh auth token
- 内置 undici ProxyAgent，HTTPS_PROXY 自动路由
- 支持自定义 API host（GitHub Enterprise）

**三个技能**：
| 技能 | 解决 |
|------|------|
| `resolve-reviews` | 所有评论（人+机器人） |
| `resolve-agent-reviews` | 仅机器人评论 |
| `resolve-human-reviews` | 仅人类评论 |

**分发方式**：`npx skills add pbakaus/agent-reviews@resolve-agent-reviews`

**学到的**：
1. **为 Agent 设计专用接口**，不要让 Agent 用人类的 CLI
2. **fix-reply 循环自动化**，Agent 应该能自己处理审查反馈
3. **云端优先设计**，不在本地做假设
4. **npx 分发模式**：用户不需要安装任何东西

---

## burn-after-login（38 ⭐）

**定位**：自毁式 Agent Skill，为浏览器自动化创建 dev 登录捷径。

**流程**：
1. 安装 skill → 运行 → 分析认证系统
2. 创建 dev-only 登录端点/令牌捷径
3. 检测浏览器自动化工具并更新 agent 指令
4. 自毁（删除自身）

**学到的**：
1. **用完即走的 Skill 模式**：不是永久的、是任务性的
2. **最低入侵原则**：只创建 dev 环境的捷径，不碰生产代码
3. **Agent 感知**：自动检测当前环境的浏览器自动化工具

---

## 综合方法论

1. **Skill 即产品**：每个功能打包为一个独立 skill，通过 npx 分发
2. **Agent-First 设计**：工具优先为 AI Agent 设计，人类辅助使用
3. **确定性 + 概率性混合**：规则覆盖 80%，LLM 补充 20%
4. **云端兼容**：Proxy 支持、多认证链、环境自适应
5. **独立品牌站**：每个项目有专属域名和文档站点
