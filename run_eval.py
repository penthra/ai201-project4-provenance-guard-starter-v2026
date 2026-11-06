#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

Runs the fixed criteria in criteria.md, including appeal persistence checks.
The report calculates all five metrics and requires every trial to pass.
"""

import argparse
import datetime as dt
import json
import sys
import uuid
from statistics import mean
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def request_json(requests, method, url, timeout, **kwargs):
    """Preserve HTTP status and the actual JSON (or non-JSON error evidence)."""
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
    except Exception as exc:
        return {"status": None, "error": f"{type(exc).__name__}: {exc}"}
    result = {"status": response.status_code}
    try:
        result["response"] = response.json() if response.content else {}
    except ValueError as exc:
        result.update(error=f"{type(exc).__name__}: {exc}",
                      response_text=response.text[:1000])
    return result


def evaluate_submission(requests, scenario, body, url, timeout):
    """Submit a sample; for appeals, verify both response and saved audit state."""
    result = request_json(requests, "POST", f"{url}/submit", timeout, json=body)
    result["sent"] = describe(body)
    result["creator_id"] = body.get("creator_id")
    payload = result.get("response", {})
    if not isinstance(payload, dict):
        result["error"] = "Expected a JSON object"
        payload = {}
    for field in ("content_id", "guess", "confidence", "model_score", "style_score", "label"):
        result[field] = payload.get(field)
    if not scenario.get("appeal_reasoning"):
        return result
    if result["status"] != 200 or not payload.get("content_id"):
        result["appeal_passed"] = False
        return result
    content_id = payload["content_id"]
    appeal = request_json(requests, "POST", f"{url}/appeal", timeout,
                          json={"content_id": content_id,
                                "reasoning": scenario["appeal_reasoning"]})
    log = request_json(requests, "GET", f"{url}/log", timeout)
    log_payload = log.get("response", {})
    entries = log_payload.get("entries", []) if isinstance(log_payload, dict) else []
    matching = [e for e in entries if isinstance(e, dict) and e.get("content_id") == content_id]
    original = any(e.get("status") == "decided" for e in matching)
    saved = any(e.get("event") == "appeal" and e.get("status") == "under_review"
                and e.get("creator_id") == body["creator_id"]
                and e.get("reasoning") == scenario["appeal_reasoning"] for e in matching)
    appeal_payload = appeal.get("response", {})
    result.update(appeal=appeal, log_status=log["status"], audit_entries=matching)
    result["appeal_passed"] = bool(
        appeal["status"] == 200 and isinstance(appeal_payload, dict)
        and appeal_payload.get("status") == "under_review"
        and appeal_payload.get("content_id") == content_id
        and log["status"] == 200 and original and saved
        and matching[-1].get("status") == "under_review")
    return result


def trial_metric(scenario, results):
    """Apply the original numeric targets, without relaxing a missed target."""
    criterion = scenario["criterion"]
    if criterion == 5:
        count = sum(isinstance(r.get("response"), dict)
                    and r.get("status") == 400
                    and bool(r["response"].get("error"))
                    and bool(r["response"].get("message")) for r in results)
        return f"{count}/4", count >= 3
    if criterion == 4:
        count = sum(r.get("appeal_passed", False) for r in results)
        return f"{count}/5", count >= 4
    valid = (len(results) == len(scenario["texts"]) and all(
        r.get("status") == 200 and r.get("guess") in ("ai", "human", "unsure")
        and isinstance(r.get("confidence"), (int, float))
        and 0 <= r["confidence"] <= 1 for r in results))
    if not valid:
        return "INCOMPLETE (request failure)", False
    if criterion == 1:
        count = sum(r["guess"] == "ai" for r in results)
        return f"{count}/10", count <= 3
    if criterion == 2:
        ai = [r["confidence"] for r in results if r["origin"] == "ai"]
        human = [r["confidence"] for r in results if r["origin"] == "human"]
        gap = mean(ai) - mean(human)
        return f"{gap:.5f} (AI {mean(ai):.5f}; human {mean(human):.5f})", gap >= 0.15
    count = len({r["guess"] for r in results})
    return f"{count}/3", count == 3


TARGETS = {1: "<= 3/10 flagged AI", 2: "AI mean - human mean >= 0.15",
           3: "3/3 labels in 15 texts", 4: ">= 4/5 appeals saved and under review",
           5: ">= 3/4 clear errors without crashes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    run_id = uuid.uuid4().hex[:10]
    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            results = []
            for i, body in enumerate(bodies_for(scenario), 1):
                # Isolate each scenario/sample within this evaluation run. Each
                # creator is reused across trials (only three submits, below 8/min).
                body = dict(body)
                body["creator_id"] = f"eval_{run_id}_c{scenario['criterion']}_{i}"
                result = evaluate_submission(requests, scenario, body, args.url, args.timeout)
                if scenario.get("origins"):
                    result["origin"] = scenario["origins"][i - 1]
                results.append(result)

            trials.append(results)
            guesses = [r.get("guess") or "—" for r in results]
            print(f"  trial {trial}: {', '.join(guesses)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Targets are the five original criteria in `criteria.md`.",
        "MET requires all three trials to meet the target; failures are retained.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        metrics = [trial_metric(scenario, results) for results in row["trials"]]
        verdict = "MET" if all(passed for _, passed in metrics) else "MISSED"
        lines.append(f"| {name} | {TARGETS[number]} | " +
                     " | ".join(value for value, _ in metrics) + f" | {verdict} |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    path.with_suffix(".json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
