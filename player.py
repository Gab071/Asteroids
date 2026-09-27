import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        # creating new variable correctly draw player and store hitbox information
        hitbox_radius = PLAYER_RADIUS*0.65
        super().__init__(x, y, hitbox_radius)
        self.rotation = 0.0
        self.shot_cooldown = 0.0
        

    def triangle(self) -> list[pygame.Vector2]:
        # drawing player on the screen as triangle using PLAYER_RADIUS
        # self.radius is the player hit_box
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(
            self.rotation + 90) * PLAYER_RADIUS / 1.5
        a = self.position + forward * PLAYER_RADIUS
        b = self.position - forward * PLAYER_RADIUS - right
        c = self.position - forward * PLAYER_RADIUS + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self) -> None:      
        if self.shot_cooldown > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOT_SPEED
        shot.velocity += rotated_with_speed_vector
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS



