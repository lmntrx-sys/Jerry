from dataclasses import dataclass
from typing import Any
from token_class import Token # pyright: ignore[reportMissingImports]

class Expr:
      def accept(self, visitor):
          pass

@dataclass
class Binary9Expr:
   left: Any
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visit_binary_expr(self)

@dataclass
class Grouping9Expr:
   expression: Any

   def accept(self, visitor):
      return visitor.visit_grouping_expr(self)

@dataclass
class Literal9Expr:
   value: Any

   def accept(self, visitor):
      return visitor.visit_literal_expr(self)

@dataclass
class Unary9Expr:
   operator: Any
   right: Any

   def accept(self, visitor):
      return visitor.visit_unary_expr(self)

