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

1. The writer sends `text` and `creator_id` as JSON to `POST /submit` in `app.py`. This gives the service the writing and identifies the submitting creator.
2. The route validates the input and assigns a unique `content_id` to a valid submission. Validation rejects unsuitable requests; the ID connects this particular decision to a later appeal.
3. `detector.model_signal(text)` measures predictability with a local language model. It adds `model_score`, from 0 to 1, with higher values meaning more AI-like.
4. `stylometry.style_signal(text)` measures sentence-length variation, vocabulary variety, and punctuation density. It adds a separate `style_score`, also from 0 to 1 with higher values meaning more AI-like.
5. `scoring.combine_signals(model_score, style_score)` combines the signals into one score using the equal weights below.
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

The raw style measurements are:

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

**Logging:** Each successful submission now records `model_score`, `style_score`, and `combined_score` through `audit.log_decision(...)`, along with its timestamp, content ID, creator ID, guess, label, and status. The response carries both signal scores and the combined score as `confidence`. All four records were read back and matched to their responses. At the time of that calibration run, the route's `guess` and reader-facing `label` were placeholders, so the mapped guesses in this table were computed separately for diagnosis. The route now calls `scoring.py::score_to_label` and returns and logs the actual guess and message.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| human | `0.00 <= score <= 0.20` | We think this text was probably written by a person. This is an automated estimate and can be wrong. |
| unsure | `0.20 < score < 0.80` | Our checks cannot reliably tell whether this text was written by a person or generated by AI. |
| ai | `0.80 <= score <= 1.00` | We think this text may have been generated by AI. This estimate can be wrong. You can request a review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->


The unsure message describes the limits of the checks without accusing the writer. A wide unsure band aims to reduce false accusations, accepting that more AI writing may receive an unsure result. The ranges match `HUMAN_THRESHOLD = 0.20` and `AI_THRESHOLD = 0.80` in `config.py`. These exact messages are implemented in `scoring.py::score_to_label`. `/submit` uses the combined score to select the guess and message, returns both, and saves both in the audit record.

### Verified label reachability

Ran `python verify_labels.py` on October 30, 2026 with the real local detector through Flask's `/submit` test client. All three synthetic style probes reached their expected labels, and each response matched its saved audit entry read back through `/log`. Full texts, content IDs, and responses are in [results/label_coverage.json](results/label_coverage.json). These examples demonstrate reachability, not authorship accuracy.

| Submitted text | Model score | Style score | Combined score | Returned guess |
|---|---:|---:|---:|---|
| Plain conventional prose | 0.9404 | 0.5295 | 0.73495 | unsure |
| Varied narrative | 0.2297 | 0.0286 | 0.12915 | human |
| Repeated unusual vocabulary | 0.8935 | 0.8125 | 0.85300 | ai |

`scoring.label_ranges()` now prints explicit inclusive and exclusive boundaries: `human: 0.00 <= score <= 0.20`, `unsure: 0.20 < score < 0.80`, and `ai: 0.80 <= score <= 1.00`. Exact boundary and neighboring-float checks passed, and a scan of 10,001 scores from 0 to 1 found no missing labels. No threshold changes were needed for this reachability check. Re-running `verify_labels.py` appends three new decisions to the audit log.


### False-positive scenario

A student writing in a second language submits a paragraph they wrote themselves. They use familiar vocabulary and sentences of similar lengths. The model finds the wording predictable, and the style signal treats the regular structure and repetition as AI-like.

Suppose the hypothetical scores are `model_score = 0.90` and `style_score = 0.80`. The combined score is `(0.5 * 0.90) + (0.5 * 0.80) = 0.85`. This is an invented example, not a measured result or an 85% verified probability of AI authorship.

Because 0.85 exceeds the 0.80 boundary, the writer receives `guess: "ai"`. This is a false positive: real human writing triggered patterns the system associates with AI.

The service logs the original decision with status `decided` and returns its `content_id`. The writer sends that ID and an explanation to `POST /appeal`, such as: “I wrote this myself. I used simple sentences because I am still learning English.” The route verifies the submission exists, records the appeal, and changes the item's latest status to `under_review`. The original decision remains in the audit log.

The response confirms the appeal was recorded. It does not automatically clear the writer or promise a completed review; a process to resolve reviews still needs to be defined. Raising the AI boundary from the starter 0.65 to the configured 0.80 places scores such as 0.70 in unsure, but does not prevent this 0.85 mistake. I accept more uncertain results to reduce accusations.

