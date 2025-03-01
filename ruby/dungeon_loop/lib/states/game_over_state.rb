require_relative 'state'
require_relative '../constants'

class GameOverState < State
  def initialize(game)
    super(game)
    @font = Gosu::Font.new(40)
  end
  
  def draw
    @font.draw_text("GAME OVER", 
                  @game.width/2 - 120, @game.height/3, 10, 1, 1, Constants::COLORS[:red])
    @font.draw_text("Final Score: #{@game.player_data[:score]}", 
                  @game.width/2 - 150, @game.height/2, 10, 1, 1, Constants::COLORS[:white])
    @font.draw_text("Press SPACE to restart", 
                  @game.width/2 - 180, @game.height*2/3, 10, 1, 1, Constants::COLORS[:white])
  end
  
  def button_down(id)
    if id == Gosu::KB_SPACE
      @game.change_state(Constants::STATE_NAMES[:menu])
    end
  end
end