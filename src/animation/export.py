from typing import Callable, Any

from src.animation.frame_manager import FrameManager


class FrameMethod:
    def __init__(self, func: Callable[[Any], Any]):
        self.ref = func.__name__
        self.func = func

    def run(self, target: Any):
        self.func(target)


def frame_method(func: Callable[[Any], Any]):
    """annotate to register method in the default FrameManager"""
    method = FrameMethod(func)
    FrameManager.default().add_method(method)
    return func


@frame_method
def none(_target):
    return False
