from dataclasses import dataclass
from typing import Any

class Stmt:
      def accept(self, visitor):
          pass

@dataclass
class Expression(Stmt):
   expression: Any

   def accept(self, visitor):
      return visitor.visit_expression_stmt(self)

@dataclass
class Print(Stmt):
   expression: Any

   def accept(self, visitor):
      return visitor.visit_print_stmt(self)

