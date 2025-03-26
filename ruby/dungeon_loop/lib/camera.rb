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
    target_x = target.x
    target_y = target.y

    # Move to camera to center of target
    desired_x = -target_x + Constants::SCREEN_WIDTH / 2
    desired_y = -target_y + Constants::SCREEN_HEIGHT / 2

    
    # Apply boundary limits with more explicit logic
    # Don't let camera go beyond left edge of game world
    @x = if desired_x > 0  
      0
    # Don't let camera go beyond right edge of game world  
    elsif desired_x < -(width - Constants::SCREEN_WIDTH)
      -(width - Constants::SCREEN_WIDTH)
    # Within bounds, use the desired position
    else
      desired_x
    end

    # Same logic for Y axis
    @y = if desired_y > 0
          0
        elsif desired_y < -(height - Constants::SCREEN_HEIGHT)
          -(height - Constants::SCREEN_HEIGHT)
        else
          desired_y
        end

    # Print debug info occasionally
    if rand < 0.1
    puts "DEBUG: Camera position: (#{@x}, #{@y}), Player position: (#{target_x}, #{target_y})" 
    puts "DEBUG: Map size: #{width}x#{height}, Screen size: #{Constants::SCREEN_WIDTH}x#{Constants::SCREEN_HEIGHT}"
    end
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