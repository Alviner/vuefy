
from argparse import ArgumentTypeError
from enum import unique, StrEnum
from typing import Any, Callable, Tuple


@unique
class Environment(StrEnum):
    STAGE = 'stage'
    PROD = 'prod'

    @classmethod
    def choices(cls) -> Tuple[str, ...]:
        return tuple(map(str, cls))


def validate(
    type: Callable[[Any], Any], constrain: Callable[[Any], bool]
) -> Callable[[Any], Any]:
    def wrapper(value: Any) -> Any:
        value = type(value)
        if not constrain(value):
            raise ArgumentTypeError
        return value

    return wrapper


positive_int = validate(int, constrain=lambda x: x > 0)
uint = validate(int, constrain=lambda x: x >= 0)
