from Token import Token
from typing import List
from tool.expr import Expr, Literal, Binary, Grouping, Unary
from TokenType import TokenType
from jerry import error

class Parser:
    def __init__(self):
        self.tokens = []
        self.current = 0

    def parser(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        return self.expression()
    
    # Comparison -> Term ( ( ">" | ">=" | "<" | "<=" ) Term )*
    def comparison(self, expr: Expr):
        """Parse a comparison expression and return the resulting AST node."""
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)


        return expr
    
    # Term -> Factor ( ( "-" | "+" ) Factor )*
    def term(self):
        """Parse a term expression and return the resulting AST node."""
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    # Factor -> Unary ( ( "/" | "*" ) Unary )*
    def factor(self):
        """Parse a factor expression and return the resulting AST node."""
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    # Unary -> ( "!" | "-" ) Unary | Primary
    def unary(self):
        """Parse a unary expression and return the resulting AST node."""
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    # Equality -> Comparison ( "!=" | "==" ) Comparison
    def eqaulity(self):
        """Parse an equality expression and return the resulting AST node."""
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    # Primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" Expression ")"
    def primary(self):
        """Parse a primary expression and return the resulting AST node."""
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression. ")
            return Grouping(expr) 

    # Error handling
    def match(self, *types):
        """Check if the current token matches any of the given types. If it does, consume the token and return True. Otherwise, return False."""
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str):
        """Consume the current token if it matches the expected type, otherwise raise an error with the provided message."""
        if self.check(type):
            return self.advance()
        raise Exception(message)
    
    def error(self, token: Token, message: str):
        error(token, message)
        return Exception(message)
    
    def check(self, type: TokenType):
        """Check if the current token is of the given type. Returns False if we've reached the end of the token list."""
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def advance(self):
        """Advance to the next token and return the previous token."""
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def expression(self):
        """Parse an expression and return the resulting AST node."""
        return self.eqaulity()

    def peek(self):
        """Return the current token without consuming it."""
        return self.tokens[self.current]
    
    def previous(self):
        """Return the most recently consumed token."""
        return self.tokens[self.current-1]
    
    def isAtEnd(self):
        """Check if we've reached the end of the token list."""
        return self.peek().type == TokenType.EOF
    
    def advance(self):
        """Advance to the next token and return the previous token."""
        if not self.isAtEnd():
            self.current += 1
        return self.previous()