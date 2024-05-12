import sys
import ast

from PIL import Image

IMAGE_SIZE = 128
IMAGE_COLOR_MODE = "RGBA"
IMAGES_PATH = "./images/"
TILE_PATH = "./images/tile.png"

if __name__ == "__main__":
    
    board = ast.literal_eval(sys.argv[1])
    size = len(board)
    
    image = Image.new(IMAGE_COLOR_MODE, (IMAGE_SIZE * size, IMAGE_SIZE * size))
    tile = Image.open(TILE_PATH).convert(IMAGE_COLOR_MODE)
    pointer_x = 0
    pointer_y = 0
    for r in range(0, size):
        pointer_x = 0
        for c in range(0, size):
            image.paste(tile, (pointer_x, pointer_y))
            piece = Image.open(IMAGES_PATH + board[r][c].lower() + ".png").convert(IMAGE_COLOR_MODE)
            image.paste(piece, (pointer_x, pointer_y), piece)
            pointer_x += IMAGE_SIZE
        pointer_y += IMAGE_SIZE
        
    image.show()