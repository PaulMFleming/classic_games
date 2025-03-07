require_relative 'constants'

class Camera
  attr_reader :x, :y, :width, :height
  
  def initialize(width, height)
    @width = width
    @height = height
    @x = 0
    @y = 0
  end

  def update(target)
    # Center camera on target (player)
    @x = -target.x + Constants::SCREEN_WIDTH / 2
    @y = -target.y + Constants::SCREEN_HEIGHT / 2

    # Limit scrolling to the bounds of the map
    @x = [0, @x].min
    @y = [0, @y].min

    # Prevent camera from going out of bounds
    @x = [-(width - Constants::SCREEN_WIDTH), @x].max
    @y = [-(height - Constants::SCREEN_HEIGHT), @y].max
  end

  def world_to_screen(x, y)
    [x + @x, y +@y]
  end

  def apply(entity)
    if entity.respond_to?(:x) && entity.respond_to?(:y)
      screen_x, screen_y = world_to_screen(entity.x, entity.y)
      [screen_x, screen_y]
    else
      [0, 0]
    end
  end
end