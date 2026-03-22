from pathlib import Path
import sys
import Scanner # type: ignore

hadError = False

def main():
    """
    main method to execute the input command/script
    """
    if len(sys.argv) > 2:
        print("Usage: python jerry.py <input_command>")
        sys.exit(64)
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runPrompt()

def runFile(path: str):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    run(lines)

def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    if hadError:
        sys.exit(65)

    for token in tokens:
        print(token)

def runPrompt():
    while True:
        try: 
            line = input("> ")
            run(line)
            hadError = False
        except EOFError:
            break


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error{where}: {message}")

def error(line: int, message: str):
    report(line, "", message)

    