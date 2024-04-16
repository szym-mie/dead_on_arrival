from src.entity.entity import Entity
from src.frame.export import frame_method
from src.frame.frame import Frame
import pygame
from pygame import K_w, K_s,K_a, K_d
import math
WIDTH, HEIGHT = 400, 400


class Player(Entity):
    def __init__(self, initial_frame: Frame):

        super().__init__(initial_frame)
        self.image = pygame.image.load("res/tex/src/player/default_player_image.xcf").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.base_player_image = self.image
        self.position = pygame.math.Vector2(0, 0)
        self.base_player_rect = self.base_player_image.get_rect(center=(640, 360))
        self.rect = self.base_player_rect.copy()
        self.player_speed = .25
        self.velocity_x = 0
        self.velocity_y = 0

    @frame_method
    def wait_fire_weapon(self, target) -> bool:
        pass

    def player_turning(self):
        mouse_coords = pygame.mouse.get_pos()
        x_change_mouse_player = (mouse_coords[0] - self.base_player_rect.centerx)
        y_change_mouse_player = (mouse_coords[1] - self.base_player_rect.centery)
        angle = int(math.degrees(math.atan2(y_change_mouse_player, x_change_mouse_player)))
        angle = angle % 360

        self.image = pygame.transform.rotate(self.base_player_image, -angle)
        self.rect = self.image.get_rect(center=self.base_player_rect.center)

    def calculate_velocities(self):
        keys = pygame.key.get_pressed()

        if keys[K_w]:
            self.velocity_y = -self.player_speed

        if keys[K_d]:
            self.velocity_x = self.player_speed

        if keys[K_s]:
            self.velocity_y = self.player_speed

        if keys[K_a]:
            self.velocity_x = -self.player_speed

        if self.velocity_x and self.velocity_y:
            self.velocity_x /= math.sqrt(1.5)
            self.velocity_y /= math.sqrt(1.5)

    def move(self):
        self.position += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        # self.base_player_rect.center = self.position
        self.rect.center = self.base_player_rect.center

    def update(self, _delta_time):
        self.calculate_velocities()
        self.move()
        self.player_turning()


