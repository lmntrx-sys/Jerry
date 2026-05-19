from dataclasses import dataclass
from typing import Any
import Token

class Stmt:
   def accept(self, visitor):
      pass

@dataclass
class Expression(Stmt):
   expression: Any

   def accept(self, visitor):
      return visitor.visitExpressionStmt(self)

@dataclass
class Print(Stmt):
   expression: Any

   def accept(self, visitor):
      return visitor.visitPrintStmt(self)

@dataclass
class Var(Stmt):
   name: Any
   initializer: Any

   def accept(self, visitor):
      return visitor.visitVarStmt(self)

