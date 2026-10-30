# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

This describes planned behavior, not a completed implementation. Scores below are hypothetical, not test results.

1. The writer sends `text` and `creator_id` as JSON to `POST /submit` in `app.py`. This gives the service the writing and identifies the submitting creator.
2. The route validates the input and assigns a unique `content_id` to a valid submission. Validation rejects unsuitable requests; the ID connects this particular decision to a later appeal.
3. `detector.model_signal(text)` measures predictability with a local language model. It adds `model_score`, from 0 to 1, with higher values meaning more AI-like.
4. `stylometry.style_signal(text)` measures sentence-length variation, vocabulary variety, and punctuation density. It adds a separate `style_score`, also from 0 to 1 with higher values meaning more AI-like.
5. `scoring.combine_signals(model_score, style_score)` combines the signals into one score using the proposed equal weights below.
6. `scoring.score_to_label(score)` maps that score to `human`, `unsure`, or `ai` and adds the full message a reader sees.
7. `audit.log_decision(...)` saves the IDs, both signal scores, combined score, guess, label, and status. The route returns the ID, scores, guess, and label as JSON so the caller can display the result.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to the local language model, measured using perplexity.

**Why that might differ between human and AI writing:**AI writing may contain more predictable word sequences. Human writing may contain unexpected choices.

**What it can't see:**Actual authorship. A real person writing simple, ordinary sentences can look predictable too.

### Signal two — the style signal

**What it measures:**how much sentence lengths vary, the number of unique words divided by the total number of words, and the amount of punctuation relative to text length.

**Why that might differ between human and AI writing:**AI-generated writing may have more consistent sentence lengths and repeated vocabulary. Human writing may vary more in sentence length, word choice, and punctuation. These are tendencies, so they do not prove who wrote the text.

**What it can't see:**This signal cannot understand the text’s meaning or identify its author. Someone can change its score by adding typos, splitting sentences, or changing punctuation. Human writing can also have a regular style and be incorrectly flagged.

The planned raw style measurements are:

- **Sentence-length spread:** standard deviation of sentence word counts divided by their mean. Low values mean similar sentence lengths. With fewer than two sentences or no words, return 0 for this raw measure; this is insufficient evidence of variation, not proof of AI authorship.
- **Type-token ratio:** distinct lowercase words divided by total words, using the provided word splitter. For example, “Cats chase cats” gives 2/3. Longer texts tend to repeat more words, so length affects this measure independently of authorship.
- **Punctuation density:** occurrences of `. , ! ? ; : - — ( )` divided by total words, with each punctuation character counted once. Return 0 if there are no words. This measures punctuation amount, not punctuation variety.

The standalone style signal in `stylometry.py::style_signal` now uses `0.5 * (1 - min(sentence_length_spread, 1)) + 0.5 * (1 - type_token_ratio)`, rounded to four decimal places. Low spread and repeated vocabulary raise the score. With fewer than two word-bearing sentences, the spread component is neutral at 0.5; text without words returns an overall 0.5. Punctuation density is reported for calibration but has no scoring weight because its direction has not been established. These are starting heuristics, not calibrated authorship probabilities. The style signal is now connected to `/submit`; both raw signal scores and the combined score are returned and logged.

The model has another blind spot: it examines only the initial token window, currently 400 tokens in `config.py`. It cannot see authorship changes beyond that window. AI text with unusual vocabulary may also score as human-like because it is hard to predict.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** My combining rule is an equal-weight average: neither signal takes priority. Both signals point in the same direction, with higher scores meaning more AI-like. There is no separate disagreement override: opposite scores such as 0.90 and 0.10 average to 0.50, inside the unsure band. Neither signal directly observes authorship.

**The numbers:** `combined_score = 0.5 * model_score + 0.5 * style_score`. In `config.py`, `WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5`; the weights sum to 1, so the result stays between the two input scores. Label boundaries are `HUMAN_THRESHOLD = 0.20` and `AI_THRESHOLD = 0.80`: human at or below 0.20, unsure above 0.20 and below 0.80, and AI at or above 0.80. Equal weights are a starting choice because neither signal has been shown more reliable on a labeled dataset. The wider unsure band is intended to reduce accusations, accepting more uncertain results. These settings are not calibrated probabilities.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** In the measured plain-conventional-prose test below, the model returned 0.9404 while style returned 0.5295, a gap of 0.4109. The predictable everyday wording pushed the model score high, while the style measurements provided a weaker AI-like signal. The equal-weight rule produces 0.7349. Under the configured 0.20/0.80 boundaries this is unsure; under the previous starter 0.35/0.65 boundaries it would be AI. Averaging reduces the influence of the high model score, but avoiding an accusation here also depends on the label boundaries. Neither score proves authorship.

