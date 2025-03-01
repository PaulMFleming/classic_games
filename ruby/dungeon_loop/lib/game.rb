require 'gosu'
require_relative 'constants'
require_relative 'states/state'
require_relative 'states/menu_state'
require_relative 'states/playing_state'
require_relative 'states/shop_state'
require_relative 'states/game_over_state'

Dir[File.join(__dir__, 'states', '*.rb')].each { |file| require file }

class Game < Gosu::Window
  attr_reader :width, :height
  attr_accessor :player_data

  def initialize
    puts "DEBUG: In Game.initialize"
    @width = Constants::SCREEN_WIDTH
    @height = Constants::SCREEN_HEIGHT
    super @width, @height
    self.caption = 'Dungeon Loop'

    puts "DEBUG: Creating game states..."
    @states = {
      Constants::STATE_NAMES[:menu] => MenuState.new(self),
      Constants::STATE_NAMES[:playing] => PlayingState.new(self),
      Constants::STATE_NAMES[:shop] => ShopState.new(self),
      Constants::STATE_NAMES[:game_over] => GameOverState.new(self)
    }

    @current_state = @states[Constants::STATE_NAMES[:menu]]

    @player_data = {
      lives: Constants::PLAYER_START_LIVES,
      score: 0,
      xp: 0,
      upgrades: {},
      new_game: true
    }
    puts "DEBUG: Entering initial state..."
    @current_state.enter
    puts "DEBUG: Game initialization complete"
  end

  def change_state(state_name)
    return unless @states.key?(state_name)

    @current_state.leave
    @current_state = @states[state_name]
    @current_state.enter
  end

  def update
    @current_state.update
  end

  def draw
    @current_state.draw
  end

  def button_down(id)
    close if id == Gosu::KbEscape && current_state == @states[Constants::STATE_NAMES[:menu]]
    @current_state.button_down(id)
  end

  def button_up(id)
    @current_state.button_up(id)
  end
end