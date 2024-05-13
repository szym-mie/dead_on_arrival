class FrameHolder:
    def __init__(self, init_frame):
        self.frame = init_frame
        self.frame_time = 0

    def set_frame(self, new_frame):
        self.frame = new_frame
        self.frame_time = 0

    def update(self, target):
        if self.frame.should_change(target, self.frame_time):
            self.frame = self.frame.next_frame
            self.frame_time = 0
        if self.frame.should_count_down(target):
            self.frame_time += 1
