---
name: figure-clarity
description: Edit a figure until it can be understood at a glance, by showing it to naive subagent critics and fixing what they misread. Use to improve the style, clarity, and messaging of a figure.
user-invocable: true
---

# Figure Clarity

A good paper figure delivers its message in a few seconds and rewards a longer look with detail. This skill is an editing loop: show the figure to a subagent that knows almost nothing, find what it cannot decode, and change the figure until each piece of information is self-evident.

Decide what the message is and what conclusions a reader needs to take away. Conversely, what information is better left in a legend (numbers, statistics, parameters). Keep every important takeaway, but lower the effort each one takes to read. A figure that passes the critics by saying less has failed. Show, don't tell: when a critic is confused, the fix is rarely more words, it is usually reimagining how to express the information visually.

Terms: the *caption* is the text block printed with the figure (journals often call it the figure legend). A *key* is an in-figure description (sometimes called a 'legend' like in matplotlib) that maps colors or symbols to meanings. Formatting (fonts, sizes, line widths, export) follows `figure-formatting`; this skill decides what to change. Numbers are in `parameters.md`; read it before the first round.

## Before the first round

1. Write the message in one sentence. If you can't, decide what the figure is for first.
2. Write a private checklist of what a reader should get without the caption: the message, what each panel, color, symbol, arrow, and axis means, the reading order, the key comparison and its rough size, and for a method, each step and why it exists. After round one, change the checklist only with the user's agreement, so the score can't rise by shrinking the target.
3. Decide who the reader is, e.g. a scientist from another field. The critics stand in for them.

## One round

1. Render at printed size. Copy the render to scratch with a neutral name like `figure.png`; file names, folders, scripts, and the caption all leak the answer.
2. Start fresh critics in parallel: new subagents that can view images, never a fork, which inherits your context.
3. Open with context, then a first impression. The context is a few high-level sentences at the level of a paper's abstract: the field, the question, and roughly what the work found or built. No numbers, no method details, and nothing about what any panel, color, symbol, or arrow means. Then tell the critic to open only the image, read no other files, load no skills, and run no commands; to say briefly what the figure is about and what its main point is; and to list the parts in the order its eye went to them. Ask nothing more yet, so the first impression comes before study.
4. Detail pass, as a second message to the same critic (e.g. SendMessage) that adds no context: for every panel, axis, color, symbol, line style, arrow, label, and number, say what it means and how confident it is; list what it could not decode or had to guess, and anything that drew its attention without telling it anything; then explain the whole figure as if to a colleague (for a method, every step and why it is there; for a result, the finding, what it is compared against, and how strong the evidence looks). Critics report what they see and don't suggest design changes; their default advice is "add a title" or "add text". Attach panel crops if the render is large.
5. Quiz each critic on checklist items its report missed. Ask it to predict, compare, or explain a step's purpose, and to answer "can't tell" rather than guess. Questions name only what is visible in the figure and never hint at the answer. Don't correct the critic.
6. Score each checklist item as understood, misread, or missed. A confident misreading is the worst outcome, because the figure is telling readers something false.
7. Fix, re-render, and start the next round with new critics. A critic that saw an earlier version has learned the figure.

Log each round: the render, misreadings, changes, score, and the word count on the figure. Comprehension should rise while the word count stays flat or falls. If words keep rising, you are fixing by telling.

## Fixing a confusion

Treat every misreading as a fault in the figure. The exception is standard knowledge in the reader's field; add it to the critic's context instead. A confusion that several critics share is real; one critic's quirk is weak evidence.

Try fixes in this order: remove the cause (meaningless variation, repetition, decoration); change the encoding or layout; add a short label where it's needed; move the item to the caption if it is a detail.

| Critic | Fix |
|---|---|
| Misses or misnames the main point | Make the key result the most salient element; mute context in gray |
| Reads meaning into meaningless variation | Make things that mean the same look the same |
| Distracted by decoration | Remove it: 3D, shadows, gradients, heavy borders, extra colors |
| Looks up colors or symbols, or mismatches them | Label data directly and drop the key |
| A color changes meaning, or panels seem unrelated | One color or symbol per concept across the figure |
| Reads in the wrong order | Left to right, top to bottom; group by proximity; number steps |
| Misjudges a difference | Shared axes and identical design for compared panels |
| Misreads an icon | A text label or the field's standard symbol |
| Can't say what a method step does | A small example of the data before and after the step |
| Describes the parts but not the whole | One dominant element per panel; split panels that make two points |
| Skips or garbles text | Fewer words; one shared label for repeated text; no coined terms |
| Can't read small text | Check the render's resolution before changing the figure |

Check each fix against the whole checklist; a fix for one item often costs another.

## Stopping

Stop when a round meets the stop threshold in `parameters.md` without the caption, and the remaining questions are caption details. Then run one round with the caption to confirm it answers the rest and doesn't contradict the figure. If the score stalls or the round limit is reached, show the user the render, the persistent misreadings, and what you tried.

Report with before and after renders, the last critic's explanation of the figure, and the changes that mattered.

Sources: Rougier et al. 2014, PLoS Comput Biol 10:e1003833; Wilke, *Fundamentals of Data Visualization*, ch. 20; Krzywinski and Wong, Nature Methods "Points of View"; Nature's research figure guide.
