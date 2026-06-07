
from dataclasses import dataclass
from config import K, SAMPLE_DOCS
from day5.orchestrator.switchboard import SwitchBoard
from day5.schema import Plan


def selftest() -> int:
    print("== Switchboard selftest (no API) ==")
 
    @dataclass
    class _Doc:
        page_content: str
        metadata:     dict
 
    corpus = [_Doc(text, {"source": src}) for text, src in SAMPLE_DOCS]
 
    def _kw(q: str, k: int = K) -> list[_Doc]:
        words = set(q.lower().split())
        return sorted(corpus,
                      key=lambda d: len(words & set(d.page_content.lower().split())),
                      reverse=True)[:k]
 
    class _FakeRetriever:
        def invoke(self, q: str) -> list: return _kw(q)
        def batch(self, qs: list) -> list: return [_kw(q) for q in qs]
 
    def _rule_plan(q: str) -> Plan:
        ql    = q.lower()
        words = set(ql.replace(",","").replace("?","").replace("!","").split())
        if words & {"hi", "hello", "hey", "thanks"}:             return Plan("smalltalk", None, "greeting")
        if any(w in ql for w in ("increase", "divided", " + ")): return Plan("math",      None, "arithmetic")
        if "why" in ql:                                           return Plan("docs", "step_back", "causal")
        if " and " in ql or ql.count(",") >= 1:                  return Plan("docs", "decompose",  "multi-intent")
        if "how does" in ql or "overview" in ql:                 return Plan("docs", "hyde",       "exploratory")
        return Plan("docs", "simple", "single lookup")
 
    def _split(q: str) -> list[str]:
        return [s.strip() for s in q.replace(" and ", ",").split(",") if s.strip()][:5]
 
    sb = SwitchBoard(
        planner       = _rule_plan,
        retriever     = _FakeRetriever(),
        decompose     = _split,
        step_back_gen = lambda q: "What are general OCR pipeline best practices?",
        hyde_retrieve = lambda q: _kw(q),
        answer        = lambda ctx, q: "[answer]",
        answer_dual   = lambda n, sb_ctx, q: "[dual answer]",
        math          = lambda q: "[math]",
        smalltalk     = lambda q: "[hi]",
    )
 
    r = sb.route("Hello!")
    assert r.trace.plan.route == "smalltalk" and r.trace.searches == 0
 
    r = sb.route("Who wrote the audit, what was the OCR rate, and the budget?")
    assert r.trace.plan.strategy == "decompose"
    assert len(r.trace.sub_questions) >= 2
    assert r.trace.searches == len(r.trace.sub_questions)
    assert r.trace.kept >= 1
 
    r = sb.route("Why did the OCR failure rate spike for European branches?")
    assert r.trace.plan.strategy == "step_back"
    assert r.trace.step_back_query is not None and r.trace.searches == 2
 
    r = sb.route("How does this company handle remote work?")
    assert r.trace.plan.strategy == "hyde"
 
    print("  all four routing paths + traces: PASS")
    r = sb.route("Who wrote the audit, what was the OCR rate, and the budget?")
    print("\nSample receipt (decompose):")
    print("\n".join("  " + ln for ln in r.trace.render().splitlines()))
    print("\nSELFTEST PASSED")
    return 0