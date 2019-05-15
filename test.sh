set -x
python barcode_generator.py \
    --n_sets 6  \
    --nucleotides 6 \
    --edit_distance 3 \
    --n_barcodes 96
python test_results.py barcode*.txt

python barcode_generator.py \
    --n_sets 6 --nucleotides 5 --edit_distance 2 \
    --n_barcodes 16 --low_complexity_filter 
python test_results.py barcode*.txt
