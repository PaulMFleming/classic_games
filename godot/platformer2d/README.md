# 2D Platformer

_This is from a course on Zenva Academy_

## Aims Of This Course

We will create multiple different gameplay features for the game, here is a list of what we will cover:

- **Player** – We will cover creating a player character which can move left and right using the arrow keys, and jump when the user presses the spacebar.
- **Enemies** – We will create enemies that will reset the player when they touch them. They will move back and forth between 2 points that can be set in the Editor.
- **Spikes** – Similarly to the enemies, we will create spikes, that when touched, reset the player.
- **Coins** – Coins will bob up and down using a sine wave to set their position. They can be collected by the player and will add to a score that appears on the screen as a UI element.

## Learnings

- `TileMapLayer` node is where the magic of game maps happens
  - this is where we can add `Tile Sets`
    - inport our `TileSet`
    - ensure `Tile Size` for `Tile Set` in Inspector (at right of Godot) matches `Tile Region` size in `TileSet` view (at bottom of Godot)
    - Some tile sheets have gaps between tiles - adjust with separation property as/if needed
- Once `TileSet` is set up - click on Draw in TileMap tab and select in the 2D level window and we can draw selected tiles as we wish (right click deletes)
- Add physics to tiles by painting which tiles we want to have Physics layer 0 set on in the TileSet tap
- Player is a `CollisionShape2D` node
  - In a more complex game, we might want some colliders to interact with some other colliders, but not all. For our game though, it’s not a problem.
    - **Layer Section** – This describes the collision layer that the object appears in. By default, all bodies are on layer 1.
    - **Mask Section** – This describes what layers the body will check for collisions. If you want this object to ignore certain layers, you can disable them here.
- call `move_and_slide()` to initiate movement
- put all physics logic in the `_physics_process` function (our physics game loop)
- `is_on_floor()` detects if Player is on the floor
- `get_tree()` function gets the current Node tree
