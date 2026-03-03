# Export Workflow 规则

## Word 导出（Markdown → .docx）

### 工具链
- **预处理**：Wolfram Engine `StringReplace`（不用 sed/perl，避免反斜杠转义问题）
- **转换**：Pandoc `/d/software/pandoc-3.8.3-windows-x86_64/pandoc-3.8.3/pandoc`

### 标准流程

```
Manuscript.md → [Wolfram 预处理] → temp.md → [Pandoc] → .docx
                                                ↓
                                          删除 temp.md
```

1. 运行 `preprocess_md.wl` 替换不兼容 LaTeX 命令（`\tag{}` → `\qquad\text{()}`）
2. 运行 pandoc：`--from markdown+footnotes+pipe_tables+tex_math_dollars --standalone`
3. 清理临时文件

### 注意事项
- 图片必须是 PNG/JPG（pandoc 不支持 PDF 嵌入 Word）
- `\tag{}` 等 amsmath 专属命令需预处理
- 用 Wolfram `StringReplace` 处理 LaTeX 文本，不用 sed/perl

## 推导日志

### 强制要求
每个 `.wl` 推导脚本**必须**同时生成 `.txt` 日志文件，包含：

| 内容 | 说明 |
|---|---|
| Kernel 版本 | `$Version` |
| PID | `$ProcessID` |
| 起止时间 | `DateString[...]` |
| 每步推导结果 | `InputForm` 格式 |
| 逐项 CHECK | `PASS` / `FAIL` + residual |
| 汇总统计 | 总数、PASS 数、FAIL 数 |

### 日志框架
使用 `log[]` 函数同时写 stdout 和文件：
```mathematica
logStream = OpenWrite[logFile];
log[msg_] := (WriteString[logStream, msg <> "\n"]; Print[msg]);
```

### 日志文件命名
- `derive_all.wl` → `derivation_log.txt`
- `verify_*.wl` → `verification_log.txt`
- 日志文件与脚本放在同一目录
