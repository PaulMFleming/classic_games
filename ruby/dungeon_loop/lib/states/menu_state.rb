require_relative 'state'
require_relative '../constants'

class MenuState < State
  def initialize(game)
    super(game)
    @title_font = Gosu::Font.new(50)
    @normal_font = Gosu::Font.new(30)
  end
  
  def enter
    # Reset player data for a new game
    @game.player_data = {
      score: 0,
      xp: 0,
      lives: Constants::PLAYER_START_LIVES,
      upgrades: {},
      new_game: true
    }
  end
  
  def draw
    @title_font.draw_text("DUNGEON LOOP", 
                       @game.width/2 - 180, 
                       @game.height/3, 
                       10, 
                       1.0, 
                       1.0, 
                       Constants::COLORS[:yellow])
                       
    @normal_font.draw_text("Press Space to Start", 
                        @game.width/2 - 130, 
                        @game.height/2, 
                        10, 
                        1.0, 
                        1.0, 
                        Constants::COLORS[:white])
  end
  
  def button_down(id)
    if id == Gosu::KB_SPACE
      @game.change_state(Constants::STATE_NAMES[:playing])
    end
  end
end