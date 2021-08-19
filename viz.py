import ast
from loguru import logger
logger.add("out.log", backtrace=True, diagnose=True)  #

source_code = """
def bubble_sort(collection: str, arb: int):
    length = len(collection)
    for i in range(length - 1):
        pass
    print(length)
    return collection, col
"""
tree = ast.parse(source_code, mode="exec")
with open("tree.ast","w") as f:
    f.write(ast.dump(tree, indent=4))

print()

def get_fields(node):
    return [f for f in dir(node) if not f.startswith("__")]


class ParamFinder(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        params = []
        l = map(lambda x: (x.arg, x.annotation.id) if x.annotation else (x.arg, None), node.args.args)
        print(list(l))
        self.generic_visit(node)
        return l

#ParamFinder().visit(tree)


def get_parameters(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.arguments):
            l = map(lambda x: (x.arg, x.annotation.id) if x.annotation else (x.arg, None), 
                    node.args)
    return l

def get_return(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            if isinstance(node.value, ast.Name):
                return list(node.value.id)
            elif isinstance(node.value, ast.Tuple):
                return list(map(lambda x: x.id, node.value.elts))

print(list(get_parameters(tree)))

print(get_return(tree))