from __future__ import annotations
from typing import Any, Callable
import sys
from pathlib import Path


# from base import ZError, ZCommand, ActiveVars, ZValue, ZBool    # <- for debugging. Use importHandler for final Project!


def importHandler(names: list[str]):
    import importlib.util
    from pathlib import Path
    import sys

    base_path = Path(__file__).resolve().parent / "base.py"

    moduleName = base_path.stem

    spec = importlib.util.spec_from_file_location(moduleName, base_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create spec for {base_path}")


    base = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = base
    spec.loader.exec_module(base)

    for name in names:
        globals()[name] = getattr(base, name)

importHandler(["ZError", "ZCommand", "ActiveVars", "ZValue", "ZBool"])


class system:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        

        self.functionRegistry: dict[str, Callable[..., Any]] = {}
                

        self.registerFunc({self.quit: "", self.getCWD: ""})


    def quit(self, cmd: ZCommand, activeVars: ActiveVars):
        errorCode = ZValue("0")

        if cmd.args[0] != "":
            errorCode.setValue(cmd.args[0], "INT", activeVars)

        sys.exit(int(errorCode.value))

    def getCWD(self, cmd:ZCommand, activeVars: ActiveVars) -> ActiveVars:
        varName = ZValue()

        if cmd.args[0] != "":
            varName.setValue(cmd.args[0], "PT", activeVars)
        
        path = Path.cwd()
        path = path.absolute()

        activeVars[varName.value].value.value = str(path)

        return activeVars

    def registerFunc(self, funcList: dict[Callable[..., Any], str]) -> None:
        """
        Register a function for a type. Its added to the functionRegistry

        Args:
            func (Callable[..., Any]): The function to generate the docstring for.
            name (Optional[str]): The name to use in the docstring. If not provided, the function's name will be used.

        """
        for func, name in funcList.items():
            if name:
                self.functionRegistry[name] = func
            else:
                self.functionRegistry[func.__name__] = func
 

def load() -> dict[str, type]:
    return {"": system}