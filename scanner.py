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
        # Check for start
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        # Add the EOF token to the end of the program
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
        char = self.advance()
        
        match char:
            # Single-character tokens
            case "(": self.addToken(TokenType.LEFT_PAREN)
            case ")": self.addToken(TokenType.RIGHT_PAREN)
            case "{": self.addToken(TokenType.LEFT_BRACE)
            case "}": self.addToken(TokenType.RIGHT_BRACE)
            case ",": self.addToken(TokenType.COMMA)
            case ".": self.addToken(TokenType.DOT)
            case "-": self.addToken(TokenType.MINUS)
            case "+": self.addToken(TokenType.PLUS)
            case ";": self.addToken(TokenType.SEMICOLON)
            case "*": self.addToken(TokenType.STAR)

            # Operator tokens (one or two characters)
            case "!":
                self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
            case "=":
                self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
            case "<":
                self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
            case ">":
                self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)

            # Slashes and Comments
            case "/":
                if self.match("/"):
                    # A comment goes until the end of the line
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)

            # Whitespace
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1

            case '"':
                self.string()

            # Default case (Unexpected characters)
            case _:
                # Check if the character is a digit (for numbers) or an alphabetic character (for identifiers)
                if self.isDigit(char):
                    self.number()
                else:
                    self.error_handler(self.line, "Unexpected character.")

    # Checking for the start of a string
    def string(self):
        # Check for the quotation mark
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                # Move to the next line
                self.line += 1
            self.advance()

            if self.isAtEnd():
                self.error_handler(self.line, "Unterminated String")
                return
            
            self.advance()
        value = self.source[self.start+1 : self.current-1]
        self.addToken(TokenType.STRING, value)

    # Look for numbers in our code
    def isDigit(self, c) -> bool:
        return "0" <= c <= "9"
    
    def number(self):
        while self.isDigit(self.peek()):
            self.advance()

        if self.peek() == self.isDigit(self.peekNext()):
            self.advance()

            while self.isDigit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.addToken(TokenType.NUMBER, value)



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
    
    def peek(self) -> str:
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]
    
        
