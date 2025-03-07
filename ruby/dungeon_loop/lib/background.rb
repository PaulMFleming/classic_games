require_relative 'constants'

class Background
  def initialize
    @background_image = Gosu::Image.new(Constants::BACKGROUND_IMAGE)
    @tile_width = @background_image.width
    @tile_height = @background_image.height
    
    # Calculate how many tiles we need to cover the map
    @tiles_x = (Constants::MAP_WIDTH.to_f / @tile_width).ceil + 1
    @tiles_y = (Constants::MAP_HEIGHT.to_f / @tile_height).ceil + 1
  end
  
  def draw(camera)
    # Calculate the visible area based on camera position
    start_x = [0, (-camera.x / @tile_width).floor].max
    start_y = [0, (-camera.y / @tile_height).floor].max
    
    end_x = [((Constants::SCREEN_WIDTH - camera.x) / @tile_width).ceil, @tiles_x].min
    end_y = [((Constants::SCREEN_HEIGHT - camera.y) / @tile_height).ceil, @tiles_y].min
    
    # Draw only tiles visible in the camera's view
    (start_y..end_y).each do |y|
      (start_x..end_x).each do |x|
        # Calculate screen position
        screen_x = x * @tile_width + camera.x
        screen_y = y * @tile_height + camera.y
        
        # Draw the background tile
        @background_image.draw(screen_x, screen_y, 0)
      end
    end
  end
end