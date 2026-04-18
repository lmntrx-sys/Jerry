from Token import Token
from typing import List
from tool.expr import Expr, Literal, Binary, Grouping, Unary
from TokenType import TokenType

class Parser:
    def __init__(self):
        self.tokens = []
        self.current = 0

    def parser(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        return self.expression()

    def comparison(self, expr: Expr):
        expr = term()

        while self.match(TokenType.GREATER,TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = term()
            expr = Binary(expr, operator, right)


        return expr

    
    # Equality -> Comparison ( "!=" | "==" ) Comparison
    def eqaulity(self):
        expr = comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    

    
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
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