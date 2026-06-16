from dataclasses import dataclass
from typing import Any
from token import Token

class Expr:
   def accept(self, visitor):
       pass

@dataclass
class Assign(Expr):
  name: Any
  value: Any
  def accept(self, visitor):
    return visitor.visitassignexpr(self)

@dataclass
class Binary(Expr):
  left: Any
  operator: Any
  right: Any

  def accept(self, visitor):
    return visitor.visitbinaryexpr(self)

    

  

@dataclass
class Grouping(Expr):
  expression: Any

  def accept(self, visitor):
    return visitor.visitgroupingexpr(self)

@dataclass
class Literal(Expr):
  value: Any

  def accept(self, visitor):
    return visitor.visitliteralexpr(self)

@dataclass
class Unary(Expr):
  operator: Any
  right: Any

  def accept(self, visitor):
    return visitor.visitunaryexpr(self)

    

@dataclass
class Variable(Expr):
  name: Any

  def accept(self, visitor):
    return visitor.visitvariableexpr(self)

