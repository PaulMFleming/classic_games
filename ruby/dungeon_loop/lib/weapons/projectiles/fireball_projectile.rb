require_relative 'projectile'

class FireballProjectile < Projectile
  def initialize(x, y, direction, damage, speed)
    super(x, y, direction, damage, speed)
    @width = 15
    @height = 15
    @color = Gosu::Color::YELLOW
    puts "DEBUG: FireballProjectile initialized at (#{x}, #{y}) with direction #{direction}"

  end

  def draw
    # Simple colored rectangle for now
    Gosu.draw_rect(@x, @y, @width, @height, @color)
  end

  def update
    super
    puts "DEBUG: FireballProjectile position (#{@x}, #{@y})"
  end
end