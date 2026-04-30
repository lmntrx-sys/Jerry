from tool.expr import Literal, Binary, Grouping, Unary, Expr
from TokenType import TokenType as Tk
from typing import Any

class Interpreter:
    def __init__(self):
        pass

    def visitLiteralExpr(self, node: Literal):
        """Visit the Literal node expression and return its value"""
        return node.value
    
    def visitGroupingExpr(self, node: Grouping):
        """Visit the Group node expression and return its value"""
        return self.evaluate(node.expression)
    
    def evaluate(self, expr: Expr):
        return expr.accept()
    
    def visitUnaryExpr(self, node: Unary) -> Any:
        """Visit the Unary node expression and return its value"""
        # recursively evaluate the operand first (Post-order traversal)
        right = self.evaluate(node.right)

        match node.operator.type: 
            case Tk.MINUS:
                return -float(right)
            case Tk.BANG:
                return not self.is_truthy(right)
            
        return None
    
    def visitBinaryExpr(self, node: Binary):
        """Visit the Binary node expression and return its value"""
        # In the Node we handle the left and right side of the operation
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        match node.operator.type:
            case Tk.MINUS:
                return float(left) - float(right)
            case Tk.SLASH:
                return float(left) / float(right)
            case Tk.STAR:
                return float(left) * float(right)
            
            # We are handling a case when a user either wants to perform simple addition or concatenation
            case Tk.PLUS:
                if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                    return float(left) + float(right)
                
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            
        return None
    
    def is_truthy(self, obj: Any) -> bool:
        """Anything that is not false or nil is true"""
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True