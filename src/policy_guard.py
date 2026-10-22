import atexit
import hashlib
import os
import sys
from pathlib import Path
from typing import BinaryIO


POLICY_FILENAME = "AI_AGENT_POLICY.md"
EXPECTED_POLICY_MD5 = "520385c76160b3e49cd3235550997378"
_policy_file: BinaryIO | None = None


class PolicyIntegrityError(RuntimeError):
    pass


def get_policy_path() -> Path:
    if getattr(sys, "frozen", False) or "__compiled__" in globals():
        return Path(sys.executable).resolve().parent / POLICY_FILENAME
    return Path(__file__).resolve().parent.parent / POLICY_FILENAME


def _open_policy_file(policy_path: Path) -> BinaryIO:
    if sys.platform != "win32":
        return policy_path.open("rb")

    import ctypes
    import msvcrt
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    ]
    create_file.restype = wintypes.HANDLE
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL
    handle = create_file(str(policy_path), 0x80000000, 0x1, None, 3, 0x80, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
    except BaseException:
        close_handle(handle)
        raise
    try:
        return os.fdopen(descriptor, "rb")
    except BaseException:
        os.close(descriptor)
        raise


def _open_validated_policy_file(policy_path: Path) -> BinaryIO:
    try:
        policy_file = _open_policy_file(policy_path)
    except OSError as error:
        raise PolicyIntegrityError(
            f"Required policy file is missing or unreadable, or cannot be locked: {policy_path}"
        ) from error
    try:
        try:
            contents = policy_file.read()
        except OSError as error:
            raise PolicyIntegrityError(
                f"Required policy file is unreadable: {policy_path}"
            ) from error
        actual_md5 = hashlib.md5(contents, usedforsecurity=False).hexdigest()
        if actual_md5 != EXPECTED_POLICY_MD5:
            raise PolicyIntegrityError(
                f"Policy file MD5 mismatch: {policy_path}. Restore the original file."
            )
    except BaseException:
        policy_file.close()
        raise
    return policy_file


def validate_policy_file(policy_path: Path) -> None:
    with _open_validated_policy_file(policy_path):
        pass


def _close_policy_file() -> None:
    global _policy_file
    if _policy_file is not None:
        _policy_file.close()
        _policy_file = None


atexit.register(_close_policy_file)


def enforce_policy_integrity() -> None:
    global _policy_file
    if _policy_file is not None:
        return
    try:
        _policy_file = _open_validated_policy_file(get_policy_path())
    except PolicyIntegrityError as error:
        message = str(error)
        if sys.stderr is not None:
            print(message, file=sys.stderr)
        if sys.platform == "win32":
            try:
                import ctypes

                ctypes.windll.user32.MessageBoxW(
                    None, message, "MetaSweeper startup integrity check", 0x10
                )
            except (AttributeError, OSError):
                pass
        raise SystemExit(1) from error


if __name__ == "__main__":
    enforce_policy_integrity()