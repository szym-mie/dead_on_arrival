from pathlib import Path
from typing import Any, Type

from src.resource.empty_loader import EmptyLoader
from src.resource.json_loader import JSONLoader
from src.resource.loader import Loader, registered_loaders
from src.resource.resource import Resource
from src.util.console import Console, console


class ResourceManager:
    def __init__(self, base_url, pack_info_url):
        self.base_url = base_url
        self.pack_info_url = pack_info_url

        self.pack = {}

        self.pack_name = 'UNKNOWN'
        self.pack_release = 'UNKNOWN'

        self.loaders = registered_loaders

        self.entry_commands = {
            'get': lambda entry: self._command_get(entry),
            'search': lambda entry: self._command_search(entry)
        }

    def reload_pack(self):
        pack_info = JSONLoader(self.pack_info_url).load(self)

        console.log_event(f'loading pack at URL {self.pack_info_url}')

        try:
            pack_data = pack_info['data']
            pack_meta = pack_info['meta']
        except KeyError:
            console.log_warn(f'malformed pack at URL {self.pack_info_url}')
            return None

        try:
            pack_name = pack_meta['name']
            pack_release = pack_meta['release']

            self.pack_name = pack_name
            self.pack_release = pack_release
        except KeyError:
            console.log_warn(f'missing metadata from pack at URL {self.pack_info_url}')
            return None

        def parse_entry_key(parents, pack_tree, next_key, next_entry):
            if next_key.startswith('#'):
                entry_command = self.entry_commands[next_key.lstrip('#')]
                if entry_command is not None:
                    walk(parents, pack_tree, entry_command(next_entry))
                else:
                    console.log_warn(f'unknown pack command {next_key}')
            else:
                walk(parents + [next_key], pack_tree, next_entry)

        def walk(parents: list[str], pack_tree, entry: Any):
            if type(entry) is dict:
                for key, next_entry in entry.items():
                    parse_entry_key(parents, pack_tree, key, next_entry)
            elif type(entry) is list:
                for i, next_entry in enumerate(entry):
                    walk(parents + [str(i)], pack_tree, next_entry)
            elif type(entry) is Resource:
                res_id = ResourceManager._get_resource_id(parents)
                pack_tree[res_id] = entry
            elif type(entry) is str:
                res_id = ResourceManager._get_resource_id(parents)
                pack_tree[res_id] = self._url_only_resource(entry)
            else:
                Console.default() \
                    .log_warn(f'malformed pack entry {entry}')

        self.pack = {}
        walk([], self.pack, pack_data)

        console.log_event(f'loaded pack {pack_name}@{pack_release}')

    def get(self, res_id):
        try:
            return self.pack[res_id].get()
        except KeyError:
            console.log_warn(f'cannot find resource {res_id} in pack {self.pack_name}')

    def unit_getter(self, unit_id):
        return lambda res_id: self.get(f'{unit_id}.{res_id}')

    def _create_loader(self, loader_name, url):
        try:
            loader_class: Type[Loader] = self.loaders[loader_name]
            return loader_class(url)
        except KeyError:
            console.log_warn(f'cannot find loader {loader_name} in pack {self.pack_name}')

    def _url_only_resource(self, path):
        rel_url = self._get_base_path(path).relative_to(self.base_url)
        return Resource(str(rel_url), self, EmptyLoader(None), False)

    def _command_get(self, entry):
        path = entry.get('path')
        loader = entry.get('loader', 'empty')
        load_later = entry.get('load_later', False)

        file_path = self._get_base_path(path)
        loader_instance = self._create_loader(loader, file_path)
        return Resource(file_path, self, loader_instance, load_later)

    def _command_search(self, entry):
        path = entry.get('path')
        loader = entry.get('loader', 'empty')
        load_later = entry.get('load_later', False)
        max_layers = entry.get('max_layers', 16)

        try:
            return self._search_path(self._get_base_path(path),
                                     loader,
                                     load_later,
                                     max_layers)
        except KeyError:
            console.log_warn(f'cannot find loader {loader} in pack {self.pack_name}')

    def _search_path(self, path: Path, loader: Loader, load_later, max_layers):
        entries = {}
        children = list(path.glob('*'))
        for dir_path in filter(lambda p: p.is_dir(), children):
            entries[dir_path.name] = self._search_path(dir_path,
                                                       loader,
                                                       load_later,
                                                       max_layers - 1)
        for file_path in filter(lambda p: p.is_file(), children):
            loader_instance = self._create_loader(loader, file_path)
            entries[file_path.stem] = Resource(file_path, self, loader_instance, load_later)

        return entries

    def _get_base_path(self, path):
        return Path(self.base_url).joinpath(path)

    @staticmethod
    def _get_resource_id(id_tokens: list[str]):
        return '.'.join(id_tokens)
