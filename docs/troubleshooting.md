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

### Table column appears "constant" but shouldn't be

**Symptom**: A paper's numerical table shows the same value (e.g., `t* = -6.48`) in every row, but your formula clearly depends on the row variable.

**Example**: In the Network Externalities paper, the formula
$$t^* = -\frac{(a-c(1+\xi))(2-n-(1-n)\gamma^2)}{(2-n)(1+\gamma)}$$
depends on $n$, yet the paper's Table 1 shows `t* = -6.48` for all $n \in \{0, 0.1, \ldots, 0.8\}$.

**Root cause**: The author likely computed `t*` at one parameter value (e.g., $n=0$) and copied it to all rows, not realizing the formula depends on that parameter.

**Solution**: Always independently recompute every cell, even if it "looks constant":
```mathematica
Do[
  tStar = tStarFormula /. {n -> nVal, (* other params *)};
  Print["n=", nVal, "  t*=", N[tStar]];
  , {nVal, 0, 0.8, 0.1}]
```

**Detection**: If a table column is constant, verify by checking: does the analytical formula contain that row variable? If yes, the "constant" is likely a copy-paste error.

### Sign claim fails at boundary parameters

**Symptom**: Paper claims `expr > 0`, and it checks out at the baseline parameters. But Wolfram gives a negative value at different parameter values.

**Example**: The expression $1 - \beta(1 + \ln\frac{c+ps}{\beta})$ is claimed positive, and indeed positive at $\beta=0.5$. But at $\beta=0.7$ it becomes negative.

**Root cause**: The sign depends on parameter conditions that the paper doesn't state. Authors often verify only at their baseline parameters.

**Solution**: Always test with 3+ parameter sets including **boundary cases**:
```mathematica
(* Baseline *)
expr /. {beta -> 0.5, c -> 1, p -> 0.2, s -> 1}  (* 0.062 > 0 *)
(* Boundary *)
expr /. {beta -> 0.7, c -> 1, p -> 0.2, s -> 1}  (* -0.077 < 0 !! *)
(* Extreme *)
expr /. {beta -> 0.9, c -> 2, p -> 0.5, s -> 2}  (* check *)
```

When a sign claim fails at boundary parameters, determine the exact condition:
```mathematica
Reduce[expr > 0, beta]  (* e.g., beta < 0.57 *)
```

### "Effective marginal cost" term written as product instead of subtraction

**Symptom**: One SPNE formula (e.g., $\pi^*$) uses `c(1+ξ)(a-1) - t` while all other formulas ($q^*$, $CS^*$, $e^*$) consistently use `a - c(1+ξ) - t`.

**Example**: In the Consumer Morality Preferences paper, Eq 15 writes:
$$\pi^* \propto \left(c(1+\xi)(a-1) - t\right)^2$$
but the correct expression (confirmed by Wolfram) is:
$$\pi^* \propto \left(a - c(1+\xi) - t\right)^2$$

**Root cause**: When hand-copying long formulas, `a - c(1+ξ)` can be misread or rearranged as `c(1+ξ)(a-1)`. These are completely different expressions — e.g., at $a=10, c=1, \xi=0.5, t=2$: the correct value is $6.5$, the wrong value is $11.5$.

**Detection**: Check structural consistency. In a symmetric Cournot SPNE, the term $(a - c(1+\xi) - t)$ (or equivalently $A - c\xi - t$ where $A = a-c$) should appear uniformly across $q^*$, $\pi^*$, $CS^*$, and $SW^*$. If one formula suddenly uses a **multiplicative** form instead of a **subtractive** form, it is almost certainly a typo.

**Projects affected**: Consumer Morality Preferences paper Eq 15.

### SW* (social welfare closed form) is the highest-risk formula

**Symptom**: The paper's displayed $SW^*$ formula has wrong denominator and/or numerator, but the optimal tax $t^*$ and comparative statics derived from $SW$ are correct.

**Example**: In the Consumer Morality Preferences paper, Eq 17 writes:
$$SW^* = \frac{4(A - c\xi - t)[\ldots]}{(4+(2-\gamma)\gamma)^2}$$
with denominator $(4+(2-\gamma)\gamma)^2$, but the correct denominator is $D^2 = [(4+(2-\gamma)\gamma)^2 A_1 - 4A_4\varphi]^2$ (matching $\pi^*$ and $CS^*$).

**Root cause**: $SW = 2\pi + CS + TR$ involves merging three components over a common denominator. The merged numerator is extremely long, making transcription errors likely. Authors often derive $t^*$ correctly from the uncombined form $dSW/dt = 0$ and only make errors when writing the combined closed-form.

**Detection**:
1. **Denominator check**: $SW^*$'s denominator should be structurally consistent with $\pi^*$ and $CS^*$ (typically $D^2$ where $D$ is the common denominator from the output equation).
2. **Cross-verify**: If $t^*$ (derived from $dSW/dt=0$) is correct but $SW^*$ doesn't match Wolfram, the error is in the transcription of $SW^*$, not in the derivation.

**Preferred representation**: For papers with complex welfare expressions, write $SW^*$ as:
$$SW^* = 2\pi^* + CS^* + TR^*$$
with each component displayed separately (all independently verified), rather than combining into one fraction.

**Projects affected**: Consumer Morality Preferences paper Eq 17; Network Externalities paper Eq 17 (SW* denominator).

### Rational expectations: FOC ordering matters

**Symptom**: Your Wolfram `Solve` result for output $q_i$ doesn't match the paper's formula. The denominators have different structures (e.g., $(1-n)^2(4-\gamma^2)$ vs $(2-n)^2 - (1-n)^2\gamma^2$).

**Root cause**: In network externalities models, $y_i$ is the consumer's expectation of network size. There are two approaches:

| Approach | Steps | Result |
|----------|-------|--------|
| **Correct** (fixed expectations) | FOC w.r.t. $q_i$ with $y_i$ fixed → substitute $y_i = q_i$ | Coefficient on $q_i$: $(2-n)$ |
| **Wrong** (pre-substituted) | Substitute $y_i = q_i$ first → FOC w.r.t. $q_i$ | Coefficient on $q_i$: $2(1-n)$ |

**Solution**: Keep expectations as separate variables during optimization:
```mathematica
(* CORRECT: y1, y2 are separate expectation variables *)
EU = (a - q1 - gamma*q2 + n*(y1 + gamma*y2) - t - c*(1+xi)) * q1 + lambda*q1;
FOC = D[EU, q1];              (* y1 does NOT change with q1 *)
FOC = FOC /. {y1 -> q1, y2 -> q2};  (* impose RE AFTER differentiation *)

(* WRONG: substituting y=q before FOC *)
EU = (a - (1-n)*q1 - (1-n)*gamma*q2 - t - c*(1+xi)) * q1 + lambda*q1;
FOC = D[EU, q1];              (* n affects the q1 coefficient *)
```

This is a general principle: **substitutions that create dependencies between the choice variable and other terms must be imposed after optimization, not before.**

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
