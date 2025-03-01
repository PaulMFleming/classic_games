require_relative 'state'
require_relative '../constants'

class ShopState < State
  def initialize(game)
    super(game)
    @font = Gosu::Font.new(30)
    @items = []
    @selected_item = 0
  end
  
  def enter
    @items = generate_shop_items
    @selected_item = 0
  end
  
  def update
    # Shop animations if any
  end
  
  def draw
    @font.draw_text("SHOP", @game.width/2 - 50, 50, 10, 1, 1, Constants::COLORS[:gold])
    @font.draw_text("XP: #{@game.player_data[:xp]}", 50, 100, 10, 1, 1, Constants::COLORS[:white])
    
    # Draw shop items
    @items.each_with_index do |item, index|
      color = (index == @selected_item) ? Constants::COLORS[:yellow] : Constants::COLORS[:white]
      @font.draw_text("#{item[:name]} - #{item[:cost]} XP", 
                    100, 150 + index * 40, 10, 1.0, 1.0, color)
    end
    
    @font.draw_text("Press SPACE to buy, ENTER to continue", 
                  @game.width/2 - 200, @game.height - 100, 10, 1, 1, Constants::COLORS[:white])
  end
  
  def button_down(id)
    case id
    when Gosu::KB_UP
      @selected_item = (@selected_item - 1) % @items.length
    when Gosu::KB_DOWN
      @selected_item = (@selected_item + 1) % @items.length
    when Gosu::KB_SPACE
      buy_item(@items[@selected_item])
    when Gosu::KB_RETURN
      # Continue game with upgrades
      @game.player_data[:new_game] = false
      @game.change_state(Constants::STATE_NAMES[:playing])
    end
  end
  
  private
  
  def generate_shop_items
    [
      {name: "Health +10", cost: 50, effect: :health_max},
      {name: "Speed +1", cost: 75, effect: :speed}
    ]
  end
  
  def buy_item(item)
    if @game.player_data[:xp] >= item[:cost]
      @game.player_data[:xp] -= item[:cost]
      
      # Update upgrades
      @game.player_data[:upgrades][item[:effect]] ||= 0
      @game.player_data[:upgrades][item[:effect]] += 1
    end
  end
end