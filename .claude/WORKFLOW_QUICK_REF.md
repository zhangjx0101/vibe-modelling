# Vibe Modelling — 经济学理论论文工作流 v3

> 专为经济学理论文章（博弈论/IO/微观理论）设计的 Claude Code 工作流。
> 借鉴 Sant'Anna 实证工作流的架构精髓，针对理论文章的核心需求（数学正确性）做本质性改造。

---

## 一、核心设计哲学

### 1.1 三大原则

| 原则 | 含义 | Sant'Anna 对应 |
|---|---|---|
| **LLM 思考 + CAS 计算** | 所有符号推导由 Wolfram 执行，Claude 负责建模和解释 | 原创（理论文章特有） |
| **先规划，后执行** | 非平凡任务必须先写计划/规格书，用户确认后再动手 | Plan-first + Spec-then-Plan |
| **先验证，再声明** | 任何数学声明必须有 Wolfram 输出支撑，禁止纯文本推理 | Verify-after |

### 1.2 承包商模式（Contractor Mode）

借鉴 Sant'Anna 的核心设计：**用户只描述目标，Claude 全权调度执行。**

用户不需要手动调用 agent 或选择 reviewer。Claude 作为 orchestrator 自动完成：

```
用户描述目标
    │
    ▼
Step 1: PLAN ────── 制定计划，用户确认
    │
    ▼
Step 2: IMPLEMENT ── 执行（调用 Skill）
    │
    ▼
Step 3: VERIFY ───── 编译/运行验证输出正确
    │                  失败 → 修复 → 重新验证（最多 2 次）
    ▼
Step 4: REVIEW ───── 自动选择 Agent 审查（按文件类型）
    │
    ▼
Step 5: FIX ──────── 按 Blocking → Major → Minor 顺序修复
    │
    ▼
Step 6: RE-VERIFY ── 确认修复无误
    │
    ▼
Step 7: SCORE ────── 质量门控评分
    │
    ├── 分数 ≥ 阈值 → 向用户报告结果
    └── 分数 < 阈值 → 回到 Step 4（最多 3 轮）
```

**Agent 自动选择规则：**

| 修改的文件类型 | 自动触发的 Agent |
|---|---|
| `.wl`（推导脚本） | math-critic → math-fixer |
| `.tex`（论文） | econ-reviewer + proofreader + latex-auditor |
| `.tex` + `.wl` 同时 | math-critic + econ-reviewer + latex-auditor |
| 含 `\cite{}` 的文件 | lit-verifier |
| 含事实性声明 | fact-checker |
| 完整论文提交前 | 全部 Agent 并行 + referee-sim |

### 1.3 指令预算管理

**Claude 可靠遵循的指令上限约 100-150 条。** 架构设计必须尊重这个限制：

- **CLAUDE.md**（~120 行）+ **始终生效的 Rules**（~150 行）= 占用核心预算
- **路径作用域的 Rules**：仅在编辑匹配文件时加载，不占用常驻预算
- **Agent 指令**：仅在被调用时加载，不占用常驻预算
- **Skill 指令**：仅在用户触发时加载，不占用常驻预算

**所以 8 条规则可以共存——因为只有 3 条始终生效，其余按需加载。**

---

## 二、五层架构

借鉴 Sant'Anna 的五层分离，适配理论文章：

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: CLAUDE.md — 项目宪法（始终加载，~120行）              │
│   核心原则、文件结构、工具路径、Skill 速查表                      │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Rules — 领域知识（路径触发 + 始终生效）                 │
│   始终生效: wolfram-first, verify-before-claim, orchestrator  │
│   路径触发: journal-style(.tex), quality-gates(.tex/.wl) 等   │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Agents — 单维度审查员（按需调用）                       │
│   math-critic, math-fixer, econ-reviewer, referee-sim 等      │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Skills — 用户命令 /xxx（用户触发）                     │
│   /derive, /verify, /write, /compile 等                       │
├─────────────────────────────────────────────────────────────┤
│ Layer 5: Hooks — 机械执行（代码自动触发，不依赖上下文）           │
│   verify-reminder, context-monitor, pre/post-compact 等       │
└─────────────────────────────────────────────────────────────┘
```

**Layer 间的关键区别：**

| 层 | 何时加载 | 能否被压缩遗忘 | 适合放什么 |
|---|---|---|---|
| CLAUDE.md | 始终 | 不会（在磁盘） | 不变的核心原则 |
| Rules（始终） | 始终 | 可能 | 必须遵守的约束 |
| Rules（路径） | 编辑匹配文件时 | 可能 | 特定场景的详细指南 |
| Agents | 被调用时 | 不会（独立上下文） | 审查检查清单 |
| Skills | 用户触发时 | 不会（独立加载） | 执行工作流 |
| Hooks | 自动 | **绝不**（是代码） | 必须 100% 可靠的机械检查 |

---

## 三、流程总览

```
研究方向
  │
  ▼
Phase 1: /idea ──────────── 头脑风暴，确定研究问题
  │                          可选: Agent Debate（3个方向对比）
  ▼
Phase 2: /lit-review ──────── 文献检索与定位
  │                            lit-verifier 自动验证真实性
  ▼
Phase 2.5: /study ──────── 深度解剖核心论文（1-3 篇）
  │                          提取模型结构、建模技巧、创新点
  │                          用 Wolfram 复现关键结果
  │                          定位自己的贡献空间
  ▼
