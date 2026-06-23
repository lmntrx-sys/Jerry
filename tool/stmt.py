from dataclasses import dataclass
from typing import Any
class Stmt:
    def accept(self, visitor):
        pass

@dataclass
class Block(Stmt):
    statements: Any

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)

@dataclass
class Expression(Stmt):
    expression: Any

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)

@dataclass
class If(Stmt):
    condition: Any
    then_branch: Any
    else_branch: Any

    def accept(self, visitor):
        return visitor.visitIfStmt(self)

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

