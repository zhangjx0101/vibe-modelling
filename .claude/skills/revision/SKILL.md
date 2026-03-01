---
name: revision
description: 审稿意见回复。解析审稿意见，逐条制定回复策略，生成 Response Letter。
argument-hint: [审稿意见文件路径]
---

# 审稿意见回复

系统性地处理审稿意见，管理论文修改，生成专业的 Response Letter。

## 工作流程

### Phase 1：解析审稿意见

读取审稿意见（PDF 或文本），将每条意见分类：

| 类别 | 定义 | 优先级 |
|---|---|---|
| **Major** | 影响结论或方法的核心问题 | 必须修改 |
| **Minor** | 改善表述或补充细节 | 建议修改 |
| **Optional** | 审稿人的风格偏好 | 可选修改 |

为每条意见标注：
- 审稿人编号（Referee 1/2/3）
- 意见编号
- 涉及的论文章节
- 是否需要重新推导

### Phase 2：制定回复策略

对每条意见制定策略：

| 策略 | 适用情况 |
|---|---|
| **Accept & Revise** | 意见正确，修改论文 |
| **Partially Accept** | 部分采纳，说明理由 |
| **Respectfully Disagree** | 礼貌地解释为何不修改 |
| **Already Addressed** | 指出论文中已有相关内容 |

### Phase 3：创建修改分支

```bash
git checkout -b revision/r1
```

### Phase 4：逐条修改

按优先级逐条处理：
1. 先处理所有 Major 意见
2. 再处理 Minor 意见
3. 最后处理 Optional 意见

每处修改需要：
- 在论文中标注修改位置（用颜色或注释）
- 记录修改内容
- 如涉及数学，用 Wolfram 重新推导

### Phase 5：生成 Response Letter

格式：

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}

\begin{document}

\title{Response to Referees' Comments}
\maketitle

We thank the editor and the referees for their constructive
comments. We have carefully revised the manuscript to address
all concerns. Below we provide a point-by-point response.

\section*{Response to Referee 1}

\subsection*{Comment 1}
\begin{quote}
``[原文引用审稿人的意见]''
\end{quote}

\textbf{Response:} We thank the referee for this insightful
comment. [详细回复...]

[See revised manuscript, Section X, page Y]

\subsection*{Comment 2}
...

\section*{Response to Referee 2}
...

\end{document}
```

### Phase 6：更新投稿日志

```markdown
## Revision #1
- 日期: [YYYY-MM-DD]
- 状态: Revised and Resubmitted
- Major 修改: X 处
- Minor 修改: Y 处
- 新增内容: [简述]
- Response Letter: revision/response_r1.tex
```

## 回复写作原则

- **感谢在先**：每条回复先感谢审稿人
- **具体引用**：指出修改在论文中的精确位置
- **不回避**：对每条意见都给出实质性回应
- **礼貌坚定**：不同意时用数据/推导支撑
- **简洁清晰**：回复长度与意见重要性成正比