Phase 3: /model ──────────── 在学习基础上设计自己的模型
  │                          Spec-then-Plan（复杂模型）
  │                          用户确认后才进入推导
  ▼
Phase 4: /derive ──────────── Wolfram 符号推导（核心）
         /verify ──────────── 数值验证（3+组参数）
         /plot ────────────── 学术图形（PDF 矢量）
  │                          ┌──────────────────────────┐
  │                          │ 对抗式数学审查              │
  │                          │ math-critic（只读，找问题）  │
  │                          │     ↓                      │
  │                          │ math-fixer（读写，修复）     │
  │                          │     ↓                      │
  │                          │ math-critic（重新审计）      │
  │                          │ ... 最多 5 轮               │
  │                          └──────────────────────────┘
  ▼
Phase 5: /write ──────────── 逐章撰写（期刊规范）
         /compile ──────────── LaTeX → PDF
  │
  ▼
Phase 6: 多 Agent 并行审查 ── 全面质量审查
         ├── econ-reviewer     经济学逻辑
         ├── referee-sim       模拟审稿人（Fresh-Context）
         ├── proofreader       语言润色
         ├── lit-verifier      文献真实性
         ├── fact-checker      事实核查
         └── latex-auditor     格式审计
  │
  ▼
Phase 7: Orchestrator Loop ── 修复 → 重新审查（最多 3 轮）
         Quality Gate 评分 → 达标才能继续
  │
  ▼
Phase 8: /snapshot ──────── Git 版本快照
  │
  ▼
Phase 9: /submit ──────── 投稿准备
         /revision ──────── 审稿回复
```

---

## 四、Skills（18 个）

Skills 是面向用户的命令（`/skill-name`）。

### Phase 1-3：研究准备

| Skill | 命令 | 功能 | 输出 |
|---|---|---|---|
| **idea** | `/idea` | 头脑风暴研究问题 | 3-5 个研究方向 + 可行性评估 |
| **lit-review** | `/lit-review` | 系统文献检索 | 分类文献列表 + Related Literature 草稿 |
| **study** | `/study` | 深度解剖核心论文 | Study_Note.md + 复现脚本 .wl |
| **model** | `/model` | 设计博弈论模型 | Model_Setup.md + 分析路线图 |

**`/study` — 论文深度学习：**

理论经济学的研究范式是**站在巨人肩膀上**：读经典论文 → 理解建模技巧 → 在此基础上创新。`/study` 将这个过程系统化。

**输入：** 1-3 篇 PDF 或 .tex 论文（用户丢给 Claude）

**工作流程：**

```
Step 1: 解剖模型结构
  ├── 参与人、时序、信息结构
  ├── 需求函数形式（线性？CES？Shubik-Levitan？）
  ├── 成本函数形式（线性？二次？含 R&D？）
  ├── 目标函数（利润？社会福利？加权目标？）
  ├── 均衡概念（Nash / SPNE / PBE）
  └── 关键 Assumption 及其作用（为什么需要？去掉会怎样？）

Step 2: 提取建模技巧
  ├── 核心创新点是什么？（新参数？新博弈结构？新目标函数？）
  ├── 哪个假设特别巧妙？为什么？
  ├── 数学处理技巧（参数化方式、求解策略、如何保证 closed-form）
  ├── 比较静态和福利分析的推导思路
  └── 论文的局限性 → 我的潜在贡献空间

Step 3: Wolfram 复现（关键步骤）
  ├── 用 Wolfram 重新推导核心均衡
  ├── 验证论文的关键 Proposition
  ├── 确认自己真正理解了模型
  └── 生成 reproduce_[AuthorYear].wl 脚本

Step 4: 输出学习笔记
  └── Study_Note_[AuthorYear].md
      ├── 模型结构速览表
      ├── 建模技巧清单
      ├── 与我的研究的关联分析
      ├── 可借鉴的元素
      └── Wolfram 复现结果
```

**典型使用场景：**

```
场景 1: 学习经典框架
  用户: /study [De Fraja & Delbono 1989]
  Claude: 解剖混合寡头基本框架，Wolfram 复现均衡
         → "公有企业最大化 SW 而非 π，这导致产量更高、价格更低"

场景 2: 借鉴最新论文的技巧
  用户: /study [一篇最新 JIE 论文]
  Claude: "这篇的创新在于用 α·SW + (1-α)·π₀ 参数化公有企业目标，
           比纯 SW 假设更灵活。我们可以借鉴这个参数化。"

场景 3: 定位贡献
  用户: /study [3 篇最相关的论文]
  Claude: "三篇都没有考虑 AI 成本削减的非对称性。
           论文 A 用线性成本，B 用二次成本但无投资，C 有投资但对称。
           你的模型可以填补：非对称 AI 投资 + 混合寡头。"

