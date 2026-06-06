from typing import Any

from config import RRF_K


def _fmt(docs) -> str:
    """Join documents or anything with .page_content into a single string"""
    return "\n".join(getattr(d, "page_content", str(d)) for d in docs)

def _sources(docs) -> list[str]:
    """Extract source file names from document metadata"""
    return [getattr(d, "metadata", {}).get("source", "?") for d in docs]

def _rrf(ranked_lists: list[list[Any]], k: int = RRF_K) -> list[Any]:
    scores:      dict[str, float] = {}
    registry:    dict[str, Any]   = {}

    for docs in ranked_lists:
        for rank, doc in enumerate(docs, start=1):
            key               = getattr(doc, "page_content", str(doc))
            registry[key]     = doc
            scores[key]       = scores.get(key, 0.0) + 1.0 / (k + rank)

    return [registry[k_] for k_, _ in sorted(scores.items(), key = lambda kv: kv[1], reverse=True)]

def _parse_lines(text: str) -> list[str]:
    """Split LLM generated line separated lists; strip common list decorators"""
    cleaned = [ln.strip(" -*•\t0123456789.") for ln in text.splitlines()]

    return [line for line in cleaned if line][:5] # cap at 5 to prevent runaway decomposition