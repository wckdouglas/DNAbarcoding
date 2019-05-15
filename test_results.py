#!/usr/bin/env python

import sys
import pyximport
pyximport.install()
from utils import min_dist

if len(sys.argv) < 2:
    print('[usage] python %s <barcode list 1> [barcode list 2] ... ' %(sys.argv[0]), file=sys.stderr) 
    print('example: python %s list1 list2 list3' %(sys.argv[0]), file=sys.stderr)
    sys.exit()


'''
for each file,
count distinct barcode,
calculate minimum edit distance
'''
for f in sys.argv[1:]:
    barcode_set = set()
    with open(f) as infile:
        for line in infile:
            # collect barcode from file
            barcode_set.add(line.strip())


    # test barcode distance
    min_distance = 1000
    for barcode in barcode_set:
        min_distance = min(min_distance, min_dist(barcode, barcode_set))

    print('%s: %i barcodes with a minimum hamming distance of %i' \
            %(f, len(barcode_set), min_distance))

