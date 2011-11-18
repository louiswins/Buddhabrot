#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>

#define WIDTH 700
#define HEIGHT 600

/* From http://eternallyconfuzzled.com/arts/jsw_art_rand.aspx */
unsigned time_seed() {
	time_t now = time(0);
	unsigned char *p = (unsigned char *)&now;
	unsigned seed = 0;
	size_t i;

	for (i = 0; i < sizeof now; ++i)
		seed = seed * (UCHAR_MAX + 2U) + p[i];

	return seed;
}

/* between -2 and 2 */
double rand_double() {
	return rand() / (RAND_MAX + 1.0) * 4.0 - 2.0;
}

/* [-2,2]x[-1,2] maps to [0,WIDTH-1]x[0,HEIGHT-1] */
unsigned pxval[WIDTH][HEIGHT] = {{0}};

int is_mandel(double x, double y, unsigned long maxiters) {
	double zx = 0,
	       zy = 0;
	while (maxiters-- > 0) {
		double zxsq = zx * zx,
		       zysq = zy * zy;
		if (zxsq + zysq > 4.0)
			return 0;
		zy = 2 * zx * zy + y;
		zx = zxsq - zysq + x;
	}
	return 1;
}

unsigned buddhabrot(unsigned long npoints, unsigned long maxiters) {
	unsigned maxval = 0;
	while (--npoints > 0) {
		double cx, cy,
		       zx, zy,
		       zxsq, zysq;
		do {
			cx = rand_double();
			cy = rand_double();
		} while (is_mandel(cx, cy, maxiters));
		zx = cx;
		zy = cy;
		zxsq = zx*zx;
		zysq = zy*zy;

		while (-2.0 < zx && zx < 2.0 && -2.0 < zy && zy < 2.0) {
			size_t pixel_x = (zx + 2.0) * WIDTH / 3.5,
			       pixel_y = (zy + 1.5) * HEIGHT / 3.0;
			if (0 <= pixel_x && pixel_x < WIDTH &&
			    0 <= pixel_y && pixel_y < HEIGHT) {
				unsigned tmp = pxval[pixel_x][pixel_y] + 1;
				pxval[pixel_x][pixel_y] = tmp;
				if (tmp > maxval) maxval = tmp;
			}
			zy = 2*zx*zy + cy;
			zx = zxsq - zysq + cx;
			zxsq = zx*zx;
			zysq = zy*zy;
		}
	}
	return maxval;
}

void gen_pgm(FILE *fp, unsigned scale) {
	size_t row,
	       col;
	fprintf(fp, "P2\n"); /* magic */
	fprintf(fp, "%d %d\n", WIDTH, HEIGHT); /* width height */
	fprintf(fp, "255\n"); /* maximum value */

	for (col = HEIGHT; col > 0; --col) {
		for (row = 0; row < WIDTH; ++row) {
			fprintf(fp, "%d ", (int)(pxval[row][col-1] * 255.0 / scale));
		}
		fputc('\n', fp);
	}
}


int main(int argc, char *argv[]) {
	unsigned maxval;
	FILE *pgmfil = NULL;

	if (argc > 1) {
		pgmfil = fopen(argv[1], "w");
		if (pgmfil == NULL) {
			fprintf(stderr, "Could not open %s.\n", argv[1]);
		}
	}
	if (pgmfil == NULL)
		pgmfil = stdout;

	maxval = buddhabrot(10000000UL, 1000LU);

	gen_pgm(pgmfil, maxval);

	fclose(pgmfil);
}
