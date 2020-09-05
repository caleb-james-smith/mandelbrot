# mandelbrot.py
import numpy as np
from PIL import Image, ImageDraw

def mandelbrot(c, N):
    z = 0
    n = 0
    while abs(z) < 2 and n < N:
        z = z*z + c
        n += 1
    return n

def pointInSet(c, N):
    z = 0
    for i in range(N):
        z = z*z + c
    inSet = abs(z) < 2
    return inSet

def scan():
    points = np.linspace(-1, 1, 21)
    for x in points:
        for y in points:
            c = complex(x, y)
            inSet = pointInSet(c, 10)
            print("({0:.1f}, {1:.1f}): {2}".format(x, y, inSet))

def drawPureDark(x, y, c, N, draw):
    color = 0
    if pointInSet(c, N):
        color = 255
    draw.point([x, y], (color, color, color))

def drawPureLight(x, y, c, N, draw):
    color = 255
    if pointInSet(c, N):
        color = 0
    draw.point([x, y], (color, color, color))

def drawIterDark(x, y, c, N, draw):
    m = mandelbrot(c, N)
    color = 0 + int(255 * m / N)
    draw.point([x, y], (color, color, color))

def drawIterLight(x, y, c, N, draw):
    m = mandelbrot(c, N)
    color = 255 - int(255 * m / N)
    draw.point([x, y], (color, color, color))

def drawColor(x, y, c, N, draw):
    m = mandelbrot(c, N)
    hue = int(255 * m / N)
    saturation = 255
    value = 255 if m < N else 0
    draw.point([x, y], (hue, saturation, value))

def plot():
    COLOR_MODE = False
    PURE_MODE  = False
    DARK_MODE  = False
    MAX_ITER = 100
    # Image size (pixels)
    WIDTH  = 1200
    HEIGHT = 800
    # Plot window
    RE_START    = -2
    RE_END      =  1
    IM_START    = -1
    IM_END      =  1
    if COLOR_MODE:
        im = Image.new('HSV', (WIDTH, HEIGHT), (255, 255, 255))
    else:
        im = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            real        = RE_START + (x / WIDTH) * (RE_END - RE_START)
            imaginary   = IM_START + (y / HEIGHT) * (IM_END - IM_START)
            c = complex(real, imaginary)
            # --- color 
            if COLOR_MODE:
                drawColor(x, y, c, MAX_ITER, draw)
            else:
                # --- pure black and white if point is in set
                if PURE_MODE:
                    if DARK_MODE:
                        # dark mode
                        drawPureDark(x, y, c, MAX_ITER, draw)
                    else:
                        # light mode
                        drawPureLight(x, y, c, MAX_ITER, draw)
                # --- black/white based on number of iterations
                else:
                    if DARK_MODE:
                        # dark mode
                        drawIterDark(x, y, c, MAX_ITER, draw)
                    else:
                        # light mode
                        drawIterLight(x, y, c, MAX_ITER, draw)
    
    if COLOR_MODE:
        im.convert('RGB').save('output.png', 'PNG')
    else:
        im.save('output.png', 'PNG')


def main():
    plot()

if __name__ == "__main__":
    main()

