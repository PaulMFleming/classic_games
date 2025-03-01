require_relative 'projectile'

class FireballProjectile < Projectile
  def initialize(x, y, direction, damage, speed)
    super(x, y, direction, damage, speed)
    @width = 15
    @height = 15
    @color = Gosu::Color::YELLOW
  end

  def draw
    # Simple colored rectangle for now
    Gosu.draw_rect(@x, @y, @width, @height, @color)
  end
end