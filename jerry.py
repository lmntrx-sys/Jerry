from pathlib import Path
import sys
from scanner import Scanner
from Token import Token, TokenType
from RuntimeError import JLXRuntimeError
from interpreter import Interpreter # TODO: remove this import and use the interpreter in the run function instead of just printing tokens

hadError = False
hadRuntimeError = False

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
    # start using the interpreter here to execute the tokens and handle any runtime errors
    interpreter = Interpreter(runtimeError)
    interpreter.interpret(tokens)
    if hadError:
        sys.exit(65)
    
    if hadRuntimeError:
        sys.exit(70)

    for token in tokens:
        print(token)

# Entry point of the program
def runPrompt():
    while True:
        try: 
            line = input("> ")
            run(line)
            hadError = False
            hadRuntimeError = False
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

def runtimeError(error: JLXRuntimeError):
    global hadRuntimeError
    hadRuntimeError = True
    print(f"{error.message}\n[line {error.token.line}]")
    sys.exit(70)

if __name__ == "__main__":
    main()