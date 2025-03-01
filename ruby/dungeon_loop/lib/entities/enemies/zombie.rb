require_relative 'enemy'
require_relative '../../constants'

class Zombie < Enemy
  def initialize(x, y, player)
    super(x, y, player)
    @health = 20
    @speed = 1
    @damage = 5
    
    # Create a temporary colored rectangle as placeholder
    @width = 30
    @height = 30
    @color = Gosu::Color::RED
  end
  
  def draw
    # Draw a colored rectangle as placeholder
    Gosu.draw_rect(@x, @y, @width, @height, @color)
    
    # Draw health bar
    Gosu.draw_rect(@x, @y - 10, @width * (@health.to_f / 20), 5, Gosu::Color::GREEN)
  end
  
  def on_collision(player)
    # Zombie specific collision behavior
    # Could add things like knockback, special effects, etc.
  end
end