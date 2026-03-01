---
name: study
description: 深度解剖核心论文。提取模型结构、建模技巧，用 Wolfram 复现关键结果，定位贡献空间。
argument-hint: [PDF/论文路径 或 论文标题]
---

# 论文深度学习

系统化学习经典或最新理论文献：解剖模型 → 提取技巧 → Wolfram 复现 → 定位贡献。

## 工作流程

### Step 1：解剖模型结构

阅读论文后提取以下要素：

| 要素 | 具体内容 |
|---|---|
| 参与人 | 谁在做决策？几个？对称/非对称？ |
| 行动空间 | 选什么变量？连续/离散？ |
| 时序 | 几个阶段？谁先谁后？ |
| 信息结构 | 完全/不完全信息？ |
| 需求函数 | 线性？CES？Shubik-Levitan？ |
| 成本函数 | 线性？二次？含投资/R&D？ |
| 目标函数 | 利润？社会福利？加权？ |
| 均衡概念 | Nash / SPNE / PBE？ |
| 关键 Assumption | 每条假设的作用是什么？去掉会怎样？ |

### Step 2：提取建模技巧

- 核心创新点是什么？（新参数？新博弈结构？新目标函数？）
- 哪个假设特别巧妙？为什么？
- 数学处理技巧（参数化方式、求解策略、如何保证 closed-form）
- 比较静态和福利分析的推导思路
- 论文的局限性 → 我的潜在贡献空间

### Step 3：Wolfram 复现

**这是最关键的步骤** — 确保真正理解了模型。

编写 `reproduce_[AuthorYear].wl` 脚本：

```mathematica
(* ============================================ *)
(* 复现: [Author (Year)] - [论文标题简称]          *)
(* ============================================ *)

(* Phase 1: 按论文设定定义模型 *)
demand = ...;
cost0 = ...; cost1 = ...;
profit0 = ...; profit1 = ...;

(* Phase 2: 复现均衡（按论文的求解方法） *)
foc = {D[profit0, q0], D[profit1, q1]};
sol = Solve[foc == 0, {q0, q1}];

(* Phase 3: 验证论文的关键 Proposition *)
Print["Proposition 1: dq*/dphi = ", D[qstar, phi] // Simplify];
Print["论文声称: > 0"];
Print["Reduce: ", Reduce[D[qstar, phi] > 0 && assumptions, params, Reals]];

(* Phase 4: 数值代入检验 *)
params = {c -> 0.3, phi -> 0.5, gamma -> 2};
Print["数值检验: q* = ", qstar /. params // N];

(* Phase 5: 保存复现结果 *)
DumpSave["reproduce_AuthorYear.mx", {qstar, ...}];
```

通过 `wolframscript -file reproduce_AuthorYear.wl` 执行。

### Step 4：输出学习笔记

生成 `Study_Note_[AuthorYear].md`：

```markdown
# Study Note: [Author (Year)]
## [论文完整标题]

### 模型结构速览
| 要素 | 设定 |
|---|---|
| 参与人 | ... |
| 时序 | ... |
| ... | ... |

### 建模技巧
1. [技巧1]: [为什么巧妙]
2. [技巧2]: [为什么巧妙]

### Wolfram 复现结果
- 均衡解: $q^* = ...$（与论文一致 ✓）
- Proposition 1: ✓ 复现成功
- Proposition 2: ✓ 复现成功

### 与我的研究的关联
- 可借鉴: ...
- 关键差异: ...
- 贡献空间: ...

### 局限性（= 我的机会）
1. ...
2. ...
```

## 注意事项

- 如果论文没有给出完整的数学推导，用 Wolfram 补全
- 如果复现结果与论文不一致，标记为"需要检查"并说明差异
- 复现脚本保留在项目目录中，方便后续引用
