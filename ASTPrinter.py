from tool.expr import Expr, Literal, Binary, Token

class ASTPrinter:
    def __init__(self):
        pass

    def printTree(self, expr) -> str:
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitGroupingExpr(self, expr) -> str:
        return self.parenthesize("group", expr.expression)
    
    def visitLiteralExpr(self, expr) -> str:
        if expr.value == None:
            return "nill"
        return str(expr.value)
    
    def visitUnaryExpr(self, expr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name: str, *exprs: Expr) -> str:

        parts = [expr.accept(self) for expr in exprs]
        return f"({name} {' '.join(parts)})"
    
if __name__ == "__main__":
    # Example usage:
    # (1 + 2) * (4 - 3)
    expression = Binary(
        left=Binary(
            left=Literal(1),
            operator=Token("PLUS", "+", None, 1),
            right=Literal(2)
        ),
        operator=Token("STAR", "*", None, 1),
        right=Binary(
            left=Literal(4),
            operator=Token("MINUS", "-", None, 1),
            right=Literal(3)
        )
    )
    printer = ASTPrinter()
    print(printer.printTree(expression))  # Output: (* (+ 1 2) (- 4 3))