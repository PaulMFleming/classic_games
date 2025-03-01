require 'gosu'
require_relative 'constants'

Dir[File.join(__dir__, 'states', '*.rb')].each { |file| require file }

class Game < Gosu::Window
  attr_reader :width, :height
  attr_accessor :player_data

  def initialize
    @width = Constants::SCREEN_WIDTH
    @height = Constants::SCREEN_HEIGHT
    super @width, @height
    self.caption = 'Dungeon Loop'

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
      upgrades: {}
    }

    @current_state.enter
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