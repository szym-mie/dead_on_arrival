from operator import itemgetter
from pathlib import Path
from typing import Any

from src.util.console import Console
from src.resource.json_loader import JSONLoader


class ResourceManager:
    def __init__(self, base_url, pack_info_url):
        self.base_url = base_url
        self.pack_info_url = pack_info_url

        self.pack = {}

        self.pack_name = 'UNKNOWN'
        self.pack_release = 'UNKNOWN'

        self.entry_commands = {
            'search': lambda entry: self.search(entry)
        }

    def reload_pack(self):
        pack_info = JSONLoader(self.pack_info_url).load()

        Console.default() \
            .log_event(f'loading pack at URL {self.pack_info_url}')

        try:
            pack_data = pack_info['data']
            pack_meta = pack_info['meta']
        except KeyError:
            Console.default() \
                .log_warn(f'malformed pack at URL {self.pack_info_url}')
            return None

        try:
            pack_name = pack_meta['name']
            pack_release = pack_meta['release']

            self.pack_name = pack_name
            self.pack_release = pack_release
        except KeyError:
            Console.default() \
                .log_warn(f'missing metadata from pack at URL {self.pack_info_url}')
            return None

        def parse_entry_key(parents, pack_tree, next_key, next_entry):
            if next_key.startswith('#'):
                entry_command = self.entry_commands[next_key.lstrip('#')]
                if entry_command is not None:
                    walk(parents, pack_tree, entry_command(next_entry))
                else:
                    Console.default() \
                        .log_warn(f'unknown pack command {next_key}')
            else:
                walk(parents + [next_key], pack_tree, next_entry)

        def walk(parents: list[str], pack_tree, entry: Any):
            if type(entry) is dict:
                for key, next_entry in entry.items():
                    parse_entry_key(parents, pack_tree, key, next_entry)
            elif type(entry) is list:
                for i, next_entry in enumerate(entry):
                    walk(parents + [str(i)], pack_tree, next_entry)
            elif type(entry) is str:
                res_id = ResourceManager.get_resource_id(parents)
                if type(entry) is str:
                    pack_tree[res_id] = self.get_base_path(entry)
                else:
                    pack_tree[res_id] = None
            else:
                Console.default() \
                    .log_warn(f'malformed pack entry {entry}')

        self.pack = {}
        walk([], self.pack, pack_data)

        Console.default() \
            .log_event(f'loaded pack {pack_name}@{pack_release}')

    def get(self, res_id):
        try:
            return self.pack[res_id]
        except KeyError:
            Console.default() \
                .log_warn(f'cannot find resource {res_id} in pack {self.pack_name}')

    def search(self, entry):
        path, max_layers = itemgetter('path', 'max_layers')(entry)
        return self.search_path(self.get_base_path(path), max_layers)

    def search_path(self, path: Path, max_layers: int):
        entries = {}
        children = list(path.glob('*'))
        for dir_path in filter(lambda p: p.is_dir(), children):
            entries[dir_path.name] = self.search_path(dir_path, max_layers - 1)
        for file_path in filter(lambda p: p.is_file(), children):
            entries[file_path.stem] = str(file_path.relative_to(self.base_url))

        return entries

    def get_base_path(self, path):
        return Path(self.base_url).joinpath(path)

    @staticmethod
    def get_resource_id(id_tokens: list[str]):
        return '.'.join(id_tokens)
