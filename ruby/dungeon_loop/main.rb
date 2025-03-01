require_relative 'lib/game'

puts "DEBUG: Starting Dungeon Loop game..."

begin
  puts "DEBUG: Creating game instance..."
  game = Game.new
  puts "DEBUG: Game instance created, showing window..."
  game.show
  puts "DEBUG: Game window closed."
rescue => e
  puts "DEBUG: Error encountered:"
  puts e.message
  puts e.backtrace
end

puts "DEBUG: Game script finished."

if __FILE__ == $DUNGEON_LOOP
  game = Game.new.play
  game.show
end