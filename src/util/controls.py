
from pyglet.window import key

from src.util.unit import Unit


class Controls(Unit):
    def __init__(self):
        self.key_press_map = {}
        self.bind_map = {}
        self.mouse_x = 0
        self.mouse_y = 0

    def set_key_press(self, sym, _mod, is_pressed):
        key_id = f"KEY_{key.symbol_string(sym)}"
        self.key_press_map[key_id] = is_pressed

    def set_mouse_press(self, sym, _mod, is_pressed):
        key_id = f"MOUSE_{key.symbol_string(sym)}"
        self.key_press_map[key_id] = is_pressed

    def define_binds(self, bind_map):
        self.bind_map = bind_map

    def attach_to_window(self, window):
        @window.event
        def on_key_press(sym, _mod):
            self.set_key_press(sym, _mod, True)

        @window.event
        def on_key_release(sym, _mod):
            self.set_key_press(sym, _mod, False)

        @window.event
        def on_mouse_press(x, y, sym, _mod):
            self.set_mouse(x, y)
            self.set_mouse_press(sym, _mod, True)

        @window.event
        def on_mouse_release(x, y, sym, _mod):
            self.set_mouse(x, y)
            self.set_mouse_press(sym, _mod, False)

        @window.event
        def on_mouse_motion(x, y, _dx, _dy):
            self.set_mouse(x, y)

    def set_mouse(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def is_pressed(self, key_sym):
        return self.key_press_map.get(key_sym, False)

    def get_bind(self, bind):
        return self.is_pressed(self.bind_map.get(bind, ''))


controls = Controls.default()
