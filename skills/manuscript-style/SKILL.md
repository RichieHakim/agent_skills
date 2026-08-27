---
name: manuscript-style
description: Style guidelines for writing manuscript text.
---

# Manuscript Style

## General principles

- Clear, concise, and engaging prose.
- Active voice.
- Use present tense to describe findings.
- Use past tense to describe methods, prior work, and scientific process.
- Plain language. Move the technical details to the methods section to keep things clean.
- Ideas should link together in a causal chain.

## General writing style

### What is good writing?
- Good scientific writing can only be written by a domain expert. To be a domain expert, you must understand what motivates your field
- Style: "Domain expert motivating and illustrating a new finding to a lamen audience."
- Decide what you are writing before you write. If you aren't sure what must be communicated, do more research.
- Every sentence must make a point. A point changes what the reader believes.
- Before writing each paragraph, state in one plain sentence what information needs to be conveyed. If that sentence is vague or not critical to the story, you aren't ready to write it. Bolster your understanding or write something else.
- Be ruthless about cutting text that does not further the points that you need to make. Budget how much text should be allocated to making each point. Ask how much reader-attention does each point deserve?

### What is lazy writing?
- Much like a cake baked at too high heat, lazy writing looks 'over-under'. It is both burnt and raw. It lacks actual cake. Lazy writing expresses a lot of specifics that don't come together to make impactful points. It states impact rather than motivating conditions that result in impact and then illustrating how the substance of the paper meets those conditions.
- Symptoms of lazy writing:
  - over-coverage: a list of discovered information without integration into greater points
  - defensibility: vague language
  - overly specific jargon
- Examples of symptoms of lazy writing:
  - "Leverages," "is the harder half," "exploits the structure"
    - These are vague, defensible words that attempt to cover an idea. Go back and figure out enough to be able to use words with narrower definitions that make a more precise point.

## Syntax
- When writing LaTeX, make each sentence a line.
```
This is the first sentence.
This is the second sentence.

This is a new paragraph.
This is the second sentence in the new para.
```

## Sections

### Introduction

#### Structure
- Start with a hook sentence. It should be short.
- First paragraph frames the field and the problem. 
- Second paragraph reviews prior work that is in the direct lineage of this work. The sequence of descriptions should point an arrow clearly at the gap that this work fills.
- Third paragraph reviews contemporary/peer work. Descriptions should circumscribe the conceptual gap and differentiate their works from ours.
- Last paragraph explicitly states the gap, describes how this work fills it, and summarizes the specific contributions of this work.

#### Style
- Reviewing prior work should involve a chronological narrative that clearly links the causal relationship between each piece of work.
- The full intro should include many references. Great introductions are essentially just a walk through references. Doing this properly is challenging, as it requires both deeply understanding each piece of work and being able to infer themes, trends, and gaps across the literature. The best introductions feel like a mini-review paper, and demonstrate expertise in the field.
- Find the tension(s).

### Results

Use Carandini's 'spine' approach [Matteo Carandini, "Some Tips for Writing Science," eNeuro 2022 (doi:10.1523/ENEURO.0497-22.2022)](https://www.eneuro.org/content/9/6/ENEURO.0497-22.2022) to structure the manuscript. Draft every topic sentence before any prose, then check that the sequence reads as a summary. Arrange your results in a logical + causal order, and write a sentence for each result. This is the top-level hierarchical structure that all other text should support. These sentences should become the last sentence of each paragraph in the Results section.

- Generally, organize the results into sections that are associated 1-to-1-ish with figures/tables/equations.
- Each section should start with motivation for the experiment/analysis, then describe the methods, then present the results, and finally interpret the results and make a clear conclusion statement. Most sections should just be one paragraph with ~5 sentences, but this can vary widely.
```
  * Given the results of the last experiment or some referenced fact, we hypothesized X.
  * We used these methods to test this hypothesis.
  * In these conditions, these are the primary results.
  * Interestingly, we also observe Y.
  * These results suggest this conclusion about the data. (spine sentence)
```

### Discussion

Rehash the spine. Add in points about broader implications, limitations, and future directions. Do not present new data, but a summary figure can be included.

### References

Aim for 50-150 main text references.

### Methods

Go wild here. Dump all the technical details here.
Include a separate Methods references section.
