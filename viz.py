import importlib
import time
import sys
import os
import cmd
from nubia import Nubia, Options, command, context, argument, PluginInterface, eventbus
from nubia.internal.cmdbase import AutoCommand
from termcolor import cprint

def get_functions(module):
    return [f for f in dir(module) if not f.startswith("__")]

@command("test")
def test():
    "Lets me mess around with Nubia"
    ctx = context.get_context()
    print(ctx.sort)
    print(ctx.sort_name)

@command("sort")
def sort():
    "Visualizes the selected sort"
    ctx = context.get_context()

    to_sort = ctx.unsorted[:]
    cprint(f"{to_sort} -> {ctx.sort(to_sort)}", "cyan")
    cprint(f"\tvia {ctx.sort_name}", "yellow")

@command("find_sort")
@argument("module_name", description="the module to get a sort from", positional=True)
def find_sort(module_name: str):
    "Finds a sort function in a given module"
    ctx = context.get_context()

    module = importlib.import_module("sorts." + module_name)
    funcs = get_functions(module)
    if len(funcs) != 1:
        raise SortModuleError("Too many functions in sort file! (Should be 1)")
    ctx.sort = getattr(module, funcs[0])
    ctx.sort_name = module_name


class NubiaFunctionContext(context.Context):
    def __init__(self):
        self.sort = None
        self.sort_name = None
        self.unsorted = list(range(10,0,-1))
        super().__init__()

    def on_connected(self, *args, **kwargs):
        pass

    def on_cli(self, cmd, args):
        self.funcs = {}
        # dispatch the on connected message
        self.verbose = args.verbose
        self.registry.dispatch_message(eventbus.Message.CONNECTED)

    def on_interactive(self, args):
        self.verbose = args.verbose
        ret = self._registry.find_command("connect").run_cli(args)
        if ret:
            raise exceptions.CommandError("Failed starting interactive mode")
        # dispatch the on connected message
        self.registry.dispatch_message(eventbus.Message.CONNECTED)

class Plugin(PluginInterface):
    def create_context(self):
        return NubiaFunctionContext()

    def get_commands(self):
        return [
            AutoCommand(test),
            AutoCommand(find_sort),
            AutoCommand(sort),
        ]

if __name__ == "__main__":

    cli = cmd.Cmd()
    plugin = Plugin()
    shell = Nubia(
            name="CLIviz",
            plugin=plugin,
            options=Options(persistent_history=False, 
                auto_execute_single_suggestions=True)
            )
    sys.exit(shell.run())