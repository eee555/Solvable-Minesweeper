import sys
from pathlib import Path


def get_runtime_mode() -> str:
    if getattr(sys, "frozen", False):
        return "pyinstaller"
    if "__compiled__" in globals():
        return "nuitka"
    return "source"


def get_executable_dir() -> Path:
    if get_runtime_mode() == "source":
        return Path(__file__).resolve().parent.parent
    return Path(sys.executable).resolve().parent


def resource_path(relative_path: str) -> Path:
    if get_runtime_mode() == "pyinstaller":
        base_path = Path(getattr(sys, "_MEIPASS", get_executable_dir()))
    else:
        base_path = get_executable_dir()
    return base_path / relative_path
