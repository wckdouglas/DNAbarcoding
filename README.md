# Barcode generator #

This repository includes a program to generate sets of DNA barcodes.

## Install ## 

The only package dependencies are *cython* and *future* (for python2). The easiest way to install is through [miniconda](https://docs.conda.io/en/latest/miniconda.html), via:

```
conda create -n test_barcode python=3.6 cython future
source activate test_barcode
```

The package should be compatible with python 2 and 3.


## Usage  ##

The executable *barcode_generator.py* is the main program.

```
usage: barcode_generator.py [-h] [-n NUCLEOTIDES] [-e EDIT_DISTANCE]
                            [--n_barcodes N_BARCODES] [--n_sets N_SETS]
                            [-o OUTPREFIX] [--low_complexity_filter]

This program generates sets of barcodes with a given minumum edit distance

optional arguments:
  -h, --help            show this help message and exit
  -n NUCLEOTIDES, --nucleotides NUCLEOTIDES
                        Number of nucleotide per barcode (default: 6)
  -e EDIT_DISTANCE, --edit_distance EDIT_DISTANCE
                        Minimum edit distance between barcodes (default: 3)
  --n_barcodes N_BARCODES
                        Number of barcodes per set (default: 96)
  --n_sets N_SETS       Number of barcode sets to generate (default: 1)
  -o OUTPREFIX, --outprefix OUTPREFIX
                        Barcode list prefix, output file would be:
                        {prefix}_1.txt, {prefix}_2.txt for different barcode
                        set (default: barcode)
  --low_complexity_filter
                        Do not include barcodes with triplet homopolymers
                        (default: False)
```


## Example ##
To generate a set of 96 6-nt barcodes with at least 3 nucleotide differences from each other, we can do:

```
python barcode_generator.py \
    --n_sets 1  \
    --nucleotides 6 \
    --edit_distance 3 \
    --n_barcodes 96 
```

This generates a output file called ```barcode_1.txt``` containing the 96 barcodes each at a line.

To validate the generated barcode:

```
python test_barcodes.py barcode_1.txt
# barcode_1.txt: 96 barcodes with a minimum hamming distance of 3 with a longest of 5 nucleotide run
```

To filter out barcodes containing homopolymer runs (e.g. AAA, CCC, TTT), we can turn on ```--low_complexity_filter```, to ignore any barcode with triplet homopolymers.


