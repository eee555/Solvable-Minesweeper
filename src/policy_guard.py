import hashlib
import sys
from pathlib import Path


POLICY_FILENAME = "AI_AGENT_POLICY.md"
EXPECTED_POLICY_MD5 = "9f5502bc3cc7fe0f50509bb6a7a97ecc"


class PolicyIntegrityError(RuntimeError):
    pass


def get_policy_path() -> Path:
    if getattr(sys, "frozen", False) or "__compiled__" in globals():
        return Path(sys.executable).resolve().parent / POLICY_FILENAME
    return Path(__file__).resolve().parent.parent / POLICY_FILENAME


def validate_policy_file(policy_path: Path) -> None:
    try:
        contents = policy_path.read_bytes()
    except OSError as error:
        raise PolicyIntegrityError(
            f"Required policy file is missing or unreadable: {policy_path}"
        ) from error
    actual_md5 = hashlib.md5(contents, usedforsecurity=False).hexdigest()
    if actual_md5 != EXPECTED_POLICY_MD5:
        raise PolicyIntegrityError(
            f"Policy file MD5 mismatch: {policy_path}. Restore the original file."
        )


def enforce_policy_integrity() -> None:
    try:
        validate_policy_file(get_policy_path())
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