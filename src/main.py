from math import floor, ceil

from pyglet.gl import *
from pyglet.math import Mat4
from pyglet.sprite import Sprite

from src.entity.player import Player
from src.frame.frame import Frame
from src.graphics.rect import Rect
from src.level.level import Level
from src.level.level_import import LevelImport
from src.resource.resource_manager import ResourceManager
from src.util.controls import Controls

window = pyglet.window.Window(caption='test', width=1280, height=720)

base_pack = ResourceManager('./res', './pack/pack_base.json')
base_pack.reload_pack()

conf_pack = ResourceManager('./conf', './pack/pack_conf.json')
conf_pack.reload_pack()

# wall_image = image.load(base_pack.get('tex.lvl.wall-d0h0-full0'))
# floor_image = image.load(base_pack.get('tex.lvl.floor-full0'))
# bullet_image = image.load(base_pack.get('tex.proj.tracer-oran0'))
wall_image = base_pack.get('tex.lvl.wall-d0h0-full0')
floor_image = base_pack.get('tex.lvl.floor-full0')
bullet_image = base_pack.get('tex.proj.tracer-oran0')
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2
bullet_sprite = Sprite(bullet_image)
bullet_frame = Frame(bullet_sprite, None, None, None, None)
# player_image = image.load(base_pack.get('tex.player.default_player_image'))
player_image = base_pack.get('tex.player.default_player_image')
player_image.anchor_x = player_image.width // 2
player_image.anchor_y = player_image.height // 2
player_sprite = Sprite(player_image)
frame = Frame(player_sprite, None, None, None, None)

controls = Controls.default()

controls.define_binds(conf_pack.get('binds'))
controls.attach_to_window(window)

level_img = base_pack.get('lvl.lvl1').get_image_data()

level_img_fmt = 'RGB'
level_img_pitch = level_img.width * len(level_img_fmt)
pix = list(level_img.get_data(level_img_fmt, level_img_pitch))
print(pix)

level = Level(wall_image, floor_image, LevelImport.from_bitmap(24, 24, pix, []))

player = Player(frame, bullet_frame, level)
player.position.x = 3
player.position.y = 3

test_rect = Rect(player_image)
test_rect.scale = 50
test_rect.position_x = 0
test_rect.position_y = 0
test_rect.position_z = 16
# with open(base_pack.get('gl.rect_v'), 'r') as vf, open(base_pack.get('gl.rect_f'), 'r') as ff:
#     vs = vf.read()
#     fs = ff.read()

Rect.update_shader(base_pack.get('gl.rect_v'), base_pack.get('gl.rect_f'))
test_projection = Mat4.orthogonal_projection(-640, 640, -360, 360, -255, 255)

test_rect2 = Rect(bullet_image)
test_rect2.scale = 50
test_rect2.position_x = 0
test_rect2.position_y = 0
test_rect2.position_z = 24


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
    glClearDepth(GLdouble(1.0))
    
    level.draw(-player.position.x * 64 + 640, -player.position.y * 64 + 360)
    player.draw()
    for bullet in player.bullet_group:
        bullet.draw()
    test_rect.rotation += 0.01
    test_rect.draw(test_projection)
    test_rect2.draw(test_projection)


def update(delta_time):
    player.update(delta_time)

    for bullet in player.bullet_group:
        bullet.update(delta_time)

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
