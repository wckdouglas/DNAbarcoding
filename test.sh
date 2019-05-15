set -x
python barcode_generator.py --n_sets 6
python test_results.py barcode*.txt
