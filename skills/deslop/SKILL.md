---
name: deslop
description: Write prose and code that reads as human-authored. Use before emitting any prose deliverable — README, PR description, docs, commit message, report, design note, code comments, user-facing summary — and whenever asked to strip the AI voice from existing text ("deslop this", "sounds like AI", "make it human"). Complements writing-style (manuscript section structure) and coding-style (Python conventions).
---

# Deslop

## What a document is

A document is news for one person. Someone can do something after reading it that they could not do before, and that difference is the whole justification for its existence. A writer who has news does not need to be told to be specific, or to vary sentence length, or to avoid clichés. The news does that work, because the shortest honest path to delivering it is already good prose.

Slop is what text looks like when document-shape gets produced with no news in it. The obligation to write arrives without anything to report, and what fills the gap is the appearance of reporting. Understanding this precisely is what lets you stop generating it, because every so-called AI tell is a forgery of some part of having news.

Negative parallelism shows the mechanism most clearly, and it is the most frequently reported tell in AI prose for a reason. "Not just X, but Y" and "it's not X, it's Y" forge the one thing a document cannot do without: a before and an after. The writer invents a belief the reader never held, corrects it, and arrives at the shape of having changed someone's mind without having changed anything. Every other tell is a smaller forgery of some part of the same act — importance that cannot be shown so it gets asserted, consequence nobody argued, arrival at nowhere, equal sections where nothing mattered more than anything else, uniform confidence where nothing was checked, bullets implying a structure that never commits to how the ideas relate.

Because these are forgeries rather than habits, substituting words does not fix them and no blocklist reaches them. The fix is to get the news, then get out of its way. Three stages, and the first one decides the outcome.

## Find out what you have

Answer three questions before the first sentence and keep the answers in front of you. Who is the one reader? What can they do now? What will they be able to do afterward?

If that third answer is not different from the second, you have no document. Say the single sentence you do have and stop. Nearly all slop is what happens when someone writes anyway, and no amount of craft downstream recovers from it.

Then inventory what you know by how you know it: ran it and watched the output, read it in the source, inferred it from something nearby, or guessing. Do this literally, in a scratch list, and calibration stops being a thing you have to remember to perform. You cannot fake modulated confidence, you can only report an inventory you actually took, and a reader deciding whether to trust you is reading for precisely this. "I benchmarked two of the four" beats any sentence engineered to cover the other two.

This stage is where documents are won. A claim that will not survive the question "how do I know this" is decoration, and every later difficulty you have making a sentence sound convincing traces back to a claim that failed here.

## Deliver it

Order by the reader's path rather than by your outline or the structure of whatever you read. A reader can only take a step from where they are standing, so open each paragraph on ground they already hold and spend the paragraph moving them one step. Length follows need: the part where they are most likely to get stuck gets the most room, which is why honest documents come out lopsided.

Inside sentences, the same principle holds at small scale. Open with what the reader already knows and end on the new payload, because the last few words carry the most weight and are what gets remembered. Let verbs do the work instead of parking the action in a noun, so "we measured drift" rather than "measurement of drift was performed." Name the same thing the same way every time; a reader tracking the encoder through a paragraph should not have to deduce that the embedding module is the same object. Say which option you would pick, and where you are guessing, say you are guessing and say what would settle it.

## Cut, then check what survived

A finished document is the residue of deletion, and the draft is where you find out what you think. Cut anything that does not move the reader along their path, including things that are true and things you enjoyed writing. Then read it aloud and repair whatever you would not say to a colleague at a whiteboard.

One check catches most of what is left. For each sentence, ask what news it carries. A sentence that carries none is a forgery of one of the kinds above, so either replace it with the fact it was standing in for or delete it. Run this on each thing you send rather than once per session, because the default voice creeps back as context fills.

## What the difference looks like

> This utility serves as a robust solution for managing large-scale data ingestion, seamlessly handling edge cases while enhancing overall pipeline reliability, a pivotal component in modern workflows.

Every clause here is a forgery, and a reader deciding whether to use this learns nothing. The same thing written by someone who has run it:

> Loads CSVs into the Postgres staging table. Handles the two malformed-row cases we hit in the 2024 exports, skips them, and logs the row numbers. Single-threaded, so a 10 GB file takes about 20 minutes; if that becomes a problem, batch the inserts.

Shorter, and it says more. It ends on the thing the reader most needs, and it tells you what the author did and did not check.

## Code

The same forgery happens in code, where comments are the usual site. A comment carries news when it says why; restating what the line does is a comment-shaped object with nothing in it.

```python
def load(path):
    """Load data from a file."""
    results = []  ## Initialize the results list
    try:
        with open(path) as f:  ## Open the file
            for line in f:  ## Iterate over each line
                results.append(line.strip())  ## Add the cleaned line
    except Exception as e:
        print(f"Error: {e}")  ## Handle any errors gracefully
        return []
    return results  ## Return the results
```

Six comments carrying nothing, and a swallowed exception that quietly turns a missing file into an empty result. What the author knew is nowhere in it:

```python
def load_barcodes(filepath):
    """Read one barcode per line, dropping the trailing newline."""
    ## latin-1: the 2024 exports carry a µ in sample names that utf-8 rejects
    with open(filepath, encoding="latin-1") as f:
        return [line.strip() for line in f]
```

One comment, and it is the one thing a reader would otherwise undo. Comment shapes and broadcasting rules, units, a workaround and the bug it exists for, an equation or paper, a choice that looks wrong until you know why. Match the surrounding file's naming and error-handling posture instead of writing generically correct code; `coding-style` covers abstraction, defensive handling, and naming. When you cannot verify a signature or a library's behavior, say so in your message rather than emitting confident code around a guess, since plausible wrong code costs a reviewer more than an admitted gap.

## The failure on the other side

Hunting tells has its own way of going wrong: clipped fragments, manufactured bluntness, contrarian positions nobody asked for, and unusual word choices stacked until the prose reads as a thesaurus attack. That is still document-shape without news, just wearing different clothes. Delve and robust are legitimate words that became suspicious through overuse, and losing the right word to avoid suspicion is a bad trade. Em dashes and semicolons are fine when the sentence wants one. Warm, plain, specific prose from someone who checked is the target.
