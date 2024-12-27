import pygame
import random
import math

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
    K_q,
)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
MAP_WIDTH = 4000
MAP_HEIGHT = 3000


#############################################
## Player ##
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/wizard_survivor_small.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.facing = "right"
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.diagonal_factor = 0.707
        self.health = 100
        self.last_shot = pygame.time.get_ticks()
        self.shot_delay = 1500
        self.score = 0
        self.shockwave_interva3000
        self.last_shockwave = 0

    def input(self):
        keys = pygame.key.get_pressed()
        
        dx = 0
        dy = 0
        
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_LEFT]:
            dx -= 1
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            dx += 1
            self.facing = "right"
            
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= self.diagonal_factor
            dy *= self.diagonal_factor
            
        # Apply speed
        self.direction.x = dx * self.speed
        self.direction.y = dy * self.speed

    def update(self):
        # Store previous facing direction
        old_facing = self.facing
        
        self.input()  # Get input first
        
        # Only flip if direction changed
        if old_facing != self.facing:
            self.surf = pygame.transform.flip(self.surf, True, False)
        
        # Apply movement
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
        
        # Keep player on the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))
        
        # Handle shooting
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shot_delay:
            self.last_shot = current_time
            return self.attack()

        # Auto Version
        if current_time - self.last_shockwave >= self.shockwave_interval:
            self.last_shockwave = current_time
            return self.create_shockwave()
        
        return None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def attack(self):
        # Create a direction vector based on which way the player is facing
        if self.facing == "right":
            direction = pygame.math.Vector2(1, 0)
        else:  # facing left
            direction = pygame.math.Vector2(-1, 0)
            
        fireball = Fireball(self.rect.x, self.rect.y, direction)
        return fireball, fireball.damage

    def create_shockwave(self):
        # Pass the facing direction to the ShockWave
        shockwave = ShockWave(self.rect.centerx, self.rect.centery, self.facing)
        return shockwave, shockwave.damage


