#!/usr/bin/python2
from PIL import Image
defcolors = [
        (102, 0, 119),
        (118, 0, 206),
        (91, 50, 171),
        (16, 11, 182),
        (8, 24, 158),
        (0, 38, 134),
        (0, 117, 133),
        (0, 137, 107),
        (0, 137, 63),
        (0, 158, 43),
        (40, 186, 28),
        (149, 224, 65),
        (250, 247, 40),
        (250, 182, 40),
        (242, 112, 15),
        (228, 68, 13),
        (234, 20, 0),
        (255, 64, 79)
    ]
def combine(c1, l1, c2, l2):
    return (int(c1*l1[0] + c2*l2[0]),
            int(c1*l1[1] + c2*l2[1]),
            int(c1*l1[2] + c2*l2[2]))
# Interpolate colors for bigger range.
colors = []
for i in range(len(defcolors)-1):
    colors.append(defcolors[i])
    colors.append(combine(0.75, defcolors[i], 0.25, defcolors[i+1]))
    colors.append(combine(0.5, defcolors[i], 0.5, defcolors[i+1]))
    colors.append(combine(0.25, defcolors[i], 0.75, defcolors[i+1]))
colors.append(defcolors[len(defcolors)-1])
colorsize = len(colors)

def mandelbrot(width, maxiters):
    # (-2, 1) x (-1.2, 1.2)
    height = int((width * 2.4) / 3)
    img = Image.new("RGB", (width+1, height+1))
    pix = img.load()
    scalex = 3.0 / width
    scaley = 2.4 / height
    for i in xrange(height+1):
        for j in xrange(width+1):
            c = complex(j * scalex - 2, i * scalex - 1.2)
            niters = is_mandel(c, maxiters)
            if niters >= 0:
                pix[j, i] = colors[niters % colorsize]
    img.save("mandel.png")
    img.show()

def is_mandel(c, maxiters):
    z = 0
    for i in xrange(maxiters):
        if z.real**2 + z.imag**2 > 4:
            return i
        z = z**2 + c
    return -1


if __name__ == '__main__':
    mandelbrot(1000, colorsize)
