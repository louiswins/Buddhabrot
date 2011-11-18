#!/usr/bin/python
import sys

def pgm2ppm(fr, fg, fb, fout=''):
    """Convert 3 grayscale PGM images to a single color PPM image.

    Assumes that the dimensions of each input image are the same, and that the
    maximum value of each is 255. Furthermore, assumes that each image has each
    row of pixels on a single line.
    """
    try:
        rfile = open(fr)
        gfile = open(fg)
        bfile = open(fb)
        if (fout == ''):
            outfile = sys.stdout
        else:
            outfile = open(fout, mode='w')

        rfile.readline()
        dimensions = rfile.readline().split()
        rfile.readline()
        # discard first three lines
        for i in range(3):
            gfile.readline()
            bfile.readline()

        outfile.write("P3\n{} {}\n255\n".format(dimensions[0], dimensions[1]))

        while True:
            reds = rfile.readline()
            if reds == '':
                break
            reds = reds.split()
            greens = gfile.readline().split()
            blues = bfile.readline().split()
            for i in range(len(reds)):
                outfile.write("{} {} {} ".format(reds[i], greens[i], blues[i]))
            outfile.write('\n')

    finally:
        rfile.close()
        gfile.close()
        bfile.close()
        if outfile != sys.stdout:
            outfile.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: {} rfile gfile bfile [outfile]".format(sys.argv[0]))
        sys.exit(1)
    if len(sys.argv) == 4:
        outfile = ''
    else:
        outfile = sys.argv[4]
    
    pgm2ppm(sys.argv[1], sys.argv[2], sys.argv[3], outfile)
