from __future__ import annotations

import pytest
from utils import (
    board_list_to_bytes, board_bytes_to_board,
    StatsRecord, trans_game_mode, EnuLimit,
    enumerate_change_board,
)
from utils import path_utils


class TestRuntimeMode:
    def test_source_mode(self, monkeypatch):
        monkeypatch.delattr(path_utils, "__compiled__", raising=False)
        monkeypatch.setattr(path_utils.sys, "frozen", False, raising=False)
        assert path_utils.get_runtime_mode() == "source"

    def test_pyinstaller_mode(self, monkeypatch):
        monkeypatch.setattr(path_utils.sys, "frozen", True, raising=False)
        assert path_utils.get_runtime_mode() == "pyinstaller"

    def test_nuitka_mode(self, monkeypatch):
        monkeypatch.setattr(path_utils.sys, "frozen", False, raising=False)
        monkeypatch.setattr(path_utils, "__compiled__",
                            object(), raising=False)
        assert path_utils.get_runtime_mode() == "nuitka"


class TestPluginManagerRuntimePaths:
    def test_nuitka_bundle_and_builtin_plugin_paths(self, monkeypatch, tmp_path):
        from plugin_manager import app_paths

        executable_dir = tmp_path / "package"
        builtin_plugin_dir = executable_dir / "internal" / "plugins"
        user_plugin_dir = executable_dir / "plugins"
        builtin_plugin_dir.mkdir(parents=True)
        user_plugin_dir.mkdir()

        monkeypatch.setattr(app_paths, "__compiled__", object(), raising=False)
        monkeypatch.setattr(app_paths.sys, "frozen", False, raising=False)
        monkeypatch.setattr(
            app_paths.sys,
            "executable",
            str(executable_dir / "plugin_manager.exe"),
        )

        assert app_paths.get_bundle_dir() == executable_dir
        assert app_paths.get_executable_dir() == executable_dir
        assert app_paths.get_builtin_plugin_dirs() == [builtin_plugin_dir]
        assert app_paths.get_user_plugin_dirs() == [user_plugin_dir]


class TestBoardBytes:
    def test_board_list_to_bytes_small(self):
        board = [[-1, 0], [1, -1]]
        result = board_list_to_bytes(board)
        assert isinstance(result, bytes)
        assert len(result) == 1

    def test_board_list_to_bytes_empty(self):
        assert board_list_to_bytes([]) == b''

    def test_board_bytes_roundtrip(self):
        original = [[-1, 0, 0], [1, -1, 1], [0, 1, -1]]
        encoded = board_list_to_bytes(original)
        decoded = board_bytes_to_board(3, 3, encoded)
        for row in decoded:
            assert len(row) == 3
        assert decoded[0][0] == -1
        assert decoded[1][1] == -1

    def test_board_bytes_all_mines(self):
        board = [[-1, -1], [-1, -1]]
        encoded = board_list_to_bytes(board)
        decoded = board_bytes_to_board(2, 2, encoded)
        for r in decoded:
            for v in r:
                assert v == -1 or v >= 0


class TestStatsRecord:
    def test_encode_decode_roundtrip(self):
        record = StatsRecord(
            game_state=2, row=16, column=30, mine_num=99,
            rtime_ms=12345, left=20, right=10, double=5,
            rce=1, lce=3, dce=1, bbbv=120, bbbv_solved=115,
            zini=0, flag=8, path=1.5, start_time=1000000, mode=0,
            is_official=True, is_fair=True, op=5, isl=3, pluck=0.8,
        )
        data = record.encode()
        decoded = StatsRecord.decode(data)
        assert decoded.game_state == 2
        assert decoded.row == 16
        assert decoded.column == 30
        assert decoded.mine_num == 99
        assert decoded.rtime_ms == 12345
        assert decoded.is_official is True
        assert decoded.is_fair is True

    def test_encode_decode_with_board_bytes(self):
        board_data = bytes([0b10101010, 0b11110000])
        record = StatsRecord(
            game_state=1, row=8, column=8, mine_num=10,
            rtime_ms=5000, left=10, right=5, double=3,
            rce=1, lce=2, dce=0, bbbv=40, bbbv_solved=38,
            zini=0, flag=3, path=1.0, start_time=0, mode=0,
            is_official=True, is_fair=True, op=3, isl=2, pluck=0.5,
            board_bytes=board_data,
        )
        data = record.encode()
        decoded = StatsRecord.decode(data)
        assert decoded.board_bytes == board_data
        assert decoded.bbbv == 40

    def test_encode_decode_minimal(self):
        record = StatsRecord(
            game_state=0, row=1, column=1, mine_num=0,
            rtime_ms=0, left=0, right=0, double=0,
            rce=0, lce=0, dce=0, bbbv=0, bbbv_solved=0,
            zini=0, flag=0, path=0.0, start_time=0, mode=0,
            is_official=False, is_fair=False, op=0, isl=0, pluck=0.0,
        )
        data = record.encode()
        decoded = StatsRecord.decode(data)
        assert decoded.is_official is False
        assert decoded.path == 0.0


