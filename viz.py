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

#collection = [3,2,1]
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
"""
tree = ast.parse(source_code, mode="exec")#, type_comments=True)
print(dir(tree))

with open("tree.ast","w") as f:
    f.write(ast.dump(tree, indent=4))


lines = [None] + source_code.splitlines()  
namespace = {"collection": [3,2,1]}

for node in tree.body[0].body:
    wrapper = ast.Module(body=[node], type_ignores=[])
    try: 
        co = compile(wrapper, "<ast>", 'exec')
        exec(co, namespace)
        for key in namespace.keys():
            if not key.startswith("__"):
                print(f"{key}: {namespace[key]}", end=", ")
        print()
    except:
        print("nah")


"""
print(list(get_parameters(tree)))
print(get_return(tree))

finder = AssignFinder()
finder.visit(tree)
ast.fix_missing_locations(tree)
print(finder.assigns)
"""