extends Node2D

var score : int = 5
var move_speed : float = 2.54
var game_over : bool = false
var ability : String = "slash"

# Called when the node enters the scene tree for the first time.
func _ready():
	move_speed = 5.4
	print(move_speed)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
