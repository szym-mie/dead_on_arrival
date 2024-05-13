import unittest


from tests.run_test import run_test
from src.animation.export import frame_method
from src.animation.frame_manager import FrameManager


@run_test
class TestFrameManager(unittest.TestCase):
    def test_add_method(self):
        class TestClass:
            @frame_method
            def test_method(self, target):
                pass

        self.assertIn('test_method', FrameManager.default().method_map)
