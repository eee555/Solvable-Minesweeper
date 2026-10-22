from .base import ClipboardHandler
from .openms import OpenmsHandler
from .saolei import SaoleiHandler


HANDLER_TYPES = (OpenmsHandler, SaoleiHandler)

__all__ = ["ClipboardHandler", "HANDLER_TYPES"]