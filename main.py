from math import floor, ceil

import pyglet
from pyglet import image
from pyglet.sprite import Sprite

from src.entity.player import Player
from src.frame.frame import Frame
from src.level.level import Level
from src.level.level_import import LevelImport
from src.resource.json_loader import JSONLoader
from src.resource.resource_manager import ResourceManager
from src.util.controls import Controls
from src.entity.projectile import Projectile

window = pyglet.window.Window(caption='test', width=1280, height=720)

base_pack = ResourceManager('./res', './pack/pack_base.json')
base_pack.reload_pack()

conf_pack = ResourceManager('./conf', './pack/pack_conf.json')
conf_pack.reload_pack()

wall_image = image.load(base_pack.get('tex.lvl.wall-d0h0-full0'))
floor_image = image.load(base_pack.get('tex.lvl.floor-full0'))
bullet_image = image.load(base_pack.get('tex.wpn.frag-item'))
bullet_sprite = Sprite(bullet_image)
bullet_frame = Frame(bullet_sprite, None, None, None, None)
player_image = image.load(base_pack.get('tex.player.default_player_image'))
player_image.anchor_x = player_image.width // 2
player_image.anchor_y = player_image.height // 2
player_sprite = Sprite(player_image)
frame = Frame(player_sprite, None, None, None, None)
player = Player(frame, bullet_frame)
player.position.x = 3
player.position.y = 3

projectile = Projectile(bullet_frame, 640 , 360, player.rotation)
controls = Controls.default()

controls.define_binds(JSONLoader(conf_pack.get('binds')).load())
controls.attach_to_window(window)

level_img = image.load(base_pack.get('lvl.lvl1')).get_image_data()

level_img_fmt = 'RGB'
level_img_pitch = level_img.width * len(level_img_fmt)
pix = list(level_img.get_data(level_img_fmt, level_img_pitch))
print(pix)

level = Level(wall_image, floor_image, LevelImport.from_bitmap(24, 24, pix, []))

@window.event
def on_draw():
    window.clear()
    level.draw(-player.position.x * 64 + 640, -player.position.y * 64 + 360)
    player.draw()
    projectile.draw()
    for bullet in  player.bullet_group:
        bullet.draw()



def update(delta_time):
    player.update(delta_time)

    for bullet in  player.bullet_group:
        bullet.update()


    if level.get_tile_at(player.position.x, player.position.y - 0.8) == 0:  # up
        player.position.y = floor(player.position.y) + 0.8

    if level.get_tile_at(player.position.x, player.position.y + 0.8) == 0:  # down
        player.position.y = ceil(player.position.y) - 0.8

    if level.get_tile_at(player.position.x - 0.8, player.position.y) == 0:  # left
        player.position.x = floor(player.position.x) + 0.8

    if level.get_tile_at(player.position.x + 0.8, player.position.y) == 0:  # right
        player.position.x = ceil(player.position.x) - 0.8


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run(1 / 60)