## Endpoint Contracts

Both endpoints accept a JSON object with `Content-Type: application/json` and return JSON. Unknown request fields are ignored. Required strings are trimmed before validation and use. Lengths count Python string characters after trimming, not bytes.

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

The appeal and log checks below were run with Windows `curl.exe` on October 30, 2026 against the updated app on port 5057. That port was used for this verification so an existing server on port 5000 could keep running. Normal `python app.py` startup still uses port 5000.

**An earlier submission**

This real submission came from `python verify_labels.py`, which sent the following JSON through Flask's `/submit` test client. Its saved content ID was reused for the appeal; no new submission was needed.

`POST /submit` request:

```json
{
  "text": "The xylophonic zephyr perplexes the quincunx. The quincuncial zephyr perplexes the syzygy. The syzygetic zephyr perplexes the xylophone. The xylophonic zephyr perplexes the quincunx.",
  "creator_id": "label-coverage-check"
}
```

Actual response: **HTTP 200**

```json
{
  "confidence": 0.853,
  "content_id": "6d406b50-c613-4f88-8cda-dde317ecc65d",
  "guess": "ai",
  "label": "We think this text may have been generated by AI. This estimate can be wrong. You can request a review.",
  "model_score": 0.8935,
  "style_score": 0.8125
}
```

**An appeal**

The file `results/appeal_request.json` contains:

```json
{
  "content_id": "6d406b50-c613-4f88-8cda-dde317ecc65d",
  "reasoning": "This is a calibration appeal. Please review the AI-like label and the limitations of the two signals."
}
```

Executed from the repository directory in Windows, using a JSON file to avoid PowerShell quoting problems:

```powershell
curl.exe --silent --show-error -i http://127.0.0.1:5057/appeal -H "Content-Type: application/json" --data-binary "@results/appeal_request.json"
```

Actual response: **HTTP/1.1 200 OK**

```json
{
  "content_id": "6d406b50-c613-4f88-8cda-dde317ecc65d",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```powershell
