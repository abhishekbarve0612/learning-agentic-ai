import re

from day4.rag_pipeline.prompts import ABSTAIN_MESSAGE


def number_context(chunks):
    lines, sources = [], {}

    for idx, chunk in enumerate(chunks, start = 1):
        lines.append(f"[{idx}] {chunk.page_content}")
        sources[idx] = {"source": chunk.metadata.get("source", "unknown"), "text": chunk.page_content}

    return "\n\n".join(lines), sources

_CITE_RE = re.compile(r"\[(\d+)\]")

def parse_cited_ids(answer_text, valid_ids):
    valid, seen, out = set(valid_ids), set(), []
    for match in _CITE_RE.finditer(answer_text):
        n = int(match.group(1))
        if n in valid and n not in seen:
            seen.add(n)
            out.append(n)

    return out

def looks_like_abstention(text: str) -> bool:
    t = (text or "").strip().lower()
    return t.startswith("i don't have enough information") or t == ABSTAIN_MESSAGE.lower()