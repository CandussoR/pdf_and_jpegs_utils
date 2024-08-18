import os
import sys
from PIL import Image

from argparser import ArgParser

def horizontally_merge_jpegs(jpegs : list, out : str, delete : bool) :
  images = [Image.open(x) for x in jpegs]
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

  new_im = Image.new('RGB', (total_width, max_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]
  
  new_im.save(out)

  if delete :
    for j in jpegs:
      os.remove(j)


if __name__ == '__main__':
  parser = ArgParser(sys.argv[1:])
  try:
    horizontally_merge_jpegs(parser.files, parser.out, parser.delete)
  except (ValueError, FileNotFoundError) as e:
    print(e)

  