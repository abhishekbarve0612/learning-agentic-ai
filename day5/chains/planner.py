from typing import Callable

from day5.prompts.planner import PLANNER_PROMPT
from day5.schema import Plan, QueryPlan


def make_planner(llm) -> Callable[[str], Plan]:
    chain = PLANNER_PROMPT | llm.with_structured_output(QueryPlan)

    def plan(question: str) -> Plan:
        qp = chain.invoke({ "question": question })

        return Plan(
            route = qp.route,
            strategy = qp.strategy,
            reasoning = qp.reasoning,
        )

    return plan