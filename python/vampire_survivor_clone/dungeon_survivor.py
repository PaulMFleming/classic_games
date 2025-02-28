import pygame
import random
import math
import json

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
        self.speed = 7
        self.diagonal_factor = 0.707
        self.health = 100
        self.last_shot = pygame.time.get_ticks()
        self.shot_delay = 1500
        self.score = 0
        self.shockwave_interval = 3000
        self.last_shockwave = 0
        self.fireball_damage = 10  # Changed base damage to 10
        self.base_shot_delay = 400
        self.shot_delay = self.base_shot_delay
        self.xp = 0
        self.level = 1
        self.xp_to_level = 200
        self.base_fireball_damage = 20  # Increased from 10
        self.fireball_damage = self.base_fireball_damage
        self.ice_blast_unlocked = False
        self.ice_blast_delay = 5000  # 5 seconds between casts
        self.last_ice_blast = 0
        self.bomb_unlocked = False
        self.bomb_delay = 2000  # 2 seconds between bombs
        self.last_bomb = 0
        self.fireball_pierce = 1  # Number of enemies a fireball can hit
        self.fireball_size = 1.0  # Scale factor for fireball size
        
    def level_up(self):
        self.level += 1
        
        # Increase fireball damage
        self.fireball_damage += 5

        # Decrease shockwave interval (increase frequency)
        self.shockwave_interval = max(1500, int(self.shockwave_interval * 0.9))
        
        # Decrease shot delay (increase speed) by 10% each level
        self.shot_delay = max(200, int(self.shot_delay * 0.9))
        
        # If ice blast is unlocked, increase its speed too
        if self.ice_blast_unlocked:
            self.ice_blast_delay = max(1000, int(self.ice_blast_delay * 0.9))
        
        # Create level up message
        level_msg = LevelUpMessage(self.level)
        Game.instance.unlock_messages.add(level_msg)
        print(f"Created level up message for level {self.level}")

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
        
        # Check for level up
        if self.xp >= self.xp_to_level:
            self.level_up()
            self.xp -= self.xp_to_level
            self.xp_to_level = int(self.xp_to_level * 1.5)  # Increase XP needed for next level
            
            # Create level up message
            level_msg = LevelUpMessage(self.level)
            Game.instance.unlock_messages.add(level_msg)
        
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
        
        # Check if player has enough XP to unlock Ice Blast
        if self.xp >= 100 and not self.ice_blast_unlocked:
            self.ice_blast_unlocked = True
            unlock_msg = IceBlastUnlockMessage()
            Game.instance.unlock_messages.add(unlock_msg)

        # Check if player has enough XP to unlock Bomb
        if self.xp >= 500 and not self.bomb_unlocked:
            self.bomb_unlocked = True
            unlock_msg = BombUnlockMessage()
            Game.instance.unlock_messages.add(unlock_msg)
        
        # Handle Ice Blast casting
        if self.ice_blast_unlocked and current_time - self.last_ice_blast >= self.ice_blast_delay:
            nearest_zombie = self.find_nearest_zombie()
            if nearest_zombie:
                ice_blast = IceBlast(self.rect.centerx, self.rect.centery, nearest_zombie)
                Game.instance.ice_blasts.add(ice_blast)
                self.last_ice_blast = current_time

        # Handle Bomb creation
        if self.bomb_unlocked and current_time - self.last_bomb >= self.bomb_delay:
            self.create_bomb(self.rect.centerx, self.rect.centery)
            self.last_bomb = current_time

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
            
        fireball = Fireball(self.rect.x, self.rect.y, direction, self.fireball_damage)
        return fireball, fireball.damage

    def create_shockwave(self):
        # Pass the facing direction to the ShockWave
        shockwave = ShockWave(self.rect.centerx, self.rect.centery, self.facing)
        return shockwave, shockwave.damage

    def find_nearest_zombie(self):
        nearest = None
        min_dist = float('inf')
        for zombie in Game.instance.zombies:
            # Only consider zombies that are north (above) of the player
            if zombie.rect.centery < self.rect.centery:
                dist = math.sqrt((zombie.rect.centerx - self.rect.centerx)**2 + 
                               (zombie.rect.centery - self.rect.centery)**2)
                if dist < min_dist:
                    min_dist = dist
                    nearest = zombie
        return nearest

    def create_bomb(self, x, y):
        bomb = Bomb(x, y)
        Game.instance.bombs.add(bomb)


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
        
        self.knockback_velocity = pygame.math.Vector2(0, 0)
        self.knockback_friction = 0.92  # Reduces velocity each frame
        self.is_being_knocked = False

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Handle knockback movement first
        if self.is_being_knocked:
            # Apply knockback velocity
            self.rect.x += self.knockback_velocity.x
            self.rect.y += self.knockback_velocity.y
            self.pos.x = self.rect.x
            self.pos.y = self.rect.y
            
            # Apply friction to slow down
            self.knockback_velocity *= self.knockback_friction
            
            # Stop knockback when velocity is very small
            if self.knockback_velocity.length() < 0.1:
                self.is_being_knocked = False
                self.knockback_velocity.x = 0
                self.knockback_velocity.y = 0
            
            # Don't do normal movement while being knocked back
            return
        
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
        
        # Only move towards player if not being knocked back
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
            self.player.xp += 15  # Increased from 5 to 15

            # Create floating XP text
            xp_text = XPText(self.rect.centerx, self.rect.top)
            Game.instance.xp_texts.add(xp_text)
            self.kill()

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
    
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Monster, self).__init__()
        self.surf = pygame.image.load("images/monster.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = "right"
        self.speed = random.randint(1, 3)
        self.player = player
        self.health = 20
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
        self.flash_interval = 100
        self.visible = True

        # Vector movement attributes
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2()
        self.acceleration = pygame.math.Vector2()

        self.knockback_velocity = pygame.math.Vector2(0, 0)
        self.knockback_friction = 0.82  # Reduces velocity each frame 
        self.is_being_knocked = False

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.is_being_knocked:
            # Apply knockback velocity
            self.rect.x += self.knockback_velocity.x
            self.rect.y += self.knockback_velocity.y
            self.pos.x = self.rect.x
            self.pos.y = self.rect.y

            # Apply friction to slow down
            self.knockback_velocity *= self.knockback_friction

            # Stop knockback when velocity is very small
            if self.knockback_velocity.length() < 0.1:
                self.is_being_knocked = False
                self.knockback_velocity.x = 0
                self.knockback_velocity.y = 0

            # Don't do normal movement while being knocked back
            return
        # Handle bounce animation
        if self.is_scaling:
            progress = (current_time - self.scale_start_time) / self.scale_duration
            if progress <= 0.25:
                self.current_scale = 1.0 + (0.1 * (progress * 4))
            elif progress <= 0.75:
                self.current_scale = 1.1 - (0.2 * ((progress - 0.25) * 2))
            elif progress <= 1:
                self.current_scale = 0.9 + (0.1 * ((progress - 0.75) * 4))
            else:
                self.current_scale = 0.95
                self.is_scaling = False
        # Handle death animation
        if self.is_dying:
            if current_time - self.death_start_time >= self.death_duration:
                self.kill()
            else:
                # Toggle visibility based on flash interval
                self.visible = ((current_time - self.death_start_time) // self.flash_interval) % 2 == 0
        # Only move towards player if not being knocked back
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < self.player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > self.player.rect.y:
            self.rect.y -= self.speed
        # Keep monster on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))

    def take_damage(self, damage):
        # Don't apply damage if already dying
        if self.is_dying:
            return

        self.health -= damage
        print(f"Monster took {damage} damage. Health now: {self.health}")

        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.death_start_time = pygame.time.get_ticks()
            self.player.score += 1
            self.player.xp += 20

            # Create floating XP text
            xp_text = XPText(self.rect.centerx, self.rect.top)
            Game.instance.xp_texts.add(xp_text)
            self.kill()

    def start_bounce_animation(self):
        if not self.is_scaling:
            self.is_scaling = True
            self.scale_start_time = pygame.time.get_ticks()

    def attack(self):
        return MonsterAttack(self.rect.x, self.rect.y, self.direction)
    
    @staticmethod
    def spawn_monster(player):
        monster = Monster(
            random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT), player
        )
        return monster


#############################################
## Weapons ##
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, damage, pierce=1, size=1.0):
        super(Fireball, self).__init__()
        # Load and scale the base surface
        self.base_surf = pygame.image.load("images/fireball.png")
        self.base_surf.set_colorkey((0, 0, 0), RLEACCEL)
        
        # Scale the surface based on size parameter
        new_width = int(self.base_surf.get_width() * size)
        new_height = int(self.base_surf.get_height() * size)
        self.surf = pygame.transform.scale(self.base_surf, (new_width, new_height))
        
        self.rect = self.surf.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10
        self.damage = damage
        self.pierce = pierce  # Number of enemies it can hit before disappearing
        self.enemies_hit = []  # Track which enemies have been hit

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Check collisions with zombies
        for zombie in Game.instance.zombies:
            if zombie not in self.enemies_hit and self.rect.colliderect(zombie.rect):
                zombie.take_damage(self.damage)
                self.enemies_hit.append(zombie)
                if len(self.enemies_hit) >= self.pierce:
                    self.kill()
                    break
        
        # Remove if off screen
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


