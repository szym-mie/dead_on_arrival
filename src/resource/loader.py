class Loader:
    def __init__(self, url):
        self.url = url

    def load(self):
        return NotImplemented

    def map_open(self, file_type: str, map_fn):
        if file_type == 'text':
            mode = 'r'
            with open(self.url, mode, encoding='utf-8') as file:
                return map_fn(self.url, file)
        elif file_type == 'binary':
            mode = 'rb'
            with open(self.url, mode) as file:
                return map_fn(self.url, file)
