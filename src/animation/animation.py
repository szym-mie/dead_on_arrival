class Animation:
    def __init__(self, animation_prototype):
        self.time = 0.0
        self.frame_index = 0
        self.frames = animation_prototype.frames
        self.frame = self.frames[self.frame_index]
        self.frame_time = 0
        self.paused = False

        self.animation_prototype = animation_prototype

    def reset_frame(self):
        self.frame_time = 0
        self.time = 0.0

    def play(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def set_frame(self, frame_index):
        self.frame_index = frame_index
        self.frame = self.frames[frame_index]
        self.frame_time = 0

    def update(self, delta_time):
        if not self.paused:
            self.time += delta_time
            time_spent = delta_time
            while self.frame_time + time_spent > self.frame.delay:
                if self.frame.next is None:
                    break
                self.set_frame(self.frame.next)
                time_spent -= self.frame.delay - self.frame_time
            self.frame_time += time_spent
