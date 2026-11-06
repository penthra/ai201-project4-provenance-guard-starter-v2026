"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Sentence-length spread, vocabulary variety over 50-word sliding windows,
and repeated three/four-word phrases form the score. Punctuation density
and whole-text vocabulary variety remain available as diagnostics.

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
from collections import Counter
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three raw measures ───────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """Sample standard deviation of sentence word counts divided by their mean.

    Higher means more varied sentence lengths. Fewer than two sentences or no
    words gives 0: insufficient evidence of variation, not evidence of AI.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    if len(lengths) < 2 or not sum(lengths):
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """Distinct lowercase words / total words; 0 for text without words.

    Higher means more vocabulary variety. Longer texts tend to have lower
    ratios even when authorship is unchanged.
    """
    tokens = words(text)
    return len(set(tokens)) / len(tokens) if tokens else 0.0


def windowed_type_token_ratio(text: str, window_size: int = 50) -> float:
    """Mean distinct-word ratio across every fixed-size sliding word window.

    For fewer than window_size words, use the whole available text. This
    reduces length dependence on longer passages; short passages still have
    length-dependent estimates. No words gives 0, as in type_token_ratio.
    """
    if window_size < 1:
        raise ValueError("window_size must be positive")
    tokens = words(text)
    if not tokens:
        return 0.0
    width = min(window_size, len(tokens))
    counts = Counter(tokens[:width])
    total = len(counts) / width
    for index in range(width, len(tokens)):
        outgoing = tokens[index - width]
        counts[outgoing] -= 1
        if counts[outgoing] == 0:
            del counts[outgoing]
        counts[tokens[index]] += 1
        total += len(counts) / width
    return total / (len(tokens) - width + 1)


def repeated_phrase_ratio(text: str) -> float:
    """Largest duplicate-occurrence fraction for three- and four-word phrases.

    Count only phrases within a sentence. For each phrase length, occurrences
    after the first are duplicates; divide by all occurrences of that length.
    No usable phrases gives 0. Repetition is a heuristic, not proof of AI:
    quotations, templates, and deliberate human repetition can also score high.
    """
    tokenized = [words(sentence) for sentence in sentences(text)]
    ratios = []
    for width in (3, 4):
        counts = Counter(
            tuple(tokens[index:index + width])
            for tokens in tokenized
            for index in range(len(tokens) - width + 1)
        )
        total = sum(counts.values())
        ratios.append((total - len(counts)) / total if total else 0.0)
    return max(ratios)


def punctuation_density(text: str) -> float:
    """Count . , ! ? ; : - — ( ) per word; 0 for text without words.

    Each character counts once. This measures amount, not variety, and can
    exceed 1. Apostrophes are excluded because the word splitter keeps them.
    """
    word_count = len(words(text))
    if not word_count:
        return 0.0
    return sum(character in ".,!?;:-—()" for character in text) / word_count


# ── Combining style measurements ──────────────────────────────────────────


def style_signal(text: str) -> float:
    """Heuristic score, 0–1, higher meaning more AI-like.

    Retain the equal-weight spread/vocabulary rule, but measure vocabulary
    over 50-word windows. Repeated-phrase evidence sets a floor on that score:
    max(0.5 * spread_score + 0.5 * vocabulary_score, repeated_phrase_ratio).
    This prevents high word variety from hiding extensive phrase duplication.
    The window size and rule are explicit provisional choices, not fitted to
    the evaluation inputs or calibrated probabilities of authorship.

    Fewer than two word-bearing sentences gives a neutral spread component;
    no words gives a neutral overall score. Punctuation has no direct weight.
    """
    if not words(text):
        return 0.5

    word_bearing_sentences = sum(bool(words(sentence)) for sentence in sentences(text))
    spread_score = (
        1.0 - min(sentence_length_spread(text), 1.0)
        if word_bearing_sentences >= 2 else 0.5
    )
    vocabulary_score = 1.0 - windowed_type_token_ratio(text)
    base_score = 0.5 * spread_score + 0.5 * vocabulary_score
    return round(max(base_score, repeated_phrase_ratio(text)), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"windowed_type_token_ratio {windowed_type_token_ratio(text)}")
    print(f"repeated_phrase_ratio     {repeated_phrase_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nHeuristic score; punctuation density is diagnostic only.")
