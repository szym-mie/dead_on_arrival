from typing import Callable, Any

from src.frame.frame_manager import FrameManager


class FrameMethod:
    def __init__(self, func: Callable[[Any], Any]):
        self.ref = func.__name__
        self.func = func

    def run(self, target: Any):
        self.func(target)


def frame_method(func: Callable[[Any], Any]):
    method = FrameMethod(func)
    FrameManager.default().add_method(method)
    return func
