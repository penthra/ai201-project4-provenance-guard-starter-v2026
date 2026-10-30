"""Run the same three synthetic test passages through both signals.

These are style probes, not a labeled human-versus-AI evaluation dataset.
Run: python compare_signals.py
"""
import json
from pathlib import Path

import detector
import stylometry


PIECES = [
    ("Plain conventional prose", (
        "Every morning I get up and make breakfast. Then I go to work and talk "
        "to the people in my office. At the end of the day I come home and "
        "make dinner. Sometimes I watch television before I go to bed."
    )),
    ("Varied narrative", (
        "Stop! The bus lurched past my corner while I wrestled a dripping "
        "umbrella into its sleeve, one shoe planted in yesterday's muddy pothole. "
        "Perfect timing. Somewhere behind me, a kid laughed; I nearly did too."
    )),
    ("Repeated unusual vocabulary", (
        "The xylophonic zephyr perplexes the quincunx. "
        "The quincuncial zephyr perplexes the syzygy. "
        "The syzygetic zephyr perplexes the xylophone. "
        "The xylophonic zephyr perplexes the quincunx."
    )),
]


def main():
    rows = []
    for name, text in PIECES:
        model_score = detector.model_signal(text)
        style_score = stylometry.style_signal(text)
        row = {
            "name": name,
            "text": text,
            "model_score": model_score,
            "style_score": style_score,
            "absolute_gap": round(abs(model_score - style_score), 4),
            "equal_weight_average": round((model_score + style_score) / 2, 4),
        }
        rows.append(row)
        print(json.dumps(row, ensure_ascii=True), flush=True)
    output = Path(__file__).resolve().parent / 'results' / 'signal_comparison.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    print(f'Saved {output}')


if __name__ == '__main__':
    main()
