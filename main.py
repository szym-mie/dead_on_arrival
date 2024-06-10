from math import floor, ceil

from pyglet import clock, app
from pyglet.gl import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GLfloat, GLdouble, glClearDepth, glClearColor, \
    glDisable, GL_CULL_FACE, GL_DEPTH_TEST, glEnable, GL_TEXTURE_2D_ARRAY, GL_TEXTURE_3D, GL_DEBUG_OUTPUT
from pyglet.math import Mat4, Vec3
from pyglet.sprite import Sprite
from pyglet.window import Window

from src.entity.create_character import create_character
from src.entity.create_weapon import create_weapon
from src.entity.world import world
from src.graphics.camera import Camera
from src.graphics.level_mesh_prototype import LevelMeshPrototype
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

glEnable(GL_DEPTH_TEST)

level_import = LevelImport.from_images(
    base_pack.get('lvl.lvl2_wall'),
    base_pack.get('lvl.lvl2_spawn'))

level = Level(level_import)
world.level = level

level_mesh_proto = LevelMeshPrototype(level, base_pack.get('imga.lvl.lvl'))
level_mesh_proto \
    .create_mesh(Vec3(0, 0, 0), 0, Vec3(1, 1, 1)) \
    .position.z = -0.7

tracer_rect_proto = RectPrototype(tracer_image)

item_rect = RectPrototype(item_image) \
    .create_mesh(Vec3(0, 0, 0), 0, Vec3(0.75, 0.75, 0.75))
item = create_weapon('mk5', tracer_rect_proto)

player_rect = RectPrototype(player_image) \
    .create_mesh(Vec3(0, 0, 0), 0, Vec3(0.75, 0.75, 0.75))
player = create_character('player')

player.position.x = 3.5
player.position.y = 28.5
player.weapon = item

projection = Mat4.perspective_projection(1280/720, 1.0, 2048.0, fov=40)
# projection = Mat4.orthogonal_projection(-640, 640, -360, 360, -255, 255)
camera = Camera(projection)
camera.scale = 64
camera.track_entity(player)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(GLfloat(0.0), GLfloat(0.0), GLfloat(0.0), GLfloat(0.0))
    glClearDepth(GLdouble(1.0))

    # camera.position = player.position
    camera.position.z = 16
    camera.update()
    player_rect.position = player.position
    player_rect.rotation = player.rotation
    item_rect.position = item.position
    item_rect.rotation = item.rotation

    level_mesh_proto.draw(camera)
    player_rect.draw(camera)
    item_rect.draw(camera)
    tracer_rect_proto.draw(camera)


def update(delta_time):
    player.update(delta_time)

    if level.get_tile_at(player.position.x, player.position.y - 0.8).is_solid:  # up
        player.position.y = floor(player.position.y) + 0.8

    if level.get_tile_at(player.position.x, player.position.y + 0.8).is_solid:  # down
        player.position.y = ceil(player.position.y) - 0.8

    if level.get_tile_at(player.position.x - 0.8, player.position.y).is_solid:  # left
        player.position.x = floor(player.position.x) + 0.8

    if level.get_tile_at(player.position.x + 0.8, player.position.y).is_solid:  # right
        player.position.x = ceil(player.position.x) - 0.8

    item.update(delta_time)
    world.update(delta_time)


sprite_image = base_pack.get('tex.hud.doa')
sprite = Sprite(sprite_image)
sprite.draw()

clock.schedule_interval(update, 1 / 60)
app.run(1 / 60)



from src.algorithms.pathfinding import PathFinder
path_finder = PathFinder(level)

print(f'{path_finder.can_hear((5, 5), (5, 11), 6)}')

tab = [[[] for _ in range(25)] for _ in range(25)]
for x in range(25):
    for y in range(25):
        if level.get_tile_at(x, y) == 0:
            tab[x][y].append('W')
start = (5, 10)
end = (11, 22)
path = path_finder.get_shortest_path(start, end)
path1 = path_finder.flank(start, end)
print(f'{path=}')
print(f'{path1=}')

for x, y in path:
    tab[x][y].append(1)

for x,y in path1:
    tab[x][y].append(2)

print(*tab, sep='\n')