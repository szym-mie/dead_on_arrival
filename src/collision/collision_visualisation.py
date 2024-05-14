

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
from src.collision.sprite_collision import SpriteCollision, collide
import pyglet

window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Masks")


BG = (0, 0, 0)
WHITE = (255, 255, 255)

# TODO check on main player sprite
class Soldier(pyglet.sprite.Sprite):
    def __init__(self, x, y, batch=None):
        super().__init__(img=pyglet.image.load('default_player_image.png'), batch=batch)
        self.x = x
        self.y = y



# TODO check on main projectile sprite
class Bullet(pyglet.sprite.Sprite):
    def __init__(self, batch=None):
        super().__init__(img=pyglet.image.SolidColorImagePattern((*self.color,  200)).create_image(10, 10), batch=batch)
        self.default_color = (255, 0, 0)
        self.color = self.default_color

    def update(self, dt):
        pos = window._mouse_x, window._mouse_y
        self.x, self.y = pos


window.set_mouse_visible(False)


soldier_batch = pyglet.graphics.Batch()
bullet_batch = pyglet.graphics.Batch()

soldier = Soldier(300, 200, batch=soldier_batch)
bullet = Bullet(batch=bullet_batch)
soldier_sprite_collision =  SpriteCollision(soldier)
bullet_sprite_collision = SpriteCollision(bullet)


@window.event
def on_draw():
    window.clear()
    soldier_batch.draw()
    bullet_batch.draw()

    if collide(soldier, bullet):
        print(f'Prefect pixel collision found')


def update(dt):
    bullet.update(dt)

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()
