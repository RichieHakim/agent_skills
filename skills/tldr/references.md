# TL;DR references

Settings for `SKILL.md`. Change them here, not there.

## Summary

| Setting | Value |
|---|---|
| Reading time for the summary, max | 1 minute |
| Supporting sentences after the opening one | 3 to 5 |

## Blind reader

| Setting | Value |
|---|---|
| Readers per round | 1 |
| Reader's account of the message, max sentences | 2 |
| Flagged items, max | 5 |
| Rounds | 1; run one more only if the reader's account missed the point |

Example of the sentence on who the user is: "A biologist who writes Python every day, knows this project's tools, and has not seen this session."

## Sentence checker

`scripts/sentence_check.py` needs Python with spaCy, the `en_core_web_trf` model, PyTorch, NumPy, and NLTK's WordNet data. It reads a markdown file (or `-` for stdin) and prints each flagged sentence, then counts per 1,000 words. Add `--json` for machine-readable output.

| Setting | Value |
|---|---|
| Python with spaCy on this machine | `/n/holylabs/kempner_rhakim_lab/Lab/rhakim/envs/spacy/bin/python` |
| spaCy model | `en_core_web_trf`; `en_core_web_sm` is about 7 times faster but missed 7 of 32 test sentences |
| Subject-to-verb distance that counts as long | more than 7 words (`--max_subject_verb_words`; the 95th percentile in 3,000 sentences of the Brown corpus) |
| Nouns in a row that count as stacked | 3 or more |
| CPU threads | 4 (`--num_threads`; more threads ran slower on a busy shared machine) |
| Time per run, including model load | about 12 seconds for a 200-word summary |
| Check on the paper's own examples | caught 29 of 30 sentences on these four patterns; nouns used as verbs are not detected |

Run it with Python's isolated mode, so that files in the working folder can't shadow its imports:

```bash
<python> -I scripts/sentence_check.py draft.md
```

To install it elsewhere (CPU only):

```bash
conda create -y -p <env> python=3.12
<env>/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
<env>/bin/pip install spacy spacy-transformers nltk numpy
<env>/bin/python -m spacy download en_core_web_trf
<env>/bin/python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

Then put `<env>/bin/python` in the first row of the table above.
