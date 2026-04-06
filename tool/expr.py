from dataclasses import dataclass
from typing import Any
from Token import Token  

class Expr:
   def accept(self, visitor):
      pass

@dataclass
class Binary(Expr):
   left: Any
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visitBinaryExpr(self)

@dataclass
class Grouping(Expr):
   expression: Any

   def accept(self, visitor):
      return visitor.visitGroupingExpr(self)

@dataclass
class Literal(Expr):
   value: Any

   def accept(self, visitor):
      return visitor.visitLiteralExpr(self)

@dataclass
class Unary(Expr):
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visitUnaryExpr(self)