### Measured comparison of both signals

Ran `python compare_signals.py` on October 30, 2026 using the Windows virtual environment and the real local detector. Each row uses exactly the same text for both signals. All three passages are synthetic style probes written for this test, not verified human-writing examples, so these results do not measure false positives or detection accuracy. Full passages and results are in [results/signal_comparison.json](results/signal_comparison.json).

| Test piece | Model score | Style score | Absolute gap | Equal-weight average | Comparison |
|---|---:|---:|---:|---:|---|
| Plain conventional prose | 0.9404 | 0.5295 | 0.4109 | 0.7349 | Split in strength: model high, style near the midpoint. |
| Varied narrative | 0.2297 | 0.0286 | 0.2011 | 0.1291 | Both low, toward human-like. |
| Repeated unusual vocabulary | 0.8935 | 0.8125 | 0.0810 | 0.8530 | Both high, toward AI-like. |

Higher values mean more AI-like for both signals. The averages above were computed by the original comparison script. `/submit` now computes both signals and calls `scoring.py::combine_signals`.


### Four-input calibration with audit verification

Ran `python calibrate_signals.py` on October 30, 2026 using the real local model and the Windows virtual environment. The script sends each input through `/submit`, prints both signals separately, and checks that the matching decision is readable through `/log`. Full texts, provenance, content IDs, and responses are saved in [results/calibration_signals.json](results/calibration_signals.json). Re-running the script appends four new decisions to `logs/audit.jsonl`.

| Input | Model score | Style score | Combined score | Diagnostic mapped guess |
|---|---:|---:|---:|---|
| Clearly AI: assistant-generated study advice | 0.7132 | 0.5146 | 0.6139 | unsure |
| Clearly human: Mark Twain narrative excerpt | 0.5516 | 0.5957 | 0.5736 | unsure |
| Formal human: Lincoln speech excerpt | 0.3267 | 0.3799 | 0.3533 | unsure |
| Lightly-edited AI: edited study advice | 0.6436 | 0.3934 | 0.5185 | unsure |

