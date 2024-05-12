import sys
import ast

from PIL import Image

IMAGE_SIZE = 128
IMAGE_COLOR_MODE = "RGB"
IMAGES_PATH = "./images/"

if __name__ == "__main__":
    
    board = ast.literal_eval(sys.argv[1])
    size = len(board)
    
    image = Image.new(IMAGE_COLOR_MODE, (IMAGE_SIZE * size, IMAGE_SIZE * size))
    pointer_x = 0
    pointer_y = 0
    for r in range(0, size):
        pointer_x = 0
        for c in range(0, size):
            piece = Image.open(IMAGES_PATH + board[r][c].lower() + ".png").convert(IMAGE_COLOR_MODE)
            image.paste(piece, (pointer_x, pointer_y))
            pointer_x += IMAGE_SIZE
        pointer_y += IMAGE_SIZE
        
    image.show()