curl.exe --silent --show-error -i "http://127.0.0.1:5057/log?limit=2"
```

Actual response: **HTTP/1.1 200 OK** (JSON formatted for readability):

```json
{
  "count": 2,
  "entries": [
    {
      "timestamp": "2026-10-30T20:27:26+00:00",
      "content_id": "6d406b50-c613-4f88-8cda-dde317ecc65d",
      "creator_id": "label-coverage-check",
      "guess": "ai",
      "model_score": 0.8935,
      "style_score": 0.8125,
      "combined_score": 0.853,
      "label": "We think this text may have been generated by AI. This estimate can be wrong. You can request a review.",
      "status": "decided"
    },
    {
      "timestamp": "2026-10-30T20:31:03+00:00",
      "content_id": "6d406b50-c613-4f88-8cda-dde317ecc65d",
      "creator_id": "label-coverage-check",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "This is a calibration appeal. Please review the AI-like label and the limitations of the two signals."
    }
  ]
}
```

Both entries reference the same content ID. The original decision remains `decided`, and the newer appeal entry makes the item's latest status `under_review`. The writer's reasoning and original creator ID are saved with the appeal. This records a request for review; it does not rescore the text or reverse the decision.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked AI to help implement the API endpoints in the corresponding project files, following the Unit 7 requirements.
- *What came back:* AI helped write the `/submit` and `/appeal` routes in `app.py` and connect them to the signal, scoring, and audit functions.
- *What I changed:* I gave follow-up instructions to guide the implementation toward the required behavior and response fields.

**Moment 2**

- *What I asked for:* I asked AI to help investigate errors that appeared while calling the API.
- *What came back:* AI explained the error messages and suggested changes to the relevant code or request commands.
- *What I changed:* I monitored the API call logs and error messages, then gave AI further instructions to address the problems I observed.

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

Run recorded on November 4, 2026 at 19:28 America/New_York by
`run_attacks.py::main`, calling `app.py::submit`.
[Full results and per-attack explanations](results/attack_run_2026-11-04_1928.md).

**56 attacks: 46 HELD, 10 BROKE.** No request crashed or returned a 5xx.
The thresholds were human <= 0.20 and AI >= 0.80, with equal signal weights.
For evasion, avoiding the AI label counts as BROKE, including `unsure`;
this does not mean the text was certified human. For false-positive attacks,
`unsure` counts as HELD because the human writer was not accused of using AI.
Prompt-injection verdicts assess the requested override or corruption.
Malformed inputs count as HELD when rejected or handled with safe abstention;
MF03 is BROKE because insufficient meaningful text received a human label.

The flood's first eight requests were within the configured allowance and
therefore HELD; the next four correctly returned 429. There were 12 flood
rows in this file, despite their target description saying 20. This run does
not replace the separate Milestone 1 flood test in **Rate Limiting**.

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 8 | 0 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 19 | 1 |
| `prompt_injection` | 6 | 6 | 0 |

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b91d31b5-cbc4-44db-b61e-478c076b44a0` | unsure | 0.324 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e195b24c-e458-4d8e-9c33-b27525f42465` | unsure | 0.379 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `54834d76-0663-4794-9912-f81c2fe5dbf7` | unsure | 0.512 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `656b905a-2e40-45ca-a81d-275d0ba6a677` | unsure | 0.544 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `1c970498-0d29-4c6a-9571-2c56b6a8235a` | unsure | 0.300 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `abd3b0ba-b488-4bb6-a516-6e01b83dfeda` | unsure | 0.349 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `d1abdb34-5f7b-4807-97ee-7f019fb51f8e` | unsure | 0.475 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `5bbfbaba-f310-44ef-9ecd-652bb038055e` | unsure | 0.302 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `a70f8ed2-3ec7-4427-a54b-56f6098e7f69` | unsure | 0.524 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0c688ed4-cf78-46a8-af11-36bec7570459` | ai | 0.811 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `ce980cd2-dc93-46b5-bce3-ad851821a14d` | unsure | 0.517 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `e8672759-c5cf-49a8-ab28-32810fa39d90` | unsure | 0.632 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `4d25186d-1ee2-4253-a160-6bf005e62f72` | unsure | 0.640 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d09bdf04-6a26-4d7a-a1a0-e0e09e57106b` | unsure | 0.623 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `401cde46-3f30-42f8-8206-6767e92a9b8e` | unsure | 0.685 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `1d3d2f64-27fd-4e13-8fa6-dd6d42de8a74` | unsure | 0.627 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `0adb21fe-918a-469a-a0bf-3bc4903fe6ee` | unsure | 0.644 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `7e69075a-2ca9-48ac-a5dc-36562b0852e1` | unsure | 0.303 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `a13de629-c343-4b48-9dbd-0893a4ffb3f2` | unsure | 0.332 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e4024c36-d993-4cc6-a3d2-317bccd2958f` | unsure | 0.200 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `675ca07c-811b-49e6-8383-9ea099e0f46a` | unsure | 0.484 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `a310e19e-51f4-4a55-9290-40faecd79541` | unsure | 0.435 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `6b8a525c-cced-4c7c-a81d-a73b0042bfc3` | unsure | 0.461 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `95e258e8-df27-4af7-860e-17f31cfd7a0c` | unsure | 0.491 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `7a9c7f96-b000-4f67-858d-2f6af9d5f44d` | human | 0.125 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `3dd0a97f-2488-42d5-b5db-e604aeff5654` | unsure | 0.256 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `61b3d35b-f3d0-48a7-851f-bcdda03dbd57` | unsure | 0.624 | HELD |
| MF06 | malformed | text is emoji only | 200 | `a68a63a2-c3c9-43af-8c64-6df2e133aa09` | unsure | 0.748 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `4f76d9a3-cb8f-475c-9441-095b934eb95c` | unsure | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `51244ecf-4b0e-4c08-85da-ac1bf507f831` | human | 0.139 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ae469e89-b745-4399-afb2-e00bce924eae` | human | 0.139 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `47053ea7-141f-4990-8168-8e096dc10e7d` | human | 0.139 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a630df87-5feb-4c97-8767-91c221128edf` | human | 0.139 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d0c7cf0c-87e5-4d45-a85b-9f2125ceacba` | human | 0.139 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `694ebae8-c4e0-43d9-b47f-f5abf700a9c5` | human | 0.139 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dba60c94-a0d6-4009-8f32-ae44ccbb8175` | human | 0.139 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2b309337-d072-4e5f-8efb-f3cddc43616e` | human | 0.139 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Ten audit log entries from the run**

These are original entries from `logs/audit.jsonl`, matched to the run by
content ID. Their timestamps use UTC, so the November 4 evening run appears
as November 5 in these entries. In order, they show:

- EV01: typo-based evasion; low model score and an unsure result.
- EV06: uneven sentence lengths; style score 0.125 pulls down the average.
- EV09: mixed human/AI text; disagreement between the signals.
- FP03: careful non-native English writing; model score above 0.80, final label unsure.
- FP05: human technical documentation; the highest combined score among the human samples.
- MF03: control-character input incorrectly receives a definite human label.
- MF06: emoji-only input; model score 0.9969, final label unsure.
- MF07: Arabic writing; high model score exposes a language-coverage concern, while the final label abstains.
- PI05: attempted audit-log injection; the recorded scores and fields remain intact.
- A flood rejection: the ninth through twelfth requests returned 429; this is one of their rejection entries. It has no decision scores because scoring did not run.

```json
[
  {
    "timestamp": "2026-11-05T00:28:40+00:00",
    "content_id": "b91d31b5-cbc4-44db-b61e-478c076b44a0",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "model_score": 0.1635,
    "style_score": 0.4843,
    "combined_score": 0.3239,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:41+00:00",
    "content_id": "abd3b0ba-b488-4bb6-a516-6e01b83dfeda",
    "creator_id": "attacker_EV06",
    "guess": "unsure",
    "model_score": 0.5727,
    "style_score": 0.125,
    "combined_score": 0.34885,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:42+00:00",
    "content_id": "a70f8ed2-3ec7-4427-a54b-56f6098e7f69",
    "creator_id": "attacker_EV09",
    "guess": "unsure",
    "model_score": 0.7042,
    "style_score": 0.3428,
    "combined_score": 0.5235000000000001,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:42+00:00",
    "content_id": "4d25186d-1ee2-4253-a160-6bf005e62f72",
    "creator_id": "attacker_FP03",
    "guess": "unsure",
    "model_score": 0.8051,
    "style_score": 0.4745,
    "combined_score": 0.6398,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:43+00:00",
    "content_id": "401cde46-3f30-42f8-8206-6767e92a9b8e",
    "creator_id": "attacker_FP05",
    "guess": "unsure",
    "model_score": 0.8005,
    "style_score": 0.5687,
    "combined_score": 0.6846,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:44+00:00",
    "content_id": "7a9c7f96-b000-4f67-858d-2f6af9d5f44d",
    "creator_id": "attacker_MF03",
    "guess": "human",
    "model_score": 0.0,
    "style_score": 0.25,
    "combined_score": 0.125,
    "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:45+00:00",
    "content_id": "a68a63a2-c3c9-43af-8c64-6df2e133aa09",
    "creator_id": "attacker_MF06",
    "guess": "unsure",
    "model_score": 0.9969,
    "style_score": 0.5,
    "combined_score": 0.7484500000000001,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:45+00:00",
    "content_id": "4f76d9a3-cb8f-475c-9441-095b934eb95c",
    "creator_id": "attacker_MF07",
    "guess": "unsure",
    "model_score": 0.9064,
    "style_score": 0.5,
    "combined_score": 0.7032,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:44+00:00",
    "content_id": "6b8a525c-cced-4c7c-a81d-a73b0042bfc3",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "model_score": 0.6401,
    "style_score": 0.281,
    "combined_score": 0.46055,
    "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T00:28:46+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "8 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP05, the human-written technical documentation, was the most concerning
result for an affected writer: it received the highest combined score among
the eight human samples, 0.6846. The model signal scored it 0.8005 and the
style signal 0.5687. Clear procedural writing was treated as evidence of AI
because predictable language can also be normal human technical prose.
The equal-weight average and 0.80 AI threshold kept the final label at
`unsure`, so this was a near miss, not an actual AI accusation. None of the
eight human samples received an AI label in this run. I would not present
the score as a calibrated probability that the writer used AI.

Among attacks marked BROKE, MF03 was the clearest unjustified authorship
decision: control-character input containing little meaningful prose was
labeled human at 0.125. This shows the route needs stronger checks for
scorable text, or an explicit abstention for unsupported input. Nine of ten
evasion inputs also avoided the AI label. Without unmodified baseline
submissions, this run alone cannot show how much each edit changed its score.

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
