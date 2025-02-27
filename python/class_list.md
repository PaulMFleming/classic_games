# Dungeon Survivor Classes

## Player Classes

- **Player**: Main player character with movement controls, health, and attack abilities

## Enemy Classes

- **Zombie**: Basic enemy that follows the player with various personalities (Wanderer, Speedy, Agile, Hunter)

## Weapon/Attack Classes

- **Fireball**: Basic projectile attack fired by the player
- **ShockWave**: Arc-shaped area attack that pushes enemies back
- **IceBlast**: Targeted attack that follows an enemy and creates an explosion
- **IceExplosion**: Area effect created when IceBlast hits a target
- **Bomb**: Deployable explosive that moves downward and explodes
- **BombExplosion**: Area effect created when a Bomb explodes

## Visual Effects/UI Classes

- **XPText**: Floating text showing XP gains when enemies die
- **PowerUpText**: Text displaying power-up effects when collected
- **LevelUpMessage**: Center-screen notification when player levels up
- **IceBlastUnlockMessage**: Notification when Ice Blast is unlocked
- **BombUnlockMessage**: Notification when Bomb is unlocked

## Game System Classes

- **Camera**: Controls the visible portion of the game world
- **PowerUp**: Collectible items that provide various bonuses (fireball, health, thanos)
- **Game**: Main game controller that manages game state and updates

## Utility Functions

- **read_high_score()**: Function to read high score from file
- **write_high_score()**: Function to write high score to file
