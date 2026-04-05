import argparse

from rag import answer_query


def parse_args():
    parser = argparse.ArgumentParser(description="Query the LennyPM RAG assistant.")
    parser.add_argument("--query", "-q", help="PM question to ask")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.query:
        query = args.query.strip()
    else:
        query = input("Enter a PM question: ").strip()

    if not query:
        print("No query provided. Use --query or enter a question.")
        return

    result = answer_query(query)
    print("\nAnswer:\n")
    print(result["answer"])
    if result["sources"]:
        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source['source_label']} ({', '.join(source['guest_names'])})")


if __name__ == "__main__":
    main()
