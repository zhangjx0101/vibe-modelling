---
description: "Git 版本管理规范：提交规范、分支策略、安全规则"
---

# Version Control 规则

## 提交规范

每次 commit 使用以下前缀：

```
idea:     研究构想
lit:      文献相关
model:    模型设定变更
derive:   推导结果
write:    论文文本
figure:   图形生成
verify:   验证结果
review:   审查修复
compile:  编译相关
submit:   投稿相关
revision: 修改相关
backup:   安全备份
```

## 强制规则

1. 每个 Phase 结束至少一次 commit
2. 重大模型修改前先 `backup:` 快照
3. 永远不要 force push main 分支
4. 修改稿和原稿必须在不同分支
5. `.wl` 脚本和 `.tex` 文件必须一起提交（保持同步）

## 分支策略

- `main`：最终投稿版本
- `draft/vN`：第 N 稿
- `revision/rN`：第 N 次修改
- 功能分支：`derive`, `write` 等（从 draft 分出）
