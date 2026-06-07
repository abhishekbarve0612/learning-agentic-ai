
import argparse
import sys

from config import ANTHROPIC_MODEL, EMBED_PROVIDER, LLM_PROVIDER, OPENAI_MODEL

from day5.orchestrator.switchboard import build_switchboard
from day5.tests.test_switchboard import selftest


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Switchboard — transparent query router.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python switchboard.py --selftest\n"
            "  python switchboard.py --trace 'Why did OCR fail?'\n"
            "  python switchboard.py --docs ./my_docs 'How do I authenticate?'\n"
        ),
    )
    ap.add_argument("question",  nargs="?",          help="question to route and answer")
    ap.add_argument("--docs",                         help="folder of .md / .txt to ingest")
    ap.add_argument("--trace",   action="store_true", help="print the routing receipt")
    ap.add_argument("--selftest",action="store_true", help="offline smoke test, no keys needed")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.question:
        ap.error("provide a question, or use --selftest")

    model = ANTHROPIC_MODEL if LLM_PROVIDER == "anthropic" else OPENAI_MODEL
    print(f"[providers] LLM={LLM_PROVIDER} ({model})  EMBED={EMBED_PROVIDER}", file=sys.stderr)

    sb  = build_switchboard(args.docs)
    res = sb.route(args.question)

    if args.trace:
        print(res.trace.render())

    print("\n" + res.answer)

 
if __name__ == "__main__":
    main()