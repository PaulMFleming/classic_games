extends Node2D

@export var spawn_count : int = 200
var star_scene = preload("res://Loops/Star.tscn")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	for i in spawn_count:
		var star = star_scene.instantiate()
		add_child(star)
		
		star.position.x = randi_range(-280, 280)
		star.position.y = randi_range(-150, 150)
