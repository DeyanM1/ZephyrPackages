from __future__ import annotations

import math
from typing import Any, Callable

# from base import ZCommand, ActiveVars    # <- for debugging. Use importHandler for final Project!


def importHandler(names: list[str]):
    import importlib.util
    from pathlib import Path
    import sys

    base_path = Path(__file__).resolve().parent / "base.py"
    print(base_path)

    moduleName = base_path.stem

    spec = importlib.util.spec_from_file_location(moduleName, base_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create spec for {base_path}")


    base = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = base
    spec.loader.exec_module(base)

    for name in names:
        globals()[name] = getattr(base, name)

importHandler(["ZCommand", "ActiveVars"])


class MoreMath:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        
        self.functionRegistry: dict[str, Callable[..., Any]] = {}

        self.registerFunc({self.fact: "", self.abs: "", self.setPI: "", self.sqrt: ""})

    def fact(self, cmd: ZCommand, activeVars: ActiveVars):
        var1 = activeVars.get(cmd.args[0])

        var1.value.setValue(str(math.factorial(float(var1.value.value))), "FLOAT", activeVars) # type: ignore

        activeVars.update({var1.name: var1}) # type: ignore
        return activeVars

    def abs(self, cmd: ZCommand, activeVars: ActiveVars):
        var1 = activeVars.get(cmd.args[0])
        var1.value.setValue(str(abs(float(var1.value.value))), "FLOAT", activeVars)  # type: ignore

        activeVars.update({var1.name: var1}) # type: ignore
        return activeVars

    def setPI(self, cmd: ZCommand, activeVars: ActiveVars):
        var1 = activeVars.get(cmd.args[0])
        var1.value.setValue(str(math.pi), "FLOAT", activeVars)  # type: ignore

        activeVars.update({var1.name: var1}) # type: ignore
        return activeVars

    def sqrt(self, cmd: ZCommand, activeVars: ActiveVars):
        var1 = activeVars.get(cmd.args[0])
        var1.value.setValue(str(math.sqrt(float(var1.value.value))), "FLOAT", activeVars)  # type: ignore

        activeVars.update({var1.name: var1}) # type: ignore
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
    return {"": MoreMath}