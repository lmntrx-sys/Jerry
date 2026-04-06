from dataclasses import dataclass
from typing import Any
from token_class import Token  # type: ignore

class Expr:
   def accept(self, visitor):
      pass

@dataclass
class Binary(Expr):
   left: Any
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visit_binary_expr(self)

@dataclass
class Grouping(Expr):
   expression: Any

   def accept(self, visitor):
      return visitor.visit_grouping_expr(self)

@dataclass
class Literal(Expr):
   value: Any

   def accept(self, visitor):
      return visitor.visit_literal_expr(self)

@dataclass
class Unary(Expr):
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visit_unary_expr(self)

