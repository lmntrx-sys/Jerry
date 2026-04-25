from dataclasses import dataclass
from typing import Any
from Token import Token  

class Expr:
   def accept(self, visitor):
      pass

@dataclass
class Binary(Expr):
   """Represents a binary expression in the AST, consisting of a left operand, an operator, and a right operand."""
   left: Any
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visitBinaryExpr(self)

@dataclass
class Grouping(Expr):
   """Represents a grouping expression in the AST, which is used to group sub-expressions together."""
   expression: Any

   def accept(self, visitor):
      return visitor.visitGroupingExpr(self)

@dataclass
class Literal(Expr):
   """Represents a literal value in the AST, such as a number, string, or boolean."""
   value: Any

   def accept(self, visitor):
      return visitor.visitLiteralExpr(self)

@dataclass
class Unary(Expr):
   """Represents a unary expression in the AST, consisting of an operator and a right operand."""
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visitUnaryExpr(self)

