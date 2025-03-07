require_relative 'state'
require_relative '../entities/player'
require_relative '../entities/enemies/zombie'
require_relative '../camera'

class PlayingState < State
  def initialize(game)
    super(game)
    @player = nil
    @enemies = []
    @projectiles = []
    @last_enemy_spawn = 0
    
    # Create a camera with the map dimensions from constants
    @camera = Camera.new(Constants::MAP_WIDTH, Constants::MAP_HEIGHT)
  end

  def enter
    # Initialize new game state or load existing
    if @game.player_data[:new_game] == false
      @player = Player.new(Constants::MAP_WIDTH/2, Constants::MAP_HEIGHT/2)
      @player.lives = @game.player_data[:lives]
      @player.score = @game.player_data[:score]
      @player.xp = @game.player_data[:xp]
      
      # Apply purchased upgrades if any
      apply_upgrades if defined?(apply_upgrades)
    else
      # New game - start player in the middle of the map
      @player = Player.new(Constants::MAP_WIDTH/2, Constants::MAP_HEIGHT/2)
      @game.player_data[:new_game] = false
    end
    
    @enemies = []
    @projectiles = []
    @last_enemy_spawn = Gosu.milliseconds
    
    # Create the camera object
    @camera = Camera.new(Constants::MAP_WIDTH, Constants::MAP_HEIGHT)
  end
  
  def leave
    # Save player data for next state
    @game.player_data[:lives] = @player.lives
    @game.player_data[:score] = @player.score
    @game.player_data[:xp] = @player.xp
  end
  
  def update
    # Get any new projectiles from player
    new_projectiles = @player.fire_weapons
    @projectiles.concat(new_projectiles) if new_projectiles.any?
    
    # Update all entities
    @player.update
    @enemies.each(&:update)
    @projectiles.each(&:update)
    
    # Important: Update camera position to follow player
    @camera.update(@player)
    
    # Handle collisions
    handle_collisions
    
    # Spawn enemies periodically
    if Gosu.milliseconds - @last_enemy_spawn > Constants::ENEMY_SPAWN_RATE * 1000
      spawn_enemy
      @last_enemy_spawn = Gosu.milliseconds
    end
    
    # Check if player died
    if @player.health <= 0
      @player.lose_life
      puts "DEBUG: Player died! Lives remaining: #{@player.lives}"
      
      @game.player_data[:lives] = @player.lives
      @game.player_data[:score] = @player.score
      @game.player_data[:xp] = @player.xp
      
      if @player.lives > 0
        @game.change_state(Constants::STATE_NAMES[:shop])
      else
        @game.change_state(Constants::STATE_NAMES[:game_over])
      end
    end
  end
  
  def draw
    # Clear screen
    Gosu.draw_rect(0, 0, Constants::SCREEN_WIDTH, Constants::SCREEN_HEIGHT, Constants::COLORS[:black])
    
    # Use the draw_entity helper method to draw entities with camera transformation
    draw_entity(@player)
    @enemies.each { |enemy| draw_entity(enemy) }
    @projectiles.each { |projectile| draw_entity(projectile) }
    
    # Draw HUD elements (score, lives, etc.) - these don't need camera transformation
    draw_hud
  end

  def draw_entity(entity)
    screen_x, screen_y = @camera.apply(entity)

    if entity.respond_to?(:draw_at)
      # If the entity has its own draw_at method, use it
      entity.draw_at(screen_x, screen_y)
    elsif entity.respond_to?(:image) && entity.image
      # If entity has an image, draw it
      if entity.respond_to?(:facing_left) && entity.facing_left
        entity.image.draw(screen_x, screen_y, 1, -1, 1)  # Flipped horizontally
      else
        entity.image.draw(screen_x, screen_y, 1)
      end
    else
      # Fallback drawing as a colored rectangle
      Gosu.draw_rect(screen_x, screen_y, entity.width, entity.height, Gosu::Color::RED)
    end
  end
  
  def button_down(id)
    # Handle gameplay input
  end
  
  private
  
  def spawn_enemy
    # Spawn enemies at random locations around the map edges
    side = rand(4)  # 0 = top, 1 = right, 2 = bottom, 3 = left
    
    case side
    when 0  # Top
      x = rand(Constants::MAP_WIDTH)
      y = 0
    when 1  # Right
      x = Constants::MAP_WIDTH
      y = rand(Constants::MAP_HEIGHT)
    when 2  # Bottom
      x = rand(Constants::MAP_WIDTH)
      y = Constants::MAP_HEIGHT
    when 3  # Left
      x = 0
      y = rand(Constants::MAP_HEIGHT)
    end
    
    # Add a new enemy at the calculated position
    @enemies << Zombie.new(x, y, @player)
  end
  
  def handle_collisions
    # Handle projectile-enemy collisions
    @projectiles.each do |projectile|
      @enemies.each do |enemy|
        if projectile.collides_with?(enemy)
          enemy.take_damage(projectile.damage)
          projectile.hit
          @player.score += 10  # Award points for hitting enemy
        end
      end
    end
    
    # Remove dead enemies and projectiles
    @enemies.reject! { |enemy| enemy.dead? }
    @projectiles.reject! { |projectile| projectile.dead? }
    
    # Check player-enemy collisions
    @enemies.each do |enemy|
      if @player.collides_with?(enemy)
        @player.take_damage(enemy.damage)
        enemy.on_collision(@player) if enemy.respond_to?(:on_collision)
      end
    end
  end
  
  def draw_hud
    @hud_font ||= Gosu::Font.new(20)
    # Draw score
    @hud_font.draw_text("Score: #{@player.score}", 10, 10, 10, 1, 1, Constants::COLORS[:white])
    
    # Draw lives
    @hud_font.draw_text("Lives: #{@player.lives}", 10, 30, 10, 1, 1, Constants::COLORS[:white])
    
    # Draw XP
    @hud_font.draw_text("XP: #{@player.xp}", 10, 50, 10, 1, 1, Constants::COLORS[:gold])
    
    # Draw health bar
    health_width = 200 * (@player.health.to_f / @player.max_health)
    Gosu.draw_rect(10, 50, 200, 20, Constants::COLORS[:red])
    Gosu.draw_rect(10, 50, health_width, 20, Constants::COLORS[:green])
  end
  
  def apply_upgrades
    # Apply upgrades from the shop
    @game.player_data[:upgrades].each do |upgrade_type, level|
      case upgrade_type
      when :health_max
        @player.max_health += level * 10
      when :fireball_damage
        # Apply weapon upgrades
      end
    end
  end
end