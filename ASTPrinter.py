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
    
    def parenthesize()
        pass