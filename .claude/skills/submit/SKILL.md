---
name: submit
description: 投稿准备。根据目标期刊调整格式，生成投稿材料清单，记录投稿状态。
argument-hint: [目标期刊名称]
---

# 投稿准备

根据目标期刊要求准备投稿材料，追踪投稿状态。

## 工作流程

### Phase 1：期刊格式调整

根据目标期刊调整论文格式：

| 期刊 | 文档类 | 引用格式 | 特殊要求 |
|---|---|---|---|
| AER | article, 12pt | Author (Year) | 匿名审稿，无致谢 |
| RAND | article, 12pt | Author (Year) | Double-spaced |
| JIE | article, 12pt | Author (Year) | Wiley 模板 |
| JET | elsarticle | Numbered | Elsevier 模板 |
| GEB | elsarticle | Numbered | Elsevier 模板 |
| IJIO | elsarticle | Numbered | Elsevier 模板 |

调整项目：
- 页边距、行距、字体大小
- 引用格式（natbib 设置）
- 标题页格式
- 脚注/尾注格式
- 图表位置（文中 vs 文末）

### Phase 2：投稿材料清单

生成并检查：

- [ ] 论文 PDF（匿名版，如期刊要求）
- [ ] 封面信（Cover Letter）
- [ ] 标题页（含作者信息，如单独要求）
- [ ] 摘要页（如单独要求）
- [ ] 在线附录 / 补充材料
- [ ] 图表（如需单独上传）
- [ ] 利益冲突声明
- [ ] 数据可获得性声明（理论文章通常 N/A）
- [ ] 推荐审稿人名单（如需）

### Phase 3：Cover Letter 模板

```
Dear Editor,

We would like to submit our manuscript entitled "[Title]"
for consideration for publication in [Journal].

[1-2 句描述研究问题]

[1-2 句描述主要贡献]

[1 句描述与期刊的契合度]

This manuscript has not been published elsewhere and is not
under consideration by another journal.

We look forward to your consideration.

Sincerely,
[Authors]
```

### Phase 4：记录投稿信息

在项目根目录创建/更新 `SUBMISSION_LOG.md`：

```markdown
## Submission #1
- 期刊: [Journal Name]
- 投稿日期: [YYYY-MM-DD]
- 稿件编号: [待分配]
- 状态: Submitted
- 备注: [任何特殊说明]
```

### Phase 5：最终检查

投稿前自动运行 quality-gates 评分：
- 分数 ≥ 85：可以投稿
- 分数 70-84：附带警告，用户决定
- 分数 < 70：阻止投稿，列出 blocking issues
