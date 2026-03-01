---
name: proofread
description: 学术英语润色。检查语法、用词、时态一致性、学术风格。
argument-hint: [.tex 文件路径或章节名]
---

# 语言润色

检查和改进论文的学术英语质量。

## 检查项

### 语法
- 主谓一致
- 时态一致（模型描述现在时，文献回顾过去时）
- 冠词使用（the/a/an）
- 介词搭配

### 学术用语
- 避免口语化："We can see that" → "We observe that"
- 避免冗余："It is obvious that" → 直接陈述
- 避免模糊："some" → 具体数量或 "several"
- 避免过于随意："Interestingly" → 删除，直接说结论

### 专业术语
- strategic complements（不是 "strategic friends"）
- social welfare（不是 "social good"）
- comparative statics（不是 "comparative static"，注意复数）
- first-order condition（不是 "first order condition"，注意连字符）

### 句子质量
- 长句拆分（超过 3 行的句子考虑拆分）
- 段落逻辑衔接（每段首句承上启下）
- 避免连续 3 个以上被动语态

## 输出格式

```markdown
# Proofread Report

## 统计
- 检查段落数: X
- 发现问题: Y 处
- 严重程度: Z major, W minor

## 修改建议
### 1. [位置: Section X, paragraph Y]
- 原文: "..."
- 建议: "..."
- 原因: [语法/用词/风格]
```
