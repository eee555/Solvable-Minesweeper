from __future__ import annotations

import copy
import math
from typing import Callable

from config.constants import GAME_EVENT_STATE_MAP
from shared_types.commands import MouseClickCommand, NewGameCommand
from shared_types.events import BoardUpdateEvent, GameStatusChangeEvent

from .mcp_server import failure

STATUS_NAMES: dict[int, str] = {}
for state_name, state_number in GAME_EVENT_STATE_MAP.items():
    STATUS_NAMES.setdefault(state_number, state_name)

TOOLS = [
    {"name": "get_board_state", "description": "Read only the visible board received through official SDK events.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
     "annotations": {"readOnlyHint": True, "openWorldHint": False}},
    {"name": "click_cell", "description": "Click a visible-board cell with explicit user-granted SDK permission.",
     "inputSchema": {"type": "object", "properties": {
         "row": {"type": "integer", "minimum": 0}, "col": {"type": "integer", "minimum": 0},
         "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"}},
         "required": ["row", "col"], "additionalProperties": False},
     "annotations": {"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False,
                     "openWorldHint": False}},
    {"name": "start_new_game", "description": "Start a game only when no game is in progress; default difficulty medium.",
     "inputSchema": {"type": "object", "properties": {
         "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"], "default": "medium"}},
         "additionalProperties": False},
     "annotations": {"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False,
                     "openWorldHint": False}},
]


class FunctionRegistry:
    def __init__(self, has_auth: Callable, request: Callable):
        self.has_auth = has_auth
        self.request = request
        self.board: dict | None = None
        self.status: int | None = None

    def update_board(self, event: BoardUpdateEvent) -> None:
        self.board = None
        rows, cols = event.rows, event.cols
        if (type(rows) is not int or type(cols) is not int or rows <= 0 or cols <= 0
                or rows * cols > 65536 or not isinstance(event.game_board, list)
                or len(event.game_board) != rows):
            return
        cells = []
        mapping = {10: -1, 11: "F", 14: "X", 15: "M", 16: "m"}
        for row in event.game_board:
            if not isinstance(row, list) or len(row) != cols:
                return
            if any(type(cell) is not int for cell in row):
                return
            cells.append(
                [cell if 0 <= cell <= 8 else mapping.get(cell, -1) for cell in row])
        if (type(event.mines_remaining) is not int
                or type(event.game_time) not in (int, float) or not math.isfinite(event.game_time)):
            return
        self.board = {"rows": rows, "cols": cols, "cells": cells,
                      "mines_remaining": event.mines_remaining, "game_time": event.game_time}

    def update_status(self, event: GameStatusChangeEvent) -> None:
        previous = self.status
        self.status = event.current_status if type(
            event.current_status) is int else None
        if self.status not in (1, 2, 3, 4) or (self.status == 1 and previous not in (None, 1)):
            self.board = None

    def execute_function(self, name: str, arguments: dict) -> dict:
        if not isinstance(arguments, dict):
            return failure("Arguments must be an object")
        if name == "get_board_state":
            if arguments:
                return failure("get_board_state accepts no arguments")
            if self.board is None or self.status not in STATUS_NAMES:
                return failure("Visible board/status unavailable; enable board events and wait for an SDK event")
            return {"success": True, **copy.deepcopy(self.board), "game_status": STATUS_NAMES[self.status]}
        if name == "click_cell":
            if set(arguments) - {"row", "col", "button"} or not {"row", "col"} <= arguments.keys():
                return failure("Expected row, col, and optional button only")
            row, col, button = arguments["row"], arguments["col"], arguments.get(
                "button", "left")
            if type(row) is not int or type(col) is not int:
                return failure("Coordinates must be integers, not booleans or strings")
            if not isinstance(button, str) or button not in ("left", "right", "middle"):
                return failure("Unknown button; use left, right, or middle")
            if self.board is None or self.status not in (1, 2):
                return failure("No actionable visible board; wait for SDK events")
            if not (0 <= row < self.board["rows"] and 0 <= col < self.board["cols"]):
                return failure("Coordinates out of bounds")
            command = MouseClickCommand(row=row, col=col, button={
                                        "left": 0, "middle": 1, "right": 2}[button])
        elif name == "start_new_game":
            if set(arguments) - {"difficulty"}:
                return failure("Expected optional difficulty only")
            difficulty = arguments.get("difficulty", "medium")
            if not isinstance(difficulty, str) or difficulty not in ("easy", "medium", "hard"):
                return failure("Unknown difficulty; use easy, medium, or hard")
            if self.status not in (1, 3, 4) or self.board is None:
                return failure("Cannot replace a playing, unknown, or unavailable game")
            command = NewGameCommand(
                level={"easy": 3, "medium": 4, "hard": 5}[difficulty])
        else:
            return failure("Unknown tool")
        if not self.has_auth(type(command)):
            return failure("Official SDK control permission not granted to this plugin; reauthorize it")
        try:
            response = self.request(command, timeout=3.0)
        except Exception:
            self.board = None
            if name == "start_new_game":
                self.status = None
            return failure("Command result unknown; do not retry automatically; wait for SDK events", "unknown")
        if response is None:
            self.board = None
            return failure("No command confirmation; result unknown; do not retry automatically", "unknown")
        if not response.success:
            return failure(response.error or "Main process rejected command; check its control switches")
        self.board = None
        if name == "start_new_game":
            self.status = None
        return {"success": True, "outcome": "confirmed", "message": "Main process confirmed; wait for fresh board events"}
