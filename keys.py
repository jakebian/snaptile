keymap = [
    ['Q', 'W', 'E', 'R'],
    ['A', 'S', 'D', 'F'],
    ['Z', 'X', 'C', 'V']
]

def get_posmap(keymap):
    posmap = {}
    for i, row in enumerate(keymap):
        for j, elem in enumerate(row):
            posmap[elem] = (i, j)
    return posmap

print get_posmap(keymap)