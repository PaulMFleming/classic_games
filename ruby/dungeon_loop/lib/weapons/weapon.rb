require_relative '../constants'

class Weapon
  attr_reader :name, :damage, :fire_rate, :direction, :projectile_speed

  UP = :up
  DOWN = :down
  LEFT = :left
  RIGHT = :right

  def initialize(name, damage, fire_rate, direction, projectile_speed, image_path=nil)
    @name = name
    @damage = damage
    @fire_rate = fire_rate
    @direction = direction
    @projectile_speed = projectile_speed
    @last_fire_time = 0

    @image = Gosu::Image.new(image_path) if image_path
    @width = @image.width if @image
    @height = @image.height if @image
  end

  def can_fire?
    Gosu.milliseconds - @last_fire_time >= @fire_rate
  end

  def fire(x, y)
    return nil unless can_fire?

    puts "DEBUG: Firing #{@name} in direction #{@direction}"
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

  def update_direction(new_direction)
    @direction = new_direction
  end
end