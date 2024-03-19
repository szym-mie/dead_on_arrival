from src.frame.frame import Frame


class Entity:
    def __init__(self, initial_frame: Frame):
        self.frame = initial_frame
        self.frame_time = 0

    def update(self):
        self.update_frame()

    def update_frame(self):
        if self.frame.should_change(self, self.frame_time):
            self.frame = self.frame.next_frame
            self.frame_time = 0
        else:
            self.frame_time += 1