场景 4: 复现并扩展
  用户: /study [d'Aspremont & Jacquemin 1988] 然后帮我把他们的 R&D 模型改成 AI 投资
  Claude: 先用 Wolfram 复现 AJ88 → 在此基础上替换成本函数 → /model 设计新模型
```

**`/study` 与其他 Skill 的协作：**

| 上游 | `/study` | 下游 |
|---|---|---|
| `/lit-review` 找到核心论文 | 深度解剖 1-3 篇 | `/model` 在此基础上创新 |
| 用户直接丢 PDF | 学习建模技巧 | `/derive` 借鉴求解策略 |
| `/revision` 审稿人推荐论文 | 学习并比较 | `/write` 补充 Related Literature |

**`/model` 的 Spec-then-Plan 协议：**（借鉴 Sant'Anna）

对于复杂或模糊的模型设计任务，先写需求规格书再做计划：

1. 问 3-5 个澄清问题
2. 生成 `quality_reports/specs/YYYY-MM-DD_description.md`
3. 每个需求标记优先级和清晰度：

| 标记 | 含义 |
|---|---|
| **MUST** | 不可妥协（如"必须有 closed-form 解"） |
| **SHOULD** | 最好有（如"最好包含混合寡头"） |
| **MAY** | 可选（如"可以加入不确定性扩展"） |
| **CLEAR** | 已完全明确 |
| **ASSUMED** | 合理假设，用户可覆盖 |
| **BLOCKED** | 无法继续，需用户回答 |

4. 用户确认规格书后，才制定推导计划

### Phase 4：数学推导（核心阶段）

| Skill | 命令 | 功能 | 输出 |
|---|---|---|---|
| **derive** | `/derive` | Wolfram 符号推导 | .wl 脚本 + LaTeX 公式 + .mx 状态文件 |
| **verify** | `/verify` | 数值代入验证 | Verification_Report.md |
| **plot** | `/plot` | 生成学术图形 | PDF 矢量图 |

**`/derive` 的 7 个标准阶段：**

```
Phase 1: 定义模型（效用/利润函数）
Phase 2: 求解子博弈（后向归纳，Solve[]）
Phase 3: 求解均衡（代入前一阶段结果）
Phase 4: 比较静态（D[] 求导）
Phase 5: 符号正负判断（Reduce[]）— 这是正确性的关键
Phase 6: 数值验证（3+组参数代入）
Phase 7: 保存结果（DumpSave[]）
```

**`/verify` 的检验标准：**

| 验证项 | 方法 | 通过标准 |
|---|---|---|
| FOC = 0 | 代入均衡值 | \|FOC\| < 10⁻¹⁰ |
| SOC < 0 | 代入均衡值 | SOC 为负 |
| 比较静态符号 | 数值求导 vs 解析 | 方向一致 |
| 福利一致性 | 直接计算 vs 公式 | 差异 < 10⁻¹⁰ |
| 非负约束 | 价格、产量、利润 | 均为非负 |

### Phase 5：写作与编译

| Skill | 命令 | 功能 | 输出 |
|---|---|---|---|
| **write** | `/write` | 撰写论文章节 | .tex 章节内容 |
| **compile** | `/compile` | LaTeX 编译 | PDF + 编译报告 |

### Phase 6：审查与核查

| Skill | 命令 | 功能 | 输出 |
|---|---|---|---|
| **proofread** | `/proofread` | 学术英语润色 | 修改建议列表 |
| **check-refs** | `/check-refs` | 参考文献真实性检查 | 验证报告 |
| **check-facts** | `/check-facts` | 特征事实/数据验证 | 验证报告 + 数据源 |

### Phase 8-9：版本与投稿

| Skill | 命令 | 功能 | 输出 |
|---|---|---|---|
| **snapshot** | `/snapshot` | Git 版本快照 | git commit |
| **submit** | `/submit` | 投稿准备 | 投稿清单 + Cover Letter |
| **revision** | `/revision` | 审稿回复 | Response Letter + 修改稿 |

### 元技能

| Skill | 命令 | 功能 | 输出 |
|---|---|---|---|
| **learn** | `/learn` | 捕获经验教训为持久化知识 | 新 Skill 或 MEMORY.md 条目 |
| **full-paper** | `/full-paper` | 端到端论文生成 | 完整论文 + 所有审查报告 |

**`/learn` — 自我进化循环：**（借鉴 Sant'Anna 最创新的设计）

当发现非显而易见的经验时：

```
Phase 1: EVALUATE — "这是否非显而易见？未来的我会受益吗？"
Phase 2: CHECK EXISTING — 搜索 .claude/skills/ 是否已有相关 Skill
Phase 3: DECIDE — 写入 MEMORY.md（通用经验）还是创建新 Skill（可复用流程）？
Phase 4: SAVE — 用 [LEARN:category] 标签记录

示例：
[LEARN:wolfram] FullSimplify 对含 Abs[] 的表达式可能超时 → 先用 PiecewiseExpand 再 Simplify
[LEARN:model] 线性需求 + 二次成本时，混合寡头必定有内点解（无需额外 Assumption）
[LEARN:latex] Wolfram TeXForm 输出 (c-1) 需手动转换为 -(1-c) 再调整外部符号
```

---

## 五、Agents（9 个）

### 5.1 对抗式数学审查（最核心的创新）

借鉴 Sant'Anna 的 Critic-Fixer 对抗模式，这是保证计算正确性的**最强机制**：

```
┌─────────────────────────────────────────┐
│         对抗式数学审查循环                  │
│                                          │
│  math-critic（只读，不能修改文件）          │
│    ├── 加载 .mx 文件                     │
│    ├── 独立用 Wolfram 复算关键结果         │
│    ├── 逐条检查 FOC/SOC/Reduce 结果      │
│    ├── 输出: math_critique.md            │
│    └── 判定: APPROVED / NEEDS REVISION   │
│              │                           │
│         NEEDS REVISION                   │
│              ↓                           │
│  math-fixer（读写，可修改 .wl 和 .tex）    │
│    ├── 读取 math_critique.md             │
│    ├── 修复推导错误                       │
│    ├── 重新运行 Wolfram 验证              │
│    └── 输出: 修改后的文件                  │
│              │                           │
│              ↓                           │
│  math-critic（重新审计，从零开始）          │
│    └── 最多 5 轮                         │
└─────────────────────────────────────────┘
```

**为什么有效？**
- **Critic 不能改文件**（只有 Read/Grep/Glob/Bash[Wolfram only] 权限）→ 没有淡化问题的动机
- **Fixer 不能自我审批**（修完必须由 Critic 重新审核）→ 杜绝"自说自话"
- **Critic 每轮从零审计**（Fresh Context）→ 无确认偏误

**math-critic 检查清单（10 项硬门控）：**

| # | 检查项 | 方法 | 失败 = |
|---|---|---|---|
| 1 | FOC 在均衡处 = 0 | Wolfram 代入验证 | BLOCKING |
| 2 | SOC 在均衡处 < 0 | Wolfram Reduce | BLOCKING |
| 3 | 均衡解唯一且在可行域内 | 检查解的个数和符号 | BLOCKING |
| 4 | 比较静态有 Reduce 支撑 | 检查每个符号声明 | BLOCKING |
| 5 | 福利函数定义一致 | 前后对比 | MAJOR |
| 6 | 成本结构前后一致 | 前后对比 | MAJOR |
| 7 | Assumption 充分 | 是否存在遗漏条件 | MAJOR |
| 8 | Corner solution 检查 | 边界条件代入 | MAJOR |
| 9 | 数值验证通过（3+组） | 参数代入 | MAJOR |
| 10 | LaTeX 公式与 Wolfram 一致 | TeXForm 输出对比 | MINOR |

**math-fixer 的约束：**
- 只能修复 Critic 明确指出的问题
- 每次修复必须附带 Wolfram 验证命令
- 不能自行添加新结论

### 5.2 经济学审查 Agents

| Agent | 职责 | 权限 | 输出 |
|---|---|---|---|
| **econ-reviewer** | 经济学逻辑和直觉 | 只读 | econ_review_report.md |
| **referee-sim** | 模拟 Referee 2（最刁难） | 只读 + Fresh Context | referee_report.md |

**referee-sim 使用 Fresh-Context Critique 模式：**（借鉴 Sant'Anna）

生成一个**完全没有对话历史**的新 Agent，只给它论文 PDF 和一个批评提示。这消除了"参与了写作过程所以有确认偏误"的问题。

```
Spawn 新 Agent:
  - 无对话上下文（Fresh Context）
  - 输入: 仅论文 .tex 文件
  - 角色: "你是顶级期刊最严格的审稿人"
  - 输出: Major/Minor 分类的审稿意见
```

**referee-sim 的 5 个审查维度：**

1. **贡献度**："这不就是 [经典论文] 加了一个参数吗？"
2. **假设合理性**："Assumption X 太强，放松后结论还成立吗？"
3. **模型选择**："为什么是 Cournot 不是 Bertrand？"
4. **遗漏因素**："忽略了进入退出/动态/不确定性的影响？"
5. **实证支撑**："数值例子太少，能否做参数扫描？"

### 5.3 文本与格式 Agents

| Agent | 职责 | 权限 | 输出 |
|---|---|---|---|
| **proofreader** | 学术英语语法/用词/风格 | 只读 | proofread_report.md |
| **lit-verifier** | 参考文献真实性（防编造） | 只读 + WebSearch | lit_verification_report.md |
| **fact-checker** | 事实性声明/数据验证 | 只读 + WebSearch | fact_check_report.md |
| **latex-auditor** | LaTeX 格式/编译质量 | 只读 + Bash | latex_audit_report.md |

### 5.4 Agent 权限分离原则

借鉴 Sant'Anna 的"分权"设计：

| 角色 | 可读文件 | 可改文件 | 可运行命令 | 可审批 |
|---|---|---|---|---|
| math-critic | ✅ | ❌ | ✅（仅 Wolfram） | ✅ |
| math-fixer | ✅ | ✅ | ✅（仅 Wolfram） | ❌ |
| econ-reviewer | ✅ | ❌ | ❌ | ✅ |
| referee-sim | ✅ | ❌ | ❌ | ✅ |
| proofreader | ✅ | ❌ | ❌ | ❌ |
| lit-verifier | ✅ | ❌ | ✅（仅 WebSearch） | ❌ |
| fact-checker | ✅ | ❌ | ✅（仅 WebSearch） | ❌ |
| latex-auditor | ✅ | ❌ | ✅（仅 pdflatex） | ❌ |

**核心原则：能找问题的不能改文件，能改文件的不能自我审批。**

### 5.5 Agent Debate 模式（可选）

借鉴 Sant'Anna 的 Agent Debate，用于模型设计阶段的方案选择：

```
/model 中遇到多种建模方案时：

Agent A: 为 Cournot 竞争辩护
Agent B: 为 Bertrand 竞争辩护
Agent C: 为 Stackelberg 竞争辩护

每个 Agent:
  - 充分论证自己方案的优势
  - 批判其他方案的弱点
  - 评估 closed-form 可解性

Claude 综合为决策矩阵，用户选择。
```

---

## 六、Rules（8 条）

### 6.1 始终生效的 Rules（~150 行，占用核心指令预算）

| 规则 | 文件 | 核心内容 |
|---|---|---|
| **wolfram-first** | `wolfram-first.md` | 所有数学运算必须通过 Wolfram |
| **verify-before-claim** | `verify-before-claim.md` | 声明前必须有 Reduce 输出 |
| **orchestrator-protocol** | `orchestrator-protocol.md` | 承包商模式的执行循环 |

**这三条始终生效，因为它们是数学正确性的底线。**

### 6.2 路径作用域的 Rules（仅匹配文件时加载）

| 规则 | 文件 | 触发路径 | 核心内容 |
|---|---|---|---|
| **plan-first** | `plan-first.md` | `*.wl` | 复杂推导先写路线图 |
| **journal-style** | `journal-style.md` | `*.tex`, `*.md` | Abstract/Intro 无数学符号 |
| **quality-gates** | `quality-gates.md` | `*.tex`, `*.wl` | 评分标准和门控阈值 |
| **version-control** | `version-control.md` | 所有文件 | Git 管理规范 |
| **session-logging** | `session-logging.md` | 所有文件 | 三时机日志记录 |

### 6.3 质量门控评分

**扣分标准（100 分制）：**

| 类别 | 扣分项 | 分值 |
|---|---|---|
| **Blocking** | 公式 LaTeX 编译失败 | -100 |
| **Blocking** | FOC/SOC 验证失败 | -100 |
| **数学** | Wolfram 未验证的符号声明 | -50 |
| **数学** | 缺少数值验证 | -20 |
| **数学** | SOC 未验证 | -20 |
| **文献** | 参考文献不存在（编造） | -30 |
| **事实** | 特征事实无数据源 | -15 |
| **写作** | Proposition 无经济学解释 | -15 |
| **写作** | Abstract/Intro 含数学符号 | -10 |
| **格式** | 交叉引用错误 | -5/处 |
| **语言** | 语法错误 | -2/处 |

**门控阈值：**

| 分数 | 门控 | 含义 |
|---|---|---|
| **< 70** | 阻止 | 必须修复 Blocking issues 才能继续 |
| **70-79** | 警告 | 允许但附带改进建议 |
| **80-89** | 可提交 | 达到投稿标准 |
| **90-94** | 良好 | 高质量 |
| **≥ 95** | 优秀 | 目标水平 |

**探索性工作**（如测试替代模型设定）门槛降至 **60/100**：
- 不需要完整的 Proposition 格式
- 不需要语言润色
- 但 FOC/SOC 验证仍然必须（数学正确性不能妥协）

### 6.4 会话日志规则（三时机记录）

借鉴 Sant'Anna 的 session-logging，在三个时机自动记录：

| 时机 | 记录什么 | 写入哪里 |
|---|---|---|
| **计划确认后** | 目标、方法、理由 | `quality_reports/session_logs/` |
| **关键决策时** | 做了什么决定、为什么 | 即时追加，不批量 |
| **会话结束时** | 摘要、质量分数、遗留问题 | 会话日志 + MEMORY.md |

> "Git 记录**做了什么**；会话日志记录**为什么这么做**。"

---

## 七、Hooks（5 个）

Hooks 是 Python/Shell 脚本，**自动触发，不依赖上下文记忆**。这是 Sant'Anna 架构中最精妙的设计——用代码保证机械性检查绝不遗漏。

### 设计原则

| 用 Hook | 用 Rule |
|---|---|
| 必须 100% 可靠的机械检查 | 需要判断力的规范 |
| 文件存在？计数器超阈值？ | 验证是否正确？写作是否规范？ |
| 即使上下文被压缩也不能忘 | 可以从 CLAUDE.md 重新加载 |

### Hook 列表

| # | Hook | 触发事件 | 功能 |
|---|---|---|---|
| 1 | **verify-reminder** | PostToolUse[Write\|Edit] | 编辑 .wl/.tex 后提醒"编译/运行验证" |
| 2 | **context-monitor** | PostToolUse[Bash\|Task] | 上下文使用率达 40%/55%/65% 时提醒 `/learn` |
| 3 | **pre-compact** | PreCompact | 压缩前保存当前计划、任务、决策到 JSON |
| 4 | **post-compact-restore** | SessionStart[compact\|resume] | 压缩后恢复状态，打印恢复指令 |
| 5 | **log-reminder** | Stop | 检查会话日志是否最近更新，提醒记录 |

### Hook 详细说明

**verify-reminder：**
编辑 `.wl` 文件后 → 提醒 "运行 wolframscript 验证结果"
编辑 `.tex` 文件后 → 提醒 "用 /compile 编译确认无误"
节流：同一文件 60 秒内不重复提醒。

**context-monitor（借鉴 Sant'Anna 的 /learn 催促机制）：**

| 上下文使用率 | 提醒内容 |
|---|---|
| 40%, 55%, 65% | "有值得记住的发现吗？用 `/learn` 在压缩前保存。" |
| 80% | "自动压缩即将到来。不要急。" |
| 90% | "完成当前任务，保证完整质量。不要偷工减料。" |

每个阈值每会话只提醒一次。

**pre-compact + post-compact-restore（上下文存活系统）：**

```
压缩前：
  1. 找到 quality_reports/plans/ 中最新未完成计划
  2. 提取当前任务（第一个未勾选的 - [ ] 项）
  3. 从会话日志提取最近决策
  4. 保存到 ~/.claude/sessions/[project-hash]/pre-compact-state.json

压缩后：
  1. 读取 pre-compact-state.json
  2. 打印恢复信息：计划名、当前任务、最近决策
  3. 指示：读取计划 → 检查 git status → 从断点继续
  4. 删除状态文件（一次性使用）
```

---

## 八、四层持久化系统

借鉴 Sant'Anna 的核心洞察：**上下文窗口是临时的，所有值得保留的信息必须写入磁盘。**

| 层 | 文件位置 | 存活于压缩？ | 内容 | 更新频率 |
|---|---|---|---|---|
| 项目宪法 | `CLAUDE.md` | ✅ | 核心原则、工具路径 | 很少变动 |
| 经验教训 | `MEMORY.md` | ✅ | `[LEARN:category]` 条目 | 每次有新发现 |
| 任务计划 | `quality_reports/plans/` | ✅ | 推导路线图、待办清单 | 每个任务一个 |
| 决策日志 | `quality_reports/session_logs/` | ✅ | 为什么做了某个决策 | 实时追加 |
| 对话上下文 | Claude 上下文窗口 | ❌ | 当前工作记忆 | 自动压缩会丢失 |

### MEMORY.md 的两层设计

| 层 | 文件 | Git 管理 | 内容 |
|---|---|---|---|
| **通用经验** | `~/.claude/MEMORY.md` | 提交 | 所有项目通用的 Wolfram/LaTeX/经济学经验 |
| **项目特定** | `项目目录/MEMORY_LOCAL.md` | 提交 | 该项目特有的参数设定、模型决策 |

**判断标准：** "另一个经济学理论项目也会受益吗？" → 通用 MEMORY.md。否则 → 项目 MEMORY_LOCAL.md。

### 计划存盘

所有推导计划保存到磁盘（不仅在上下文中）：

```
quality_reports/
├── plans/
│   ├── 2026-03-01_equilibrium-derivation.md
│   ├── 2026-03-05_welfare-analysis.md
│   └── 2026-03-10_comparative-statics.md
├── session_logs/
│   ├── 2026-03-01_session.md
│   └── 2026-03-05_session.md
└── reviews/
    ├── math_critique.md
    ├── econ_review_report.md
    └── referee_report.md
```

---

## 九、协作关系

### 9.1 Skill 串行管道

```
/idea → /lit-review → /study → /model → /derive → /verify → /plot → /write → /compile
                        │                  ↑                              │
                  深度解剖核心论文           │      ┌── 对抗式数学审查 ──┐   │
                  Wolfram 复现              │      │ math-critic        │   │
                        │                  │      │    ↕               │   │
                        ▼                  │      │ math-fixer         │   │
                  在学习基础上建模           │      └────────────────────┘   │
                                           │                               │
                                           └──── 如果审查发现数学错误 ────────┘
```

### 9.2 Phase 6 并行审查

```
                    ┌─── econ-reviewer ─── econ_review_report.md
                    ├─── referee-sim ───── referee_report.md（Fresh Context）
完整论文 .tex/.pdf ──┼─── proofreader ───── proofread_report.md
                    ├─── lit-verifier ──── lit_verification_report.md
                    ├─── fact-checker ──── fact_check_report.md
                    └─── latex-auditor ─── latex_audit_report.md
```

**汇总时按严重程度排序：**
1. **Blocking**：数学错误、编译失败、文献编造 → 必须修复
2. **Major**：经济学逻辑、事实错误、审稿人核心质疑 → 应该修复
3. **Minor**：语言、格式、细节 → 建议修复

### 9.3 Orchestrator 自动调度

用户只需说目标，Orchestrator 自动选择 Agent：

| 用户说 | Orchestrator 做 |
|---|---|
| "帮我看看这篇论文的模型" | /study → 解剖模型 + Wolfram 复现 → Study_Note.md |
| "推导均衡" | /derive → math-critic/fixer 对抗审查 → /verify |
| "写 Section 3" | /write → /compile → proofreader + latex-auditor |
| "准备投稿" | 全部 Agent 并行 → quality-gate 评分 → /submit |
| "回复审稿意见" | /revision → 定向修改 → 相关 Agent 重新审查 |

### 9.4 Rules 的加载时机

```
始终生效（核心预算内）:
  wolfram-first ──────── 贯穿全流程
  verify-before-claim ── 贯穿全流程
  orchestrator-protocol ─ 贯穿全流程

路径触发（按需加载）:
  plan-first ──────── 编辑 .wl 时
  journal-style ───── 编辑 .tex 时
  quality-gates ───── 编辑 .tex/.wl 时
  version-control ─── 所有文件
  session-logging ─── 所有文件
```

### 9.5 Hooks 的触发时机

```
编辑 .wl/.tex 后 → verify-reminder（提醒编译验证）
每次 Bash/Task 后 → context-monitor（监控上下文用量）
压缩前 → pre-compact（保存状态到 JSON）
压缩后/恢复时 → post-compact-restore（打印恢复指令）
每次响应后 → log-reminder（提醒更新会话日志）
```

---

## 十、文件结构

```
~/.claude/
├── skills/                         # 18 个 Skills
│   ├── idea/SKILL.md               # Phase 1: 研究构想
│   ├── lit-review/SKILL.md         # Phase 2: 文献检索
│   ├── study/SKILL.md              # Phase 2.5: 论文深度学习 ★新增
│   ├── model/SKILL.md              # Phase 3: 模型设计
│   ├── derive/SKILL.md             # Phase 4: Wolfram 符号推导
│   ├── verify/SKILL.md             # Phase 4: 数值验证
│   ├── plot/SKILL.md               # Phase 4: 绘图
│   ├── write/SKILL.md              # Phase 5: 论文撰写
│   ├── compile/SKILL.md            # Phase 5: LaTeX 编译
│   ├── proofread/SKILL.md          # Phase 6: 语言润色
│   ├── check-refs/SKILL.md         # Phase 6: 文献验证
│   ├── check-facts/SKILL.md        # Phase 6: 事实核查
│   ├── snapshot/SKILL.md           # Phase 8: Git 快照
│   ├── submit/SKILL.md             # Phase 9: 投稿
│   ├── revision/SKILL.md           # Phase 9: 审稿回复
│   ├── learn/SKILL.md              # 元技能: 经验捕获 ★新增
│   └── full-paper/SKILL.md         # 端到端
│
├── agents/                         # 9 个 Agents
│   ├── math-critic.md              # 数学审计（只读）★新增
│   ├── math-fixer.md               # 数学修复（读写）★新增
│   ├── econ-reviewer.md            # 经济学审查
│   ├── referee-sim.md              # 模拟审稿人（Fresh Context）
│   ├── proofreader.md              # 语言润色
│   ├── lit-verifier.md             # 文献验证
│   ├── fact-checker.md             # 事实核查
│   └── latex-auditor.md            # LaTeX 审计
│
├── rules/                          # 8 条 Rules
│   ├── wolfram-first.md            # [始终] 数学必须经过 Wolfram
│   ├── verify-before-claim.md      # [始终] 先验证再声明
│   ├── orchestrator-protocol.md    # [始终] 承包商模式执行循环 ★新增
│   ├── plan-first.md               # [路径] 复杂推导先规划
│   ├── journal-style.md            # [路径] 期刊写作规范
│   ├── quality-gates.md            # [路径] 质量门控
│   ├── version-control.md          # [路径] Git 版本管理
│   └── session-logging.md          # [路径] 三时机会话日志
│
├── hooks/                          # 5 个 Hooks ★新增
│   ├── verify-reminder.py          # 编辑后提醒验证
│   ├── context-monitor.py          # 上下文用量监控
│   ├── pre-compact.py              # 压缩前保存状态
│   ├── post-compact-restore.py     # 压缩后恢复状态
│   └── log-reminder.py             # 提醒更新会话日志
│
├── MEMORY.md                       # 跨会话通用经验
└── WORKFLOW_QUICK_REF.md           # 本文档
```

**各项目目录结构：**

```
项目文件夹/
├── CLAUDE.md                       # 项目宪法（~120行）
├── MEMORY_LOCAL.md                 # 项目特定经验
├── *.wl                            # Wolfram 推导脚本
├── *.tex                           # LaTeX 论文
├── *.pdf                           # 图形和编译输出
├── *.mx                            # Wolfram 状态文件
└── quality_reports/
    ├── plans/                      # 推导计划（存盘）
    ├── session_logs/               # 会话日志
    ├── specs/                      # 需求规格书
    └── reviews/                    # Agent 审查报告
```

---

## 十一、与 Sant'Anna 的对照

| 维度 | Sant'Anna（实证） | Vibe Modelling v2（理论） | 借鉴/改造 |
|---|---|---|---|
| 计算工具 | R / Stata | Wolfram Engine | 改造 |
| 核心产出 | Beamer slides + R packages | LaTeX 论文 + 数学证明 | 改造 |
| 承包商模式 | ✅ orchestrator-protocol | ✅ 相同架构 | 借鉴 |
| 对抗式审查 | quarto-critic / quarto-fixer | math-critic / math-fixer | **核心借鉴** |
| Fresh-Context | quarto-critic | referee-sim | 借鉴 |
| 路径作用域 Rules | 14 条路径触发 | 5 条路径触发 | 借鉴 |
| 指令预算管理 | ~150 条上限 | 相同约束 | 借鉴 |
| /learn 自我进化 | ✅ | ✅ | 借鉴 |
| Spec-then-Plan | ✅ MUST/SHOULD/MAY | ✅ 用于 /model | 借鉴 |
| 四层持久化 | MEMORY + plans + logs + hooks | 相同架构 | 借鉴 |
| Hooks（5个） | 7 个 Python/Shell hooks | 5 个（适配理论场景） | 借鉴 |
| Agent Debate | ✅ | ✅ 用于模型选择 | 借鉴 |
| 两级质量 | 80(production) / 60(exploration) | 80(production) / 60(exploration) | 借鉴 |
| 教学审查 | pedagogy-reviewer（13模式） | 无（不做教学） | 不适用 |
| R 代码审查 | r-reviewer | 无 | 不适用 |
| Wolfram 正确性 | 无 | math-critic 10 项硬门控 | **原创** |
| FOC/SOC 验证 | 无 | verify-before-claim | **原创** |
| 论文深度学习 | 无 | /study（解剖+复现+定位贡献） | **原创** |

---

## 十二、实施批次

### Batch 1 — 基础设施 + 核心推导
1. 目录结构
2. `/derive` — Wolfram 符号推导
3. `/verify` — 数值验证
4. `/compile` — LaTeX 编译
5. `wolfram-first` 规则
6. `verify-before-claim` 规则
7. `MEMORY.md` 模板

### Batch 2 — 对抗式审查 + 写作
8. `math-critic` Agent（只读，核心创新）
9. `math-fixer` Agent（读写）
10. `orchestrator-protocol` 规则
11. `/write` — 论文撰写
12. `/model` — 模型设计
13. `/plot` — Wolfram 绘图
14. `econ-reviewer` Agent
15. `referee-sim` Agent（Fresh Context）
16. `journal-style` 规则
17. `quality-gates` 规则

### Batch 3 — 辅助审查 + 元技能
18. `/idea` — 研究构想
19. `/lit-review` — 文献检索
20. `/study` — 论文深度学习（Wolfram 复现）
21. `/proofread` — 语言润色
22. `/check-refs` — 参考文献验证
23. `/check-facts` — 事实核查
24. `/learn` — 经验捕获
25. `proofreader` Agent
26. `lit-verifier` Agent
27. `fact-checker` Agent
28. `latex-auditor` Agent

### Batch 4 — 持久化 + 版本管理
29. 5 个 Hooks（verify-reminder, context-monitor, pre/post-compact, log-reminder）
30. `/snapshot` — Git 版本快照
31. `/submit` — 投稿准备
32. `/revision` — 审稿意见回复
33. `version-control` 规则
34. `plan-first` 规则
35. `session-logging` 规则

### Batch 5 — 整合与测试
36. `/full-paper` — 端到端工作流
37. 在 AI 论文项目上端到端测试
38. 调优和迭代

---

## 十三、典型使用场景

### 场景 1：从零开始一篇论文

```
用户: 我想研究 AI 如何影响混合寡头中的企业竞争

Claude (Orchestrator):
  1. /idea → 提出 3-5 个方向（可选 Agent Debate）
  2. 用户选择方向
  3. /lit-review → 文献检索 → lit-verifier 自动验证
  4. /study → 深度解剖 2-3 篇核心论文 → Wolfram 复现关键结果
  5. /model → 在学习基础上设计模型 → Spec-then-Plan → Wolfram 预检
  6. 用户确认模型
  7. /derive → 完整符号推导
  8. math-critic/fixer 对抗审查（最多 5 轮）
  9. /verify → 数值验证
  10. /plot → 生成图形
  11. /write → 逐章撰写
  12. /compile → 生成 PDF
  13. 6 个 Agent 并行审查
  14. Orchestrator 修复循环（最多 3 轮）
  15. Quality Gate 评分 ≥ 80 → /snapshot → /submit
```

### 场景 2：学习经典论文后建模

```
用户: [丢入 d'Aspremont & Jacquemin 1988 的 PDF]
      帮我学习这篇的 R&D 投资模型，然后改成 AI 成本削减

/study:
  1. 解剖 AJ88 模型结构:
     - 两阶段: Stage 1 企业选 R&D 投入 x → Stage 2 Cournot 竞争
     - 成本函数: c_i(x_i, x_j) = A - x_i - βx_j（含溢出 β）
     - R&D 成本: γx²/2（二次调整成本）
  2. 提取建模技巧:
     - 用线性溢出参数 β 控制外部性强度（巧妙！）
     - 二次 R&D 成本保证内点解
     - 合作 vs 非合作的对比框架
  3. Wolfram 复现 → reproduce_AJ1988.wl → 验证均衡解
  4. 输出 Study_Note_AJ1988.md

/model:（在 /study 基础上）
  将 AJ88 的 R&D 投资 → 替换为 AI 成本削减参数 φ
  将对称双寡头 → 改为混合寡头（公有 + 私有）
  保留二次调整成本的处理技巧
```

### 场景 3：推导出错后的修复（对抗式审查）

```
math-critic 发现: "Proposition 3 的比较静态 ∂q₁*/∂φ > 0
                   缺少 Wolfram Reduce 支撑" [BLOCKING]

math-fixer:
  1. 运行 Reduce[D[q1star, phi] > 0 && 0<c<1 && ...]
  2. 发现: 仅在 γ > γ̄ 时成立（不是全参数域）
  3. 修改 Proposition 3，添加条件 "when γ > γ̄"
  4. 更新 .tex 文件

math-critic (Round 2):
  审计通过 → APPROVED
```

### 场景 4：回复审稿意见

```
用户: [粘贴审稿意见]

/revision → 解析意见，分类 Major/Minor/Optional
  ├── Major 1: "Assumption 太强"
  │   → /derive 补充放松假设后的推导
  │   → math-critic/fixer 验证新结果
  ├── Major 2: "缺少 Bertrand 对比"
  │   → /model 设计 Bertrand 变体
  │   → /derive 推导
  ├── Minor 1-5: 文字修改
  │   → /write 修改
  └── 生成 Response Letter + 标注版论文
      → /compile → /snapshot
```

---

## 十四、工具依赖

| 工具 | 路径 | 用途 |
|---|---|---|
| Wolfram Engine 14.3.0 | `/d/Wolf/wolframscript.exe` | 所有符号计算 |
| MikTeX (pdflatex) | `/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe` | LaTeX 编译 |
| Git | 系统 PATH | 版本管理 |
| Python 3 | 系统 PATH | Hooks 脚本 |

---

## 十五、渐进式采用

**不需要第一天就用全部。** 从最小核心开始，按需扩展：

```
Level 0: CLAUDE.md + wolfram-first 规则
         → 已经比纯对话好很多

Level 1: + /derive + /verify + /compile
         → 核心推导工作流

Level 2: + math-critic/fixer + orchestrator-protocol
         → 对抗式数学审查（质量飞跃）

Level 3: + /study + /write + /model + econ-reviewer + referee-sim
         → 论文学习 + 完整写作和审查

Level 4: + Hooks + /learn + 持久化系统
         → 跨会话经验积累

Level 5: + 全部辅助 Agent + /full-paper
         → 端到端自动化
```
