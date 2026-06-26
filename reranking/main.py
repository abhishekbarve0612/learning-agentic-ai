import argparse
import config
from reranking import providers
from reranking.corpus import AUDIT_DOCS, DEFAULT_QUERY, FAT_AUDIT_DOCS
from reranking.pipeline import build_compression_retriever, build_rag_chain, format_docs
from reranking.retrieval.base_retriever import build_base_retriever, build_vectorstore


def _print_funnel(docs, query):
    embeddings = providers.get_embeddings()
    cross_encoder = providers.get_cross_encoder()

    vs = build_vectorstore(docs, embeddings)
    base = build_base_retriever(vs, k=config.NET_K)

    stage1 = base.invoke(query)

    print(f"STAGE 1 The Net (FAISS, k={config.NET_K}) <-------------- recall")
    print("Retrieved ids", [d.metadata["id"] for d in stage1])

    pairs = [(query, d.page_content) for d in stage1]
    scores = cross_encoder.score(pairs)
    ranked = sorted(zip(stage1, scores), key = lambda x: x[1], reverse=True)

    print("STAGE 2 The Scalpel (cross encoder) <------------- precision")
    print("rescored: ")
    for d, s in ranked:
        tag = "<-- PROMOTED" if d.metadata.get("role") == "needle" else ""
        print(f"id={d.metadata['id']} score={s} {tag}")

    kept = [d for d, _ in ranked[:config.RERANK_TOP_K]]
    print(f"   top_n={config.RERANK_TOP_K} kept ids:", [d.metadata["id"] for d in kept])

    if config.COMPRESSION_MODE != "none":
        retriever = build_compression_retriever(docs)
        final = retriever.invoke(query)
        before = sum(len(d.page_content) for d in kept)
        after = sum(len(d.page_content) for d in final)
        print("STAGE 3: The Laser compression mode <--------------- trim filler")
        print(f"   chars before compression: {before}   after: {after}"
              f"   ({100*(before-after)//max(before,1)}% removed)")
        return final
    return kept

def main():
    ap = argparse.ArgumentParser(description="Session 3.2 two-stage retrieval funnel")
    ap.add_argument("--query", default=DEFAULT_QUERY)
    ap.add_argument("--fat", action="store_true", help="use the padded corpus (shows compression value)")
    ap.add_argument("--compression", choices=["none", "embeddings_filter", "llm_extractor"],
                    help="override COMPRESSION_MODE")
    ap.add_argument("--show-funnel", action="store_true", help="print a per-stage teaching trace")
    args = ap.parse_args()

    if args.compression:
        config.COMPRESSION_MODE = args.compression

    docs = FAT_AUDIT_DOCS if args.fat else AUDIT_DOCS
    print("=" * 64)
    print(" TWO-STAGE RETRIEVAL + CONTEXTUAL COMPRESSION ".center(64, "="))
    print("=" * 64)
    print(f"Query: {args.query}")
    print(f"Embeddings: {config.EMBED_PROVIDER}  |  LLM: {config.LLM_PROVIDER}  |  "
          f"compression: {config.COMPRESSION_MODE}")

    
    if args.show_funnel:
        survivors = _print_funnel(docs, args.query)
    else:
        survivors = build_compression_retriever(docs).invoke(args.query)

    llm = providers.get_llm()
    if llm is None:
        # Key-free dry run: show exactly what would be injected, don't call an LLM.
        print("\n── DRY RUN (LLM_PROVIDER='none') ─ chunks that would be injected ──")
        print(format_docs(survivors))
        print("\n(Set LLM_PROVIDER to generate an actual answer.)")
        return

    chain = build_rag_chain(build_compression_retriever(docs), llm)
    print("\n── ANSWER ──")
    print(chain.invoke(args.query))

if __name__ == "__main__":
    main()