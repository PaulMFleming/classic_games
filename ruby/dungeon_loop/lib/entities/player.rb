require_relative 'entity'
require_relative '../constants'
require_relative '../weapons/projectiles/fireball_projectile'
require_relative '../weapons/projectiles/projectile'
require_relative '../weapons/weapon'
require_relative '../weapons/fireball'

class Player < Entity
  attr_accessor :lives, :score, :xp, :health, :max_health, :speed, :weapons

  def initialize(x, y)
    super(x, y, Constants::PLAYER_IMAGE)
    @health = Constants::PLAYER_START_HEALTH
    @max_health = Constants::PLAYER_MAX_HEALTH
    @lives = Constants::PLAYER_START_LIVES
    @score = 0
    @xp = 0
    @speed = Constants::PLAYER_SPEED
    @weapons = []

    equip_weapon(FireballWeapon.new)
  end

  def update
    handle_movement
    fire_weapons
  end

  def draw
    super
    Gosu.draw_rect(@x, @y - 10, @width * @health / Constants::PLAYER_START_HEALTH, 5, Constants::COLORS[:green])
  end

  def take_damage(amount)
    @health -= amount
    @heallt = [0, @health].max
  end

  def lose_life
    @lives -= 1
    @health = Constants::PLAYER_START_HEALTH
  end

  def equip_weapon(weapon)
    return false if @weapons.length >= 4
    @weapons << weapon
    true
  end

  def fire_weapons
    fired_projectiles = []
    
    @weapons.each do |weapon|
      projectile = weapon.fire(@x, @y)
      if projectile
        puts "DEBUG: Adding projectile to fired_projectiles array: #{projectile.inspect}"
        fired_projectiles << projectile 
      end
    end
    
    # Add this debug to see if projectiles are being returned
    puts "DEBUG: Returning #{fired_projectiles.length} projectiles from fire_weapons"
    
    # Return the array of fired projectiles
    fired_projectiles
  end

  private

  def handle_movement
    @x -= @speed if Gosu.button_down?(Gosu::KB_LEFT) && @x > 0
    @x += @speed if Gosu.button_down?(Gosu::KB_RIGHT) && @x < Constants::SCREEN_WIDTH - @width
    @y -= @speed if Gosu.button_down?(Gosu::KB_UP) && @y > 0
    @y += @speed if Gosu.button_down?(Gosu::KB_DOWN) && @y < Constants::SCREEN_HEIGHT - @height
  end
end