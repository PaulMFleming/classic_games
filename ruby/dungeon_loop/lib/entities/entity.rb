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

  def collides_with?(entity)
    @x < entity.x + entity.width &&
    @x + @width > entity.x &&
    @y < entity.y + entity.height &&
    @y + @height > entity.y
  end
end