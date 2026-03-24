from typing import List
from TokenType import TokenType
from Token import Token

class Scanner:
    def __init__(self, source: str, error_handler):
        self.source: str = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_handler = error_handler

    # Initialize the scanner with the source code to be scanned
    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "EOF", None))
        return self.tokens
    
    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal))
    
    # Recognizing lexemes and operators
    def scanToken(self):
        case = self.advance()
        if case == "(":
            self.addToken(TokenType.LEFT_PAREN)
        elif case == ")":
            self.addToken(TokenType.RIGHT_PAREN)
        elif case == "{":
            self.addToken(TokenType.LEFT_BRACE)
        elif case == "}":
            self.addToken(TokenType.RIGHT_BRACE)
        elif case == ",":
            self.addToken(TokenType.COMMA)
        elif case == ".":
            self.addToken(TokenType.DOT)
        elif case == "-":
            self.addToken(TokenType.MINUS)
        elif case == "+":
            self.addToken(TokenType.PLUS)
        elif case == ";":
            self.addToken(TokenType.SEMICOLON)
        elif case == "*":
            self.addToken(TokenType.STAR)
        elif case == "!":
            self.addToken(TokenType.BANG)

        # Operators with two characters
        elif case == "=":
            self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)

        elif case == "<":
            self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        
        elif case == ">":
            self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)

        elif case == "/":
            if self.match("/"):
                while self.peek() != "\n" and self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
            

        else:
            self.error_handler(self.line, "Unexpected character.")

    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    
    # Check if the end of the source code has been reached
    def isAtEnd(self) -> bool:
        return self.current >=len(self.source)
    
