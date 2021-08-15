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
    print(dir(ctx))
    ctx.funcs["func"] = "funky"
    print(ctx.funcs)

@command("find_sort")
@argument("module_name", description="the module to get a sort from", positional=True)
def find_sort(module_name):
    "Finds a sort function in a given module"
    module = importlib.import_module("sorts." + module_name)
    funcs = get_functions(module)
    if len(funcs) != 1:
        raise SortModuleError("Too many functions in sort file! (Should be 1)")
    return getattr(module, funcs[0])

class NubiaFunctionContext(context.Context):
    def __init__(self):
        self.funcs = {}
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
        ]

if __name__ == "__main__":

    cli = cmd.Cmd()

    #LIB_NAME = "bubble_sort"
    #lib = LIB_NAME if LIB_NAME else input("File to get sort from: ")

    #unsorted = list(range(100,0,-1))

    #start = time.process_time()
    #print(sort(unsorted), sep=",")
    #print(f"Processing time: {time.process_time() - start}")

    plugin = Plugin()
    shell = Nubia(
            name="CLIviz",
            #command_pkgs=commands,
            plugin=plugin,
            options=Options(persistent_history=False, 
                auto_execute_single_suggestions=True)
            )
    sys.exit(shell.run())