from tool.expr import Literal, Binary, Grouping, Unary, Expr
from TokenType import TokenType as Tk
from typing import Any
from jerry import error

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
                return not self.isTruthy(right)
            
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
            case Tk.GREATER:
                return float(left) > float(right)
            case Tk.GREATER_EQUAL:
                return float(left) >= float(right)
            case Tk.LESS:
                return float(left) < float(right)
            case Tk.LESS_EQUAL:
                return float(left) >= float(right)
            case Tk.BANG_EQUAL:
                return not self.isEqual(left, right)
            case Tk.EQUAL_EQUAL:
                return self.isEqual(left, right)
            
            # We are handling a case when a user either wants to perform simple addition or concatenation
            # We also want to hadle cases where these occur: "scone" + 4 -> "scone4"
            case Tk.PLUS:
                if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                    return float(left) + float(right)
                
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                
                if isinstance(left, str) and isinstance(right, (float, int)):
                    return left + str(right)
            
        return None
    
    def isEqual(self, left, right) -> bool:
        return left == right
    
    def isTruthy(self, obj: Any) -> bool:
        """Anything that is not false or nil is true"""
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True