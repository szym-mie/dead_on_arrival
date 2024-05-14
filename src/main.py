from math import floor, ceil

from pyglet import clock, app
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GLfloat, GLdouble, glClearDepth, glClearColor
from pyglet.math import Mat4, Vec3
from pyglet.window import Window

from src.entity.create_character import create_character
from src.entity.create_weapon import create_weapon
from src.entity.world import world
from src.graphics.camera import Camera
from src.graphics.rect_prototype import RectPrototype
from src.level.level import Level
from src.level.level_import import LevelImport
from src.resource.default_resource_packs import base_pack, conf_pack, load_all
from src.util.controls import controls

window = Window(caption='test', width=1280, height=720)

load_all()

wall_image = base_pack.get('tex.lvl.wall-d0h0-full0')
floor_image = base_pack.get('tex.lvl.floor-full0')

tracer_image = base_pack.get('tex.proj.tracer-oran0')
item_image = base_pack.get('tex.wpn.mk5-hold0')
player_image = base_pack.get('tex.player.default_player_image')

controls.define_binds(conf_pack.get('binds'))
controls.attach_to_window(window)

level_img = base_pack.get('lvl.lvl1').get_image_data()

level_img_fmt = 'RGB'
level_img_pitch = level_img.width * len(level_img_fmt)
pix = list(level_img.get_data(level_img_fmt, level_img_pitch))
print(pix)

level = Level(wall_image, floor_image, LevelImport.from_bitmap(24, 24, pix, []))
world.level = level

tracer_rect_proto = RectPrototype(tracer_image)

item_rect = RectPrototype(item_image) \
    .create_mesh(Vec3(0, 0, 0), 0, Vec3(0.75, 0.75, 0.75))
item = create_weapon('mk5', tracer_rect_proto)

player_rect = RectPrototype(player_image) \
    .create_mesh(Vec3(0, 0, 0), 0, Vec3(0.75, 0.75, 0.75))
player = create_character('player')
player.position.x = 3
player.position.y = 3
player.weapon = item


tx = 0

test_rect_proto = RectPrototype(tracer_image)
test_rect_proto.create_mesh(Vec3(tx, 0, 0), tx, Vec3(1, 1, 1))
tx += 1
test_rect_proto.create_mesh(Vec3(tx, 0, 0), tx, Vec3(1, 1, 1))
tx += 1
test_rect_proto.create_mesh(Vec3(tx, 0, 0), tx, Vec3(1, 1, 1))
tx += 1
test_rect_proto.create_mesh(Vec3(tx, 0, 0), tx, Vec3(1, 1, 1))
tx += 1

projection = Mat4.orthogonal_projection(-640, 640, -360, 360, -255, 255)
camera = Camera(projection)
camera.scale = 64
# camera.track_entity(player)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
    glClearDepth(GLdouble(1.0))

    camera.position = player.position
    camera.update()
    player_rect.position = player.position
    player_rect.rotation = player.rotation
    item_rect.position = item.position
    item_rect.rotation = item.rotation

    level.draw(-player.position.x * 64 + 640, -player.position.y * 64 + 360)
    player_rect.draw(camera)
    item_rect.draw(camera)
    test_rect_proto.draw(camera)
    tracer_rect_proto.draw(camera)


def update(delta_time):
    player.update(delta_time)
    item.update(delta_time)
    world.update(delta_time)

    if level.get_tile_at(player.position.x, player.position.y - 0.8) == 0:  # up
        player.position.y = floor(player.position.y) + 0.8

    if level.get_tile_at(player.position.x, player.position.y + 0.8) == 0:  # down
        player.position.y = ceil(player.position.y) - 0.8

    if level.get_tile_at(player.position.x - 0.8, player.position.y) == 0:  # left
        player.position.x = floor(player.position.x) + 0.8

    if level.get_tile_at(player.position.x + 0.8, player.position.y) == 0:  # right
        player.position.x = ceil(player.position.x) - 0.8


clock.schedule_interval(update, 1 / 60)
app.run(1 / 60)
