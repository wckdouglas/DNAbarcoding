#!usr/bin/env python

from __future__ import print_function
from builtins import range
from itertools import product, cycle
import sys
import re
import pyximport 
pyximport.install()
from utils import hamming_distance, min_dist
import argparse


def getopt():
    parser = argparse.ArgumentParser(description = 'This program generates sets of barcodes with a given minumum edit distance')
    parser.add_argument('-n', '--nucleotides', type=int, default=6,  help = 'Number of nucleotide per barcode (default: 6)')
    parser.add_argument('-e','--edit_distance', default=3, type=int, help = 'Minimum edit distance between barcodes (default: 3)')
    parser.add_argument('--n_barcodes', default=96, type=int, help = 'Number of barcodes per set (default: 96)')
    parser.add_argument('--n_sets',default=1, type=int, help = 'Number of barcode sets to generate (default: 1)')
    parser.add_argument('-o','--outprefix', default='barcode', help = 'Barcode list prefix, output file would be: '\
                                                                        '{prefix}_1.txt, {prefix}_2.txt for different barcode set '\
                                                                        '(default: barcode)')
    parser.add_argument('--low_complexity_filter', action='store_true', help = 'Do not include barcodes with triplet homopolymers (default: False)')
    args = parser.parse_args()
    return args


class BarcodeGenerator():
    '''
    Barcode generator: using a brute force way to iterate over all possible combination of nucleotides,
                    compare newly-synthesized barcode to stored-barcode,
                    if hamming distance is less than a threshold, the new barcode will be stored.

    input params:
        total_nucleotide: number of nucleotide for each barcode
        min_distance: at least how many nucleotide difference between each barcode pair
        n_barcodes:  total number of barcode needed
        filter_low_complexity: remove barcode with low complexity 3-mers (e.g. AAACAG, CAGAAA),
                            to avoid polymerase slippage errors
    
    Example:
    > barcode_generator = BarcodeGenerator()
    > barcode_generator.generate_barcode()
    > barcodes = barcode_generator.print_barcodes()
    '''
    def __init__(self, 
                total_nucleotide = 6, 
                min_distance = 3,
                n_barcodes = 96,
                n_sets = 1,
                filter_low_complexity = False):
        
        self.phantom_barcodes = ['N' * total_nucleotide]
        self.barcode_sets = []
        self.total_nucleotide = total_nucleotide
        self.min_distance = min_distance
        self.n_barcodes = n_barcodes
        self.filter_low_complexity = filter_low_complexity
        self.low_complexity_filter = re.compile('AAA|CCC|GGG|TTT')
        self.n_sets = n_sets
    

    def generate_barcode(self):
        '''
        1. loop through all possible combination of nucleotides
        2. check hamming distance between the newly-generated barcode and existing barcode
        3. if not closer than threshold, the newly-generated barcode will be accepted
            - if filter_low_complexity, check the if the newly-generated barcode has low-complexity subseq
        '''
        possible_combination = 4**self.total_nucleotide
        self.max = 0
        for start in range(possible_combination):
            if start % 1000 == 0:
                print('Starting from %i' %start, file=sys.stderr)
            accepted_barcodes = set(self.phantom_barcodes)
            tested = 0
            iterator = cycle(product('ACTG', repeat=self.total_nucleotide))
            while tested <= possible_combination + start:
                barcode = next(iterator)
                if tested >= start:
                    barcode = ''.join(barcode)
                    is_low_complexity = self.low_complexity_filter.search(barcode)
                    is_far_enough = min_dist(barcode, accepted_barcodes) >= self.min_distance 
                    if is_far_enough and (not self.filter_low_complexity or not is_low_complexity):
                        accepted_barcodes.add(barcode)
                tested += 1

            accepted_barcodes = accepted_barcodes-set(self.phantom_barcodes)
            self.max = max(self.max, len(accepted_barcodes))
            if len(accepted_barcodes) >= self.n_barcodes:
                self.barcode_sets.append(accepted_barcodes)
            
            if len(self.barcode_sets) == self.n_sets:
                break


    def test_barcodes(self, barcode_set):
        '''
        validate stored barcodes to check if they are at leasts ${min_distance} nucleotide apart
        '''
        for bc1 in barcode_set:
            for bc2 in barcode_set:
                if bc1 != bc2:
                    assert hamming_distance(bc1, bc2) >= self.min_distance, \
                            'Bad barcodes %s and %s' %(bc1,bc2)
        print('All barcode had at least %i nucleotide distance apart' %self.min_distance, file=sys.stderr)


    def print_barcodes(self, set_number = 0):
        '''
        return barcode
        '''
        assert set_number < len(self.barcode_sets)
        return list(self.barcode_sets[set_number])[:self.n_barcodes]


    def write(self, outprefix):
        '''
        writing out barcode sets to file
        '''
        for i, barcode_set in enumerate(self.barcode_sets):
            out_file = '{prefix}_{file_num}.txt'\
                        .format(prefix = outprefix,
                                file_num = i+1)
            with open(out_file, 'w') as out:
                for bc in self.print_barcodes(set_number=i):
                    print(bc, file=out)
            print('Written %s' %out_file, file = sys.stderr)


def main():
    '''
    main function,
    '''
    args = getopt() #    collect commandline arguments
    bg = BarcodeGenerator(total_nucleotide = args.nucleotides,
                        min_distance = args.edit_distance,
                        n_barcodes = args.n_barcodes,
                        n_sets = args.n_sets,
                        filter_low_complexity = args.low_complexity_filter)
    bg.generate_barcode()
    bg.write(args.outprefix)


if __name__ == '__main__':
    main()

        


