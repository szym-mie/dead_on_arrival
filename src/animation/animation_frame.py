class AnimationFrame:
    def __init__(self, config):
        self.texture = config.get('tex')
        self.next = config.get('next')
        self.delay = config.get('delay', 1.0)
