from pathlib import Path
import sys
from typing import Final
from scanner import Scanner
from Token import Token, TokenType
from RuntimeError import JLXRuntimeError
from interpreter import Interpreter

class JerryLox:
    # It lives here so it persists across multiple calls to run()
    _INTERPRETER: Final = Interpreter()
    
    hadError = False
    hadRuntimeError = False

    @classmethod
    def main(cls):
        if len(sys.argv) > 2:
            print("Usage: python jerry.py <input_command>")
            sys.exit(64)
        elif len(sys.argv) == 2:
            cls.runFile(sys.argv[1])
        else:
            cls.runPrompt()

    @classmethod
    def runFile(cls, path: str):
        # We read the whole file as one string for the scanner
        source = Path(path).read_text(encoding="utf-8")
        cls.run(source)
        
        if cls.hadError: sys.exit(65)
        if cls.hadRuntimeError: sys.exit(70)

    @classmethod
    def runPrompt(cls):
        while True:
            try: 
                line = input("> ")
                if not line: continue
                cls.run(line)
                cls.hadError = False # Reset so one error doesn't kill the session
            except EOFError:
                break


    @classmethod
    def run(cls, source: str):
        scanner = Scanner(source, cls.error)
        tokens = scanner.scanTokens()

        from parser import Parser
        parser = Parser(tokens, cls.error)
        expression = parser.parse() 

        if cls.hadError: return 

        cls._INTERPRETER.interpret(expression, cls.runtimeError)


    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        cls.hadError = True

    @classmethod
    def error(cls, token: Token, message: str):
        if token.type == TokenType.EOF:
            cls.report(token.line, " at end", message)
        else:
            cls.report(token.line, f" at '{token.lexeme}'", message)

    @classmethod
    def runtimeError(cls, error: JLXRuntimeError):
        print(f"{error.message}\n[line {error.token.line}]")
        cls.hadRuntimeError = True

if __name__ == "__main__":
    JerryLox.main()