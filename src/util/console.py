import re
import inspect
from io import StringIO

import pyglet.window.key as key

from src.util.unit import Unit


class Console(Unit):
    def __init__(self):
        self.output = StringIO()
        self.input = StringIO()

    def input_key(self, new_key, new_mod):
        if new_key != key.ENTER:
            self.input.write(Console.get_key_string(new_key, new_mod))
        else:
            self.send_command()

    def send_command(self):
        command = self.input.read().split(' ')
        # TODO
        self.write_line('# TODO')

    _filename_pattern = re.compile(r'[^/\\]+$')

    def log_event(self, message):
        self.write_line(f'# : {message}')

    def log_warn(self, message):
        try:
            caller_frame = inspect.getouterframes(inspect.currentframe())[1]
            filename = Console._filename_pattern.search(caller_frame.filename)
            source = f'{filename}:{caller_frame.lineno}[{caller_frame.function}]'
            self.write_line(f'\x1b1! {source}: {message}\x1b0')
        except IndexError:
            self.write_line(f'\x1b1! (no frame info): {message}\x1b0')
        finally:
            del caller_frame

    def write_line(self, text):
        self.output.write(text + '\n')

    @staticmethod
    def get_key_string(new_key, new_mod):
        abs_str = key.symbol_string(new_key)
        if new_mod & key.MOD_SHIFT:
            return abs_str.upper()
        else:
            return abs_str.lower()


console = Console.default()
