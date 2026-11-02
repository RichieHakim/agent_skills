---
name: r
description: Reply codes, invoked as /reply-codes or its short form /r. The user ends or starts a message with "/r <code>" to set the length or shape of your reply to that message, such as "/r 1" for one sentence or "/r b" for short bullets.
argument-hint: "<code> [message]"
disable-model-invocation: true
---

# Reply codes

The user added a reply code to this message. Look it up in the table below and shape your reply to this message that way. The code applies to this reply only. Answer the rest of the message as usual, and don't mention the code.

A code is a letter, a number, or a number followed by a letter, such as `2` or `3b`; the number sets the count. Codes can be combined with spaces, such as `q 2`. If the text after `/r` is not a code, it is a format request in the user's own words, such as `/r one paragraph, then a table`; follow it.

When the user starts a message with `/r` or `/reply-codes`, the message arrives below as ARGUMENTS, and its first word or words are the code.

<!-- scripts/reply_codes.py reads this table. Keep the three columns and the backticks around each code. -->

| Code | Reply format | With a number N first, such as `3b` |
|---|---|---|
| `N` alone, such as `2` | | Respond in N sentences. |
| `w` | Respond in a few words; a full sentence isn't needed. | Respond in at most N words. |
| `p` | Respond in one short paragraph of plain language. | Respond in N short paragraphs of plain language. |
| `b` | Respond with bullets of a few words each. | Respond with exactly N bullets of a few words each. |
| `y` | Start with yes or no, then give one sentence on why. | |
| `t` | Respond with a table and at most one sentence around it. | |
| `f` | Make a figure and show it. | |
| `q` | Just answer; don't edit files or run anything. | |
