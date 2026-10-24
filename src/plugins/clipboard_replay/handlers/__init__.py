from .base import ClipboardHandler
from .openms import OpenmsHandler
from .saolei import SaoleiHandler
from .classic95 import Classic95Handler


HANDLER_TYPES = (OpenmsHandler, SaoleiHandler, Classic95Handler)

__all__ = ["ClipboardHandler", "HANDLER_TYPES"]
