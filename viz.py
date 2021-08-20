import ast
from loguru import logger
logger.add("out.log", backtrace=True, diagnose=True)  #


def get_fields(node):
    return [f for f in dir(node) if not f.startswith("__")]


class ParamFinder(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        l = map(lambda x: (x.arg, x.annotation.id) if x.annotation else (x.arg, None), node.args.args)
        self.generic_visit(node)
        return list(l)


#ParamFinder().visit(tree)

class AssignFinder(ast.NodeVisitor):
    assigns = {}
    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            key = node.targets[0].id
        elif isinstance(node.targets[0], ast.Tuple):
            key = "unparse"

        if isinstance(node.value, ast.Constant):
            value = node.value.value
        elif isinstance(node.value, ast.Call):
            value = ParamFinder().visit(node)
        else:
            value = "Unparseable"
        self.assigns[key] = value
        self.generic_visit(node)

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
                return [node.value.id]
            elif isinstance(node.value, ast.Tuple):
                return list(map(lambda x: x.id, node.value.elts))

source_code = """
def bubble_sort(collection):
    length = len(collection)
    for i in range(length - 1):
        swapped = False
        for j in range(length - 1 - i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break  # Stop iteration if the collection is sorted.
    return collection

s = bubble_sort([3,2,1])
"""
tree = ast.parse(source_code, mode="exec")

with open("tree.ast","w") as f:
    f.write(ast.dump(tree, indent=4))
print(list(get_parameters(tree)))
print(get_return(tree))

finder = AssignFinder()
finder.visit(tree)
ast.fix_missing_locations(tree)
print(finder.assigns)


lines = [None] + source_code.splitlines()  
test_namespace = {}

for node in tree.body:
    wrapper = ast.Module(body=[node], type_ignores=[])
    co = compile(wrapper, "<ast>", 'exec')
    exec(co, test_namespace)

print(test_namespace.keys())