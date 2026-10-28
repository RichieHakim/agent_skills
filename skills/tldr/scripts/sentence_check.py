"""
Find sentence features in a markdown text that reading research ties to slower reading.

Method follows Clark, Martin & Mahowald (arXiv 2610.29162), appendix B: parse with spaCy,
read features off the dependency tree. Inline code, URLs and file paths are replaced by one
placeholder word, and fenced code blocks are dropped, before parsing.

Features (names as they appear in the output):
    orc_no_relativizer      object relative clause with no "that"/"which"/"who(m)"
    orc_with_relativizer    object relative clause with one
    stacked_nouns           3+ nouns joined by compound arcs (all-proper-noun names excluded)
    long_subject_verb       subject more than ``--max_subject_verb_words`` (default 7) words from its verb
    long_verb_object        verb to direct object, same threshold (extra, not in the task list)
    inanimate_animate_candidate  non-person subject of a verb that normally needs a living subject
Plus the standardized mean dependency length of the text (z-score within sentence-length bins,
against ``dl_reference.json``, see ``build_dl_reference.py``).

Usage:
    python sentence_check.py reply.md [--model en_core_web_trf] [--json]
    cat reply.md | python sentence_check.py - --json
"""

from typing import Dict, List, Optional

import argparse
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import spacy
import torch
from nltk.corpus import wordnet

logger = logging.getLogger("sentence_check")

PLACEHOLDER = "CODEREF"  ## one noun-like word that stands in for code, URLs and paths
DIR_CODE = Path(__file__).resolve().parent
FILEPATH_DL_REFERENCE = str(DIR_CODE / "dl_reference.json")

## Sentence-length bins from the paper (words, punctuation excluded); longer sentences are dropped.
BINS_DL = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 30)]

RELATIVIZERS = {"that", "which", "who", "whom", "whose"}
RELATIVE_ADVERBS = {"where", "when", "why", "whereby", "wherein"}  ## no object gap: not object relatives
## Verbs that normally take a living subject. Lemmas.
VERBS_LIVING = {
    "eat", "swallow", "bite", "promise", "forget", "hope", "expect", "ask", "want",
    "know", "hide", "misunderstand", "complain", "refuse",
}
## Surface forms too: the transformer model's lemmatizer is unreliable ("hoped" -> "hop").
FORMS_VERBS_LIVING = {
    form for base in VERBS_LIVING for form in (base, base + "s", base + "es", base + "ed", base + "d", base + "ing", base[:-1] + "ing")
} | {"ate", "eaten", "bit", "bitten", "forgot", "forgotten", "hid", "hidden", "knew", "known", "misunderstood"}
PRONOUNS_PERSON = {
    "i", "you", "he", "she", "we", "they", "who", "whom", "someone", "somebody", "everyone",
    "everybody", "anyone", "anybody", "nobody", "one", "me", "us", "them",
}
## WordNet hypernym roots that mark a living or agentive subject (people, groups, animals).
SYNSETS_LIVING = {"person.n.01", "social_group.n.01", "animal.n.01", "organism.n.01"}

PATTERN_FENCE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M)
PATTERN_INLINE_CODE = re.compile(r"`[^`\n]+`")
PATTERN_URL = re.compile(r"(https?://|www\.)\S+")
## Paths: ~/x, ./x, /x/y, or a/b/c.ext. A lone "and/or" or "case/when" is not a path.
PATTERN_PATH = re.compile(
    r"(?<![\w/])(~|\.{1,2})?(/[\w.\-]+){1,}/?(?![\w/])|(?<![\w/])[\w.\-]+(/[\w.\-]+){2,}"
)
## Bare identifiers an agent forgot to put in backticks: snake_case words and calls like is_file().
PATTERN_IDENTIFIER = re.compile(r"\b\w+_\w+(\(\))?|\b\w+\(\)")
PATTERN_LIST_START = re.compile(r"^\s*([-*+]|\d+[.)])\s+")


@dataclass
class CheckConfig:
    path_input: str = "-"
    model: str = "en_core_web_trf"
    max_subject_verb_words: int = 7
    json_output: bool = False
    num_threads: int = 4
    dir_save: Optional[str] = None
    log_level: str = "INFO"


