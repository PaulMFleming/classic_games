class Entity
  attr_reader :x, :y, :width, :height

  def initialize(x, y, image_path=nil)
    @x = x
    @y = y
    @image = Gosu::Image.new(image_path) if image_path
    @width = @image.width if @image
    @height = @image.height if @image
  end

  def update
    # Base logic here
  end

  def draw
    @image.draw(@x, @y, 1)
  end

  def draw_at(screen_x, screen_y)
    if @image
      if @facing_left
        @image.draw(screen_x, screen_y, 0, -1, 1)
      else
        @image.draw(screen_x, screen_y, 1)
      end
    else
      Gosu.draw_rect(screen_x, screen_y, @width, @height, Gosu::Color::RED)
    end
  end

  def collides_with?(entity)
    @x < entity.x + entity.width &&
    @x + @width > entity.x &&
    @y < entity.y + entity.height &&
    @y + @height > entity.y
  end
end