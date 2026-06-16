from Token import Token
from typing import List
from tool.expr import Assign, Literal, Binary, Grouping, Unary, Variable
from tool.stmt import Expression, Print, Block, Stmt
from TokenType import TokenType
from jerry import JerryLox as jlx
from tool.stmt import Var

class Parser:

    class ParseError(Exception):
        """Custom exception for parser errors to allow for synchronizing."""
        pass

    def __init__(self, tokens: List[Token], error_handler):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parser(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        return self.expression()
    
    # Comparison -> Term ( ( ">" | ">=" | "<" | "<=" ) Term )*
    def comparison(self):
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
        
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        
    def synchronize(self):
        """Discards tokens until it finds a statement boundary."""
        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            match self.peek().type:
                case (TokenType.CLASS | TokenType.FUN | TokenType.VAR | 
                      TokenType.FOR | TokenType.IF | TokenType.WHILE | 
                      TokenType.PRINT | TokenType.RETURN):
                    return
        
        self.advance()


    def parse(self):
        """Parse the list of tokens and return a list of statements (AST nodes)."""
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
    
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
        raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str):
        """Report a parsing error at the given token with the provided message."""
        self.error_handler(token, message)
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
        return self.assignment()
    
    def declaration(self):
        """Parse a declaration and return the resulting AST node."""
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.Stmt()
        except Exception as e:
            self.synchronize()
            return None
    
    def Stmt(self):
        """Parse a statement and return the resulting AST node."""
        if self.match(TokenType.IF): return self.ifStatement()
        if (self.match(TokenType.PRINT)): return self.printStatement()

        if self.match(TokenType.LEFT_BRACE): return self.block()
        return self.expressionStatement()
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch = self.Stmt()
        elseBranch = None

        if self.match(TokenType.ELSE):
            elseBranch = self.Stmt()
        return Stmt.If(condition, thenBranch, elseBranch)
    
    def printStatement(self):
        """Parse a print statement and return the resulting AST node."""
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Print(value)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return Var(name, initializer)
    
    def expressionStatement(self):
        """Parse an expression statement and return the resulting AST node."""
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression")
        return Expression(expr)
    
    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block")
        return Block(statements)
    
    def assignment(self):
        expr = self.eqaulity()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")

        return expr

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
    