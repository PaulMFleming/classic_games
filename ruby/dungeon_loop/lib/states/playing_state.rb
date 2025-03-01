require_relative 'state'
require_relative '../entities/player'
require_relative '../entities/enemies/zombie'

class PlayingState < State
  def enter
    # Load or create player
    if @game.player_data[:new_game]
      @player = Player.new(@game.width/2, @game.height/2)
      @player.lives = @game.player_data[:lives]
      @player.score = @game.player_data[:score]
      @player.xp = @game.player_data[:xp]
      
      # Apply purchased upgrades
      apply_upgrades
    else
      # New game
      @player = Player.new(@game.width/2, @game.height/2)
      @game.player_data[:new_game] = false
    end
    
    @enemies = []
    @projectiles = []
    @powerups = []
    @last_enemy_spawn = Gosu.milliseconds
  end
  
  def leave
    # Save player data for next state
    @game.player_data[:lives] = @player.lives
    @game.player_data[:score] = @player.score
    @game.player_data[:xp] = @player.xp
  end
  
  def update
    @player.update
    
    # Spawn enemies periodically
    if Gosu.milliseconds - @last_enemy_spawn > 2000 # Every 2 seconds
      spawn_enemy
      @last_enemy_spawn = Gosu.milliseconds
    end
    
    @enemies.each(&:update)
    @projectiles.each(&:update)
    handle_collisions
    
    # Check if player died
    if @player.health <= 0
      @player.lose_life
      if @player.lives > 0
        @game.change_state(Constants::STATE_NAMES[:shop])
      else
        @game.change_state(Constants::STATE_NAMES[:game_over])
      end
    end
  end
  
  def draw
    @player.draw
    @enemies.each(&:draw)
    @projectiles.each(&:draw)
    @powerups.each(&:draw)
    
    # Draw HUD
    draw_hud
  end
  
  def button_down(id)
    # Handle gameplay input
  end
  
  private
  
  def spawn_enemy
    @enemies << Zombie.new(rand(@game.width), -50, @player)
  end
  
  def handle_collisions
    # Projectile-enemy collisions
    @projectiles.each do |projectile|
      @enemies.each do |enemy|
        if projectile.collides_with?(enemy)
          enemy.take_damage(projectile.damage)
          projectile.hit
          @player.score += 1
          @player.xp += 5
          break
        end
      end
    end
    
    # Enemy-player collisions
    @enemies.each do |enemy|
      if enemy.collides_with?(@player)
        @player.take_damage(enemy.damage)
        enemy.on_collision(@player)
      end
    end
    
    # Clean up dead entities
    @enemies.reject!(&:dead?)
    @projectiles.reject!(&:dead?)
  end
  
  def draw_hud
    # Draw score
    Gosu.draw_text("Score: #{@player.score}", 10, 10, 10, 1, 1, Constants::COLORS[:white])
    
    # Draw lives
    Gosu.draw_text("Lives: #{@player.lives}", 10, 30, 10, 1, 1, Constants::COLORS[:white])
    
    # Draw XP
    Gosu.draw_text("XP: #{@player.xp}", 10, 50, 10, 1, 1, Constants::COLORS[:gold])
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