def read_high_score():
    try:
        with open("high_score.json", "r") as file:
            return json.load(file)["high_score"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return 0

def write_high_score(score):
    with open("high_score.json", "w") as file:
        json.dump({"high_score": score}, file)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type="fireball"):
        super(PowerUp, self).__init__()
        self.surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.power_type = power_type
        
        if power_type == "fireball":
            # Red orb for speed boost
            pygame.draw.circle(self.surf, (255, 0, 0), (15, 15), 15)
            pygame.draw.circle(self.surf, (255, 200, 200), (10, 10), 5)
        elif power_type == "health":
            # Green orb for health boost
            pygame.draw.circle(self.surf, (0, 255, 0), (15, 15), 15)
            pygame.draw.circle(self.surf, (200, 255, 200), (10, 10), 5)
        elif power_type == "thanos":
            # Purple orb for Thanos snap
            pygame.draw.circle(self.surf, (147, 0, 211), (15, 15), 15)  # Purple
            pygame.draw.circle(self.surf, (218, 112, 214), (10, 10), 5)  # Light purple highlight
        
        self.rect = self.surf.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 45000  # Disappear after 45 seconds if not collected

    def update(self):
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()

class Game:
    instance = None
    
    def __init__(self):
        Game.instance = self
        pygame.init()
        pygame.display.set_caption("Dungeon Survivor")
        
        # Add with other sprite groups
        self.unlock_messages = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0

        # Add debug font initialization
        self.debug_font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 72)
        self.high_score = read_high_score()

        self.bg_tile = pygame.image.load("images/background.png")
        self.tile_size = self.bg_tile.get_width()

        self.player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        self.zombies = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.shockwaves = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()  # Add power-ups group
        self.last_power_up_spawn = pygame.time.get_ticks()
        self.power_up_spawn_delay = 2000  # Start with X seconds between spawns
        self.min_power_up_delay = 1500    # Minimum 1.5 seconds between spawns
        self.power_up_delay_decrease = 50  # Decrease by 50ms each spawn

        # Add spawn control variables
        self.zombie_spawn_delay = 2000  # Start with 2 seconds between spawns
        self.last_spawn = pygame.time.get_ticks()
        self.min_spawn_delay = 500  # Fastest spawn rate (milliseconds)
        self.difficulty_increase_rate = 50  # How much to decrease delay
        self.max_zombies = 150  # Maximum zombies allowed at once

        self.xp_texts = pygame.sprite.Group()

        self.ice_blasts = pygame.sprite.Group()
        self.ice_explosions = pygame.sprite.Group()
        self.unlock_messages.update()
        self.bombs = pygame.sprite.Group()
        self.bomb_explosions = pygame.sprite.Group()

        for _ in range(10):
            zombie = Zombie.spawn_zombie(self.player)
            self.zombies.add(zombie)

        # Add after other game properties
        self.game_start_time = pygame.time.get_ticks()
        self.base_zombie_speed = 2
        self.base_monster_speed = 1.5
        self.base_spawn_delay = 2000  # Initial spawn delay (2 seconds)
        self.min_spawn_delay = 500    # Fastest spawn rate (0.5 seconds)
        self.speed_increase_rate = 0.1  # How much to increase speed every minute
        self.last_zombie_spawn = pygame.time.get_ticks()
        
        self.power_up_texts = pygame.sprite.Group()
        
    def get_current_difficulty(self):
        # Calculate minutes elapsed
        minutes_elapsed = (pygame.time.get_ticks() - self.game_start_time) / 60000
        # Increase speed by 10% every minute, cap at 3x original speed
        speed_multiplier = min(3.0, 1.0 + (minutes_elapsed * self.speed_increase_rate))
        return speed_multiplier
        
    def spawn_zombie(self):
        # Spawn multiple zombies each cycle
        num_zombies = random.randint(3, 5)  # Spawn 3-5 zombies at once
        
        for _ in range(num_zombies):
            # Spawn away from player
            while True:
                x = random.randint(100, MAP_WIDTH - 100)
                y = random.randint(100, MAP_HEIGHT - 100)
                # Check distance from player
                dx = x - self.player.rect.centerx
                dy = y - self.player.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 200:  # At least 200 pixels from player
                    break
            
            zombie = Zombie.spawn_zombie(self.player)
            zombie.speed = self.base_zombie_speed * self.get_current_difficulty()
            self.zombies.add(zombie)

    def spawn_monster(self):
        num_monsters = random.randint(1, 3)  # Spawn 1-3 monsters at once

        for _ in range(num_monsters):
            while True:
                x = random.randint(100, MAP_WIDTH - 100)
                y = random.randint(100, MAP_HEIGHT - 100)
                dx = x - self.player.rect.centerx
                dy = y - self.player.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 300:  # At least 300 pixels from player
                    break

            monster = Monster.spawn_monster(self.player)
            monster.speed = self.base_monster_speed * self.get_current_difficulty()
            self.monsters.add(monster)

    def show_game_over_screen(self):
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        return False
                    if event.key == K_SPACE:
                        return True

            self.screen.fill((0, 0, 0))
            
            # Game Over text
            game_over_text = self.game_over_font.render("Game Over", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
            
            # Score text
            score_text = self.debug_font.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            
            # High Score text
            high_score_text = self.debug_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            
            # Instructions text
            instructions_text = self.debug_font.render("Press SPACE to restart or ESC to quit", True, (255, 255, 255))
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150))
            
            # Draw everything
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(high_score_text, high_score_rect)
            self.screen.blit(instructions_text, instructions_rect)
            
            pygame.display.flip()
            self.clock.tick(60)

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
            self.monsters.update()
            self.fireballs.update()
            self.shockwaves.update()
            self.bombs.update()
            self.bomb_explosions.update()
            self.unlock_messages.update()

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

            for monster in self.monsters:
                if not monster.is_dying or (monster.is_dying and monster.visible):
                    self.screen.blit(monster.surf, self.camera.apply(monster))
                    
                    debug_text = monster.debug_font.render(
                        f"Monster ({int(monster.health)}hp)",
                        True, (255, 300, 255)
                    )
                    text_rect = debug_text.get_rect(
                        midbottom=self.camera.apply(monster).midtop
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
            speed_multiplier = self.get_current_difficulty()
            minutes_elapsed = (pygame.time.get_ticks() - self.game_start_time) / 60000
            
            debug_text = self.debug_font.render(
                f"Score: {self.player.score} | Health: {self.player.health} | " +
                f"Level: {self.player.level} | XP: {self.player.xp} | " +
                f"Difficulty: {speed_multiplier:.1f}x | Time: {int(minutes_elapsed)}m",
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
                    # Use the arc collision detection
                    if shockwave.is_point_in_arc(zombie.rect.centerx, zombie.rect.centery):
                        zombie.take_damage(shockwave.damage)
                        zombie.start_bounce_animation()  # Start bounce animation
                        
                        # Calculate knockback direction with random angle
                        knockback_speed = 25  # Initial speed of knockback
                        base_angle = math.atan2(
                            zombie.rect.centery - shockwave.center_y,
                            zombie.rect.centerx - shockwave.center_x
                        )
                        random_angle = math.radians(random.uniform(-30, 30))
                        final_angle = base_angle + random_angle
                        
                        # Set knockback velocity
                        zombie.knockback_velocity.x = math.cos(final_angle) * knockback_speed
                        zombie.knockback_velocity.y = math.sin(final_angle) * knockback_speed
                        zombie.is_being_knocked = True

            # Handle enemy spawning
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn >= self.zombie_spawn_delay:
                self.spawn_zombie()

                if random.random() < 0.2:  # 10% chance to spawn a monster
                    self.spawn_monster()

                self.last_spawn = current_time
                # Increase difficulty (decrease spawn delay)
                if self.zombie_spawn_delay > self.min_spawn_delay:
                    self.zombie_spawn_delay -= self.difficulty_increase_rate


            # Modify zombie-player collision check
            zombie_collision = pygame.sprite.spritecollideany(self.player, self.zombies)
            if zombie_collision:
                current_time = pygame.time.get_ticks()
                if current_time - zombie_collision.last_collision >= zombie_collision.collision_cooldown:
                    self.player.take_damage(1)
                    zombie_collision.last_collision = current_time
                    zombie_collision.start_bounce_animation()
                    
                    # Add knockback
                    knockback_distance = 100
                    if zombie_collision.rect.x < self.player.rect.x:
                        zombie_collision.rect.x -= knockback_distance
                        zombie_collision.pos.x = zombie_collision.rect.x  # Update position vector
                    else:
                        zombie_collision.rect.x += knockback_distance
                        zombie_collision.pos.x = zombie_collision.rect.x  # Update position vector
                    if zombie_collision.rect.y < self.player.rect.y:
                        zombie_collision.rect.y -= knockback_distance
                        zombie_collision.pos.y = zombie_collision.rect.y  # Update position vector
                    else:
                        zombie_collision.rect.y += knockback_distance
                        zombie_collision.pos.y = zombie_collision.rect.y  # Update position vector

            # Check for player death
            if self.player.health <= 0:
                # Update high score if needed
                if self.player.score > self.high_score:
                    self.high_score = self.player.score
                    write_high_score(self.high_score)
                
                # Show game over screen and handle restart
                if self.show_game_over_screen():
                    # Reset game state for restart
                    self.__init__()
                else:
                    running = False
                    break

            # Update and draw power-ups
            self.power_ups.update()
            for power_up in self.power_ups:
                self.screen.blit(power_up.surf, self.camera.apply(power_up))
            
            # Spawn power-ups periodically
            current_time = pygame.time.get_ticks()
            if current_time - self.last_power_up_spawn >= self.power_up_spawn_delay:
                self.spawn_power_up()
                self.last_power_up_spawn = current_time
            
            # Check for power-up collection
            power_up_collision = pygame.sprite.spritecollideany(self.player, self.power_ups)
            if power_up_collision:
                if power_up_collision.power_type == "fireball":
                    # Increase damage and reduce shot delay
                    self.player.fireball_damage += 5
                    self.player.shot_delay = max(200, self.player.shot_delay - 100)
                    # Show floating text to indicate power-up effect
                    power_text = PowerUpText(self.player.rect.centerx, self.player.rect.top, 
                                           "Fireball +5 DMG!")
                    self.power_up_texts.add(power_text)
                elif power_up_collision.power_type == "health":
                    self.player.health = min(100, self.player.health + 15)
                    power_text = PowerUpText(self.player.rect.centerx, self.player.rect.top, 
                                           "Health +15!")
                    self.unlock_messages.add(power_text)
                elif power_up_collision.power_type == "thanos":
                    # Get all zombies and randomly eliminate half
                    zombie_list = list(self.zombies)
                    zombies_to_remove = random.sample(zombie_list, len(zombie_list) // 2)
                    for zombie in zombies_to_remove:
                        zombie.take_damage(999)  # Instant kill
                    power_text = PowerUpText(self.player.rect.centerx, self.player.rect.top, 
                                           "Thanos Snap!")
                    self.unlock_messages.add(power_text)
                power_up_collision.kill()

            # Add after other sprite updates
            self.xp_texts.update()
            for xp_text in self.xp_texts:
                self.screen.blit(xp_text.surf, self.camera.apply(xp_text))

            # Add with other sprite updates
            self.ice_blasts.update()
            self.ice_explosions.update()
            
            # Add collision checks for ice explosions
            for explosion in self.ice_explosions:
                for zombie in self.zombies:
                    if math.sqrt((zombie.rect.centerx - explosion.center_x)**2 + 
                               (zombie.rect.centery - explosion.center_y)**2) <= explosion.radius:
                        zombie.take_damage(explosion.damage)
            
            # Add with other sprite drawing
            for ice_blast in self.ice_blasts:
                self.screen.blit(ice_blast.surf, self.camera.apply(ice_blast))
            for ice_explosion in self.ice_explosions:
                self.screen.blit(ice_explosion.surf, self.camera.apply(ice_explosion))

            # Add with other sprite updates
            self.unlock_messages.update()
            
            # Add with other sprite drawing
            for msg in self.unlock_messages:
                self.screen.blit(msg.surf, msg.rect)

            self.bombs.update()
            self.bomb_explosions.update()
            
            for bomb in self.bombs:
                self.screen.blit(bomb.surf, self.camera.apply(bomb))
            for explosion in self.bomb_explosions:
                self.screen.blit(explosion.surf, self.camera.apply(explosion))

            # Draw power-up texts directly to screen
            self.power_up_texts.update()
            for text in self.power_up_texts:
                self.screen.blit(text.surf, text.rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def spawn_power_up(self):
        # Spawn away from player
        while True:
            x = random.randint(100, MAP_WIDTH - 100)
            y = random.randint(100, MAP_HEIGHT - 100)
            # Check distance from player
            dx = x - self.player.rect.centerx
            dy = y - self.player.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 100:  # At least 200 pixels from player
                break
        
        # Randomly choose power-up type
        power_type = random.choice(["fireball", "health", "thanos"])
        power_up = PowerUp(x, y, power_type)
        self.power_ups.add(power_up)
        print(f"{power_type} power-up spawned at ({x}, {y})")  # Debug message

        # Decrease spawn delay
        if self.power_up_spawn_delay > self.min_power_up_delay:
            self.power_up_spawn_delay = max(
                self.min_power_up_delay,
                self.power_up_spawn_delay - self.power_up_delay_decrease
            )


class ShockWave(pygame.sprite.Sprite):
    def __init__(self, x, y, player_facing):
        super(ShockWave, self).__init__()
        self.center_x = x
        self.center_y = y
        self.radius = 20
        self.max_radius = 300
        self.growth_speed = 15
        self.damage = 1
        
        # Arc parameters
        self.arc_angle = 120  # Degrees (1/3 of circle)
        
        # Set start_angle based on player facing direction
        if player_facing == "right":
            self.start_angle = 120
        else:  # facing left
            self.start_angle = -60
        
        # Make surface bigger to accommodate larger radius
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


class XPText(pygame.sprite.Sprite):
    font = None
    
    def __init__(self, x, y):
        super(XPText, self).__init__()
        if XPText.font is None:
            XPText.font = pygame.font.Font(None, 24)
        self.surf = XPText.font.render("+15 XP", True, (0, 255, 0))  # Increased from 5 to 15
        self.rect = self.surf.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 1000
        self.float_speed = 1
        self.y_offset = 0
        
    def update(self):
        # Float upward
        self.y_offset -= self.float_speed
        self.rect.y += self.y_offset
        
        # Kill after lifetime
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()


class IceBlast(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super(IceBlast, self).__init__()
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (0, 191, 255), (10, 10), 10)  # Light blue
        pygame.draw.circle(self.surf, (135, 206, 250), (7, 7), 4)   # Highlight
        self.rect = self.surf.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.target = target
        self.speed = 10
        self.has_hit = False
        self.explosion_delay = 500  # 0.5 seconds
        self.hit_time = 0
        self.aoe_damage = 20
        self.aoe_radius = 200

    def update(self):
        if not self.has_hit:
            # Move towards target
            target_pos = pygame.math.Vector2(self.target.rect.center)
            direction = target_pos - self.pos
            if direction.length() > 0:
                direction = direction.normalize()
                self.pos += direction * self.speed
                self.rect.center = self.pos
            
            # Check if we've hit the target
            if self.rect.colliderect(self.target.rect):
                self.target.kill()  # Instant kill
                self.has_hit = True
                self.hit_time = pygame.time.get_ticks()
        else:
            # Check if it's time for AOE explosion
            if pygame.time.get_ticks() - self.hit_time >= self.explosion_delay:
                self.create_ice_explosion()
                self.kill()

    def create_ice_explosion(self):
        explosion = IceExplosion(self.rect.centerx, self.rect.centery, self.aoe_damage, self.aoe_radius)
        Game.instance.ice_explosions.add(explosion)


class IceExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, radius):
        super(IceExplosion, self).__init__()
        self.center_x = x
        self.center_y = y
        self.radius = radius
        self.damage = damage
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 500  # 0.5 seconds
        
    def update(self):
        progress = (pygame.time.get_ticks() - self.creation_time) / self.lifetime
        if progress >= 1:
            self.kill()
        else:
            # Create new surface each update
            self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            alpha = int(255 * (1 - progress))
            pygame.draw.circle(
                self.surf, 
                (135, 206, 250, alpha), 
                (self.radius, self.radius), 
                self.radius
            )


class IceBlastUnlockMessage(pygame.sprite.Sprite):
    def __init__(self):
        super(IceBlastUnlockMessage, self).__init__()
        self.font = pygame.font.Font(None, 48)
        self.surf = self.font.render("Ice Blast Unlocked!", True, (0, 191, 255))
        self.rect = self.surf.get_rect()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//5)
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 2000  # 2 seconds
        
    def update(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//5)

        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()


class BombUnlockMessage(pygame.sprite.Sprite):
    def __init__(self):
        super(BombUnlockMessage, self).__init__()
        self.font = pygame.font.Font(None, 48)
        self.surf = self.font.render("Bomb Unlocked!", True, (255, 140, 0))  # Orange text
        self.rect = self.surf.get_rect()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//5)
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 2000  # 2 seconds
        
    def update(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//5)

        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bomb, self).__init__()
        self.surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (139, 69, 19), (10, 10), 10)  # Brown circle
        pygame.draw.circle(self.surf, (205, 133, 63), (7, 7), 4)    # Lighter brown highlight
        self.rect = self.surf.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 5
        self.distance_traveled = 0
        self.max_distance = 200
        self.explosion_radius = 150
        self.damage = 15

    def update(self):
        # Move downward
        self.pos.y += self.speed
        self.rect.center = self.pos
        self.distance_traveled += self.speed

        # Explode when max distance reached
        if self.distance_traveled >= self.max_distance:
            self.create_explosion()
            self.kill()

    def create_explosion(self):
        # Damage all zombies within radius
        for zombie in Game.instance.zombies:
            dx = zombie.rect.centerx - self.rect.centerx
            dy = zombie.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= self.explosion_radius:
                zombie.take_damage(self.damage)
                
        # Create visual explosion
        explosion = BombExplosion(self.rect.centerx, self.rect.centery, self.explosion_radius)
        Game.instance.bomb_explosions.add(explosion)


class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(BombExplosion, self).__init__()
        self.center_x = x
        self.center_y = y
        self.radius = radius
        self.damage = 30
        self.surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(x, y))
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 500  # 0.5 seconds
        
    def update(self):
        progress = (pygame.time.get_ticks() - self.creation_time) / self.lifetime
        if progress >= 1:
            self.kill()
        else:
            # Create new surface each update
            self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            alpha = int(255 * (1 - progress))
            pygame.draw.circle(
                self.surf, 
                (255, 140, 0, alpha),  # Orange color with alpha
                (self.radius, self.radius), 
                self.radius
            )


class LevelUpMessage(pygame.sprite.Sprite):
    def __init__(self, level):
        super(LevelUpMessage, self).__init__()
        self.font = pygame.font.Font(None, 48)
        self.surf = self.font.render(f"Level {level}!", True, (255, 215, 0))  # Gold color
        
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect = self.surf.get_rect(center=(screen_width//2, screen_height//5))

        self.layer = 10

        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 2000  # 2 seconds
        
    def update(self):
        # keep centred even if the view changes
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//5)

        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()


class PowerUpText(pygame.sprite.Sprite):
    font = None
    
    def __init__(self, x, y, message):
        super(PowerUpText, self).__init__()
        if PowerUpText.font is None:
            PowerUpText.font = pygame.font.Font(None, 36)
        self.surf = PowerUpText.font.render(message, True, (240, 240, 240))
        self.rect = self.surf.get_rect()

        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//3)        

        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 1000  # 1 second
        self.float_speed = 1
        self.y_offset = 0
        
    def update(self):
        # Float upward
        # self.y_offset -= self.float_speed
        # self.rect.y += self.y_offset

        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.rect.center = (screen_width//2, screen_height//3)

        
        # Kill after lifetime
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()


if __name__ == "__main__":
    game = Game()
    game.run()

