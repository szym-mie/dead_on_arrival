from __future__ import annotations
import src.animation.export as frame_export


class FrameManager:
    def __init__(self):
        self.method_map = dict()
        self.surface_map = dict()

    def add_method(self, method: frame_export.FrameMethod):
        self.method_map[method.ref] = method
        print('add method')
        print(method)

    def add_surface(self, surface):
        pass

    @staticmethod
    def default() -> FrameManager:
        return _default_frame_manager_instance


_default_frame_manager_instance = FrameManager()
