require_relative '../constants'

class Weapon
  attr_reader :name, :damage, :fire_rate, :direction, :projectile_speed

  UP = :up
  DOWN = :down
  LEFT = :left
  RIGHT = :right

  def initialize(name, damage, fire_rate, projectile_speed)
    @name = name
    @damage = damage
    @fire_rate = fire_rate
    @projectile_speed = projectile_speed
    @last_fire_time = 0
  end

  def can_fire?
    Gosu.milliseconds - @last_fire_time >= @fire_rate
  end

  def fire(x, y)
    return nil unless can_fire?

    @last_fire_time = Gosu.milliseconds
    create_projectile(x, y)
  end

  # Override this in subclasses to create specific projectiles
  def create_projectile(x, y)
    raise NotImplementedError, "Subclasses must implement a create_projectile method"
  end

  def upgrade
    # Base upgrade system - override in subclasses
    @damage += 1
  end

  def to_s
    "#{@name} (#{@direction})"
  end
end