require_relative 'lib/game'

if __FILE__ == $DUNGEON_LOOP
  game = Game.new.play
  game.show
end