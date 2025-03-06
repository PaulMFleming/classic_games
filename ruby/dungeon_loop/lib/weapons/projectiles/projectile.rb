class Projectile
  attr_reader :x, :y, :damage, :width, :height
  
  def initialize(x, y, direction, damage, speed, image_path=nil)
    @x = x
    @y = y
    @direction = direction
    @damage = damage
    @speed = speed
    @width = 10
    @height = 10
    @hit = false

    if image_path && !image_path.empty?
      @image = Gosu::Image.new(image_path)
      @width = @image.width
      @height = @image.height
    end
  end

  def draw
    if @image
      @image.draw(@x, @y, 1)
    else
      # Default drawing if no image (for debugging)
      Gosu.draw_rect(@x, @y, @width, @height, Gosu::Color::WHITE)
    end
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