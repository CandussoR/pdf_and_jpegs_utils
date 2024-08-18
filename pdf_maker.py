import sys
from PIL import Image
from argparser import ArgParser

def pdf_maker(jpegs, out):
    images = [Image.open(j) for j in jpegs]
    images[0].save(out, "PDF", resolution = 100.0, save_all = True, append_images = images[1:])

if __name__ == '__main__':
    parser = ArgParser(sys.argv[1:])
    pdf_maker(parser.files, parser.out)