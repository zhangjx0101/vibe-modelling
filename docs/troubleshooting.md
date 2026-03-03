# Troubleshooting

Solutions to known issues, collected from real project experience.

## Pandoc Issues

### `\tag{}` produces warnings in Word export

**Symptom**: Pandoc warns `Could not convert TeX math \tag{...}`, formula numbers appear as raw LaTeX in Word.

**Cause**: `\tag{}` is an amsmath-specific command. Pandoc's built-in TeX parser doesn't support it.

**Solution**: Preprocess with Wolfram before running pandoc:

```mathematica
(* preprocess_md.wl *)
text = Import["Manuscript.md", "Text"];
text = StringReplace[text,
  "\\tag{" ~~ n:Shortest[Except["}"]..] ~~ "}" :>
  "\\qquad\\text{(" <> n <> ")}"
];
Export["Manuscript_temp.md", text, "Text"];
```

Then run pandoc on the preprocessed file:
```bash
pandoc Manuscript_temp.md -o output.docx \
  --from markdown+footnotes+pipe_tables+tex_math_dollars \
  --standalone
rm Manuscript_temp.md
```

### sed/perl fail on LaTeX files

**Symptom**: Trying to use `sed 's/\\tag/\\qquad/g'` produces garbled output — `\t` becomes a tab character.

**Cause**: Shell and sed/perl have their own backslash escaping rules that conflict with LaTeX's backslashes. You'd need 4+ layers of escaping to get it right.

**Solution**: Don't use sed/perl for LaTeX text processing. Use Wolfram `StringReplace` instead — it handles backslashes cleanly without shell interference.

### PDF figures not embedded in Word

**Symptom**: Pandoc ignores PDF figures, or they appear as broken links in the .docx.

**Cause**: Pandoc cannot embed PDF images in Word documents (Word doesn't natively support PDF images).

**Solution**: Convert figures to PNG at 300 DPI:

```mathematica
(* In Wolfram *)
fig = Import["figures/Figure1.pdf"];
Export["figures/Figure1.png", fig, ImageResolution -> 300];
```

Then reference the PNG version in your Markdown/LaTeX.

---

## Wolfram Issues

### `FullSimplify` hangs or takes very long

**Symptom**: `FullSimplify[expr]` runs for minutes without returning.

**Cause**: Expressions containing `Abs[]`, `Piecewise`, or deeply nested fractions can cause `FullSimplify` to explore an exponential search space.

**Solution**:
```mathematica
(* Instead of FullSimplify, try: *)
Simplify[expr]                           (* less aggressive *)
PiecewiseExpand[expr] // Simplify        (* for Abs[] *)
Factor[Numerator[expr]] / Factor[Denominator[expr]]  (* manual *)
```

### `Reduce` returns very complex conditions

**Symptom**: `Reduce[expr > 0 && assumptions]` returns a condition spanning multiple lines with many cases.

**Cause**: The expression has different sign behavior in different parameter regions.

**Solutions**:
1. Add tighter parameter constraints:
   ```mathematica
   Reduce[expr > 0 && 0 < c < cbar && phi > 0 && 0 < gamma < 1,
     {c, phi, gamma}, Reals]
   ```

2. Fall back to numerical verification:
   ```mathematica
   Table[{cv, pv, gv, N[expr /. {c->cv, phi->pv, gamma->gv}]},
     {cv, {0.1, 0.3, 0.5}},
     {pv, {0.5, 1.0, 2.0}},
     {gv, {0.3, 0.5, 0.7}}]
   ```

3. Simplify the claim: instead of proving globally, prove under the paper's Assumption 1.

### Closed-form solutions give wrong numerical results

**Symptom**: A Ferrari/Cardano/quartic formula computes correctly for some parameter values but produces complex numbers or wrong values for others.

**Cause**: Radical-based closed-form solutions often have multiple branches. The correct branch depends on the sign of discriminants, which changes across the parameter space.

**Solution**: Don't use closed-form formulas for computation. Instead:
1. Prove **existence** analytically (Intermediate Value Theorem)
2. Prove **uniqueness** analytically (Descartes' rule, monotonicity)
3. Use `FindRoot` for actual numerical values:
   ```mathematica
   phiTilde = phi /. FindRoot[numerator[c0, g0, phi], {phi, 0.5}]
   ```

### `Solve` returns empty list `{}`

**Symptom**: `Solve[system, vars]` returns `{}`.

**Causes**:
- System is inconsistent (no solution exists)
- Variables appear in unexpected forms (e.g., `q0` vs `q[0]`)
- Need to specify domain: `Solve[..., Reals]`

**Solution**: Check the system manually, try `Reduce` instead, or simplify one equation at a time.

---

## Math Verification Issues

### A formula "should be" correct but Wolfram says FAIL

**Symptom**: `Simplify[derived - paper]` returns a non-zero residual.

**Possible causes**:
1. **Typo in paper formula**: The paper has a sign error, wrong coefficient, or wrong exponent
2. **Different but equivalent forms**: The expressions are mathematically equal but `Simplify` can't see it
3. **Error in the derivation script**: Your Wolfram code has a bug

**Debugging steps**:
```mathematica
(* Step 1: Check if numerically equal *)
N[derived /. {c->0.3, phi->0.5, gamma->0.5}]
N[paper /. {c->0.3, phi->0.5, gamma->0.5}]

(* Step 2: Try harder simplification *)
FullSimplify[derived - paper]
Factor[derived - paper]
Expand[derived] - Expand[paper]

(* Step 3: If numerically different, the paper has an error *)
(* Check each factor/term systematically *)
```

### Table values don't match

**Symptom**: Your Wolfram-computed numerical values differ from the paper's Table.

**Most likely cause**: The paper's table was computed by hand or with an earlier (possibly incorrect) version of the formulas.

**Solution**: Trust Wolfram's values if your symbolic derivations all PASS. Recompute the entire table:
```mathematica
Table[{cv, gv, pv, N[formula /. {c->cv, gamma->gv, phi->pv}]},
  {cv, caseValues}, {gv, gammaValues}, {pv, phiValues}]
```

---

## Git / Workflow Issues

### `.gitignore` blocks my project files

**Symptom**: `git add project/...` has no effect; files don't appear in `git status`.

**Cause**: The default `.gitignore` uses `*` to ignore everything, only whitelisting `.claude/`, `README.md`, etc. The `project/` directory is intentionally excluded (research content stays private).

**This is by design**: The repo only tracks the workflow configuration, not your research. Your project files are backed up via BaiduSyncdisk (or other sync).

### Context compression loses my work

**Symptom**: After a long session, Claude seems to forget earlier derivations or decisions.

**Cause**: The conversation context window has a limit; older messages get compressed.

**Solution**: The `pre-compact` hook automatically reminds Claude to save state. You can also manually:
```
You: /learn 刚发现 FullSimplify 对含 Abs 的表达式会超时，需要先 PiecewiseExpand
You: /snapshot backup before major model change
```

Key information is persisted to:
- `MEMORY.md` — global learnings
- `MEMORY_LOCAL.md` — project-specific learnings
- `.mx` files — Wolfram state snapshots
- `derivation_log.txt` — complete derivation records
