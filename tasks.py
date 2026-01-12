import argparse
import subprocess
import sys


def run_streamlit():
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app/main.py"],
        check=True,
    )


def build_book_embeddings():
    subprocess.run([sys.executable, "scripts/build_book_embeddings.py"], check=True)


def sanity_check():
    subprocess.run([sys.executable, "scripts/sanity_check_referential.py"], check=True)


def run_tests():
    subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    args = parser.parse_args()

    commands = {
        "run": run_streamlit,
        "build-books": build_book_embeddings,
        "check-ref": sanity_check,
        "test": run_tests,
    }

    if args.command not in commands:
        raise SystemExit(f"Commande inconnue: {args.command}")

    commands[args.command]()


if __name__ == "__main__":
    main()
