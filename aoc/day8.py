import math


def find_layers(image, columns, rows):
    layers = [[]]
    x_coord = 0
    y_coord = 0
    max_col = columns - 1
    max_row = rows - 1
    current_layer = 0
    for digit in image:
        layers[current_layer].append(int(digit))
        if x_coord < max_col and y_coord < max_row:
            x_coord += 1
        elif x_coord == max_col and y_coord < max_row:
            x_coord = 0
            y_coord += 1
        elif x_coord < max_col and y_coord == max_row:
            x_coord += 1
        else:
            x_coord = 0
            y_coord = 0
            current_layer += 1
            layers.append([])

    return layers[:-1]


def find_layer_with_fewest(image, digit):
    min_layer = 0
    min_amount = math.inf
    l = 0
    for layer in image:
        amount = layer.count(digit)
        if amount < min_amount:
            min_layer = l
            min_amount = amount
        l += 1
    return min_layer


def find_showing_color(pixel):
    for layer in pixel:
        if layer != 2:
            return layer


def convert_to_pixels(layers):
    pixels = []
    length = len(layers[0])
    for l in range(length):
        pixel = []
        for layer in layers:
            pixel.append(layer[l])
        pixels.append(find_showing_color(pixel))
    return pixels


def one_layer_array(pixels, columns):
    return [pixels[i : i + columns] for i in range(0, len(pixels), columns)]


def sol_a(image, columns, rows):
    layers = find_layers(image, columns, rows)
    layer = find_layer_with_fewest(layers, 0)
    return layers[layer].count(1) * layers[layer].count(2)


def sol_b(image, columns, rows):
    layers = find_layers(image, columns, rows)
    pixels = convert_to_pixels(layers)
    return one_layer_array(pixels, columns)


def solve(path):
    rows = 6
    columns = 25

    image = []
    with open(path) as f:
        for line in f:
            for digit in line.rstrip():
                image.append(digit)
    a = sol_a(image, columns, rows)
    b = sol_b(image, columns, rows)
    return (a, b)
