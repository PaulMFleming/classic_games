# Four Mini Projects

_This is from a course on Zenva Academy_

- Prerequisites: Basic skills in Godot and GDScript

## Aims of this course:

- Alter object properties via script
- Build UIs
- Work with physics
- Construct loops for repeated code
- Add collision detection
- Practically apply tools to projects

## Projects

### Balloon Popper

#### Learnings

- We need a camera in 3D scenes in order for Godot to know which direction to render our screen.
- Set a material on an object by adding a new Resource of type `StandardMaterial3D`
- Add event listeners to Nodes to listen for events like mouse clicks
- `@export` before a variable in a scene allows individual instances of the scenes variables to be manipulated independently
- UI elements like Labels are 2D elements that apply directly to the players screen

### Physics

#### Learnings

- New 2D Scene
- For the Player node we used the type `RigidBody2D`
- Sprite is a child node of Player node
- Pixel art appears blurry in Godot by default, we can change that in Project Settings > Rendering > Textures > Default Texture Filter set to Nearest
- Add a `CollisionShape2D` to our player node so we can use the physics system and detect collisions
- Add a `Camera2D` node so we can see
- `Gravity Scale` and `Mass` (& other attributes) affect the physics of a `Rigidbody2D` node.
- `GravityScale` of 0 makes a node not be affected by gravity
- `GravityScale` of 1 makes it fall
- `get_global_mouse_position` is a useful function for getting direction between player and mouse
- The linear value `Damp` on a `RigidBody2D` changes drag when player moves
- Crate node also gets a sprite and a collision object
- set different drag on player and crate
