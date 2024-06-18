from cProfile import Profile
from math import floor, ceil, pi

from pyglet import clock, app
from pyglet.gl import *
from pyglet.math import Mat4, Vec3, Vec2
from pyglet.media import Player
from pyglet.sprite import Sprite
from pyglet.window import Window

from src.bounds.bcircle import BCircle
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
# window.set_mouse_visible(False)

load_all()

wall_image = base_pack.get('tex.lvl.wall-d0h0-full0')
floor_image = base_pack.get('tex.lvl.floor-full0')

tracer_image = base_pack.get('tex.proj.tracer-oran0')
pp9_item_image = base_pack.get('tex.wpn.pp9-hold0')
conda_item_image = base_pack.get('tex.wpn.conda-hold0')
mk5_item_image = base_pack.get('tex.wpn.mk5-hold0')
vls_item_image = base_pack.get('tex.wpn.vls-hold0')
player_image = base_pack.get('tex.char.player_torso_l')
recruit_image = base_pack.get('tex.char.recruit_torso_l')

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

pp9_item_rect_proto = RectPrototype(pp9_item_image)
conda_item_rect_proto = RectPrototype(conda_item_image)
mk5_item_rect_proto = RectPrototype(mk5_item_image)
vls_item_rect_proto = RectPrototype(vls_item_image)

player_rect_proto = RectPrototype(player_image)
player_rect = player_rect_proto \
    .create_mesh(Vec3(0, 0, 0), 0, Vec3(0.75, 0.75, 0.75))
player = create_character('player')

recruit_rect_proto = RectPrototype(recruit_image)

player.position.x = 3.5
player.position.y = 28.5

entities = []
items = []
wpts = []

for x, y, tile in level.all_tiles():
    ts = tile.spawn_id
    if tile.spawn_id > 0:
        print(x, y, tile.spawn_id)
    if 60 <= ts < 64:
        player.position.x = x + .5
        player.position.y = y + .5
        player.rotation = pi / 2 * ts // 60
    if 16 <= ts < 20:
        character = create_character('recruit')
        character.position.x = x + .5
        character.position.y = y + .5
        character.rotation = (ts % 60) * pi / 2
        entities.append((
            recruit_rect_proto.create_mesh(Vec3(), 0, Vec3(0.75, 0.75, 0.75)),
            character,
            BCircle(Vec2(), 0.5)
        ))
        weapon = create_weapon('mk5', tracer_rect_proto)
        weapon.position = character.position  # Set initial position
        character.weapon = weapon  # Assign weapon to character

        # Add weapon to items list
        items.append((
            pp9_item_rect_proto.create_mesh(Vec3(), 0, Vec3(0.75, 0.75, 0.75)),
            weapon
        ))
    if ts == 12:
        item = create_weapon('pp9', tracer_rect_proto)
        item.position.x = x + .5
        item.position.y = y + .5
        items.append((
            pp9_item_rect_proto.create_mesh(Vec3(), 0, Vec3(0.75, 0.75, 0.75)),
            item
        ))
    if ts == 13:
        item = create_weapon('conda', tracer_rect_proto)
        item.position.x = x + .5
        item.position.y = y + .5
        items.append((
            conda_item_rect_proto.create_mesh(Vec3(), 0, Vec3(0.75, 0.75, 0.75)),
            item
        ))
    if ts == 14:
        item = create_weapon('mk5', tracer_rect_proto)
        item.position.x = x + .5
        item.position.y = y + .5
        items.append((
            mk5_item_rect_proto.create_mesh(Vec3(), 0, Vec3(0.75, 0.75, 0.75)),
            item
        ))
    if ts == 15:
        item = create_weapon('vls', tracer_rect_proto)
        item.position.x = x + .5
        item.position.y = y + .5
        items.append((
            vls_item_rect_proto.create_mesh(Vec3(), 0, Vec3(0.75, 0.75, 0.75)),
            item
        ))
    if ts == 8:
        wpts.append((x + .5, y + .5))

print(entities)
print(items)
print(wpts)


projection = Mat4.perspective_projection(1280/720, 1.0, 2048.0, fov=40)
# projection = Mat4.orthogonal_projection(-640, 640, -360, 360, -255, 255)
camera = Camera(projection)
camera.scale = 64
camera.track_entity(player)

sound_player = Player()


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
    for rect, entity, bcircle in entities:
        rect.position = entity.position
        rect.rotation = entity.rotation
        bcircle.center.x = entity.position.x
        bcircle.center.y = entity.position.y
    for rect, it in items:
        rect.position = it.position
        rect.rotation = it.rotation

    level_mesh_proto.draw(camera)
    player_rect_proto.draw(camera)
    recruit_rect_proto.draw(camera)
    pp9_item_rect_proto.draw(camera)
    conda_item_rect_proto.draw(camera)
    mk5_item_rect_proto.draw(camera)
    vls_item_rect_proto.draw(camera)
    tracer_rect_proto.draw(camera)


pr = Profile()


def update(delta_time):
    pr.enable()

    player.update(delta_time)

    if level.get_tile_at(player.position.x, player.position.y - 0.8).is_solid:  # up
        player.position.y = floor(player.position.y) + 0.8

    if level.get_tile_at(player.position.x, player.position.y + 0.8).is_solid:  # down
        player.position.y = ceil(player.position.y) - 0.8

    if level.get_tile_at(player.position.x - 0.8, player.position.y).is_solid:  # left
        player.position.x = floor(player.position.x) + 0.8

    if level.get_tile_at(player.position.x + 0.8, player.position.y).is_solid:  # right
        player.position.x = ceil(player.position.x) - 0.8




    for rect, entity, bcircle in entities:
        entity.update_(player.position, delta_time)

        rect.position = entity.position
        rect.rotation = entity.rotation
        bcircle.center.x = entity.position.x
        bcircle.center.y = entity.position.y


    prev_weapon = player.weapon
    for _, it in items:
        it.update(delta_time)
        if player.want_to_grab and not player.grabbed_item:
            print(player.pickup_zone.center, it.position)
            if player.pickup_zone.test_point(it.position) and it != prev_weapon:
                print(it, player.weapon)
                player.weapon = it
                player.grabbed_item = True
                sound_player.next_source()
                sound_player.queue(base_pack.get('snd.player.equip'))
                sound_player.seek(0)
                sound_player.play()
    world.update(delta_time, entities)

    pr.disable()


sprite_image = base_pack.get('tex.hud.hp-point1')
print(f'{sprite_image=}')
sprite = Sprite(sprite_image)
sprite.draw()

clock.schedule_interval(update, 1 / 60)
app.run(1 / 60)

world.level.test_collisions(Vec3(5.5, 7.2), Vec3(10.3, 9.3))

pr.print_stats()
