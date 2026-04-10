---
name: latex-manuscript
description: Patterns for efficiently working in LaTeX manuscript repositories — ingesting structure, viewing figures, reading reviewer comments, and making edits.
user-invocable: true
---

# LaTeX Manuscript Handling

Patterns for reducing friction when working in LaTeX manuscript repos.

## 1. Repo reconnaissance

LaTeX manuscripts follow predictable layouts. Run this upfront:

```bash
# Find the master .tex file (the one with \documentclass)
grep -rl '\\documentclass' *.tex

# Enumerate all \input / \include to get the section tree
grep -rn '\\input\|\\include' MASTER.tex

# Find all figure directories
find . -name 'figure*' -type d

# Find custom macros / variables
grep -rl '\\newcommand\|\\DeclareFigureNumber\|\\def\\' *.tex other/*.tex
```

Read the **variables/macros file** early — it defines figure reference commands, custom labels, and numbering that you need to parse the rest of the manuscript.

## 2. Viewing PDF figures

PDF figures can't be viewed directly. Convert to PNG first:

```bash
# macOS (built-in, fast, no dependencies)
sips -s format png figure.pdf --out figure.png

# Linux (requires poppler-utils)
pdftoppm -png -r 200 -singlefile figure.pdf figure
```

Batch convert all figures in a repo:
```bash
for d in figures/figure_*/; do
  [ -f "$d/figure.pdf" ] && sips -s format png "$d/figure.pdf" --out "$d/figure.png"
done
```

Then use the Read tool on the `.png` files to visually inspect them.

## 3. Reading the manuscript efficiently

**Parallel section reads**: Launch multiple Read calls simultaneously for all section files. A typical structure:
- `text/abstract.tex`, `text/introduction.tex`, `text/results.tex`, `text/discussion.tex`, `text/methods.tex`
- `other/title.tex`, `other/variables.tex`

**Figure legends**: Each figure directory typically has `legend.tex`. Read all legends in one batch with a subagent.

**Methods can be huge** (500-1000+ lines). Read in chunks or use Grep to find specific sections by `\subsection` or `\label`.

## 4. Finding issues in manuscript text

```bash
# Placeholder text and editorial notes
grep -rn 'TODO\|FIXME\|XXX\|figure X\|fig X\|(stats)\|BS suggested\|PLACEHOLDER' text/

# Overly precise p-values (might need rounding)
grep -rn 'p=[0-9]\.[0-9]*e-' text/

# Check for "novel" / overclaiming language
grep -rn 'novel\|first\|unprecedented\|breakthrough' text/
```

## 5. LaTeX editing style

When editing LaTeX manuscripts:

- **Match the existing style exactly**: indentation, spacing, citation format (`\autocite` vs `\cite`), figure reference macros
- **Check for custom commands** before writing raw LaTeX. E.g., the repo may define `\figref{key}` instead of raw `\textbf{Figure N}`
- **Preserve line structure**: Many LaTeX repos put one sentence or one paragraph per line. Don't reflow unless asked
- **Use the Edit tool**, not sed/awk. The Edit tool shows exactly what changes and preserves surrounding context
- **Test that edits don't break compilation** by checking for unmatched braces, unclosed environments, etc.

Common patterns:
```latex
% Adding a statistical test result
(paired $t$-test, $p < 0.05$)
(Wilcoxon signed-rank test, $p = 0.0078$)
($p < 0.001$, permutation test, 1000 shuffles)

% Adding a limitation acknowledgment
We note that this comparison was performed on $N=4$ animals; replication in larger cohorts would further strengthen these conclusions.

% Softening a claim
% BEFORE: "FR provides a novel and flexible approach"
% AFTER:  "FR provides an effective approach"
```

## 6. Working with reviewer response documents (.docx)

Reviewer response docs are usually Word files. Use the docx skill's unpack/edit/pack workflow:

```bash
# Unpack to editable XML
python3 scripts/office/unpack.py responses.docx unpacked/

# Edit unpacked/word/document.xml with the Edit tool

# Repack
python3 scripts/office/pack.py unpacked/ responses_revised.docx --original responses.docx
```

**Extracting text from reviewer XML** for analysis:
```python
import xml.etree.ElementTree as ET
tree = ET.parse('unpacked/word/document.xml')
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in tree.getroot().iter(f'{{{ns["w"]}}}p'):
    texts = []
    for t in p.iter(f'{{{ns["w"]}}}t'):
        if t.text: texts.append(t.text)
    line = ''.join(texts).strip()
    if line:
        bold = p.find('.//w:rPr/w:b[@w:val="1"]', ns)
        gray = p.find('.//w:rPr/w:color[@w:val="999999"]', ns)
        tag = '[REVIEWER]' if gray else '[RESPONSE]' if bold else ''
        print(f'{tag} {line[:200]}')
```

**Formatting conventions in response docs:**
- Reviewer text is typically gray (`color val="999999"`)
- Author responses are bold
- TODOs / incomplete items are often red (`color val="ff0000"`)
- When inserting new response paragraphs into the XML, copy the `<w:pPr>` and `<w:rPr>` structure from existing response paragraphs to match formatting

## 7. Subagent strategy

For manuscript work, subagents are most useful for:
- **Parallel reads**: Read all section files + all legends simultaneously
- **Figure conversion**: Batch convert PDFs to PNGs
- **Targeted edits**: Send a subagent to make a specific set of edits to one file while you work on another
- **Legend/methods audits**: "Check all figure legends for missing error bar descriptions"

Avoid using subagents for decisions that require cross-section understanding (e.g., "should we move this figure to the supplement?"). Do those yourself.

## 8. Common reviewer response patterns

Checklist of things reviewers commonly request that can be addressed via manuscript text alone:

| Request | Where to edit |
|---------|--------------|
| Report error bar types | Figure legends |
| Specify statistical tests | Results, near each p-value |
| Acknowledge sample size limitations | Results, near the relevant comparison |
| Tone down claims | Abstract + Discussion |
| Clarify methodology | Results or Methods |
| Add software/data availability | Methods (new subsection) |
| Fix figure labeling | Figure legends |
| Remove overclaiming ("novel", "first") | Abstract, Introduction, Discussion |
