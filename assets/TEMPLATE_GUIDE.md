# Word Template Customization Guide

## File Location

`assets/academic-template.docx` — this is the pandoc reference template.

## How It Works

Pandoc reads **style definitions** from the template, not content. You modify styles in Word, save the file, and all future exports inherit your formatting.

## Step-by-Step: Customize in Word

### 1. Open the Template

Open `assets/academic-template.docx` in Word. You'll see placeholder text showing different styles.

### 2. Modify Styles

In Word: **Home tab → Styles panel → right-click a style → Modify**

Here are the styles to change for an economics journal format:

### Core Styles to Modify

| Style Name | Recommended Setting | Notes |
|---|---|---|
| **Normal** | 12pt Times New Roman, Double spacing, First line indent 0.5" | Body text |
| **Heading 1** | 14pt Times New Roman Bold, Centered, Space before 24pt | Section titles (1. Introduction) |
| **Heading 2** | 12pt Times New Roman Bold, Left-aligned, Space before 18pt | Subsections (1.1 Model Setup) |
| **Heading 3** | 12pt Times New Roman Bold Italic, Left-aligned, Space before 12pt | Sub-subsections |
| **Title** | 16pt Times New Roman Bold, Centered, Space after 24pt | Paper title |
| **Author** | 12pt Times New Roman, Centered | Author names |
| **Abstract** | 11pt Times New Roman, Indented both sides 0.5" | Abstract block |
| **Block Text** | 11pt Times New Roman, Indented both sides 0.5" | Block quotes |
| **Table Caption** | 10pt Times New Roman Bold, Centered | "Table 1: ..." |
| **Image Caption** | 10pt Times New Roman, Centered | "Figure 1: ..." |
| **Footnote Text** | 10pt Times New Roman, Single spacing | Footnotes |

### Page Setup

**Layout tab → Margins → Custom Margins:**
- Top: 1" (2.54 cm)
- Bottom: 1" (2.54 cm)
- Left: 1" (2.54 cm)
- Right: 1" (2.54 cm)

**Layout tab → Size:**
- Letter (8.5" × 11") for US journals
- A4 (210 × 297 mm) for European journals

### Header/Footer

**Insert tab → Header / Footer:**
- Header: Paper short title (left), Page number (right)
- Or: Just page number centered in footer

### 3. Save

Save the file (keep as .docx). Do NOT change the filename or location.

## Usage

After customizing, export with:

```bash
pandoc input.md -o output.docx --reference-doc=assets/academic-template.docx
```

## Style Name Mapping

How pandoc maps Markdown to Word styles:

| Markdown | Word Style |
|---|---|
| `# Heading` | Heading 1 |
| `## Heading` | Heading 2 |
| `### Heading` | Heading 3 |
| Regular paragraph | Normal (Body Text) |
| `> Blockquote` | Block Text |
| `**bold**` | Bold character style |
| `*italic*` | Italic character style |
| `$$math$$` | OMML equation |
| `![caption](image)` | Image + Image Caption |
| `[^1]` footnote | Footnote Text |
| `| table |` | Table + Table Caption |
| `` `code` `` | Verbatim Char |

## Common Journal Formats

### AER / RAND / JIE Style
- 12pt Times New Roman
- Double-spaced throughout
- 1-inch margins
- Numbered sections
- Footnotes (not endnotes)
- Tables at end or inline

### Elsevier Style (GEB, IJIO)
- 11pt or 12pt
- 1.5 or double spacing
- Numbered sections
- Author-date citations

## Tips

- Only modify **style definitions**, not the placeholder content
- If a style doesn't exist, create it with the exact name from the mapping table
- Test with a short document first before converting your full paper
- Math formulas are rendered as OMML regardless of template — the template controls surrounding text only
