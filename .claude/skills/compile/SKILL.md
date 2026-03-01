---
name: compile
description: 编译 LaTeX 论文为 PDF。自动处理多遍编译、交叉引用、参考文献。
argument-hint: [.tex 文件路径]
---

# LaTeX 编译

将 `.tex` 论文文件编译为 PDF，确保零警告零错误。

## 工具路径

- **pdflatex**: `/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe`
- **bibtex**: `/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/bibtex.exe`

## 工作流程

### Step 1：检查 .tex 文件

在编译前快速检查常见问题：
- 所有 `\begin{...}` 都有对应的 `\end{...}`
- 所有 `\ref{...}` 和 `\cite{...}` 的目标存在
- 图片文件路径正确且文件存在
- 必需的宏包（packages）已声明

### Step 2：编译

标准编译流程（带参考文献）：

```bash
cd "论文目录"
# 第1遍：生成 .aux 文件
"/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe" -interaction=nonstopmode paper.tex
# 处理参考文献（如果有 .bib 文件）
"/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/bibtex.exe" paper
# 第2遍：解析引用
"/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe" -interaction=nonstopmode paper.tex
# 第3遍：确保所有交叉引用正确
"/c/Users/Admin/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe" -interaction=nonstopmode paper.tex
```

如果没有 `.bib` 文件，跳过 bibtex 步骤，但仍需运行 pdflatex **3 遍**以确保交叉引用正确。

### Step 3：检查编译输出

检查 `.log` 文件中的问题：

| 级别 | 关键词 | 处理方式 |
|---|---|---|
| 错误 | `! ...` | **必须修复**，编译已中断 |
| 警告 | `Warning` | 检查是否影响输出 |
| 未定义引用 | `undefined reference` | 需要额外编译遍数或修复 label |
| Overfull hbox | `Overfull \hbox` | 检查是否影响排版美观 |
| 缺少字体 | `Font ... not found` | MiKTeX 会自动下载，确认即可 |

### Step 4：验证 PDF

编译成功后确认：
- PDF 文件已生成且大小合理
- 页数与预期一致
- 报告编译结果（警告数、错误数）

## 期刊格式模板

### JIE (Journal of Industrial Economics) 风格

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{setspace}\doublespacing
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{natbib}
\bibliographystyle{aer}  % 或 chicago
```

### AER (American Economic Review) 风格

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{setspace}\doublespacing
\usepackage{amsmath,amssymb}
\usepackage{natbib}
\bibliographystyle{aer}
```

## 常见问题

- **缺少宏包**：MiKTeX 首次遇到会自动下载安装，允许联网
- **图片找不到**：检查路径是否相对于 .tex 文件所在目录
- **编码错误**：确保 .tex 文件为 UTF-8 编码，使用 `\usepackage[utf8]{inputenc}`
- **数学符号渲染异常**：确认 `amsmath` 和 `amssymb` 已加载
