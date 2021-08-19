import ast
from loguru import logger
logger.add("out.log", backtrace=True, diagnose=True)  #

source_code = """
def bubble_sort(collection):
    length = len(collection)
    for i in range(length - 1):
        pass
    print(length)
    return collection
"""
tree = ast.parse(source_code, mode="exec")
with open("tree.ast","w") as f:
    f.write(ast.dump(tree, indent=4))

print()

def get_fields(node):
    return [f for f in dir(node) if not f.startswith("__")]

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"{get_fields(node)=}")
        print(node.name)
        print(get_fields(node.args))
        print(get_fields(node.args.args))
        print(get_fields(node.args.args[0]))
        print(node.args.args[0].arg)