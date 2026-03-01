---
name: snapshot
description: Git 版本快照。在关键节点创建版本快照，管理分支策略。
argument-hint: [快照描述，如 "model setup complete"]
---

# Git 版本快照

在论文开发的关键节点创建 Git 版本快照，保护工作进度。

## 工作流程

### Phase 1：检查状态

```bash
git status
git log --oneline -5
```

确认：
- 当前分支
- 未提交的更改
- 最近的提交历史

### Phase 2：创建快照

根据当前阶段选择 commit 前缀：

| 前缀 | 阶段 | 示例 |
|---|---|---|
| `idea:` | 研究构想 | `idea: AI cost reduction in mixed duopoly` |
| `lit:` | 文献相关 | `lit: add related literature section` |
| `model:` | 模型设定 | `model: initial Cournot setup with AI` |
| `derive:` | 推导结果 | `derive: equilibrium solved` |
| `write:` | 论文文本 | `write: Section 3 equilibrium analysis` |
| `figure:` | 图形 | `figure: comparative statics plots` |
| `verify:` | 验证 | `verify: numerical verification passed` |
| `review:` | 审查修复 | `review: fix SOC verification` |
| `compile:` | 编译 | `compile: clean PDF output` |
| `submit:` | 投稿 | `submit: JIE first submission` |
| `revision:` | 修改 | `revision: R1 referee 1 comments` |
| `backup:` | 安全备份 | `backup: before changing cost structure` |

### Phase 3：执行

```bash
# 添加所有相关文件（排除临时文件）
git add *.tex *.bib *.wl *.pdf figures/

# 创建带前缀的 commit
git commit -m "<prefix>: <描述>"
```

### Phase 4：分支管理（如需）

```
main ────────────────────── 最终投稿版本
  ├── draft/v1 ──────────── 第一稿
  │     ├── derive ──────── 推导分支
  │     └── write ───────── 写作分支
  ├── revision/r1 ───────── R&R 第一次修改
  └── revision/r2 ───────── R&R 第二次修改
```

创建新分支：
```bash
git checkout -b draft/v1    # 开始新草稿
git checkout -b revision/r1 # 开始修改
```

## 自动快照时机

以下节点应自动提醒创建快照：
- 模型设计确认后
- 每个推导阶段完成后
- 重大修改前（先 backup）
- 审查修复后
- 编译成功后
- 投稿前

## 安全规则

- **永远不要** force push main 分支
- 修改稿和原稿**必须**在不同分支
- 重大模型修改前**必须**先 backup 快照