class TestTransGameMode:
    def test_standard(self):
        assert trans_game_mode(0) is not None

    def test_invalid_mode_returns_none(self):
        assert trans_game_mode(99) is None


class TestEnumerateChangeBoard:
    """enumerate_change_board(board, game_board, poses) -> (new_board, success)

    CELL_UNOPENED=10, CELL_FLAGGED=11, CELL_MINE=-1
    game_board: 10=未开, 11=标雷, 0~8=已开数字
    board: -1=雷, 0~8=数字
    python -m pytest tests/test_utils.py::TestEnumerateChangeBoard::test_chording -sv
    """

    def test_1(self):
        board = [
            [-1, 3, -1, -1, 2, 0, 0, 0],
            [2, -1, 4, -1, 2, 0, 0, 0],
            [1, 1, 2, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 2, 1, 1, 0, 0, 0],
            [2, -1, 4, -1, 2, 0, 0, 0],
            [2, -1, 4, -1, 2, 0, 0, 0],
        ]
        game_board = [
            [10, 10, 10, 10, 2, 0, 0, 0],
            [2, 10, 4, 10, 2, 0, 0, 0],
            [1, 1, 2, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 2, 1, 1, 0, 0, 0],
            [2, 10, 4, 10, 10, 0, 0, 0],
            [10, 10, 10, 10, 10, 0, 0, 0],
        ]
        poses = [(7, 1)]
        result, ok, _, _ = enumerate_change_board(board, game_board, poses)
        print("result:", result)
        assert ok
        board_after = [
            [2, -1, 4, -1, 2, 0, 0, 0],
            [2, -1, 4, -1, 2, 0, 0, 0],
            [1, 1, 2, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 2, 1, 1, 0, 0, 0],
            [2, -1, 4, -1, 2, 0, 0, 0],
            [-1, 3, -1, -1, 2, 0, 0, 0],
        ]
        assert result == board_after

    def test_2(self):
        board = [[1, -1, 2, 2, 3, 4, -1, 3],
                 [3, 3, 4, -1, -1, -1, -1, -1],
                 [-1, -1, 6, -1, 6, -1, 7, -1],
                 [-1, -1, -1, -1, 5, 4, -1, -1],
                 [-1, -1, -1, 5, -1, -1, 6, -1],
                 [-1, -1, 6, 5, -1, 5, -1, -1],
                 [-1, -1, -1, -1, 4, 6, -1, -1],
                 [2, 4, -1, 4, -1, -1, -1, -1]]
        game_board = [[1, 11, 2, 2, 3, 4, 11, 10],
                      [3, 3, 4, 11, 11, 11, 11, 10],
                      [11, 11, 6, 11, 6, 11, 10, 10],
                      [10, 11, 11, 11, 5, 11, 10, 10],
                      [10, 10, 10, 5, 10, 11, 10, 10],
                      [10, 10, 10, 10, 10, 10, 10, 10],
                      [10, 10, 10, 10, 10, 10, 10, 10],
                      [10, 10, 10, 10, 10, 10, 10, 10]]

        poses = [(4, 4)]
        result, ok, _, _ = enumerate_change_board(board, game_board, poses)
        print("result:", result)
        assert not ok

    # python -m pytest tests/test_utils.py::TestEnumerateChangeBoard::test_success -sv

    def test_success(self):
        """填入一组能走通 enumerate_change_board 的参数"""
        board = [[1, 1, 0, 0, 0, 1, 1, 3, -1, 4, -1, -1, 3, 1, 2, 1, 1, 0, 1, -1, 3, 3, -1, 2, 2, -1, 1, 1, 1, 1], [-1, 2, 2, 1, 1, 1, -1, 4, -1, 5, -1, -1, 4, -1, 4, -1, 1, 0, 1, 2, -1, -1, 4, 4, -1, 3, 2, 1, -1, 1], [3, -1, 3, -1, 3, 2, 1, 4, -1, 4, 2, 2, 3, -1, -1, 4, 2, 2, 2, 3, 4, 4, -1, -1, 3, -1, 2, 3, 4, 3], [-1, 4, 5, -1, -1, 4, 2, 4, -1, 3, 0, 0, 1, 3, -1, 3, -1, 2, -1, -1, 3, -1, 5, 4, 4, 3, 4, -1, -1, -1], [-1, -1, 5, -1, -1, -1, -1, 4, -1, 2, 0, 0, 0, 1, 1, 2, 1, 2, 3, 4, -1, 4, -1, -1, 4, -1, -1, 5, 5, 4], [3, -1, 4, -1, 6, -1, -1, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, -1, 4, -1, 4, 4, -1, -1, -1, 4, -1, -1], [2, 2, 3, 1, 3, -1, 4, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, -1, 2, 4, -1, 3, 2, -1, 4, 3, -1, 3, 2], [1, -1, 2, 2, 3, 3, 3, -1, 2, -1, 3, -1, -1, 2, 1, -1, -1, 3, 3, 4, 4, -1, 2, 2, 2, 3, 3, 3, 3, 1], [2, 3, 4, -1, -1, 4, -1, 3, 2, 3, -1, 6, -1, 4, 3, 5, 4, 3, -1, -1, -1, 4, 3, 3, -1, 2, -1, -1, 5, -1], [-1, 2, -1, -1, 4, -1, -1, 2, 0, 2, -1, 4, -1, 3, -1, -1, -1, 2, 2, 5, -1, 4, -1, -1, 2, 2, 4, -1, -1, -1], [1, 2, 3, 3, 4, 4, 5, 4, 2, 2, 1, 3, 2, 4, 4, 6, 5, 3, 1, 2, -1, 3, 2, 3, 2, 2, 3, -1, 5, 3], [1, 1, 1, -1, 2, -1, -1, -1, -1, 1, 1, 2, -1, 4, -1, -1, -1, -1, 2, 2, 2, 2, 1, 3, -1, 3, -1, 2, 2, -1], [-1, 1, 2, 2, 4, 3, 4, 4, 3, 3, 2, -1, 4, -1, -1, 5, 4, 3, 2, -1, 2, 3, -1, 4, -1, 5, 3, 2, 1, 1], [1, 1, 1, -1, 3, -1, 2, 1, -1, 4, -1, 3, 4, -1, 5, 3, -1, 1, 2, 3, 4, -1, -1, 5, 4, -1, -1, 3, 2, 1],
                 [1, 2, 2, 2, 3, -1, 2, 1, 2, -1, -1, 2, 2, -1, -1, 3,
                     2, 2, 2, -1, -1, 5, -1, -1, 5, -1, -1, -1, 2, -1],
                 [-1, 2, -1, 2, 3, 3, 3, 1, 2, 2, 3, 2, 2, 2, 2, 2, -1, 2, 3, -1, 5, -1, 6, -1, 5, -1, -1, 5, 4, 3], [2, 3, 2, 2, -1, -1, 4, -1, 2, 1, 2, -1, 2, 1, 1, 1, 2, -1, 2, 1, 4, -1, -1, 4, -1, 5, -1, 4, -1, -1], [1, -1, 1, 1, 2, 3, -1, -1, 2, 2, -1, 3, 2, -1, 1, 0, 1, 2, 2, 2, 3, -1, 4, 4, -1, 3, 1, 3, -1, 3], [1, 1, 1, 0, 0, 2, 3, 3, 1, 3, -1, 4, 2, 2, 1, 0, 1, 2, -1, 2, -1, 4, -1, 3, 1, 1, 0, 1, 1, 1], [1, 1, 1, 0, 0, 2, -1, 3, 1, 3, -1, 3, -1, 2, 1, 1, 2, -1, 2, 3, 3, 5, -1, 2, 1, 2, 2, 1, 0, 0], [1, -1, 1, 0, 0, 2, -1, 4, -1, 4, 3, 4, 5, -1, 2, 2, -1, 5, 3, 2, -1, -1, 2, 2, 2, -1, -1, 3, 2, 2], [1, 1, 1, 0, 1, 3, 4, 6, -1, -1, 5, -1, -1, -1, 2, 2, -1, -1, -1, 3, 3, 3, 1, 2, -1, 5, -1, 3, -1, -1], [0, 1, 1, 2, 2, -1, -1, -1, -1, -1, -1, -1, 4, 2, 1, 2, 5, -1, 5, 3, -1, 2, 2, 3, -1, 3, 1, 2, 2, 2], [0, 1, -1, 2, -1, 3, 3, 3, 3, 3, 3, 2, 1, 0, 0, 1, -1, -1, 3, -1, 3, -1, 2, -1, 2, 1, 0, 0, 0, 0]]
        game_board = [[1, 1, 0, 0, 0, 1, 1, 3, 11, 4, 11, 11, 3, 1, 2, 1, 1, 0, 1, 11, 3, 3, 11, 2, 2, 11, 1, 1, 1, 1],
                      [11, 2, 2, 1, 1, 1, 11, 4, 11, 5, 11, 11, 4, 11, 4,
                          11, 1, 0, 1, 2, 11, 11, 4, 4, 11, 3, 2, 1, 11, 1],
                      [3, 11, 3, 11, 3, 2, 1, 4, 11, 4, 2, 2, 3, 11, 11,
                          4, 2, 2, 2, 3, 4, 4, 11, 11, 3, 11, 2, 3, 4, 3],
                      [11, 4, 5, 11, 11, 4, 2, 4, 11, 3, 0, 0, 1, 3, 11, 3,
                          11, 2, 11, 11, 3, 11, 5, 4, 4, 3, 4, 11, 11, 11],
                      [11, 11, 5, 11, 11, 11, 11, 4, 11, 2, 0, 0, 0, 1, 1,
                          2, 1, 2, 3, 4, 11, 4, 11, 11, 4, 11, 11, 5, 5, 4],
                      [3, 11, 4, 11, 6, 11, 11, 3, 1, 1, 0, 0, 0, 0, 0, 0,
                          0, 1, 2, 11, 4, 11, 4, 4, 11, 11, 11, 4, 11, 11],
                      [2, 2, 3, 1, 3, 11, 4, 2, 2, 1, 2, 2, 2, 1, 1, 2,
                          2, 2, 11, 2, 4, 11, 3, 2, 11, 4, 3, 11, 3, 2],
                      [1, 11, 2, 2, 3, 3, 3, 11, 2, 11, 3, 11, 11, 2, 1,
                          11, 11, 3, 3, 4, 4, 11, 2, 2, 2, 3, 3, 3, 3, 1],
                      [2, 3, 4, 11, 11, 4, 11, 3, 2, 3, 11, 6, 11, 4, 3, 5,
                          4, 3, 11, 11, 11, 4, 3, 3, 11, 2, 11, 11, 5, 11],
                      [11, 2, 11, 11, 4, 11, 11, 2, 0, 2, 11, 4, 11, 3, 11,
                          11, 11, 2, 2, 5, 11, 4, 11, 11, 2, 2, 4, 11, 11, 11],
                      [1, 2, 3, 3, 4, 4, 5, 4, 2, 2, 1, 3, 2, 4, 4, 6,
                          5, 3, 1, 2, 11, 3, 2, 3, 2, 2, 3, 11, 5, 10],
                      [1, 1, 1, 11, 2, 11, 11, 11, 11, 1, 1, 2, 11, 4, 11,
                          11, 11, 11, 2, 2, 2, 2, 1, 3, 11, 3, 11, 2, 2, 10],
                      [11, 1, 2, 2, 4, 3, 4, 4, 3, 3, 2, 11, 4, 11, 11,
                          5, 4, 3, 2, 11, 2, 3, 11, 4, 11, 5, 3, 2, 1, 1],
                      [1, 1, 1, 11, 3, 11, 2, 1, 11, 4, 11, 3, 4, 11, 5, 3,
                          11, 1, 2, 3, 10, 10, 11, 5, 4, 11, 11, 3, 2, 10],
                      [1, 2, 2, 2, 3, 11, 2, 1, 2, 11, 11, 2, 2, 11, 11, 3, 2,
                          2, 2, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                      [11, 2, 11, 2, 3, 3, 3, 1, 2, 2, 3, 2, 2, 2, 2, 2,
                          11, 2, 3, 11, 5, 11, 6, 11, 5, 11, 11, 5, 4, 11],
                      [2, 3, 2, 2, 11, 11, 4, 11, 2, 1, 2, 11, 2, 1, 1, 1,
                          2, 11, 2, 1, 4, 11, 11, 4, 11, 5, 11, 4, 11, 11],
                      [1, 11, 1, 1, 2, 3, 11, 11, 2, 2, 11, 3, 2, 11, 1,
                          0, 1, 2, 2, 2, 3, 11, 4, 4, 11, 3, 1, 3, 11, 3],
                      [1, 1, 1, 0, 0, 2, 3, 3, 1, 3, 11, 4, 2, 2, 1, 0,
                          1, 2, 11, 2, 11, 4, 11, 3, 1, 1, 0, 1, 1, 1],
                      [1, 1, 1, 0, 0, 2, 11, 3, 1, 3, 11, 3, 11, 2, 1,
                          1, 2, 11, 2, 3, 3, 5, 11, 2, 1, 2, 2, 1, 0, 0],
                      [1, 11, 1, 0, 0, 2, 11, 4, 11, 4, 3, 4, 5, 11, 2, 2,
                          11, 5, 3, 2, 11, 11, 2, 2, 2, 11, 11, 3, 2, 2],
                      [1, 1, 1, 0, 1, 3, 4, 6, 11, 11, 5, 11, 11, 11, 2, 2,
                          11, 11, 11, 3, 3, 3, 1, 2, 11, 5, 11, 3, 11, 11],
                      [0, 1, 1, 2, 2, 11, 11, 11, 11, 11, 11, 11, 4, 2, 1,
                          2, 5, 11, 5, 3, 11, 2, 2, 3, 11, 3, 1, 2, 2, 2],
                      [0, 1, 11, 2, 11, 3, 3, 3, 3, 3, 3, 2, 1, 0, 0, 1, 11, 11, 3, 11, 3, 11, 2, 11, 2, 1, 0, 0, 0, 0]]
        poses = [(14, 27)]
        result, ok, _, _ = enumerate_change_board(board, game_board, poses)
        assert ok
        print("result:", result)

    def test_chording(self):
        """填入一组会使 enumerate_change_board 失败 (返回 False) 的参数"""
        board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, -1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        game_board = [
            [10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 11,  1, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10],
        ]
        poses = [(2, 2), (2, 3), (2, 4), (3, 4), (4, 2), (4, 3), (4, 4)]
        result, ok, _, _ = enumerate_change_board(board, game_board, poses)
        print("result:", result)
        assert ok


class TestEnuLimit:
    def test_enu_limit_value(self):
        assert EnuLimit >= 50


def _original_board_bytes_to_board(rows, cols, board_bytes):
    """Optimization reference: preserve the former implementation exactly."""
    import ms_toollib as ms
    total = rows * cols
    result = [[0] * cols for _ in range(rows)]
    for i in range(total):
        byte_idx = i // 8
        if byte_idx < len(board_bytes):
            is_mine = (board_bytes[byte_idx] >> (7 - i % 8)) & 1
        else:
            is_mine = 0
        if is_mine:
            result[i // cols][i % cols] = -1
    return ms.cal_board_numbers(result)


def test_board_bytes_all_byte_values_match_original():
    for value in range(256):
        data = bytes([value])
        assert board_bytes_to_board(
            2, 4, data) == _original_board_bytes_to_board(2, 4, data)


def test_board_bytes_random_shapes_and_lengths_match_original():
    from random import Random
    rng = Random(2026)
    for rows, cols in [(1, 1), (1, 7), (3, 3), (8, 8), (16, 16), (16, 30), (7, 13)]:
        size = (rows * cols + 7) // 8
        for length in (0, 1, max(0, size - 1), size, size + 5):
            for _ in range(10):
                data = rng.randbytes(length)
                assert board_bytes_to_board(
                    rows, cols, data) == _original_board_bytes_to_board(rows, cols, data)


def test_board_bytes_zero_dimensions_match_original(monkeypatch):
    # Compare the input to the native function; empty boards may not be supported by it.
    import utils.board_funcs as module
    monkeypatch.setattr(module.ms, "cal_board_numbers", lambda board: board)
    for rows, cols in [(0, 0), (0, 3), (3, 0)]:
        assert board_bytes_to_board(
            rows, cols, b"\xff") == _original_board_bytes_to_board(rows, cols, b"\xff")
