---
name: tldr
description: Rewrite your recent long or dense replies as a short summary for a busy reader, then check it with a reader who has no context. Use when the user types /tldr or asks for the short version, a summary, or the headlines of what you reported.
---

# TL;DR

The user found your recent replies hard to read. Rewrite them as a short, plain summary that a busy reader can take in quickly. If you have the `deslop` skill, load it first; every rule in it applies. Don't apologize or describe the rewrite; send only the result. Limits, paths, and settings are in `references.md` in this skill's folder; read it before you start.

You write the summary, because you know what your own terms mean; an agent without your context would have to guess. A new agent then reads your summary with no context and reports what it could not follow, because only such a reader can spot your private terms. Those terms come from this session, not from project memory, so an ordinary new subagent is blind enough.

1. **Choose what to rewrite.** If the user named a reply or a topic, rewrite that. Otherwise, rewrite your replies since the user's last real request.
2. **Save the detail first.** If the long version holds anything that the summary will drop, write it to a file where the project keeps reports. Every decision, number, caveat, failed check, and path must survive somewhere.
3. **Find the point.** In one sentence: what is the user's overall goal, and where does this work leave it? What must the user decide or do now?
4. **Draft the summary:**
   - One sentence with the answer, the result, or the decision needed.
   - A few full sentences, most important first. Each says what you found or did and what it means for the goal. Write sentences, not newspaper headlines or fragments under bold labels.
   - Any decision that the user must make, with what each option costs.
   - The absolute path to the full detail.
5. **Check the sentences.** If the sentence checker in this skill's `references.md` is installed, save the draft to a file and run `scripts/sentence_check.py` on it. The script parses each sentence, as Clark, Martin & Mahowald (2026) did, and lists sentences with a dropped "that", stacked nouns, a subject far from its verb, or a thing doing what only living things do. That last one is only a candidate: "it" may mean an agent, which can know things. Rewrite each flagged sentence that a reader would stumble on, and leave the rest.
6. **Test it on a blind reader.** Start a new subagent that has not seen this conversation; do not give it a copy of your session. Give it only three things: one sentence on who the user is and what they already know, the user's last request in the user's words, and your draft. Tell it to open no files, run no commands, and load no skills. Ask it to:
   - say briefly what happened and what it is being asked to decide or do;
   - quote, most important first, the few words, phrases, or references that most kept it from understanding the point or the decision.

   Don't explain the draft to it or suggest answers. Readers nitpick at a steady rate however clear the text is, so the number of flags is not a score; asking for only the worst few keeps the list useful.
7. **Fix and check.** Describe or replace each item that it flagged, unless the user clearly knows it; a term that a reader can't decode needs a plain description, not a new name. If its account of the message differs from your point, rewrite the opening. Then compare the summary with the original: no decision, caveat, or failed check is lost, and nothing new is claimed.
8. **Send the summary.**
