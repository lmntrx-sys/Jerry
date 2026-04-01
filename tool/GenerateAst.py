import sys
from typing import List

def main():
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)


    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
        "Binary    : left, operator, right",
        "Grouping  : expression",
        "Literal   : value",
        "Unary     : operator, right"
    ])

def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = f"{output_dir}/{base_name.lower()}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write("from dataclasses import dataclass\n")
        f.write("from typing import Any\n")
        f.write("from token_class import Token\n\n")

        # The Base class
        f.write(f"class {base_name}:\n")
        f.write("      def accept(self, visitor):\n")
        f.write("          pass\n\n")

        # The Ast Classes
        for type_str in types:
            class_name = type_str.split(":")[0].strip()
            fields = type_str.split(":")[1].strip()
            define_type(f, base_name, class_name, fields)


def define_type(f, base_name, class_name, field_list):
    f.write("@dataclass\n")
    f.write(f"class {class_name}9{base_name}:\n")

    # Write fields
    fields = field_list.split(", ")
    for field in fields:
        f.write(f"   {field}: Any\n")
    f.write("\n    def accept(self, visitor):\n")
    f.write(f"         return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n")


if __name__ == "__main__":
    main()