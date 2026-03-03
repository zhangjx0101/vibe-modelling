# Wolfram Engine Guide

Practical tips for using Wolfram Engine in the Vibe Modelling workflow.

## Setup

**Default path**: `/d/Wolf/wolframscript.exe` (Windows)

To check your installation:
```bash
wolframscript -code "Print[$Version]"
# Expected: 14.3.0 for Microsoft Windows (64-bit) ...
```

## Execution Modes

### Inline (< 5 steps)

For quick one-off calculations:
```bash
wolframscript -code "Solve[x^2 + 3x + 2 == 0, x]"
wolframscript -code "D[x^3 + 2x, x]"
wolframscript -code "Reduce[a*x + b > 0 && a > 0, x]"
```

### Script (5+ steps)

For multi-step derivations, write a `.wl` file:
```bash
wolframscript -file derivations/derive_all.wl
```

## Derivation Log Framework

Every `.wl` derivation script should generate a log file. Here's the standard framework:

```mathematica
(* === LOGGING SETUP === *)
logFile = "derivations/derivation_log.txt";
logStream = OpenWrite[logFile];

log[msg_String] := (WriteString[logStream, msg <> "\n"]; Print[msg]);
logExpr[label_String, expr_] := log[label <> ToString[InputForm[expr]]];

nPass = 0; nFail = 0;
check[name_String, expr_] := Module[{s = Simplify[expr]},
  If[s === 0,
    log["  CHECK " <> name <> ": PASS"]; nPass++,
    log["  CHECK " <> name <> ": FAIL  (residual = "
        <> ToString[InputForm[s]] <> ")"]; nFail++
  ]
];

(* Header *)
log["Kernel:  " <> $Version];
log["PID:     " <> ToString[$ProcessID]];
log["Start:   " <> DateString[...]];

(* === YOUR DERIVATIONS HERE === *)
(* ... *)

(* Footer *)
log["Total: " <> ToString[nPass + nFail]];
log["  PASS: " <> ToString[nPass]];
log["  FAIL: " <> ToString[nFail]];
Close[logStream];
```

**What the log captures**:
- Kernel version, PID, timestamps (reproducibility)
- Each derived expression in `InputForm`
- PASS/FAIL for every formula check
- Summary statistics

## Using Wolfram for LaTeX Text Processing

**Problem**: sed/perl fail when processing LaTeX files because `\t` is interpreted as tab, `\\` needs multiple escaping layers, and results are unpredictable.

**Solution**: Wolfram's `StringReplace` handles backslashes cleanly:

```mathematica
(* Replace \tag{N} with \qquad\text{(N)} for pandoc compatibility *)
text = Import["Manuscript.md", "Text"];
text = StringReplace[text,
  "\\tag{" ~~ n:Shortest[Except["}"]..] ~~ "}" :>
  "\\qquad\\text{(" <> n <> ")}"
];
Export["Manuscript_temp.md", text, "Text"];
```

**Why this works**: In Wolfram strings, `\\` is literally `\` — no shell layer, no regex escaping confusion.

**When to use**: Anytime you need to find-and-replace patterns in LaTeX/Markdown files, especially patterns involving backslashes.

## Common Operations

### Solve and Verify

```mathematica
(* Solve FOC *)
foc = D[profit, q] // Expand;
qStar = q /. Solve[foc == 0, q][[1]];

(* Verify SOC *)
soc = D[profit, {q, 2}];
Reduce[soc < 0 && phi > 0 && c > 0, {phi, c}]

(* Check against paper formula *)
check["eq(8) q*", Simplify[qStar - paperFormula]]
```

### Sign Determination

```mathematica
(* MANDATORY: Use Reduce[], never claim sign by inspection *)
Reduce[D[qStar, phi] > 0 && 0 < c < 1 && phi > 0, {c, phi}]

(* If Reduce returns complex conditions, fall back to numerical *)
Table[{c, phi, N[D[qStar, phi] /. {c -> cv, phi -> pv}]},
  {cv, {0.1, 0.3, 0.5}}, {pv, {0.5, 1.0, 2.0}}]
```

### LaTeX Output

```mathematica
(* Generate LaTeX for paper *)
ToString[TeXForm[qStar]]

(* For display equations *)
"$$" <> ToString[TeXForm[qStar]] <> "$$"
```

### State Persistence

```mathematica
(* Save state for later use *)
DumpSave["derivations/state.mx", {qStar, tStar, SWstar}];

(* Load in another script *)
Get["derivations/state.mx"];
```

## Common Pitfalls

### 1. `FullSimplify` on `Abs[]` may timeout

```mathematica
(* BAD: can hang *)
FullSimplify[Abs[expr]]

(* GOOD: expand first *)
PiecewiseExpand[Abs[expr]] // Simplify
```

### 2. `Reduce` returns complex conditions

When `Reduce[expr > 0 && assumptions]` gives a long, complex condition instead of `True`:

```mathematica
(* Add more constraints *)
Reduce[expr > 0 && 0 < c < cbar && phi > 0 && 0 < gamma < 1,
  {c, phi, gamma}, Reals]

(* Or fall back to numerical verification *)
Table[N[expr /. {c -> cv, phi -> pv, gamma -> gv}],
  {cv, {0.1, 0.5}}, {pv, {0.5, 2.0}}, {gv, {0.3, 0.7}}]
```

### 3. `Solve` returns multiple solutions

```mathematica
(* Always check how many solutions *)
sols = Solve[system, vars];
Length[sols]  (* Should be 1 for unique equilibrium *)

(* If multiple, check which is economically meaningful *)
Select[sols, (q0 /. #) > 0 && (q1 /. #) > 0 &]
```

### 4. Ferrari formula and closed-form solutions

Complex closed-form solutions (like Ferrari's quartic formula) can have multiple branches. If the paper presents one branch, it may fail for parameter ranges where a different branch applies.

**Better approach**: Prove existence (IVT) + uniqueness (Descartes' rule), then use `FindRoot` for numerical values.

### 5. Numerical precision

```mathematica
(* Use exact arithmetic for symbolic work *)
c = 3/10;  (* NOT 0.3 *)

(* Switch to numerical only for final output *)
N[result, 10]  (* 10 significant digits *)
```

## 7-Phase Script Structure

For comprehensive derivation scripts, follow this structure:

```
Phase 1: Model Definition     — utility, demand, profit, CS, TR, SW
Phase 2: Stage 2 Equilibrium  — FOC → BR → solve system
Phase 3: Optimal Tax           — substitute, FOC/SOC, solve for t*
Phase 4: SPNE Results          — substitute t*, welfare components
Phase 5: Welfare Analysis      — comparative statics, sign conditions
Phase 6: Benchmark Comparison  — private duopoly, welfare gap
Phase 7: Appendix + Numerics   — tables, threshold computations
```

Each phase logs its results and checks against the paper. The final summary shows PASS/FAIL counts.
