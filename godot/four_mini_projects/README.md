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
- Convert Crate node to a Scene so we can add multiples

##### Physics Properties

- **Mass** – How heavy the object is in kilograms. The heavier it is, the more force required to move it.
- **Physics Material Override** – This is a resource where you can define levels of bounciness, friction, etc for the object.
- **Gravity Scale** – How strongly gravity will pull down the object.
- **Linear Velocity** – The velocity that will be applied each frame.
- **Linear Damp** – This acts as drag applied to the velocity, think air resistance.
- **Angular Velocity** – The velocity but for rotation.
- **Angular Damp** – Drag applied to the angular velocity.

### Loops

#### Learnings

- We can preload scenes like this

```
var star_scene = preload("res://Loops/Star.tscn")

# instansiate
var star = star_scene.instantiate()

# add as child element
add_child(star)
```

- ranges are different for float and int:

```
randi_range(1, 5)
randf_range(0.2, 1.4)
```

- change background color in Project Settings > Rendering > Environmnet > Default Clear Color

### Collision

#### Learnings

- `StaticBody3D` node is for having physical, static objects in a 3D game world
- Add a `MeshInstance3D` child node to the `StaticBody3D`, we gie it a Box Mesh
- We add a `CollisionShape3D` as a child node of our `StaticBody3d` node
- We can rotate the box on the x axis to get a slope - this is our ski slope
- `RigidBody3D` for our Player
- Create child nodes and give them Surface Materials to create a model of a player character on skis
- Add the `CollisionShape3D` child node to Player
- Add Camera (this is a child of Player) and Lighting nodes
- Add a `WorldEnvironment` child node and change background to custom color
