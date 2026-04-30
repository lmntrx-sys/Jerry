from pathlib import Path
import sys
from scanner import Scanner
from Token import Token, TokenType

hadError = False

# Main method to execute the input command/script
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

# Run the source code from a file
def runFile(path: str):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    run(lines)

# Run the source code through the scanner and print the tokens
def run(source: str):
    scanner = Scanner(source, error)
    tokens = scanner.scanTokens()
    if hadError:
        sys.exit(65)

    for token in tokens:
        print(token)

# Entry point of the program
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

def error(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)

def error(line: int, message: str):
    report(line, "", message)

if __name__ == "__main__":
    main()