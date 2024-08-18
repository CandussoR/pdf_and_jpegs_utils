import os
import sys
from typing import Tuple
from pypdf import PdfMerger, PdfReader, PdfWriter, PageObject
from pypdf.generic import RectangleObject
from argparser import ArgParser
from pdf_maker import pdf_maker


def leaflet_maker(files : list[str], out : str, delete : bool):
    multiple_files = len(files) > 1
    filenames = []

    for ix, f in enumerate(files):
        print(ix, f)
        page = 0
        reader = PdfReader(f)
        writer = PdfWriter()

        while page < len(reader.pages):
            leaflet, left = set_leaflet_and_left(reader.pages[page:])
            l = [*reader.pages[page:page+leaflet]]
            width  = max(p.mediabox.right for p in l) * 2
            height = max(p.mediabox.top   for p in l)
            rectangle = max(p.mediabox    for p in l)
            if left:
                for n in range(left):
                    blank_page = PageObject().create_blank_page(width=width, height=height)
                    blank_page.mediabox = rectangle
                    l.append(blank_page) 
            assert len(l) == leaflet, f"{len(l)} : {leaflet}"

            signature : list[PageObject] = create_leaflet(leaflet, l)

            for n in range(0, len(signature) - 1, 2):
                blank_page = writer.add_blank_page(width=width, height=height)
                blank_page.merge_page(signature[n])

                right = signature[n].mediabox.right

                blank_page.merge_translated_page(signature[n + 1], right, 0)

            page += leaflet

            if multiple_files:
                path, ext = os.path.splitext(out)
                tmp_out = f'{path}_tmp_{ix}{ext}'
                with open(tmp_out, 'wb') as fw:
                    writer.write(fw)
                if tmp_out not in filenames :
                    filenames.append(tmp_out)
            else:
                with open(out, 'wb') as fw:
                    writer.write(fw) 

    # PDF merger
    if multiple_files:
        merge = PdfWriter()
        for f in filenames:
            merge.append(f)
        merge.write(out)
        merge.close()

    if delete:
        for f in filenames:
            os.remove(f)

def set_leaflet_and_left(pages : list[PageObject]) -> Tuple[int, int]:
    '''Returns a tuple with the number of pages in leaflet and what's left to add.'''
    leaflet = 4 * 4
    left = 0
    number_of_pages : int = len(pages)
    if number_of_pages < 4:
        leaflet = 4
    elif number_of_pages < leaflet and number_of_pages % 4 != 0:
        left = 4 - (number_of_pages % 4)                    
        leaflet = number_of_pages + left
    elif number_of_pages < leaflet :
        leaflet = number_of_pages
    return leaflet, left


def create_leaflet(number_of_pages : int, pages : list) -> list:
    '''Ordering the pages of a leaflet.'''
    new_page_order = []
    first_on_leaf = 0
    last_page = number_of_pages - 1
    while len(new_page_order) != len(pages):
        new_page_order.append(pages[last_page - first_on_leaf])
        new_page_order.append(pages[first_on_leaf])
        new_page_order.append(pages[first_on_leaf + 1])
        new_page_order.append(pages[last_page - first_on_leaf - 1])
        first_on_leaf += 2
    return new_page_order


if __name__ == '__main__':
    args = ArgParser(sys.argv[1:])
    leaflet_maker(args.files, args.out)