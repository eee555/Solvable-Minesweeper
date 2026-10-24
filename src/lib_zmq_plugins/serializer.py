from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

import enum
import msgspec

from lib_zmq_plugins.shared.base import (
    BaseQueryResult, CommandResponse, get_struct_tag,
)

if TYPE_CHECKING:
    from lib_zmq_plugins.shared.base import BaseCommand, BaseEvent, BaseQuery


def _enc_hook(obj: object) -> Any:
    """编码 hook：将 Enum 转为其原始值"""
    if isinstance(obj, enum.Enum):
        return obj.value
    raise NotImplementedError(f"Cannot encode {type(obj).__name__}")


def _dec_hook(type_hint: type, obj: object) -> object:
    """解码 hook：将原始值还原为 Enum"""
    if isinstance(type_hint, type) and issubclass(type_hint, enum.Enum):
        return type_hint(obj)
    raise NotImplementedError(f"Cannot decode to {type_hint.__name__}")


def _make_union(types: list[type]) -> type:
    """将类型列表转为 Union 类型，供 msgspec 多态反序列化使用"""
    if len(types) == 1:
        return types[0]
    return Union[tuple(types)]  # type: ignore


class Serializer:
    """序列化器，持有上层注册的类型信息"""

    def __init__(self) -> None:
        self._event_types: list[type[BaseEvent]] = []
        self._command_types: list[type[BaseCommand]] = []
        self._query_types: list[type[BaseQuery]] = []
        # 基类始终可解：服务端在无处理器/异常时只返回 BaseQueryResult
        self._query_result_types: list[type[BaseQueryResult]] = [
            BaseQueryResult]
        self._query_tags: set[str] = set()
        self._query_result_tags: set[str] = {get_struct_tag(BaseQueryResult)}
        self._event_union: type = object
        self._command_union: type = object
        self._query_union: type = object
        self._query_result_union: type = BaseQueryResult

    def register_event_types(self, *types: type[BaseEvent]) -> None:
        self._event_types.extend(types)
        self._event_union = _make_union(self._event_types)

    def register_command_types(self, *types: type[BaseCommand]) -> None:
        self._command_types.extend(types)
        self._command_union = _make_union(self._command_types)

    def register_query_types(self, *types: type[BaseQuery]) -> None:
        self._query_types.extend(types)
        self._query_tags.update(get_struct_tag(query_type)
                                for query_type in types)
        self._query_union = _make_union(self._query_types)

    def register_query_result_types(self, *types: type[BaseQueryResult]) -> None:
        self._query_result_types.extend(types)
        self._query_result_tags.update(get_struct_tag(
            result_type) for result_type in types)
        self._query_result_union = _make_union(self._query_result_types)

    def is_query_tag(self, tag: str) -> bool:
        """该 tag 是否属于已注册的查询请求"""
        return tag in self._query_tags

    def is_query_result_tag(self, tag: str) -> bool:
        """该 tag 是否属于已注册的查询响应"""
        return tag in self._query_result_tags

    def encode_event(self, event: BaseEvent) -> bytes:
        return msgspec.msgpack.encode(event, enc_hook=_enc_hook)

    def decode_event(self, data: bytes) -> BaseEvent:
        if not self._event_types:
            raise ValueError("No event types registered")
        return msgspec.msgpack.decode(
            data, type=self._event_union, dec_hook=_dec_hook
        )

    def encode_command(self, cmd: BaseCommand) -> bytes:
        return msgspec.msgpack.encode(cmd, enc_hook=_enc_hook)

    def decode_command(self, data: bytes) -> BaseCommand:
        if not self._command_types:
            raise ValueError("No command types registered")
        return msgspec.msgpack.decode(
            data, type=self._command_union, dec_hook=_dec_hook
        )

    def encode_response(self, resp: CommandResponse) -> bytes:
        return msgspec.msgpack.encode(resp, enc_hook=_enc_hook)

    def decode_response(self, data: bytes) -> CommandResponse:
        return msgspec.msgpack.decode(
            data, type=CommandResponse, dec_hook=_dec_hook
        )

    def encode_query(self, query: BaseQuery) -> bytes:
        return msgspec.msgpack.encode(query, enc_hook=_enc_hook)

    def decode_query(self, data: bytes) -> BaseQuery:
        if not self._query_types:
            raise ValueError("No query types registered")
        return msgspec.msgpack.decode(
            data, type=self._query_union, dec_hook=_dec_hook
        )

    def encode_query_result(self, result: BaseQueryResult) -> bytes:
        return msgspec.msgpack.encode(result, enc_hook=_enc_hook)

    def decode_query_result(self, data: bytes) -> BaseQueryResult:
        if not self._query_result_types:
            raise ValueError("No query result types registered")
        return msgspec.msgpack.decode(
            data, type=self._query_result_union, dec_hook=_dec_hook
        )
