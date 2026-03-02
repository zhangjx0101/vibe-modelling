---
name: export-word
description: 将 LaTeX 论文转为 Word (.docx)，公式为 Word 原生可编辑格式（OMML）。
argument-hint: [.tex 文件路径]
---

# 导出 Word 文档

将 LaTeX 论文通过 Pandoc 转为 `.docx` 文件，所有数学公式自动转为 Word 原生可编辑公式（OMML 格式）。

## 工具

- **Pandoc**: `pandoc`（已安装 3.8.3）
- **pdflatex**: `/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe`

## 工作流程

### Step 1：确认源文件

检查 `.tex` 文件是否存在且可编译：
- 确认文件路径正确
- 确认 PDF 编译无错误（如有错误先修复）
- 识别是否有 `.bib` 参考文献文件

### Step 2：转换为 Word

**基本转换：**

```bash
cd "论文目录"
pandoc paper.tex -o paper.docx
```

**带参考文献转换：**

```bash
pandoc paper.tex --bibliography=references.bib --citeproc -o paper.docx
```

**带自定义模板转换（如需特定字体/排版）：**

```bash
pandoc paper.tex --reference-doc=template.docx -o paper.docx
```

### Step 3：处理特殊情况

#### 图片
- Pandoc 会自动嵌入图片（PDF 图需先转为 PNG/EMF）
- 如有 PDF 矢量图，先用以下方式检查是否需要转换：

```bash
# 如果论文中引用了 .pdf 图片，Pandoc 可能无法嵌入
# 建议同时准备 .png 版本用于 Word 导出
```

#### 自定义 LaTeX 命令
- 如果 `.tex` 中有自定义宏（`\newcommand`），Pandoc 会自动展开
- 如有复杂宏无法解析，需要在转换前手动展开

#### 交叉引用
- `\ref{}`、`\eqref{}` 会被转为 Word 中的文本
- `\cite{}` 配合 `--citeproc` 会转为正确的引用格式

### Step 4：验证输出

转换完成后检查：

| 检查项 | 方法 |
|---|---|
| 文件已生成 | 确认 `.docx` 文件存在且大小合理 |
| 公式可编辑 | 提示用户在 Word 中双击公式确认 |
| 图片完整 | 确认所有图片已嵌入 |
| 参考文献 | 确认引用列表完整 |
| 中文支持 | 如有中文内容，确认显示正常 |

### Step 5：报告结果

输出：
- Word 文件路径和大小
- 转换是否有警告
- 提醒用户检查公式和图片

## 公式转换原理

```
Wolfram TeXForm[] → LaTeX $...$ / $$...$$ → Pandoc → OMML (Word 原生公式)
```

- `$inline$` → Word 行内公式
- `$$display$$` 或 `\begin{equation}` → Word 独立公式
- `\begin{align}` → Word 多行公式

所有公式在 Word 中双击即可编辑，与手动在 Word 中插入公式效果完全一致。

## 常用选项

| 选项 | 用途 | 示例 |
|---|---|---|
| `--reference-doc` | 使用 Word 模板（字体、样式） | `--reference-doc=template.docx` |
| `--bibliography` | 指定参考文献文件 | `--bibliography=refs.bib` |
| `--citeproc` | 处理引用 | 配合 `--bibliography` 使用 |
| `--csl` | 引用格式样式 | `--csl=apa.csl` |
| `--toc` | 生成目录 | `--toc` |
| `--number-sections` | 章节编号 | `--number-sections` |

## 注意事项

- 公式精确度依赖 Wolfram `TeXForm[]` 生成的 LaTeX，不要手动修改公式
- 复杂的 TikZ 图形不会转换，需要作为图片嵌入
- Word 文档主要用于审稿交流或合作者编辑，最终投稿仍以 PDF 为准
