class Resource:
    def __init__(self, url, loader, load_later):
        self.url = url
        self.loader = loader
        print(vars(loader))
        print(loader.url)
        self.is_loaded = not load_later
        if load_later:
            self.value = None
        else:
            self.value = loader.load()

    def get(self):
        if not self.is_loaded:
            self.value = self.loader.load()
        return self.value

