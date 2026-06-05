# LEARNINGS.md

Running log of what I've learned, broken, and figured out.
Two kinds of entries:
  BUGS  — what broke → root cause → the fix
  NOTES — concepts I worked out or want to remember

═══════════════════════════════════════════════════════════
BUGS
═══════════════════════════════════════════════════════════

[Day 1]
  OpenAI client didn't work with my wrapper
  → broke:  AttributeError: 'OpenAI' object has no attribute 'messages'
  → cause:  the wrapper is written for the Anthropic SDK. OpenAI's SDK
            uses a different method (client.chat.completions.create),
            not client.messages.create — the two SDKs aren't drop-in
            compatible.
  → fix:    used the Anthropic client. (If I ever want OpenAI, I'd need
            a separate code path using its own method + message format.)

  temperature=1.5 on Haiku returned a 400 error
  → cause:  the valid temperature range is model-dependent. Haiku here
            accepts 0–1.0; values above that are rejected.
  → fix:    used 1.0. Didn't need >1.0 to see the effect anyway.
  → bonus:  on Opus 4.7/4.8, temperature/top_p/top_k are rejected
            entirely (any non-default value = 400). Omit them and steer
            with prompting instead. So my llm.py only sends temperature
            when it's explicitly set, to stay compatible across models.

  Strict structured output rejected my schema
  → broke:  400 "output_config.format.schema: For 'object' type,
            'additionalProperties' must be explicitly set to false"
  → cause:  strict JSON-schema mode requires every object to declare
            additionalProperties:false (i.e. "no extra fields allowed").
            Pydantic's model_json_schema() doesn't emit that by default.
  → fix:    add model_config = ConfigDict(extra="forbid") to the model.
            It makes Pydantic reject unknown fields AND emit
            additionalProperties:false in the schema.
            (Fallback for nested models: post-process the schema dict and
            set additionalProperties=False on each object in $defs too.)
  → note:   .parse() handles this automatically — a concrete reason to
            prefer it over hand-built output_config schemas.

  Manual JSON extraction failed with json.loads char 0
  → broke:  JSONDecodeError "Expecting value: line 1 column 1 (char 0)"
            on all 7 inputs.
  → cause:  the model wrapped its JSON in markdown code fences
            (```json ... ```). The JSON inside was perfect; the backticks
            at char 0 aren't valid JSON, so json.loads choked.
  → fix:    (1) prompt: explicitly forbid fences, instruction placed LAST
            ("ONLY raw JSON, no ```json blocks, no backticks").
            (2) defensive: strip fences before parsing (strip_fences()).
            In production do BOTH — "I told it not to" is not a guarantee;
            one stray fence in 50 calls crashes the pipeline.
  → meta:   "Expecting value ... char 0" = the string is empty OR starts
            with a non-JSON char. Most common cause = code fences.
  → debug lesson: I PRINTED the raw value and it instantly showed the
            fence. My (and Claude's) initial guess — empty text / wrong
            content block — was WRONG. Print the real value, don't theorize.


═══════════════════════════════════════════════════════════
NOTES — Temperature & determinism
═══════════════════════════════════════════════════════════

- Temperature is a sharpening/flattening dial on the model's probability
  distribution over the next token. It is NOT a "randomness" dial I can
  rely on.
    • temp 0  → greedy, picks the single most likely token → most
                predictable / most repetitive.
    • temp 1  → samples in proportion to real probabilities → more varied.
- I had this backwards at first: I expected temp 0 to vary. It's the
  opposite — low temp = LESS variety. Confirmed with the ocean-sentence
  drill (1/5 distinct at temp 0, 3/5 at temp 1).
- Output variety needs TWO things at once:
    (1) a high-enough temperature, AND
    (2) a prompt the model isn't already "decided" about.
  A low-entropy prompt ("name a random fruit" → always "mango") shows
  little variety even at temp 1, because there's almost no competing
  probability mass to surface.
- temp 0 is "more predictable," NOT "guaranteed identical." Floating-point
  and infrastructure differences mean even temp 0 can vary run to run.
- Practical rule: low temp for extraction/classification (want stable,
  predictable output); higher temp for brainstorming/creative drafts.

═══════════════════════════════════════════════════════════
NOTES — Tokens, cost, limits
═══════════════════════════════════════════════════════════

- Read token counts from msg.usage (input_tokens / output_tokens), never
  estimate from word/char count — tokens ≠ words.
- Pricing is per token, input and output priced separately; output costs
  much more than input. (This is why later cost-cutting fights to keep
  OUTPUT short while input can be padded/cached cheaply.)
- max_tokens is a HARD cap on output. It cuts off mid-word/mid-sentence if
  hit — it does NOT shape length. The model can also stop earlier on its
  own (stop_reason "end_turn") if the answer is complete for the context.

═══════════════════════════════════════════════════════════
NOTES — Prompting (Anthropic tutorial ch. 1–7)
═══════════════════════════════════════════════════════════

- More specific / descriptive prompts → better, more consistent responses.
  Saw this concretely in the specificity-ladder grid: vague v1 rambled and
  invented categories; explicit v4 (allowed list + definitions + few-shot +
  "reply with ONLY one word") nailed even the empty/emoji/no-content inputs
  as "unknown".
- The loop that IS prompt engineering: change one thing → re-run → read the
  diff. Don't improve by vibes; measure.
- Few-shot (giving 1–3 input→output examples) significantly improves output
  format consistency and determinism. The model pattern-matches hard on the
  examples.
- Asking the model to think step by step (chain-of-thought) before answering
  improves answer quality on anything needing reasoning.
- Separate instructions from the data being processed (delimiters / XML
  tags) so the model never confuses "the thing to classify" with "the
  command." (This is also the seed of prompt-injection defense later.)
- Why preceding text steers what comes next: the model predicts the most
  probable continuation given everything so far. So earlier tokens bias
  later ones — if it generated sentence 2, sentence 3 is pulled toward
  sentence 2 more than sentence 1. This is exactly WHY prefill, system
  prompts, and few-shot examples work: I'm front-loading the context that
  the model will then continue in line with.

═══════════════════════════════════════════════════════════
NOTES — Output control: stop_sequences + prefill 
═══════════════════════════════════════════════════════════

- stop_sequences: pass a closing delimiter (e.g. "</answer>") and the API
  halts generation the instant the model emits it. Cuts trailing chit-chat
  ("hope that helps!"), which saves output tokens and latency.
    • the stop sequence itself is NOT included in the returned text.
    • stop_reason comes back as "stop_sequence" (vs "end_turn" when the
      model decided it was done) — useful for knowing which happened.
    • only saves tokens when the model WOULD have kept talking; does
      nothing if it'd stop cleanly anyway.

- Prefill: I can start the assistant's turn for it by putting text in an
  assistant-role message. The model continues FROM that text (and echoes it
  back at the start of the response). This steers format AND kills the
  opening preamble — it can't say "Sure! Here's..." if I've already started
  its turn mid-thought.

- The sandwich (my own derivation — works cleanly):
    prefill assistant turn with the OPENING tag  → kills preamble
    set the CLOSING tag as a stop sequence        → kills postamble
  Result: the entire response IS the content — nothing to parse off either
  end. (Opening tag = I wrote it so I have it; closing tag = stop sequence
  eats it so it's never returned.)
    • Name the tag for the CONTENT (<answer>, <category>, <json>) — do NOT
      use <assistant>, it collides with the API role name.
    • Caveat: prefilling the answer tag immediately denies the model any
      thinking space. Fine for simple classification (faster, cleaner).
      For tasks needing reasoning, let it think first, then wrap only the
      final answer. (ch.05 formatting vs ch.06 step-by-step trade off here.)




═══════════════════════════════════════════════════════════
NOTES — Structured output
═══════════════════════════════════════════════════════════

- Structured output = "make the model emit data of a guaranteed SHAPE."
  Universal concept across providers; the API differs per provider.
- Two strengths:
    (1) prompt-and-validate — ask for JSON, validate after. Works
        everywhere, guarantees nothing. (Manual extraction — hit the fence bug.)
    (2) schema-enforced / constrained decoding — provider guarantees the
        shape by restricting which tokens can be generated. Stronger,
        provider-specific. (Structured extraction with output format / .parse().)
- HOW constrained decoding works: at each generation step the model has a
  probability distribution over next tokens. Constrained decoding MASKS
  (zeroes) any token that would break the schema, so the model can only
  sample legal tokens. Output is correct BY CONSTRUCTION — a malformed
  token was never possible.

- Does it cost extra tokens / retry internally? NO.
    • It's ONE pass, prevention at sampling time — NOT a detect-then-resend
      loop. No internal evaluator, no extra round trips, no retry tokens.
    • Output token count ≈ same as plain prompting (often slightly LESS,
      since the model can't ramble/add preamble).
    • Provider-side cost: compiling the schema into a "grammar," which is
      why they cache it (~24h). That's their compute, not my output tokens.
    • Contrast: the manual retry loop (Day 4) makes MULTIPLE full calls —
      pays input+output tokens PER attempt. Correct but multiplies cost.

- IMPORTANT LIMIT: structured output guarantees SHAPE, not CONTENT.
    • It ensures valid JSON, right fields, right types, valid enums.
    • It does NOT ensure the VALUE is correct — model can emit a
      wrong-but-validly-typed value (live example: it read "1499" as
      amount 14.99 once). Catching that is evals' job, not structured
      output's.


═══════════════════════════════════════════════════════════
NOTES — SDK: .parse()
═══════════════════════════════════════════════════════════

- Anthropic's SDK has .parse() too (NOT OpenAI-only). Pass the Pydantic
  model, get a typed object back. Cleaner than manual
  schema→call→json.loads→validate, and it handles strict-mode schema
  details (like additionalProperties) for me.
- Variable schema per scenario: pass the schema/model as a wrapper param;
  each call site supplies whichever it needs; schema=None default for
  plain-text calls. Same wrapper, different schema per call.
- Learn the manual pipeline FIRST (so failures are debuggable — see the
  fence bug), THEN use .parse() in real code. Manual pattern is portable
  across providers; .parse() is per-SDK convenience sugar.
- Caveat I keep hitting: exact signatures/param names/return shape are
  SDK-version-specific. Confirm from the doc, don't trust a remembered
  snippet.


═══════════════════════════════════════════════════════════
NOTES — Schema constraints: what's enforced vs not
═══════════════════════════════════════════════════════════

- Pydantic supports rich constraints (Field(ge=, le=, pattern=, etc.),
  custom @field_validator). But not all get enforced during generation.
- Enforced during generation (grammar can express these):
    types, required fields, enum/Literal sets, nesting/array structure.
- NOT enforced during generation (caught only by post-validation):
    numeric ranges (ge/le), regex patterns, length limits, cross-field
    rules, custom validators.
- What happens to an unsupported constraint: it gets DEMOTED into the
  field's text DESCRIPTION (a hint, e.g. "Must be at least 100") and
  code still validates it after. So it moves from "guaranteed by sampling"
  to "checked by Pydantic."
- Safe stance regardless of provider/version: assume the model is only
  ENCOURAGED toward my constraints; MY validation in code is what makes
  them true.

═══════════════════════════════════════════════════════════
NOTES — Layers: structured output + validation + retry
═══════════════════════════════════════════════════════════

- These are LAYERS, not competitors:
    • structured output → guarantees shape (free, one pass).
    • Pydantic validation → enforces my content rules (raises on violation).
    • retry loop → catches the raise, feeds the error back, asks
      for a corrected attempt, caps attempts. THIS IS ALL MY CODE.
- Structured output has NO awareness of my validation. When my Pydantic
  rules fail, NOTHING auto-retries. The retry decision, the error-feedback
  message, the attempt cap, and the give-up behavior are all my job.
- On exhausting retries, I choose the failure behavior (app logic):
    raise/fail loud (financial, medical) · return safe default (pipeline
    must continue) · flag for human review (production edge cases).


═══════════════════════════════════════════════════════════
NOTES — Provider portability
═══════════════════════════════════════════════════════════

- Structured output is NOT Anthropic-only. Rough landscape:
    • OpenAI: most mature — "Structured Outputs" (response_format), plus an
      older looser "JSON mode" (valid JSON, NOT schema-guaranteed).
    • Gemini: "controlled generation" (response_schema / response_mime_type).
    • DeepSeek / OpenAI-compatible servers: usually JSON mode, schema
      enforcement uneven.
    • Open source: Outlines, Guidance, llama.cpp grammars — where rigorous
      constrained decoding was pioneered; hosted features productize this.
- CONCEPT is portable ("define schema, validate output"); the exact API is
  NOT (output_config vs response_format vs response_schema). Hide the
  difference behind my own wrapper (llm.py) — same pattern I already use.
- Connection: tool calling uses the SAME mechanism — model emits
  structured args matching a tool's schema. Structured output and tool use
  are one capability wearing two hats.

═══════════════════════════════════════════════════════════
NOTES — Python / tooling odds & ends
═══════════════════════════════════════════════════════════

- repr() and the !r format spec do the same thing: show the raw/quoted
  representation of a string (useful for seeing whitespace, empty strings,
  hidden characters in debug output).
- str.ljust(n) pads a string with spaces up to width n — used it to align
  the columns in the specificity-ladder grid.



═══════════════════════════════════════════════════════════
NOTES — Compliance terms (came up in docs)
═══════════════════════════════════════════════════════════

- PHI = Protected Health Information (identifiable health data).
- HIPAA = US law governing how PHI must be protected. "HIPAA eligible" =
  the service can be used compliantly for PHI (usually under an agreement).
- ZDR = Zero Data Retention — provider doesn't store prompts/responses
  after the request completes.
- Gotcha: with structured outputs, prompts/responses are under ZDR, BUT the
  JSON SCHEMA is cached ~24h and does NOT get the same protection. So never
  put PHI in schema field names, enum values, or regex patterns — only in
  the message content (which is protected).