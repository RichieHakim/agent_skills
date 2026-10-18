---
name: figure-clarity
description: Edit a figure until it can be understood at a glance, by showing it to naive critics and fixing what they misread. Use to improve the style, clarity, and messaging of a figure.
user-invocable: true
---

# Figure Clarity

A good paper figure delivers its message in a few seconds and rewards a longer look with detail. This skill is an editing loop: show the figure to critics who know nothing about the project, find what they cannot decode, and change the figure until each piece of information is self-evident.

Keep every important takeaway, but lower the effort each one takes to read. A figure that passes the critics by saying less has failed. Only numbers, formulas, statistics, and parameters belong in the caption; what an axis, region, line, symbol, measure, or control *is* must be readable from the figure. Show, don't tell: when a critic is confused, the fix is rarely more words; it is usually a new way to show the information.

Terms: the *caption* is the text printed with the figure (journals often call it the figure legend). A *key* maps colors or symbols to meanings inside the figure. Formatting follows `figure-formatting`; this skill decides what to change. Numbers are in `parameters.md`; read it before the first round.

## Before the first round

1. Write the message in one sentence. If you can't, decide what the figure is for first.
2. Trace the flow of information yourself: for each panel, what was measured, what was done to it, what is plotted, and where it goes next. If you can't trace it, no reader can.
3. Decide who the reader is, e.g. a biologist from another field. The critics stand in for them.
4. Write the *message items*, a private checklist of what that reader should get without the caption: the message, the reading order, the key comparison and its rough size, and for a method, each step and why it exists. After round one, change them only with the user's agreement, so the score can't rise by shrinking the target.

## One round

1. Render at printed size. Put only the render, named `figure.png`, in an empty scratch folder. File names, scripts, captions, and other figures all leak the answer.
2. From this render, add to the checklist one *term item* per visible word, abbreviation, symbol, and color; one *axis item* per axis: the quantity in plain words, its unit or what one tick step means, and what a high value looks like; and one *flow item* per arrow or link between panels: what goes in, what comes out, and where it appears next. Rebuild these every round, since fixes add labels.
3. Start fresh critics in parallel, each a new CLI session started in that folder (`claude -p --model <critic model> --session-id <id>`, then `--resume <id>` for each later message). Subagents of your own session load the project's memory and already know the answer. First ask each critic, in a message of its own, what it already knows about this project, and replace any critic that knows something. Never show a critic another figure or a caption.
4. The context is one sentence naming only the field and the reader, e.g. "A figure from a neuroscience paper; read it as a biologist from another field." Never state the question, the finding, the method, or which data are real. One critic per round gets only "This is a figure from a scientific paper." Tell it to open only `figure.png`, read no other files, load no skills, and run no commands; to say briefly what the figure is about and what its main point is; and to list the parts in the order its eye went to them. Ask nothing more yet, so the first impression comes before study.
5. Detail pass, as a second message that adds no context: for every panel, axis, color, symbol, line style, arrow, label, and number, say what it means in plain words and tag it [read] (naming the mark it was read from), [inferred], or [can't tell]. Mark every word or symbol the reader would not know, even if the critic does. List what drew its attention without telling it anything. Then explain the whole figure as if to a colleague, following the data from the first panel to the last: for a method, every step and why it is there; for a result, the finding, what it is compared against, and how strong the evidence looks. Critics report; they don't suggest design changes, which default to "add text". Attach panel crops if the render is large.
6. Quiz each critic on every term, axis, and flow item, and on the message items its report missed: "What does <label> mean, and what would a value of <tick> mean?", "Follow <point> from panel A to its mark in panel C." Ask it to predict, compare, or explain why a step exists. Questions name only what is visible and never hint at the answer. Send each critic only its own questions. Don't correct it.
7. A separate fresh scorer gets the checklist and the critics' full answers; the agent that edits the figure does not score it, and the scorer scores every item as written. *Understood*: correct and [read] before the quiz. *Partial*: correct and [read] only in the quiz. *Missed*: [inferred], [can't tell], wrong, a restated label, or an answer from knowledge the reader wouldn't have. *Misread*: wrong and [read], the worst outcome, because the figure is telling readers something false.
8. Fix, re-render, and start the next round with new critics. A critic that saw an earlier version has learned the figure.

Log each round: the render, misreadings, changes, score, the word count on the figure, and the terms and axes no critic read from the figure. Comprehension should rise while the word count stays flat or falls. If words keep rising, you are fixing by telling.

## Fixing a confusion

Treat every misreading as a fault in the figure. The exception is knowledge the reader already has; name the reader more precisely in the context sentence instead. A confusion that several critics share is real; one critic's quirk is weak evidence.

A term no critic can read needs a visual definition, not a new name: a small inline example of a high and a low value, or the data before and after the step. Printing the quiz answer beside a mark, or swapping one term for another, is a label edit. If two rounds of label edits leave a shared confusion, redesign the panel or split the figure.

Try fixes in this order: remove the cause (variation that means nothing, repetition, decoration such as 3D, shadows, and gradients); change the encoding or layout; add a short label where it's needed; move the item to the caption if it is a number, formula, statistic, or parameter.

| Critic | Fix |
|---|---|
| Misses or misnames the main point | Make the key result the most salient element; mute context in gray |
| Can't say what an axis value means | Name the quantity in plain words with a real unit; mark a reference value (zero, chance, baseline, control) |
| Can't follow data from one panel to the next | Draw the link: an arrow, a shared color, or the same example highlighted in both panels |
| Looks up colors or symbols, or mismatches them | Label data directly and drop the key |
| A color changes meaning, or panels seem unrelated | One color or symbol per concept across the figure |
| Reads in the wrong order | Left to right, top to bottom; group by proximity; number steps |
| Misjudges a difference | Shared axes and identical design for compared panels |
| Can't say what a method step does | A small example of the data before and after the step |
| Describes the parts but not the whole | One dominant element per panel; split panels that make two points |
| Skips or garbles text | Fewer words; one shared label for repeated text; no coined terms |

Check each fix against the whole checklist; a fix for one item often costs another.

## Stopping

Stop when a round meets the stop thresholds in `parameters.md` without the caption. A shared confusion that has only had label edits, or a word count over the cap, blocks stopping. If the score stalls or the round limit is reached, show the user the render, the persistent misreadings, and what you tried.

Focus your report just on the essential changes that were made.

Sources: Rougier et al. 2014, PLoS Comput Biol 10:e1003833; Wilke, *Fundamentals of Data Visualization*, ch. 20; Krzywinski and Wong, Nature Methods "Points of View"; Nature's research figure guide.
