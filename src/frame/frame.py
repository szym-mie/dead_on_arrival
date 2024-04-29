from typing import Any


class Frame:
    def __init__(self, sprite, next_frame, delay, skip_method, hold_method):
        """

        :param sprite: surface to display
        :param next_frame: next frame pointer
        :param delay: delay to next frame
        :param skip_method: return True to skip to new frame now
        :param hold_method: return True to stop the delay countdown
        """
        self.sprite = sprite
        self.next_frame = next_frame
        self.delay = delay
        self.skip_method = skip_method
        self.hold_method = hold_method

    def skip(self, target: Any) -> bool:
        return self.skip_method.run(target)

    def should_count_down(self, target: Any) -> bool:
        return not self.hold_method.run(target)

    def should_change(self, target: Any, time: float) -> bool:
        if time < self.delay or self.skip(target):
            return True
        return False
