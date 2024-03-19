from typing import Any


class Frame:
    def __init__(self, surface, next_frame, delay, run_method, wait_method):
        self.surface = surface
        self.next_frame = next_frame
        self.delay = delay
        self.run_method = run_method
        self.wait_method = wait_method

    def run(self, target: Any) -> Any:
        return self.run_method.run(target)

    def wait(self, target: Any) -> bool:
        return self.wait_method.run(target)

    def should_change(self, target: Any, time: float) -> bool:
        if time < self.delay or self.wait(target):
            return True
        return False
