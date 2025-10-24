# src/ad2subnets/call_other_script.py
from pathlib import Path
import os
import sys
import importlib
import importlib.util
from contextlib import contextmanager

@contextmanager
def temp_argv(argv):
    old = sys.argv[:]
    sys.argv = argv
    try:
        yield
    finally:
        sys.argv = old

def _import_from_path(path, module_name="__adidnsdump__"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

def call_other_script_programmatically(args_list, module_path):
    """
    Call another script's main() as if from CLI.

    args_list: list[str] you would pass after the program name
    module_path: either a module name like 'adidnsdump' or a filesystem path to a .py file
    """
    # Decide how to import
    looks_like_path = (
        module_path.endswith(".py")
        or os.path.sep in module_path
        or (os.path.altsep and os.path.altsep in module_path)
    )

    if looks_like_path:
        mod = _import_from_path(module_path, module_name="__adidnsdump__")
        prog_name = module_path
    else:
        mod = importlib.import_module(module_path)
        prog_name = module_path

    if not hasattr(mod, "main"):
        raise AttributeError(f"{module_path} does not define main()")

    try:
        with temp_argv([prog_name] + list(args_list)):
            return mod.main()
    except SystemExit as e:
        if e.code not in (0, None):
            raise
        return None



def find_script(script):
    current_dir = Path(__file__).resolve().parent
    target = current_dir / "adidnsdump.py"

    if not target.exists():
        raise FileNotFoundError(f"adidnsdump.py not found in {current_dir}")

    return str(target)