def parse_args() -> CheckConfig:
    """Parse the command line into a CheckConfig (defaults come from the dataclass)."""
    defaults = CheckConfig()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path_input", help="Markdown file, or - for stdin.")
    parser.add_argument("--model", default=defaults.model, help="spaCy model: en_core_web_trf or en_core_web_sm.")
    parser.add_argument(
        "--max_subject_verb_words",
        type=int,
        default=defaults.max_subject_verb_words,
        help="Flag a subject more than this many words from its verb.",
    )
    parser.add_argument("--num_threads", type=int, default=defaults.num_threads, help="torch CPU threads (transformer model).")
    parser.add_argument("--json", dest="json_output", action="store_true", help="Print JSON instead of text.")
    parser.add_argument("--dir_save", default=None, help="Optional: also write result.json here.")
    parser.add_argument("--log_level", default=defaults.log_level)
    return CheckConfig(**vars(parser.parse_args()))


def clean_markdown(text: str) -> List[str]:
    """
    Turn markdown into blocks of plain prose, one block per paragraph or list item.

    Fenced code is removed; inline code, URLs, paths and bare identifiers become ``PLACEHOLDER``;
    emphasis, heading and link markup is stripped.

    Args:
        text (str): Raw markdown.

    Returns:
        (List[str]): Non-empty blocks of text.
    """
    text = PATTERN_FENCE.sub("", text)
    text = PATTERN_INLINE_CODE.sub(PLACEHOLDER, text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  ## [label](url) -> label
    text = PATTERN_URL.sub(PLACEHOLDER, text)
    text = PATTERN_PATH.sub(PLACEHOLDER, text)
    text = PATTERN_IDENTIFIER.sub(PLACEHOLDER, text)
    text = re.sub(r"(\*\*|__|\*|(?<!\w)_|_(?!\w))", "", text)  ## emphasis markers
    blocks: List[str] = []
    current: List[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        is_break = stripped == ""
        is_new_unit = bool(PATTERN_LIST_START.match(line)) or stripped.startswith(("#", "|", ">"))
        if is_break or is_new_unit:
            if current:
                blocks.append(" ".join(current))
            current = []
        if is_break or re.fullmatch(r"[|\s:\-]+", stripped):  ## blank line or table rule
            continue
        stripped = re.sub(r"^(#+|>|[-*+]|\d+[.)])\s*", "", stripped)
        current.append(stripped)
    if current:
        blocks.append(" ".join(current))
    return [block for block in blocks if re.search(r"\w", block)]


def words_of(sentence) -> List:
    """Tokens that count as words: not punctuation, not whitespace."""
    return [token for token in sentence if not (token.is_punct or token.is_space)]


def word_distance(index_word: Dict[int, int], token_a, token_b) -> int:
    """Distance in words (punctuation skipped) between two tokens of one sentence."""
    return abs(index_word[token_a.i] - index_word[token_b.i])


def index_words(sentence) -> Dict[int, int]:
    """Map token index -> position among words. Punctuation maps to the next word's position."""
    mapping: Dict[int, int] = {}
    count = 0
    for token in sentence:
        mapping[token.i] = count
        if not (token.is_punct or token.is_space):
            count += 1
    return mapping


def mean_dependency_length(sentence) -> Optional[float]:
    """Mean arc length in words over non-punctuation arcs, excluding the root. ``None`` if no arcs."""
    index_word = index_words(sentence=sentence)
    lengths = [
        word_distance(index_word=index_word, token_a=token, token_b=token.head)
        for token in sentence
        if not (token.is_punct or token.is_space) and token.head.i != token.i and not token.head.is_punct
    ]
    return float(np.mean(lengths)) if lengths else None


def bin_of_length(num_words: int) -> Optional[str]:
    """Name of the paper's length bin ('6-10'), or ``None`` for sentences longer than 30 words."""
    for low, high in BINS_DL:
        if low <= num_words <= high:
            return f"{low}-{high}"
    return None


def is_living_noun(token) -> bool:
    """True if a noun refers to a person, group or animal (spaCy entity type or WordNet)."""
    if token.ent_type_ in {"PERSON", "ORG", "NORP", "GPE"} or token.pos_ == "PROPN":
        return True
    for synset in wordnet.synsets(token.lemma_.lower(), pos="n")[:2]:  ## first two senses only
        for path in synset.hypernym_paths():
            if any(node.name() in SYNSETS_LIVING for node in path):
                return True
    return False


def resolve_subject(verb):
    """Subject of a verb. Looks through conjunction (shared subject) and relative pronouns."""
    verb_with_subject = verb
    subject = next((c for c in verb.children if c.dep_ in {"nsubj", "nsubjpass"}), None)
    if subject is None and verb.dep_ == "conj":
        verb_with_subject = verb.head
        subject = next((c for c in verb.head.children if c.dep_ in {"nsubj", "nsubjpass"}), None)
    if subject is not None and subject.tag_ in {"WDT", "WP"}:  ## "a check that covered ... forgot"
        clause = verb_with_subject
        subject = clause.head if clause.dep_ == "relcl" else None
    return subject


def find_features(sentence, max_subject_verb_words: int) -> List[dict]:
    """
    Find all features in one parsed sentence.

    Args:
        sentence (spacy.tokens.Span): One sentence.
        max_subject_verb_words (int): Subject-verb (and verb-object) gap that counts as long.

    Returns:
        (List[dict]): One dict per hit with keys feature, words.
    """
    hits: List[dict] = []
    index_word = index_words(sentence=sentence)

    for token in sentence:
        ## Object relative clauses: the clause has its own (non-relative-pronoun) subject.
        if token.dep_ == "relcl":
            subjects = [c for c in token.children if c.dep_ in {"nsubj", "nsubjpass"}]
            own_subjects = [c for c in subjects if c.tag_ not in {"WDT", "WP", "WP$"} and c.lower_ not in RELATIVIZERS]
            has_relative_adverb = any(c.lower_ in RELATIVE_ADVERBS for c in token.children)
            if own_subjects and len(own_subjects) == len(subjects) and not has_relative_adverb:
                candidates = list(token.children) + [g for c in token.children if c.dep_ == "prep" for g in c.children]
                relativizer = next(
                    (c for c in candidates if c.dep_ not in {"nsubj", "nsubjpass"} and (c.tag_ in {"WDT", "WP"} or c.lower_ in RELATIVIZERS)),
                    None,
                )
                feature = "orc_no_relativizer" if relativizer is None else "orc_with_relativizer"
                words = f"{token.head.text} <- {own_subjects[0].text} {token.text}"
                hits.append(dict(feature=feature, words=words))

        ## Stacked nouns: the compound subtree under a head that is not itself a compound modifier.
        if token.dep_ != "compound":
            members = [token]
            stack = [c for c in token.children if c.dep_ == "compound"]
            while stack:
                member = stack.pop()
                members.append(member)
                stack.extend(c for c in member.children if c.dep_ == "compound")
            nouns = [m for m in members if m.pos_ in {"NOUN", "PROPN"}]
            if len(nouns) >= 3 and not all(m.pos_ == "PROPN" for m in nouns):
                members.sort(key=lambda m: m.i)
                span = sentence.doc[members[0].i : members[-1].i + 1]
                hits.append(dict(feature="stacked_nouns", words=span.text))

        if token.pos_ in {"VERB", "AUX"}:
            ## Long subject-verb and verb-object gaps.
            for child in token.children:
                if child.dep_ in {"nsubj", "nsubjpass", "csubj"}:
                    gap = word_distance(index_word=index_word, token_a=child, token_b=token)
                    if gap > max_subject_verb_words:
                        hits.append(dict(feature="long_subject_verb", words=f"{child.text} ... {token.text} ({gap} words)"))
                if child.dep_ == "dobj":
                    gap = word_distance(index_word=index_word, token_a=child, token_b=token)
                    if gap > max_subject_verb_words:
                        hits.append(dict(feature="long_verb_object", words=f"{token.text} ... {child.text} ({gap} words)"))

            ## Non-person subject with a verb for living things.
            if token.lemma_.lower() in VERBS_LIVING or token.lower_ in FORMS_VERBS_LIVING:
                subject = resolve_subject(verb=token)
                if subject is not None:
                    is_pronoun_open = subject.lower_ in {"it", "this", "that"}
                    is_candidate = (
                        subject.text == PLACEHOLDER
                        or is_pronoun_open
                        or (subject.pos_ == "NOUN" and subject.lower_ not in PRONOUNS_PERSON and not is_living_noun(token=subject))
                    )
                    if is_candidate:
                        hits.append(dict(feature="inanimate_animate_candidate", words=f"{subject.text} {token.text}"))
    return hits


def check_text(text: str, nlp, reference_dl: dict, max_subject_verb_words: int) -> dict:
    """
    Run all checks on a markdown text.

    Args:
        text (str): Markdown.
        nlp (spacy.Language): Loaded spaCy pipeline.
        reference_dl (dict): Per-bin mean and sd of sentence mean dependency length for this model.
        max_subject_verb_words (int): See ``find_features``.

    Returns:
        (dict): ``sentences`` (flagged ones), ``counts``, ``rates_per_1000_words``, ``num_words``,
            ``num_sentences``, ``dependency_length`` (raw and standardized means).
    """
    blocks = clean_markdown(text=text)
    flagged: List[dict] = []
    num_words = 0
    num_sentences = 0
    lengths_raw: List[float] = []
    lengths_z: List[float] = []
    for doc in nlp.pipe(blocks):
        for sentence in doc.sents:
            num_in_sentence = len(words_of(sentence=sentence))
            if num_in_sentence == 0:
                continue
            num_words += num_in_sentence
            num_sentences += 1
            for hit in find_features(sentence=sentence, max_subject_verb_words=max_subject_verb_words):
                flagged.append(dict(hit, sentence=sentence.text.strip()))
            name_bin = bin_of_length(num_words=num_in_sentence)
            length = mean_dependency_length(sentence=sentence)
            if name_bin is not None and length is not None:
                stats = reference_dl[name_bin]
                lengths_raw.append(length)
                lengths_z.append((length - stats["mean"]) / stats["sd"])
    names_feature = [
        "orc_no_relativizer", "orc_with_relativizer", "stacked_nouns", "long_subject_verb", "long_verb_object",
        "inanimate_animate_candidate",
    ]
    counts = {name: sum(1 for hit in flagged if hit["feature"] == name) for name in names_feature}
    rates = {name: (1000.0 * counts[name] / num_words if num_words else 0.0) for name in names_feature}
    return dict(
        num_words=num_words,
        num_sentences=num_sentences,
        flagged=flagged,
        counts=counts,
        rates_per_1000_words=rates,
        dependency_length=dict(
            num_sentences_used=len(lengths_z),
            mean_raw_words=float(np.mean(lengths_raw)) if lengths_raw else None,
            mean_standardized=float(np.mean(lengths_z)) if lengths_z else None,
        ),
    )


def format_text_report(result: dict) -> str:
    """Human-readable report: one block per flagged sentence, then counts and rates."""
    lines: List[str] = []
    for hit in result["flagged"]:
        lines.append(f"[{hit['feature']}] {hit['words']}\n    {hit['sentence']}")
    lines.append("")
    lines.append(f"words: {result['num_words']}  sentences: {result['num_sentences']}")
    lines.append(f"{'feature':32s} {'count':>6s} {'per 1000 words':>15s}")
    for name, count in result["counts"].items():
        lines.append(f"{name:32s} {count:6d} {result['rates_per_1000_words'][name]:15.2f}")
    dl = result["dependency_length"]
    if dl["mean_standardized"] is not None:
        lines.append(
            f"mean dependency length: {dl['mean_raw_words']:.2f} words raw, "
            f"{dl['mean_standardized']:+.2f} sd vs reference ({dl['num_sentences_used']} sentences of 1-30 words)"
        )
    return "\n".join(lines)


def main() -> None:
    config = parse_args()
    logging.basicConfig(level=config.log_level, stream=sys.stderr, format="%(levelname)s %(message)s")
    if config.path_input != "-":
        assert Path(config.path_input).is_file(), f"Input not found: {config.path_input}"
    assert Path(FILEPATH_DL_REFERENCE).is_file(), f"Missing {FILEPATH_DL_REFERENCE}; run build_dl_reference.py"
    with open(FILEPATH_DL_REFERENCE) as file:
        references = json.load(file)
    assert config.model in references, f"No dependency-length reference for {config.model}"
    text = sys.stdin.read() if config.path_input == "-" else Path(config.path_input).read_text()
    torch.set_num_threads(config.num_threads)
    nlp = spacy.load(config.model)
    result = check_text(
        text=text, nlp=nlp, reference_dl=references[config.model], max_subject_verb_words=config.max_subject_verb_words
    )
    result["config"] = asdict(config)
    print(json.dumps(result, indent=2) if config.json_output else format_text_report(result=result))
    if config.dir_save is not None:
        os.makedirs(config.dir_save, exist_ok=True)
        filepath = str(Path(config.dir_save) / "result.json")
        with open(filepath + ".tmp", "w") as file:
            json.dump(result, file, indent=2)
        os.replace(filepath + ".tmp", filepath)


if __name__ == "__main__":
    main()
