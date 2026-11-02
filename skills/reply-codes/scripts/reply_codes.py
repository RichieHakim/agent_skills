#!/usr/bin/env python3
"""Claude Code UserPromptSubmit hook for reply codes.

When a message ends with a reply code, such as "why did the job fail? /r 1",
this hook attaches the matching format instruction for Claude, for that message
only. The codes are read from the table in ../SKILL.md, so edit them there.

A message without a code prints nothing and goes through unchanged. A mistyped
code prints a warning that the user sees. Needs Python 3.6+ and the standard
library only.
"""
import json
import os
import re
import sys

PATH_SKILL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "SKILL.md"
)

## Text, then whitespace, then "/r" and at most 60 characters on the last line.
## Trailing punctuation is dropped, so "why? /r 1." gives "1".
RE_TRAILING = re.compile(r"\S\s+/r[ \t]+([^\n]{1,60}?)[\s.!?]*$")
## One code: an optional count, then an optional letter.
RE_CODE = re.compile(r"^(\d{1,3})?([a-z])?$")
## The number placeholder in the table's third column.
RE_PLACEHOLDER = re.compile(r"\bN\b")
## "1 short paragraphs" -> "one short paragraph", "1 words" -> "one word".
RE_ONE_PLURAL = re.compile(r"\b1 ((?:\w+ )?\w+?)s\b")


def load_table(path):
    """Read the code table in SKILL.md.

    Returns two dicts keyed by letter: instructions for the letter alone, and
    templates for the letter after a number. The key "" is a number alone.
    """
    single, counted = {}, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 3:
                continue
            m = re.match(r"^`(\w+)`", cells[0])
            if not m:
                continue
            key = "" if m.group(1) == "N" else m.group(1)
            if cells[1]:
                single[key] = cells[1]
            if cells[2]:
                counted[key] = cells[2]
    return single, counted


def instruction_for(token, single, counted):
    """Return the instruction for one code, or None if it isn't a known code."""
    m = RE_CODE.match(token)
    if not token or not m:
        return None
    count, letter = m.group(1), m.group(2) or ""
    if count is None:
        return single.get(letter)
    if int(count) == 0 or letter not in counted:
        return None
    text = RE_PLACEHOLDER.sub(str(int(count)), counted[letter])
    if int(count) == 1:
        text = RE_ONE_PLURAL.sub(r"one \1", text)
    return text


def emit(payload):
    print(json.dumps(payload))


def warn(message):
    emit({"systemMessage": "/r: " + message})


def main():
    try:
        prompt = json.load(sys.stdin).get("prompt") or ""
    except ValueError:
        return
    m = RE_TRAILING.search(prompt)
    if not m:
        return
    text = m.group(1).strip()

    try:
        single, counted = load_table(PATH_SKILL)
    except OSError as e:
        warn("could not read the code table in %s (%s)" % (PATH_SKILL, e))
        return
    if not single and not counted:
        warn("found no codes in the table in %s" % PATH_SKILL)
        return

    tokens = [t.strip(",;") for t in text.lower().split()]
    instructions = [instruction_for(t, single, counted) for t in tokens]
    if all(instructions):
        body = " ".join(instructions)
    elif len(tokens) == 1 and RE_CODE.match(tokens[0]):
        known = ", ".join(sorted(k for k in set(single) | set(counted) if k))
        warn("unknown code '%s'. Codes: a number, %s. See %s" % (text, known, PATH_SKILL))
        return
    else:
        body = "Format the reply this way: %s." % text.rstrip(".")

    context = (
        'The user ended this message with "/r %s", a reply code. '
        "For this reply only: %s Don't mention the code." % (text, body)
    )
    emit({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    })


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # a hook bug must never block the user's message
        warn("hook error: %r" % (e,))
