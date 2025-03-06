require 'gosu'

module Constants
  SCREEN_WIDTH = 800
  SCREEN_HEIGHT = 600
  FPS = 60

  PLAYER_SPEED = 5
  PLAYER_START_LIVES = 5
  PLAYER_MAX_HEALTH = 100
  PLAYER_START_HEALTH = 100
  PLAYER_IMAGE = 'assets/images/player.png'

  ZOMBIE_IMAGE = 'assets/images/zombie.png'

  ENEMY_SPAWN_RATE = 2

  STATE_NAMES = {
    menu: :menu,
    playing: :playing,
    shop: :shop,
    game_over: :game_over
  }

  COLORS = {
    white: Gosu::Color::WHITE,
    black: Gosu::Color::BLACK,
    red: Gosu::Color::RED,
    green: Gosu::Color::GREEN,
    blue: Gosu::Color::BLUE,
    yellow: Gosu::Color::YELLOW,
    gray: Gosu::Color::GRAY,
    gold: Gosu::Color.new(255, 255, 215, 0)
  }

    WEAPON_COSTS = {
    fireball: 0,    # Starting weapon is free
    ice_blast: 100,
    bomb: 150,
    lightning: 200
  }

  DIRECTION_NAMES = {
    up: "Up",
    down: "Down", 
    left: "Left",
    right: "Right"
  }
end