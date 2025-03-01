# Dungeon Loop

## To-Do List

- [ ]
- [ ] State machine implementation
- [ ] Player and Entity Classes
- [ ] Core files setup
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
│ │ └── enemies/
│ │ ├── enemy.rb # Base enemy class
│ │ ├── zombie.rb # Basic enemy
│ │ └── monster.rb # Ranged enemy
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
