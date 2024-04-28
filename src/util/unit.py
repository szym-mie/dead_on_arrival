from typing import Any


class Unit:
    _default_instance: Any = None

    @classmethod
    def default(cls):
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance
