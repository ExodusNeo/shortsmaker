"""For tests that swap shortsmaker functions by name: which module owns each one."""
import importlib
import pkgutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import shortsmaker  # noqa: E402

MODULES = [importlib.import_module(f"shortsmaker.{i.name}") for i in pkgutil.iter_modules(shortsmaker.__path__)]
# Built on import, before any test installs a fake. Other modules call a function as `owner.name`, so a fake set on
# its owner reaches every caller.
OWNER = {name: mod for mod in MODULES for name, obj in vars(mod).items()
         if callable(obj) and getattr(obj, "__module__", None) == mod.__name__}


def owner(name: str):
    """The module that defines function `name` (KeyError for anything else)."""
    return OWNER[name]
