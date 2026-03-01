---
name: plot
description: 用 Wolfram Engine 生成学术论文级别的图形，导出 PDF 矢量图。
argument-hint: [图形描述或要展示的结论]
---

# Wolfram 绘图

用 Wolfram Engine 生成学术论文级别的高质量图形。

## 核心原则

1. **所有图形使用 PDF 矢量格式**（投稿首选）
2. **学术风格**：Frame、FrameLabel、黑白友好
3. **每个核心 Proposition 配一张图**

## 图形类型与用途

| 图形类型 | Wolfram 函数 | 适用场景 |
|---|---|---|
| 函数曲线 | `Plot` | 比较静态（单参数） |
| 多曲线比较 | `Plot[{f1, f2}, ...]` | 不同情形对比 |
| 参数区域 | `RegionPlot` | 过度投资 vs 不足投资区域 |
| 等高线 | `ContourPlot` | 两参数下的等值线 |
| 三维曲面 | `Plot3D` | 福利随两参数变化 |
| 参数图 | `ParametricPlot` | 轨迹、效率前沿 |

## 学术风格模板

### 基础样式

```mathematica
academicStyle = {
  Frame -> True,
  FrameStyle -> Directive[Black, 12],
  FrameTicksStyle -> Directive[Black, 10],
  LabelStyle -> Directive[Black, 12],
  ImageSize -> 400,
  PlotStyle -> {
    Directive[Black, Thick],                    (* 实线 *)
    Directive[Black, Thick, Dashed],            (* 虚线 *)
    Directive[Gray, Thick, DotDashed]           (* 点划线 *)
  }
};
```

### 彩色样式（适用于工作论文或在线版本）

```mathematica
colorStyle = {
  Frame -> True,
  FrameStyle -> Directive[Black, 12],
  LabelStyle -> Directive[Black, 12],
  ImageSize -> 400,
  PlotStyle -> {
    Directive[RGBColor[0.2, 0.4, 0.7], Thick],     (* 深蓝 *)
    Directive[RGBColor[0.85, 0.33, 0.1], Thick, Dashed],  (* 橙红 *)
    Directive[RGBColor[0.47, 0.67, 0.19], Thick, DotDashed] (* 绿色 *)
  }
};
```

## 工作流程

### Step 1：加载推导结果

```mathematica
Get["path/results.mx"];
```

### Step 2：生成图形

```mathematica
(* 示例：比较静态图 *)
fig = Plot[
  {q0star, q1star} /. {c -> 0.3, gamma -> 2},
  {phi, 0, 1},
  Frame -> True,
  FrameLabel -> {"\[Phi] (AI efficiency)", "Output"},
  PlotStyle -> {
    Directive[Black, Thick],
    Directive[Black, Thick, Dashed]
  },
  PlotLegends -> Placed[{"Public firm", "Private firm"}, {0.7, 0.8}],
  ImageSize -> 400
];
```

### Step 3：导出 PDF

```mathematica
Export["path/Figure1.pdf", fig];
```

### Step 4：在 LaTeX 中引用

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{Figure1.pdf}
  \caption{Effect of AI efficiency on equilibrium output. Solid line: public firm; dashed line: private firm. Parameters: $c=0.3$, $\gamma=2$.}
  \label{fig:output-phi}
\end{figure}
```

## 图形设计指南

### Caption 规范
- 首句描述图形内容
- 说明线型/颜色/区域的含义
- 列出使用的参数值
- 无需看正文即可理解图形

### 配色方案

**区域图（RegionPlot）推荐配色：**
- 浅蓝 + 浅橙：`RGBColor[0.65, 0.81, 0.94]` + `RGBColor[0.99, 0.75, 0.44]`
- 浅绿 + 浅粉：适用于区分两种政策区域

**曲线图推荐：**
- 黑白投稿：实线 + 虚线 + 点划线（通过线型区分）
- 彩色版本：深蓝 + 橙红 + 绿色（色盲友好）

### 排版细节
- `ImageSize -> 400`（适合单栏论文）
- `ImageSize -> 300`（适合双栏论文）
- FrameLabel 字体大小 12pt
- Tick 标签字体大小 10pt
- PlotRange 适当留白，不要太紧凑

## 常见问题

- **图形太大/太小**：调整 `ImageSize` 和 LaTeX 中的 `width`
- **中文乱码**：在 FrameLabel 中使用英文，中文说明放 caption
- **Export 失败**：检查目标目录是否存在
- **RegionPlot 渲染慢**：降低 `PlotPoints`，如 `PlotPoints -> 50`
