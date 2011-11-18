#!/usr/bin/python2
from PIL import Image
import random
import sys

def buddhabrot(x1, y1, x2, y2, pxwidth, npoints, maxiters):
    dx, dy = x2-x1, y2-y1
    pxheight = int((float(pxwidth) * dy) / dx)
#    img = Image.new("RGB", (width+1, height+1))
#    pix = img.load()
    pxvals = [[0 for j in xrange(pxheight)] for i in xrange(pxwidth)]
    maxval = 0
    for i in xrange(npoints):
        # Find c = (x, y) for mandelbrot set
        x, y = random.uniform(-2, 2), random.uniform(-2, 2)
        while is_mandel(complex(x, y), maxiters):
            x, y = random.uniform(-2, 2), random.uniform(-2, 2)
        zx, zy = x, y
        n = 0
        while abs(zx) < 2 and abs(zy) < 2:
            px = int(round((zx-x1) * pxwidth / dx))
            py = int(round((zy-y1) * pxheight / dy))
            if 0 <= px and px < pxwidth and 0 <= py and py < pxheight:
                tmp = pxvals[px][py] + 1
                pxvals[px][py] = tmp
                if tmp > maxval:
                    maxval = tmp
            zx, zy = zx**2 - zy**2 + x, 2*zx*zy + y
            n += 1
    #img.save("mandel.png")
    #img.show()
    print "P2"
    print pxwidth, pxheight
    print "255"
    for row in pxvals:
        for col in row:
            print (col * 255 / maxval),
        print

def is_mandel(c, maxiters):
    z = 0
    for i in xrange(maxiters):
        if z.real**2 + z.imag**2 > 4:
            return False
        z = z**2 + c
    return True


if __name__ == '__main__':
    buddhabrot(-2, -2, 2, 2, 500, 500000, 200)
