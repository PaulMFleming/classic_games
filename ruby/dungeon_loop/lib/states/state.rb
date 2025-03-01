class State
  def initialize(game)
    @game = game
  end

  def enter
    # Called when entering the state
  end

  def leave
    # Called when leaving the state
  end

  def update
    # Handle state logic
  end

  def draw
    # Draw the state elements
  end

  def button_down(id)
    # Handle input
  end

  def button_up(id)
    # Handle input release
  end
end