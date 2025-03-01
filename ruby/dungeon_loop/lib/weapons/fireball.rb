require_relative 'weapon'
require_relative '../projectiles/fireball_projectile'

class FireballWeapon < Weapon
  def initialize(direction = Weapon::RIGHT)
    # name, damage, fire_rate (ms), direction, projectile_speed
    super("Fireball", 10, 1000, direction, 8)
  end
  
  def create_projectile(x, y)
    FireballProjectile.new(x, y, @direction, @damage, @projectile_speed)
  end
  
  def upgrade
    super
    @fire_rate = (@fire_rate * 0.9).to_i  # 10% faster firing
    @projectile_speed += 1
  end
end