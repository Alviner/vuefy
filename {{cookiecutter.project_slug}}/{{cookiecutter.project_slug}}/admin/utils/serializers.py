import typing as t
from datetime import date, datetime

from pydantic import BaseModel
from wsrpc_aiohttp import serializer


def config_serializers() -> None:
    @serializer.register(date)
    @serializer.register(datetime)
    def _serialize_dt(value: t.Union[date, datetime]) -> str:
        return value.isoformat()

    @serializer.register(BaseModel)
    def _serialize_pydantic(value: BaseModel) -> t.Mapping[str, t.Any]:
        return value.dict(exclude_unset=True, by_alias=True)
