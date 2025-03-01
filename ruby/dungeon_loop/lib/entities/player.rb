require_relative 'entity'
require_relative '../constants'

class Player < Entity
  attr_accessor :lives, :score, :xp, :health

  def initialize(x, y)
    super(x, y, Constants::PLAYER_IMAGE)
    @health = Constants::PLAYER_START_HEALTH
    @lives = Constants::PLAYER_START_LIVES
    @score = 0
    @xp = 0
    @speed = Constants::PLAYER_SPEED
    @weapon = nil
  end

  def update
    handle_movement
    handle_attack if @weapon
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
    @weapon = weapon
  end

  private

  def handle_movement
    @x -= @speed if Gosu.button_down?(Gosu::KB_LEFT) && @x > 0
    @x += @speed if Gosu.button_down?(Gosu::KB_RIGHT) && @x < Constants::SCREEN_WIDTH - @width
    @y -= @speed if Gosu.button_down?(Gosu::KB_UP) && @y > 0
    @y += @speed if Gosu.button_down?(Gosu::KB_DOWN) && @y < Constants::SCREEN_HEIGHT - @height
  end
end