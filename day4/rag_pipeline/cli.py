
import sys
from dotenv import load_dotenv

from factory import make_embeddings, make_llm
from day4.rag_pipeline.ingest import chunk_docs, load_corpus
from day4.rag_pipeline.orchestrate import answer_question
from day4.rag_pipeline.retriever import build_retriever
from day4.rag_pipeline.prompts import prompt

load_dotenv()

def setup(docs_path=None):
    print("Loading embedding model...")
    embeddings = make_embeddings()

    print("Loading documents...")
    docs = load_corpus(docs_path)

    print(f"Loaded {len(docs)} document(s)")

    print("Chunking documents....")
    chunks = chunk_docs(docs)
    print(f"  Created {len(chunks)} chunk(s)")

    print("Building vector index...")
    retriever = build_retriever(chunks, embeddings)

    print("Creating LLM...")
    llm = make_llm()

    print("Pipeline ready!\n")

    return retriever, llm

def main():
    docs_path = sys.argv[1] if len(sys.argv) > 1 else None
    retriever, llm = setup(docs_path)

    print("=" * 50)
    print("   RAG Pipeline CLI")
    print("   Ask questions about the loaded documents.")
    print("   Type 'quit' or 'exit' to stop.")
    print("=" * 50)

    while True:
        try:
            question = input("\n>>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if not question:
            continue

        if question.lower() in ("quit", "exit"):
            print("\nBye!")
            break

        try:
            answer = answer_question(question, retriever, llm, prompt)

            print(f"\n{answer.text}")

            if not answer.abstained and answer.cited:
                print("\nSources cited:")
                for cid in answer.cited:
                    src = answer.sources[cid]
                    print(f"   [{cid}]  {src['source']}")

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()