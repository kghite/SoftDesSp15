from swampy.TurtleWorld import *
from math import *
import copy

def draw_line(turtle, angle, start_x, start_y, line_length):
	turtle.x = start_x
	turtle.y = start_y
	turtle.lt(angle)
	turtle.fd(line_length)

def snow_flake_side(turtle, length, level):
	""" Draw a side of the snowflake curve with side
		length length and recursion depth of level """
	if level == 0:
		# Draw base case
		draw_line(turtle, 0, turtle.x, turtle.y, length)
		draw_line(turtle, -60, turtle.x, turtle.y, length)
		draw_line(turtle, 120, turtle.x, turtle.y, length)
		draw_line(turtle, -60, turtle.x, turtle.y, length)
	else:
		snow_flake_side(beth, length/3.0, level-1)
		rt(turtle, 60)
		snow_flake_side(beth, length/3.0, level-1)
		lt(turtle, 120)
		snow_flake_side(beth, length/3.0, level-1)
		rt(turtle, 60)
		snow_flake_side(beth, length/3.0, level-1)

def snow_flake(turtle, length, level):
	snow_flake_side(turtle, length, level)
	lt(turtle, 120)
	snow_flake_side(turtle, length, level)
	lt(turtle, 120)
	snow_flake_side(turtle, length, level)

def recursive_tree(turtle, branch_length, level):
	""" Draw a tree with branch length branch_length
		and recursion depth of level """
	if level == 0:
		fd(turtle, branch_length)
	else:
		fd(turtle, branch_length)
		clone = copy.copy(turtle)
		lt(clone, 30)
		recursive_tree(clone, branch_length*0.6, level-1)
		Turtle.undraw(clone)
		bk(turtle, branch_length/3.0)
		clone = copy.copy(turtle)
		rt(clone, 40)
		recursive_tree(clone, branch_length*0.64, level-1)
		Turtle.undraw(clone)


# Initialize turtle stuff
world = TurtleWorld()
beth = Turtle()
beth.set_color('green')
beth.set_pen_color('red')
beth.delay = 0.1
lt(beth, 90)

#snow_flake(beth, 75, 4)
recursive_tree(beth, 100, 3)

wait_for_user()