from __future__ import annotations
from typing import Any, Callable

import FakeRPi.GPIO as GPIO # type: ignore

# from base import ZError, ZCommand, ActiveVars, ZValue, ZBool    # <- for debugging. Use importHandler for final Project!


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

importHandler(["ZError", "ZCommand", "ActiveVars", "ZValue", "ZBool"])


class gpio:
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        
        self.value = ZBool("~0")

        self.functionRegistry: dict[str, Callable[..., Any]] = {}

        if len(cmd.args) > 0 and cmd.args[0] != "":
            boardType: ZValue = ZValue()
            boardType.setValue(cmd.args[0], "PT", activeVars)
            
            match boardType.value:
                case "BCM":
                    GPIO.setmode(GPIO.BCM) # type: ignore
                case "BOARD":
                    GPIO.setmode(GPIO.BOARD) # type: ignore
                case _:
                    print("ERROR: wrong board Type. SUPPORTED: BCM/BOARD")
                    quit()
                

        self.registerFunc({self.SETUP: "", self.SET: "", self.READ: "", self.CLEAN: ""})


    def SETUP(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 1 and cmd.args[1] != "" and cmd.args[0] != "":
            pin: ZValue = ZValue()
            pin.setValue(cmd.args[0], "INT", activeVars)
            
            pinType: ZValue = ZValue()
            pinType.setValue(cmd.args[1], "PT", activeVars)

            match pinType.value:
                case "IN":
                    GPIO.setup(int(pin.value), GPIO.IN) # type: ignore
                case "OUT":
                    GPIO.setup(int(pin.value), GPIO.OUT) # type: ignore
                case _:
                    raise ZError(114)
        else:
            raise ZError(114)
    
    def SET(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        if len(cmd.args) > 0 and cmd.args[0] != "":
            pin: ZValue = ZValue()
            pin.setValue(cmd.args[0], "INT", activeVars)
            
            pinValue: ZBool = ZBool()
            pinValue.setValue(cmd.args[1])

            match pinValue.getBool():
                case True:
                    GPIO.output(int(pin.value), GPIO.HIGH) # type: ignore
                case False:
                    GPIO.output(int(pin.value), GPIO.LOW) # type: ignore

    def READ(self, cmd: ZCommand, activeVars: ActiveVars):
        pin: ZValue = ZValue()
        pin.setValue(cmd.args[0], "INT", activeVars)


        rawValue = GPIO.input(int(pin.value))# type: ignore

        match rawValue:
            case 1:
                self.value.setValue("~1")
            case 0:
                self.value.setValue("~0")
            case _: # type: ignore
                pass

    def CLEAN(self, cmd: ZCommand, activeVars: ActiveVars):
        GPIO.cleanup() #  type: ignore


    def onChange(self) -> str:
        return self.value.value

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
    return {"": gpio}