from abc import abstractmethod
from typing import Any, Protocol, TypeVar

T = TypeVar('T', bound='Comparable')


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __lt__(self: T, other: T) -> bool:
        ...

    def __gt__(self: T, other: T) -> bool:
        return (not self < other) and self != other

    def __le__(self: T, other: T) -> bool:
        return self < other or self == other

    def __ge__(self: T, other: T) -> bool:
        return (not self < other)