**Input provenance:** The human narrative is the opening four sentences of Chapter II of [Mark Twain's The Adventures of Tom Sawyer](https://www.gutenberg.org/files/74/74-h/74-h.htm). The formal human sample is the opening three sentences of [Lincoln's Second Inaugural Address](https://www.nps.gov/linc/learn/historyculture/lincoln-second-inaugural.htm). Both are public-domain human writing, but historical texts may have appeared in the model's training data and do not represent today's student writing. The AI passage was generated by the assistant for this test. The edited version changes “clear” to “simple,” replaces one sentence with a shorter version, and adds a personal aside. The assistant made these edits; this simulates light editing rather than testing a human editor.

**What surprised me:** The known-human Twain excerpt scored 0.5736, slightly above the midpoint. Both signals contributed: model 0.5516 and style 0.5957. Regular sentence lengths and repeated vocabulary can push the style heuristic upward even for genuine human writing. The formal-human sample scored lower on both signals (0.3267 and 0.3799), so formality alone did not cause an AI-like result in this case. These observations concern these excerpts only.

**Why edited AI matters:** Editing lowered the model score by 0.0696 and the style score by 0.1212, reducing the combined score from 0.6139 to 0.5185. The style signal was more sensitive to these changes: splitting a sentence changes length variation, and an added aside changes vocabulary variety. The known AI origin did not change. The broad unsure band avoids firm accusations for these human samples, but also leaves both known-AI examples unsure. Four samples do not establish accuracy.

**Logging:** Each successful submission now records `model_score`, `style_score`, and `combined_score` through `audit.log_decision(...)`, along with its timestamp, content ID, creator ID, guess, label, and status. The response carries both signal scores and the combined score as `confidence`. All four records were read back and matched to their responses. The route's `guess` and reader-facing `label` remain placeholders for Milestone 5; the mapped guesses in this table were computed separately for diagnosis.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | `0.00 <= score <= 0.20` | Our checks suggest this text was written by a person. This is an automated estimate. |
| unsure | `0.20 < score < 0.80` | Our checks cannot reliably determine how this text was written. |
| high-confidence AI | `0.80 <= score <= 1.00` | Our checks suggest this text may be AI-generated. This can be wrong. You can request a review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->


The unsure message describes the limits of the checks without accusing the writer. A wide unsure band aims to reduce false accusations, accepting that more AI writing may receive an unsure result. These are proposed ranges and messages, not implemented behavior.

### False-positive scenario

A student writing in a second language submits a paragraph they wrote themselves. They use familiar vocabulary and sentences of similar lengths. The model finds the wording predictable, and the style signal treats the regular structure and repetition as AI-like.

Suppose the hypothetical scores are `model_score = 0.90` and `style_score = 0.80`. The combined score is `(0.5 * 0.90) + (0.5 * 0.80) = 0.85`. This is an invented example, not a measured result or an 85% verified probability of AI authorship.

Because 0.85 exceeds the proposed 0.80 boundary, the writer receives `guess: "ai"` and: “Our checks suggest this text may be AI-generated. This can be wrong. You can request a review.” This is a false positive: real human writing triggered patterns the system associates with AI.

The service logs the original decision with status `decided` and returns its `content_id`. The writer sends that ID and an explanation to `POST /appeal`, such as: “I wrote this myself. I used simple sentences because I am still learning English.” The route verifies the submission exists, records the appeal, and changes the item's latest status to `under_review`. The original decision remains in the audit log.

The response confirms the appeal was recorded. It does not automatically clear the writer or promise a completed review; a process to resolve reviews still needs to be defined. Raising the AI boundary from the starter 0.65 to the configured 0.80 places scores such as 0.70 in unsure, but does not prevent this 0.85 mistake. I accept more uncertain results to reduce accusations and will test the boundaries on genuine human writing during calibration.

## Endpoint Contracts

These describe the planned implementation. Both endpoints accept a JSON object with `Content-Type: application/json` and return JSON. Unknown request fields are ignored. Required strings are trimmed before validation and use. Lengths count Python string characters after trimming, not bytes.

### POST /submit

**Request**

| Field | Type | Required | Validation and meaning |
|---|---|---|---|
| `text` | string | Yes | 20–10,000 characters and at least three model tokens. The writing to check. The model uses its configured initial token window; the style signal uses the full accepted text. |
| `creator_id` | string | Yes | 1–100 characters. Identifies the submitting creator; this does not authenticate them. |

**Success: HTTP 200**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | A new UUID identifying this submission. Resubmitting identical text creates a new ID. |
| `guess` | string | Exactly `human`, `unsure`, or `ai`, using the ranges in Label Variants. |
| `confidence` | number | Combined AI-likeness score from 0 to 1. Higher means more AI-like, not greater certainty in whichever label was selected. This is not a calibrated probability of authorship. |
| `label` | string | The exact reader-facing message from Label Variants. |
| `model_score` | number | Model AI-likeness score from 0 to 1. |
| `style_score` | number | Style AI-likeness score from 0 to 1. |

The decision is logged with status `decided`. The response's `confidence` value is stored as `combined_score` in the audit log.

### POST /appeal

**Request**

| Field | Type | Required | Validation and meaning |
|---|---|---|---|
| `content_id` | string | Yes | A non-empty ID matching an existing submission, exactly after trimming. |
| `reasoning` | string | Yes | 1–5,000 characters explaining why the writer disputes the decision. |

**Success: HTTP 200**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | The submission ID supplied in the request. |
| `status` | string | Always `under_review`. |
| `message` | string | Always “Your appeal has been recorded for review.” |

Any existing submission may be appealed, regardless of its original guess. A repeated valid appeal adds another appeal entry and returns HTTP 200. The creator ID is looked up from the original decision. This starter design does not authenticate the appellant. Appeals preserve the original decision and do not automatically rescore the text.

### Errors

| HTTP status | `error` value | When returned |
|---|---|---|
| 400 | `invalid_input` | Body is not a JSON object, fields are missing, types or lengths are invalid, or submission text has fewer than three model tokens. |
| 404 | `not_found` | An otherwise valid appeal names an ID with no original submission. |
| 503 | `detector_unavailable` | A valid submission cannot be scored because the local model cannot load. No successful decision is recorded. |

Error responses contain exactly two string fields: `error`, the code above, and `message`, a readable explanation. Validate request fields before model scoring or appeal lookup. For example:

```json
{
  "error": "invalid_input",
  "message": "The text field must be a string between 20 and 10000 characters after trimming."
}
```

Rate limiting belongs to a later unit and remains disabled for this design.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
