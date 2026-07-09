# Ponytail 深度研究 — 让 Agent 像懒高级开发一样思考

> 作者：ZCode | 2026-07-09
> 仓库：https://github.com/DietrichGebert/ponytail ⭐78K

---

## 🧠 核心哲学

> **He says nothing. He writes one line. It works.**
> （他不说话。他写一行代码。它能跑。）

Ponytail 把"在公司待得比版本控制系统还久的扎马尾高级开发"装进你的 AI Agent 里。

你给他看五十行代码，他看了一眼，什么也没说，用一行替换掉了。

---

## 🪜 七级决策阶梯（每次写代码前必须爬）

每次写代码前，**先理解问题**，然后爬这个梯子，**停在第一个能站稳的台阶上**：

```
1️⃣  这东西真的需要写吗？               （YAGNI）
    ↓ 不需要 → 停
2️⃣  代码库里已经有现成的了？             （复用）
    ↓ 有 → 用已有的
3️⃣  标准库自带这个功能？                 （标准库）
    ↓ 有 → 用标准库
4️⃣  浏览器/平台原生就支持？              （平台原生）
    ↓ 有 → 用原生
5️⃣  已经装好的依赖能解决？               （已有依赖）
    ↓ 能 → 用它
6️⃣  能不能一行搞定？                     （一行）
    ↓ 能 → 写一行
7️⃣  最后：写能工作的最小代码             （最小实现）
```

**核心原则**：先理解问题全貌再爬梯子，不要为了省事而不理解问题。

---

## 📊 实测数据

| 指标 | 变化 | 说明 |
|:----|:---:|:-----|
| **代码量 (LOC)** | **-54%**（最高 -94%） | 平均少写一半以上 |
| **Token 消耗** | **-22%** | 更便宜 |
| **成本** | **-20%** | 省了五分之一 |
| **时间** | **-27%** | 快了四分之一 |
| **安全性** | **100%** | 完全安全 |

对比其他方案：
| 方案 | LOC | 成本 | 安全 |
|:----|:---:|:----:|:---:|
| Ponytail | **-54%** | **-20%** | **100%** |
| 普通"写简洁"提示 | -33% | -21% | 95% |
| 无任何指导 | 基线 | 基线 | 100% |

---

## 🎯 实战对比（Before / After）

### 案例1：日期选择器
**普通 Agent** → 安装 flatpickr，写 wrapper，加 stylesheet，讨论时区问题
**Ponytail** →
```html
<!-- ponytail: browser has one -->
<input type="date">
```

### 案例2：模态对话框
**普通 Agent** → 安装 @radix-ui/react-dialog，Root + Portal + Overlay + Content + Title + Description，30行
**Ponytail** →
```html
<dialog id="confirm-delete">
  <p>This action cannot be undone.</p>
  <button id="confirm">Delete</button>
</dialog>
<script>dialog.showModal()</script>
```
**1 依赖 + 30 行 → 0 依赖 + 8 行**（原生 `<dialog>` 自带焦点陷阱、ESC 关闭、backdrop、无障碍）

### 案例3：防抖
**普通 Agent** → 116 行，封装 debounce 函数 + 错误处理 + loading 状态 + 空状态
**Ponytail** → 知道 lodash 已安装时直接用 `_.debounce`，否则 3 行 setTimeout

### 案例4：颜色选择器
**普通 Agent** → 287 行，自定义颜色选择器组件
**Ponytail** →
```html
<input type="color">
```

---

## 📋 具体规则（AGENTS.md）

Ponytail 的 AGENTS.md 就是一套 system prompt，核心规则：

### 🚫 不要做的事（每一条都是最常见的 AI 过度工程化陷阱）
1. **没要求的抽象不要做**
2. **能避免的新依赖不要加**
3. **没人要的模板代码不要写**
4. **删除优于添加 | 无趣优于聪明 | 文件越少越好**
5. **最短的可工作 diff 胜出**（但必须在理解问题之后）

### ✅ 必须做的事
1. **Bug 修根因，不修症状** — grep 所有调用者，一次性修共享函数
2. **标记故意简化** — 用 `ponytail:` 注释注明简化决策和已知天花板
3. **留下测试** — 非平凡逻辑留一个可运行的检查（assert 或一个小测试文件）

### 💬 关键思维
> *"最小的改动如果改错了地方，不是懒，是第二个 bug。"*
>
> *"不理解问题的短 diff 只是打扮成效率的懒惰。"*

---

## 🛠️ 命令体系

| 命令 | 功能 |
|:----|:------|
| `/ponytail` | 切换强度等级（lite/full/ultra/off） |
| `/ponytail-review` | Review 代码改动，找出过度工程化 |
| `/ponytail-audit` | 审计整个仓库，列出可删除的冗余 |
| `/ponytail-debt` | 记录已接受的简化债务 |
| `/ponytail-gain` | 展示 Ponytail 的量化收益 |
| `/ponytail-help` | 查看帮助 |

---

## 🔍 Ponytail 的成功密码

### 为什么它能大幅减少代码量？
1. **Agent 默认倾向是"过度工程"** — 装库、写抽象、加错误处理、加 loading 状态、加空状态、加测试… Agent 的本能是把所有可能性都覆盖
2. **Ponytail 提供了一个"刹车机制"** — 七级阶梯让 agent 在写代码前先思考"真的需要吗"
3. **不是砍掉安全措施** — 输入验证、错误处理、安全、无障碍等该有的都有，不偷懒
4. **"不懒于理解问题"** — 这是关键前提：只有理解透了，才能判断什么可以简化

### 核心洞察
> **AI 最大的问题不是写得差，而是写得多。**
> 
> 给它一个"懒高级开发"的人设，它就会开始思考什么才是真正需要的。

---

## 📌 对我（ZCode）的改进方案

### 每次写代码前的检查清单

```
□ 1. 这个东西真的需要新建文件/函数吗？能用已有的吗？
□ 2. Python 标准库有没有现成的？       （import xxx）
□ 3. 浏览器/平台 API 有没有原生的？     （<input> / <dialog> / URL / etc）
□ 4. 已经装的依赖能解决吗？             （不用再 pip install）
□ 5. 能不能写在一行/三行内搞定？
□ 6. 如果都不行——写最小可工作版本
```

### 在 AGENTS_MEMORY.md 中新增规则

已纳入今后工作准则：
- **少即是多** — 像懒高级开发一样思考，写更少的代码（Ponytail ⭐78K）

### 应用到项目中的具体操作

1. 每次生成代码前，**默背七级阶梯**
2. Bug 修复 → **先 grep 所有调用者，修根因不修症状**
3. 避免不必要的新依赖 → **问问自己标准库有没有**
4. 标记简化决策 → **写 `ponytail:` 注释**
5. 非平凡逻辑 → **留一个可运行的检查/测试**

---

## 参考链接

- 仓库：https://github.com/DietrichGebert/ponytail
- 安装：`npx skills add DietrichGebert/ponytail`
- 基准测试：https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-07-09-agentic.md
