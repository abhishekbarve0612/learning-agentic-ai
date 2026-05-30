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
NOTES — Python / tooling odds & ends
═══════════════════════════════════════════════════════════

- repr() and the !r format spec do the same thing: show the raw/quoted
  representation of a string (useful for seeing whitespace, empty strings,
  hidden characters in debug output).
- str.ljust(n) pads a string with spaces up to width n — used it to align
  the columns in the specificity-ladder grid.