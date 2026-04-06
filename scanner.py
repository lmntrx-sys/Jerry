from typing import List
from TokenType import TokenType
from Token import Token

KEYWORDS = {
    "and":    TokenType.AND,
    "class":  TokenType.CLASS,
    "else":   TokenType.ELSE,
    "false":  TokenType.FALSE,
    "for":    TokenType.FOR,
    "fun":    TokenType.FUN,
    "if":     TokenType.IF,
    "nil":    TokenType.NIL,
    "or":     TokenType.OR,
    "print":  TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":  TokenType.SUPER,
    "this":   TokenType.THIS,
    "true":   TokenType.TRUE,
    "var":    TokenType.VAR,
    "while":  TokenType.WHILE,
}

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
        """Scanning of code to produce a List of tokens"""
        # Check for start
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        # Add the EOF token to the end of the program
        self.tokens.append(Token(TokenType.EOF, "EOF", None, self.line))
        return self.tokens
    
    def advance(self) -> str:
        """Consume the current character and return it"""
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, type: TokenType, literal: object = None):
        """Add a token to the list of tokens"""
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    
    # Recognizing lexemes and operators
    def scanToken(self):
        """Scan a single token from the source code, and identify its type based on hard-coded rules."""
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
                elif self.isAlpha(char):
                    self.identifier()
                else:
                    self.error_handler(self.line, "Unexpected character.")

    # Recognizing identifiers and reserved keywords
    def identifier(self):
        """ Recognize identifiers and reserved keywords by consuming characters until a non-alphanumeric character is encountered, and then checking if the resulting string matches any reserved keywords."""
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.addToken(TokenType.IDENTIFIER)
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.addToken(token_type)

    def isAlpha(self, c) -> bool:
        """Check if the character is an alphabetic character or an underscore"""
        return ('a'<=c<='z') or \
                ('A'<=c<='Z')or \
                c == '_'

    def isAlphaNumeric(self, c: str) -> bool:
        """Check if the character is an alphabetic character, a digit, or an underscore"""
        return self.isAlpha(c) or self.isDigit(c)

    # Checking for the start of a string
    def string(self):
        """Check for the start of a string and consume characters until the closing quotation mark is found"""
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
        """Check if the character is a digit"""
        return "0" <= c <= "9"
    
    def number(self):
        """Look for numbers in our code and consume characters until the end of the number is reached"""
        while self.isDigit(self.peek()):
            self.advance()

        if self.peek() == self.isDigit(self.peekNext()):
            self.advance()

            while self.isDigit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.addToken(TokenType.NUMBER, value)



    def match(self, expected: str) -> bool:
        """Check if the next character matches the expected character, and consume it if it does"""
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    
    # Check if the end of the source code has been reached
    def isAtEnd(self) -> bool:
        """Check if the end of the source code has been reached"""
        return self.current >=len(self.source)
    
    def peek(self) -> str:
        """Look at the current character without consuming it"""
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]
    
    def peekNext(self):
        """Look at the next character without consuming it"""
        # We've reached the end of the string
        if self.current + 1>=len(self.source):
            return "\0"
        return self.source[self.current+1]
    
        
