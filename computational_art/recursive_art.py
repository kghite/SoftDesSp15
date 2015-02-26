""" Author: Kathryn Hite
    Date: 2/18/15
    Description: Generate random art """

import math
import random
from PIL import Image

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    function_parts = ["prod", "avg", "cos_pi", "sin_pi", "divide", "power"]
    function = random.choice(function_parts)

    #it's often kind of a convention (at least from what I've seen) to put your base case in a recursive function first, instead of at the end.

    if max_depth > 0:
        if min_depth > 0:
            if function == "avg" or function == "prod":
                return [function, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
            else:
                return [function, build_random_function(min_depth-1, max_depth-1)]
        else:
            function_parts = ["prod", "avg", "cos_pi", "sin_pi", "divide", "power", "x", "y"]
            function = random.choice(function_parts)
            if function == "avg" or function == "prod":
                return [function, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
            elif function == "x" or function == "y":
                if random.randint(0,2) == 1:
                    return "x"
                else:
                    return "y"
            else:
                return [function, build_random_function(min_depth, max_depth-1)]
                #looks like you forgot to give min_depth - 1 as the argument here. Or was this intentional? 
                #Correct me if I'm wrong, it looks like your approach to randomly choosing whether or not to go deeper/recurse more once you've reached min_depth is to randomly choose a function, and then go deeper if that function happens to be cos_pi, sin_pi, divide, or power. This works, but isn't the most robust, as it means that you can't have prod or avg appear deeper than min_depth in your function, reducting the randomness.
                #that could all be arguably intentional, but there would have to be comments explaining your thought process.
    else:
        #or, try return random.choice(['x','y'])!
        if random.randint(0,1) == 1:
            return "x"
        else:
            return "y"

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["sin_pi", ["divide", ["x"]]], 1, 0)
        1.0
    """
    if f[0] == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y)) / 2.0
    elif f[0] == "cos_pi":
        return math.cos(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "sin_pi":
        return math.sin(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "divide":
        return evaluate_random_function(f[1], x, y)/2.0
    elif f[0] == "power":
        return evaluate_random_function(f[1], x, y)**2.0
    elif f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    else:
        raise Exception('Could not evalutate function ' + str(f))
    #nice and elegant. :)


def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    x = float(val)
    a = float(input_interval_start)
    b = float(input_interval_end)
    c = float(output_interval_start)
    d = float(output_interval_end)

    #good thought to force everything to be a float, but do note that python will cast ints to float automatically whenever you have a float involved in the operation. So, all you need to guard against is the division being integer division if you get really unlucky. To get rid of that problem, multiply by 1.0 first. So, this code segment could be reduced to term1 = 1.0*(val - input_interval_start)/(input_interval_end - input_interval_start)

    term1 = (x - a)/(b - a)
    term2 = d - c
    remapped = term1 * term2 + c

    return remapped


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(12, 13)
    green_function = build_random_function(12, 13)
    blue_function = build_random_function(12, 13)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
