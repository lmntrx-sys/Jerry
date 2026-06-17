import sys
from typing import List

def main():
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)


    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
        "Assign    : name, value",
        "Binary    : left, operator, right",
        "Grouping  : expression",
        "Literal   : value",
        "Unary     : operator, right",
        "Variable   : name",
    ])

    define_ast(output_dir, "Stmt", [
        "Block      : statements",
        "Expression : expression",
        "If         : condition, then_branch, else_branch",
        "Print      : expression",
        "Var        : name, initializer"
    ])

def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = f"{output_dir}/{base_name.lower()}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write("from dataclasses import dataclass\n")
        f.write("from typing import Any\n")

        # The Base class
        f.write(f"class {base_name}:\n")
        f.write("    def accept(self, visitor):\n")
        f.write("        pass\n\n")

        # The Ast Classes
        for type_str in types:
            class_name = type_str.split(":")[0].strip()
            fields = type_str.split(":")[1].strip()
            define_type(f, base_name, class_name, fields)


def define_type(f, base_name, class_name, field_list):
    f.write("@dataclass\n")
    f.write(f"class {class_name}({base_name}):\n")

    # Write fields
    fields = field_list.split(", ")
    for field in fields:
        f.write(f"    {field}: Any\n")

    f.write("\n    def accept(self, visitor):\n")
    f.write(f"        return visitor.visit{class_name}{base_name}(self)\n\n")


if __name__ == "__main__":
    main()