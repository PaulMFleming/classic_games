require_relative 'enemy'
require_relative '../../constants'

class Zombie < Enemy
  attr_accessor :health, :speed, :damage
  def initialize(x, y, player)
    super(x, y, player,  Constants::ZOMBIE_IMAGE)
    @health = 20
    @speed = 1
    @damage = 5
    @direction = :right
    @facing_left = false
    @original_image = @image
  end
  
  def draw
    if @facing_left
      @image.draw(@x, @y, 0, -1, 1)
    else
      @image.draw(@x, @y, 1)
    end
    
    # Draw health bar
    Gosu.draw_rect(@x, @y - 10, @width * (@health.to_f / 20), 5, Gosu::Color::GREEN)
  end
  
  def on_collision(player)
    # Zombie specific collision behavior
    # Could add things like knockback, special effects, etc.
  end
end