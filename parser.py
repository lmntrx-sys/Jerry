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
        expr = self.term()

        while self.match(TokenType.GREATER,TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)


        return expr
    
    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
    
    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    # Equality -> Comparison ( "!=" | "==" ) Comparison
    def eqaulity(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression. ")
            return Grouping(expr) 

    
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise Exception(message)
    
    def error(self, token: Token, message: str):
        error(token, message)
        return Exception(message)
    
    def check(self, type: TokenType):
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def expression(self):
        return self.eqaulity()

    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current-1]
    
    def isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()