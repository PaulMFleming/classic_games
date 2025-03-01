class Projectile
  attr_reader :x, :y, :damage, :width, :height
  
  def initialize(x, y, direction, damage, speed)
    @x = x
    @y = y
    @direction = direction
    @damage = damage
    @speed = speed
    @width = 10
    @height = 10
    @hit = false
  end
  
  def update
    case @direction
    when Weapon::UP
      @y -= @speed
    when Weapon::DOWN
      @y += @speed
    when Weapon::LEFT
      @x -= @speed
    when Weapon::RIGHT
      @x += @speed
    end
    
    # Check if out of bounds
    if @x < 0 || @x > Constants::SCREEN_WIDTH || 
       @y < 0 || @y > Constants::SCREEN_HEIGHT
      @hit = true
    end
  end
  
  def hit
    @hit = true
  end
  
  def dead?
    @hit
  end
  
  def collides_with?(entity)
    @x < entity.x + entity.width &&
    @x + @width > entity.x &&
    @y < entity.y + entity.height &&
    @y + @height > entity.y
  end
end