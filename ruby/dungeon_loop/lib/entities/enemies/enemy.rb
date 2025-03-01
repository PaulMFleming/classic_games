require_relative '../entity'

class Enemy < Entity
  attr_reader :damage, :health
  
  def initialize(x, y, player)
    super(x, y)
    @player = player
    @health = 10
    @speed = 1
    @damage = 1
    @dead = false
  end
  
  def update
    # Base enemy update logic
    move_towards_player
  end
  
  def take_damage(amount)
    @health -= amount
    @dead = true if @health <= 0
  end
  
  def on_collision(player)
    # Default collision behavior
  end
  
  private
  
  def move_towards_player
    # Calculate direction to player
    dx = @player.x - @x
    dy = @player.y - @y
    
    # Normalize direction
    length = Math.sqrt(dx * dx + dy * dy)
    if length > 0
      dx /= length
      dy /= length
    end
    
    # Move in that direction
    @x += dx * @speed
    @y += dy * @speed
  end
end