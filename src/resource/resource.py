class Resource:
    def __init__(self, url, resource_manager, loader, load_later):
        self.url = url
        self.loader = loader
        self.resource_manager = resource_manager
        self.is_loaded = not load_later
        if load_later:
            self.value = None
        else:
            self.value = loader.load(self.resource_manager)

    def get(self):
        if not self.is_loaded:
            self.value = self.loader.load(self.resource_manager)
        return self.value

