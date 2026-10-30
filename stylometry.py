"""
Signal two: the style signal.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three raw measurements describe the shape of the text. Sentence-length spread
and vocabulary variety form the score; punctuation density is reported for
calibration and has no scoring weight yet.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how many punctuation characters per word?

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


def punctuation_density(text: str) -> float:
    """Count . , ! ? ; : - — ( ) per word; 0 for text without words.

    Each character counts once. This measures amount, not variety, and can
    exceed 1. Apostrophes are excluded because the word splitter keeps them.
    """
    word_count = len(words(text))
    if not word_count:
        return 0.0
    return sum(character in ".,!?;:-—()" for character in text) / word_count


# ── Combining two measures ───────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """Return a heuristic 0–1 score, with higher meaning more AI-like.

    Invert spread after clipping it to 0–1, and invert vocabulary variety.
    Average the two components with equal weights. Spread at or above 1
    contributes 0; identical sentence lengths contribute 1. With fewer than
    two word-bearing sentences, the spread component is neutral (0.5).
    Text without words also gets a neutral overall score of 0.5.

    Punctuation density is diagnostic only until calibration supports a
    direction and scale. These choices are starting heuristics, not calibrated
    evidence of authorship. Typos, text length, and sentence splitting can
    change the result without changing the author.
    """
    if not words(text):
        return 0.5

    word_bearing_sentences = sum(bool(words(sentence)) for sentence in sentences(text))
    spread_score = (
        1.0 - min(sentence_length_spread(text), 1.0)
        if word_bearing_sentences >= 2 else 0.5
    )
    vocabulary_score = 1.0 - type_token_ratio(text)
    return round(0.5 * spread_score + 0.5 * vocabulary_score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nHeuristic score; punctuation density is diagnostic only.")
