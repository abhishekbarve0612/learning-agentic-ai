from dataclasses import dataclass, field
from typing import Literal, Optional
from pydantic import BaseModel, Field


class QueryPlan(BaseModel):
    route: Literal['docs', 'math', 'smalltalk'] = Field(...)
    strategy: Literal['simple', 'decompose', 'step_back', 'hyde'] = Field(
        "simple",
        description=(
            "simple: one lookup. decompose: multiple distinct intents. "
            "step_back: causal/'why' question. hyde: broad/exploratory. "
            "NEVER use hyde for an exact number, name, or date."
        )
    )
    reasoning: str = Field(..., description="One sentence explaining the choice.")


@dataclass
class Plan:
    route: str          # docs | math | smalltalk
    strategy: Optional[str]       # simple | decompose | step_back | hyde
    reasoning: str


@dataclass
class Trace:
    question:             str
    plan:                 Plan
    sub_questions:         list[str]      = field(default_factory=list)
    step_back_query:      str            = None
    hyde_excerpt:         str            = None
    candidates:           int            = 0                            # total chunjks retrieved before fusion / cutoff
    kept:                 int            = 0
    top_sources:          list[str]      = field(default_factory=list)
    llm_calls:            int            = 0
    searches:             int            = 0

    def render(self) -> str:

        p = self.plan

        out = [
            "-- ROUTING RECEIPT " + "_" * 40,
            f"  route        {p.route}",
            f"  strategy     {p.strategy if p.route == 'docs' else '-'}",
            f"  reasoning    {p.reasoning[:80]}",
        ]

        if self.sub_questions:
            out.append("  sub-question     ")
            out += [f"   {i}. {q} " for i, q in enumerate(self.sub_questions, 1)]
        
        if self.step_back_query:
            out.append(f"   step-back            {self.step_back_query}")

        if self.hyde_excerpt:
            out.append(f"   hyde-dooc           {self.hyde_excerpt[:70]}....")

        if self.candidates:
            srcs = ", ".join(self.top_sources[:4])
            out.append(f"   retrieval:      {self.candidates}   candidates -> kept  {self.kept} [{srcs}]")
        
        out.append(f"   cost              {self.llm_calls}  LLM Call(s) + {self.searches} search(es)")
        out.append("-" * 50)

        return "\n".join(out)


@dataclass
class Result:
    answer: str
    trace: Trace
