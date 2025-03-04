# Dungeon Loop

Dungeon Loop Game

## Bug List

- [x] Lives are not decreasing when new round starts

## To-Do List

- [ ] add Zombie image
- [x] change player direction with movement
- [x] fix bugs introduced by weapons
- [x] implement fireball weapon
- [x] add projectile class
- [x] add weapon class
- [x] fix lives bug
- [x] fix any bugs from below tasks to get basic implementation running
- [x] Game over state
- [x] Shop state
- [x] Menu state
- [x] Zombie Class
- [x] Enemy Class
- [x] State machine implementation
- [x] Player and Entity Classes
- [x] Core files setup
- [x] set up basic structure following this outline:

```
dungeon_loop/
├── main.rb # Entry point
├── lib/
│ ├── game.rb # Main game class with state management
│ ├── constants.rb # Game constants
│ ├── states/
│ │ ├── state.rb # Base state class
│ │ ├── menu_state.rb # Main menu
│ │ ├── playing_state.rb # Main gameplay
│ │ ├── shop_state.rb # Shop after death
│ │ └── game_over_state.rb # Game over screen
│ ├── entities/
│ │ ├── entity.rb # Base entity class
│ │ ├── player.rb # Player with lives system
│ | └── enemies/      <-- This subdirectory
│ |     ├── enemy.rb  <-- Base enemy class
│ |     ├── zombie.rb <-- Specific enemy implementation
│ |     └── monster.rb
│ ├── weapons/
│ │ ├── weapon.rb # Base weapon class
│ │ ├── fireball.rb # Basic weapon
│ │ ├── ice_blast.rb # Unlockable weapon
│ │ └── bomb.rb # Unlockable weapon
│ ├── ui/
│ │ ├── hud.rb # Game HUD (lives, score, etc.)
│ │ ├── shop_ui.rb # Shop interface elements
│ │ └── notifications.rb # Message pop-ups
│ ├── items/
│ │ ├── item.rb # Base item class
│ │ ├── powerup.rb # In-game powerups
│ │ └── shop_item.rb # Items in the shop
│ └── utils/
│ ├── collision.rb # Collision detection
│ ├── score.rb # Score handling
│ └── save_system.rb # Save/load game state
└── assets/
├── images/ # Game sprites and images
└── sounds/ # Sound effects and music
```