#############################################
## Enemies ##
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super(Zombie, self).__init__()
        self.surf = pygame.image.load("images/Zombie.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = "right"
        self.speed = random.randint(1, 3)
        self.player = player
        self.health = 10
        self.last_collision = 0
        self.collision_cooldown = 500  # Milliseconds between collisions
        
        # Animation states
        self.original_surf = self.surf.copy()  # Store original surface
        self.current_scale = 1.0
        self.is_scaling = False
        self.scale_start_time = 0
        self.scale_duration = 300  # 1 second for scale animation
        
        # Death animation
        self.is_dying = False
        self.death_start_time = 0
        self.death_duration = 1000  # 1 second for death animation
        self.flash_interval = 100  # Flash every 100ms
        self.visible = True
        
        # Vector movement attributes
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2()
        self.acceleration = pygame.math.Vector2()
        
        # Randomize zombie personality
        self.max_speed = random.uniform(1.0, 3.0)
        self.steering_force = random.uniform(0.05, 0.15)
        
        # Wandering attributes
        self.wander_angle = random.uniform(0, math.pi * 2)
        self.wander_radius = random.uniform(30, 70)
        self.angle_change = random.uniform(0.2, 0.4)
        
        # Randomize behavior weights
        self.wander_weight = random.uniform(0.2, 0.4)
        self.seek_weight = 1.0 - self.wander_weight
        
        # Assign personality type
        if self.wander_weight > 0.35:
            self.personality = "Wanderer"
        elif self.max_speed > 2.5:
            self.personality = "Speedy"
        elif self.steering_force > 0.12:
            self.personality = "Agile"
        else:
            self.personality = "Hunter"
        
        # Debug font
        self.debug_font = pygame.font.Font(None, 20)

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Handle bounce animation
        if self.is_scaling:
            progress = (current_time - self.scale_start_time) / self.scale_duration
            if progress <= 0.25:  # First quarter - scale up to 1.1
                self.current_scale = 1.0 + (0.1 * (progress * 4))
            elif progress <= 0.75:  # Middle half - scale down to 0.9
                self.current_scale = 1.1 - (0.2 * ((progress - 0.25) * 2))
            elif progress <= 1:  # Last quarter - return to normal
                self.current_scale = 0.9 + (0.1 * ((progress - 0.75) * 4))
            else:  # Animation complete
                self.current_scale = 0.95
                self.is_scaling = False
            
            # Apply scale
            scaled_size = (
                int(self.original_surf.get_width() * self.current_scale),
                int(self.original_surf.get_height() * self.current_scale)
            )
            self.surf = pygame.transform.scale(self.original_surf, scaled_size)
        
        # Handle death animation
        if self.is_dying:
            if current_time - self.death_start_time >= self.death_duration:
                self.kill()  # Actually remove the zombie
            else:
                # Toggle visibility based on flash interval
                self.visible = ((current_time - self.death_start_time) // self.flash_interval) % 2 == 0
        
        # Move towards player
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < self.player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > self.player.rect.y:
            self.rect.y -= self.speed

        # Keep zombie on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

    def take_damage(self, damage):
        # Don't apply damage if already dying
        if self.is_dying:
            return
            
        self.health -= damage
        print(f"Zombie took {damage} damage. Health now: {self.health}")  # Better debug message
        
        if self.health <= 0:
            self.health = 0  # Prevent negative health
            self.is_dying = True
            self.death_start_time = pygame.time.get_ticks()
            self.player.score += 1  # Increment score when zombie dies

    def start_bounce_animation(self):
        if not self.is_scaling:
            self.is_scaling = True
            self.scale_start_time = pygame.time.get_ticks()

    def attack(self):
        return ZombieAttack(self.rect.x, self.rect.y, self.direction)

    

    @staticmethod
    def spawn_zombie(player):
        zombie = Zombie(
            random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT), player
        )
        return zombie


#############################################
## Weapons ##
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super(Fireball, self).__init__()
        self.surf = pygame.image.load("images/fireball.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 30
        self.damage = 10

    def update(self):
        # Move in the fixed direction
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Remove fireball when it leaves the screen
        if self.rect.right < 0 or self.rect.left > MAP_WIDTH:
            self.kill()
        if self.rect.top < 0 or self.rect.bottom > MAP_HEIGHT:
            self.kill()


#############################################
## Game ##
class Camera:
    def __init__(self, width, height):
        # camera is a rectangle that represents the portion of the game world that the player can see
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        else:
            return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # limit scrolling to the world size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0

        # Add debug font initialization
        self.debug_font = pygame.font.Font(None, 36)

        self.bg_tile = pygame.image.load("images/background.png")
        self.tile_size = self.bg_tile.get_width()

        self.player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        self.zombies = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.shockwaves = pygame.sprite.Group()

        # Add spawn control variables
        self.zombie_spawn_delay = 2000  # Start with 2 seconds between spawns
        self.last_spawn = pygame.time.get_ticks()
        self.min_spawn_delay = 500  # Fastest spawn rate (milliseconds)
        self.difficulty_increase_rate = 50  # How much to decrease delay
        self.max_zombies = 150  # Maximum zombies allowed at once

        for _ in range(10):
            zombie = Zombie.spawn_zombie(self.player)
            self.zombies.add(zombie)

    def spawn_zombie(self):
        # Don't spawn if at max zombies
        if len(self.zombies) >= self.max_zombies:
            return

        # Spawn from random edge of the map
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, MAP_WIDTH)
            y = 0
        elif side == 1:  # Right
            x = MAP_WIDTH
            y = random.randint(0, MAP_HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, MAP_WIDTH)
            y = MAP_HEIGHT
        else:  # Left
            x = 0
            y = random.randint(0, MAP_HEIGHT)

        zombie = Zombie(x, y, self.player)
        self.zombies.add(zombie)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    running = False

            # Get pressed keys but don't pass them to update
            pressed_keys = pygame.key.get_pressed()
            
            # Change this line to not pass pressed_keys
            attack_result = self.player.update()
            if attack_result is not None:
                if isinstance(attack_result[0], Fireball):
                    self.fireballs.add(attack_result[0])
                elif isinstance(attack_result[0], ShockWave):
                    self.shockwaves.add(attack_result[0])

            self.zombies.update()
            self.fireballs.update()
            self.shockwaves.update()

            self.camera.update(self.player)

            # Tile the background
            for x in range(0, MAP_WIDTH, self.tile_size):
                for y in range(0, MAP_HEIGHT, self.tile_size):
                    self.screen.blit(
                        self.bg_tile,
                        self.camera.apply(
                            pygame.Rect(x, y, self.tile_size, self.tile_size)
                        ),
                    )

            self.screen.blit(self.player.surf, self.camera.apply(self.player))
            for zombie in self.zombies:
                if not zombie.is_dying or (zombie.is_dying and zombie.visible):
                    self.screen.blit(zombie.surf, self.camera.apply(zombie))
                    
                    # Draw personality type above zombie
                    debug_text = zombie.debug_font.render(
                        f"{zombie.personality} ({int(zombie.health)}hp)", 
                        True, (255, 255, 255)
                    )
                    text_rect = debug_text.get_rect(
                        midbottom=self.camera.apply(zombie).midtop
                    )
                    self.screen.blit(debug_text, text_rect)
            for fireball in self.fireballs:
                pygame.draw.rect(
                    self.screen, (255, 0, 0), self.camera.apply(fireball), 1
                )  # Debug rectangle
                self.screen.blit(fireball.surf, self.camera.apply(fireball))
            for shockwave in self.shockwaves:
                self.screen.blit(shockwave.surf, self.camera.apply(shockwave))

            # Draw health and score
            debug_text = self.debug_font.render(
                f"Score: {self.player.score} | Health: {self.player.health}", 
                True, (255, 255, 255)
            )
            self.screen.blit(debug_text, (10, 10))

            # Check for collisions between fireballs and zombies
            for fireball in self.fireballs:
                zombie_hit = pygame.sprite.spritecollideany(fireball, self.zombies)
                if zombie_hit and not zombie_hit.is_dying:  # Only hit if not already dying
                    zombie_hit.take_damage(fireball.damage)
                    fireball.kill()

            # Check for shockwave collisions
            for shockwave in self.shockwaves:
                for zombie in self.zombies:
                    if zombie.is_dying:  # Skip if already dying
                        continue
                    # Calculate distance between zombie and shockwave center
                    distance = ((zombie.rect.centerx - shockwave.center_x) ** 2 + 
                              (zombie.rect.centery - shockwave.center_y) ** 2) ** 0.5
                    if distance <= shockwave.radius:
                        zombie.take_damage(shockwave.damage)

            # Add zombie-player collision check with knockback
            zombie_collision = pygame.sprite.spritecollideany(self.player, self.zombies)
            if zombie_collision:
                current_time = pygame.time.get_ticks()
                if current_time - zombie_collision.last_collision >= zombie_collision.collision_cooldown:
                    self.player.take_damage(1)
                    # zombie_collision.take_damage(3)
                    zombie_collision.last_collision = current_time
                    zombie_collision.start_bounce_animation()  # Start bounce animation
                    
                    # Add knockback
                    knockback_distance = 100
                    if zombie_collision.rect.x < self.player.rect.x:
                        zombie_collision.rect.x -= knockback_distance
                    else:
                        zombie_collision.rect.x += knockback_distance
                    if zombie_collision.rect.y < self.player.rect.y:
                        zombie_collision.rect.y -= knockback_distance
                    else:
                        zombie_collision.rect.y += knockback_distance

            # Handle zombie spawning
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn >= self.zombie_spawn_delay:
                self.spawn_zombie()
                self.last_spawn = current_time
                # Increase difficulty (decrease spawn delay)
                if self.zombie_spawn_delay > self.min_spawn_delay:
                    self.zombie_spawn_delay -= self.difficulty_increase_rate

            pygame.display.flip()
            self.clock.tick(60)

    pygame.quit()


class ShockWave(pygame.sprite.Sprite):
    def __init__(self, x, y, player_facing):
        super(ShockWave, self).__init__()
        self.center_x = x
        self.center_y = y
        self.radius = 10
        self.max_radius = 150
        self.growth_speed = 6
        self.damage = 1
        
        # Arc parameters
        self.arc_angle = 120  # Degrees (1/3 of circle)
        
        # Set start_angle based on player facing direction
        if player_facing == "right":
            self.start_angle = -60  # Centers the 120-degree arc to the right (-60 to +60)
        else:  # facing left
            self.start_angle = 120  # Centers the 120-degree arc to the left (120 to 240)
        
        self.surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        # Clear the surface
        self.surf.fill((0, 0, 0, 0))
        
        # Draw the arc instead of full circle
        pygame.draw.arc(
            self.surf,
            (0, 255, 255, 128),  # Color with alpha
            (
                self.max_radius - self.radius,
                self.max_radius - self.radius,
                self.radius * 2,
                self.radius * 2
            ),
            math.radians(self.start_angle),  # Start angle in radians
            math.radians(self.start_angle + self.arc_angle),  # End angle
            max(1, int(self.radius / 3))  # Line width
        )
        
        # Expand the radius
        self.radius += self.growth_speed
        
        # Kill the sprite when it reaches max size
        if self.radius >= self.max_radius:
            self.kill()

    def is_point_in_arc(self, point_x, point_y):
        # Calculate angle and distance to point
        dx = point_x - self.center_x
        dy = point_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        angle = math.degrees(math.atan2(dy, dx)) % 360
        
        # Normalize the angle relative to start_angle
        relative_angle = (angle - self.start_angle) % 360
        
        # Check if point is within arc
        return (distance <= self.radius and 
                distance >= self.radius - max(1, int(self.radius / 3)) and 
                relative_angle <= self.arc_angle)


if __name__ == "__main__":
    game = Game()
    game.run()

