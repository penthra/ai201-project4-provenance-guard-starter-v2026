# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 16:34
- Auto-marked BROKE (5xx, crash, no response): **0**
- Reviewed: **46 HELD, 10 BROKE, 0 remaining**

Verdicts were reviewed against the same rules as the before run; see the
review policy below. All 56 outcomes have a verdict.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `25c31927-bf16-41eb-a1e4-2aba08782fe8` | unsure | 0.307 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `9eff8e35-2ab7-424b-9ee4-85a5e48c254b` | unsure | 0.361 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `7a1dc557-3d59-4030-8f14-21fea143b8c8` | unsure | 0.486 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `0c1e120e-8fff-4c81-80f0-cef17897076c` | unsure | 0.527 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `de809b55-ffdc-46c4-9bb3-57ef56b60fa7` | unsure | 0.277 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `4faf21ba-1259-4a84-9704-ad634a148b96` | unsure | 0.324 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `7c9eb5a7-9d31-48b2-9916-a8f63e092419` | unsure | 0.457 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `24b023bc-05dd-4bab-9be2-3a01f828b532` | unsure | 0.302 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `fd9ae47c-f4ba-4a6e-856f-7c671ae68a3c` | unsure | 0.502 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `1d73d2ea-abfe-449d-b1b6-6bf57bc1719d` | ai | 0.818 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `357f7db1-c6c2-4a17-967e-922c34e0b162` | unsure | 0.493 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `acf0c6cf-3c72-484d-a190-260c0806f8a3` | unsure | 0.617 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `45785e1e-5922-4578-893d-c6b1adc75966` | unsure | 0.616 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `12ade363-0277-46c1-a024-cbbb7399cc6c` | unsure | 0.619 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `bf1e1242-da54-4689-8318-47d3bb894120` | unsure | 0.675 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `697c46a6-11e5-4bb3-8a86-3e047717142c` | unsure | 0.622 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `548ffa94-8fde-4862-8b56-604a0797c35b` | unsure | 0.627 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `75a19c93-f306-4c7c-8c50-76b087d90d30` | unsure | 0.303 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `94ce61e6-eb32-4ba2-906a-956f371d97f6` | unsure | 0.332 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `8407b2b2-39f9-4821-832b-36b9404dee36` | unsure | 0.200 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f681eeeb-5a78-48c7-a781-d77e0f134d56` | unsure | 0.481 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `fb8967ee-84ba-4d94-86a1-3af4486ae9cb` | unsure | 0.436 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4f11ac17-f378-4f17-8129-71744b418856` | unsure | 0.461 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `838a6a80-4e39-4fba-bf56-f84cb3112ef9` | unsure | 0.465 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `6c3a7c4c-28ea-4860-a3bc-f5202f4a6ea6` | human | 0.125 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `8b8e5d94-97a7-4b85-9865-693afd313c6a` | unsure | 0.256 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `55bbcb6c-0b28-4899-884d-51b5dfae6f06` | unsure | 0.624 | HELD |
| MF06 | malformed | text is emoji only | 200 | `15f05be8-857e-45f6-a738-9f2d092e5e4f` | unsure | 0.748 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `c3f293d6-ceab-49d9-a634-3a7f6b227fa8` | unsure | 0.703 | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cbaff17a-0e56-4f14-9bc7-861f73e1aceb` | human | 0.139 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `57f0f8e0-1490-43c2-b4f5-7b4ecccbf35b` | human | 0.139 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `99e26c4b-8918-4cd1-b1ec-2c20662f7e62` | human | 0.139 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b51b257f-d38a-49df-915c-d8b33a6d9f56` | human | 0.139 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `012656de-ff1a-4463-805a-0b7300a2ea76` | human | 0.139 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1021dc83-3599-4f78-9eac-3ecda70f56e7` | human | 0.139 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `60368ee4-8fd4-47b7-bf7c-bcd0649b3bf8` | human | 0.139 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `44ca442f-1d25-4c28-b05a-4f33ab5e5af6` | human | 0.139 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 8 | 0 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 19 | 1 |
| `prompt_injection` | 6 | 6 | 0 |

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "25c31927-bf16-41eb-a1e4-2aba08782fe8",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.30670000000000003,
  "model_score": 0.1635,
  "style_score": 0.4499,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "9eff8e35-2ab7-424b-9ee4-85a5e48c254b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3613,
  "model_score": 0.5943,
  "style_score": 0.1283,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "7a1dc557-3d59-4030-8f14-21fea143b8c8",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.48605,
  "model_score": 0.6662,
  "style_score": 0.3059,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "0c1e120e-8fff-4c81-80f0-cef17897076c",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.52705,
  "model_score": 0.6114,
  "style_score": 0.4427,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "de809b55-ffdc-46c4-9bb3-57ef56b60fa7",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.27695,
  "model_score": 0.3212,
  "style_score": 0.2327,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "4faf21ba-1259-4a84-9704-ad634a148b96",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.32415,
  "model_score": 0.5727,
  "style_score": 0.0756,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "7c9eb5a7-9d31-48b2-9916-a8f63e092419",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.45675,
  "model_score": 0.5862,
  "style_score": 0.3273,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "24b023bc-05dd-4bab-9be2-3a01f828b532",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3019,
  "model_score": 0.2452,
  "style_score": 0.3586,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "fd9ae47c-f4ba-4a6e-856f-7c671ae68a3c",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.50175,
  "model_score": 0.7042,
  "style_score": 0.2993,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "1d73d2ea-abfe-449d-b1b6-6bf57bc1719d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8181499999999999,
  "model_score": 0.9792,
  "style_score": 0.6571,
  "label": "We think this text may have been generated by AI. This estimate can be wrong. You can request a review.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "357f7db1-c6c2-4a17-967e-922c34e0b162",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4928,
  "model_score": 0.6175,
  "style_score": 0.3681,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "acf0c6cf-3c72-484d-a190-260c0806f8a3",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.61685,
  "model_score": 0.7387,
  "style_score": 0.495,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "45785e1e-5922-4578-893d-c6b1adc75966",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.61565,
  "model_score": 0.8051,
  "style_score": 0.4262,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "12ade363-0277-46c1-a024-cbbb7399cc6c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6194999999999999,
  "model_score": 0.8329,
  "style_score": 0.4061,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "bf1e1242-da54-4689-8318-47d3bb894120",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6746,
  "model_score": 0.8005,
  "style_score": 0.5487,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "697c46a6-11e5-4bb3-8a86-3e047717142c",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6219,
  "model_score": 0.8814,
  "style_score": 0.3624,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "548ffa94-8fde-4862-8b56-604a0797c35b",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.62655,
  "model_score": 0.8816,
  "style_score": 0.3715,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "75a19c93-f306-4c7c-8c50-76b087d90d30",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.30289999999999995,
  "model_score": 0.3223,
  "style_score": 0.2835,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "94ce61e6-eb32-4ba2-906a-956f371d97f6",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.33225000000000005,
  "model_score": 0.4625,
  "style_score": 0.202,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "8407b2b2-39f9-4821-832b-36b9404dee36",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.20035,
  "model_score": 0.2044,
  "style_score": 0.1963,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "f681eeeb-5a78-48c7-a781-d77e0f134d56",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.48055000000000003,
  "model_score": 0.5943,
  "style_score": 0.3668,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "fb8967ee-84ba-4d94-86a1-3af4486ae9cb",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4357,
  "model_score": 0.4998,
  "style_score": 0.3716,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "4f11ac17-f378-4f17-8129-71744b418856",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.46055,
  "model_score": 0.6401,
  "style_score": 0.281,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "838a6a80-4e39-4fba-bf56-f84cb3112ef9",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.46465,
  "model_score": 0.5583,
  "style_score": 0.371,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "6c3a7c4c-28ea-4860-a3bc-f5202f4a6ea6",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.125,
  "model_score": 0.0,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "8b8e5d94-97a7-4b85-9865-693afd313c6a",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "55bbcb6c-0b28-4899-884d-51b5dfae6f06",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6238,
  "model_score": 0.9976,
  "style_score": 0.25,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "15f05be8-857e-45f6-a738-9f2d092e5e4f",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.7484500000000001,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c3f293d6-ceab-49d9-a634-3a7f6b227fa8",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "Our checks cannot reliably tell whether this text was written by a person or generated by AI.",
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "cbaff17a-0e56-4f14-9bc7-861f73e1aceb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "57f0f8e0-1490-43c2-b4f5-7b4ecccbf35b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "99e26c4b-8918-4cd1-b1ec-2c20662f7e62",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "b51b257f-d38a-49df-915c-d8b33a6d9f56",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "012656de-ff1a-4463-805a-0b7300a2ea76",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "1021dc83-3599-4f78-9eac-3ecda70f56e7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "60368ee4-8fd4-47b7-bf7c-bcd0649b3bf8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "44ca442f-1d25-4c28-b05a-4f33ab5e5af6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.13935,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this text was probably written by a person. This is an automated estimate and can be wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

## Review policy

Uses the same goal-based review policy as the before run. Evasions count as
BROKE when they avoid an AI label, including unsure. Human false-positive
samples count as HELD when not labeled AI. Prompt injection is judged by
requested overrides and output/log corruption; matching audit entries were
checked. Unsupported inputs may be rejected or receive unsure; MF03's human
label is BROKE. The first eight flood requests are allowed; the remaining
four must be rejected. The file has 12 flood rows, despite the target wording
saying 20. Every verdict matched the before run: 46 HELD, 10 BROKE.
