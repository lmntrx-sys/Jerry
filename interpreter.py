from tool.expr import Literal, Binary, Grouping, Unary, Expr
from TokenType import TokenType as Tk
from typing import Any
from RuntimeError import JLXRuntimeError

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
        return expr.accept(self)
    
    def visitUnaryExpr(self, node: Unary) -> Any:
        """Visit the Unary node expression and return its value"""
        # recursively evaluate the operand first (Post-order traversal)
        right = self.evaluate(node.right)

        match node.operator.type: 
            case Tk.MINUS:
                self.checkNumberOperand(node.operator, right)
                return -float(right)
            case Tk.BANG:
                return not self.isTruthy(right)
            
        return None
    
    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, float): return
        raise JLXRuntimeError(operator, "Operand must be number.")
    
    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float): return
        raise JLXRuntimeError(operator, "Operands must be numbers.")

    def visitBinaryExpr(self, node: Binary):
        """Visit the Binary node expression and return its value"""
        # In the Node we handle the left and right side of the operation
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        match node.operator.type:
            case Tk.MINUS:
                return float(left) - float(right)
            
            # Handling division by zero
            case Tk.SLASH:
                self.checkNumberOperands(node.operator, left, right)
                if right == 0:
                    raise JLXRuntimeError(node.operator, "division by zero")
                else:
                    return float(left) / float(right)
            case Tk.STAR:
                self.checkNumberOperands(node.operator, left, right)
                return float(left) * float(right)
            case Tk.GREATER:
                self.checkNumberOperands(node.operator, left, right)
                return float(left) > float(right)
            case Tk.GREATER_EQUAL:
                self.checkNumberOperands(node.operator, left, right)
                return float(left) >= float(right)
            case Tk.LESS:
                self.checkNumberOperands(node.operator, left, right)
                return float(left) < float(right)
            case Tk.LESS_EQUAL:
                self.checkNumberOperands(node.operator, left, right)
                return float(left) <= float(right)
            case Tk.BANG_EQUAL:
                self.checkNumberOperands(node.operator, left, right)
                return not self.isEqual(left, right)
            case Tk.EQUAL_EQUAL:
                self.checkNumberOperands(node.operator, left, right)
                return self.isEqual(left, right)
            
            # We are handling a case when a user either wants to perform simple addition or concatenation
            case Tk.PLUS:
                self.checkNumberOperands(node.operator, left, right)
                if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                    return float(left) + float(right)
                
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                
                raise JLXRuntimeError(f"Operands must be two numbers or two strings.")
            
        return None
    
    def isEqual(self, left, right) -> bool:
        return left == right
    
    def error(self, token, message):
        from jerry import JerryLox as jlx
        jlx.error(token, message)
        return Exception(message)
    
    def interpret(self, expr: Expr, error_handler):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except JLXRuntimeError as e:
            error_handler(e)
            
    def stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"
        
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
    
    def isTruthy(self, obj: Any) -> bool:
        """Anything that is not false or nil is true"""
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True