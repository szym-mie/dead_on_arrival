from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic, Callable, IO

R = TypeVar('R')


class Loader(ABC, Generic[R]):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def load(self) -> R:
        return NotImplemented

    class FileType(Enum):
        text = 't'
        binary = 'b'

    @staticmethod
    def map_open(url: str, file_type: FileType, map_fn: Callable[[IO], R]) -> R:
        mode = 'r' + file_type.value
        with open(url, mode, encoding='utf-8') as f:
            return map_fn(f)

