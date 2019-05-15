cpdef int hamming_distance(str s1,str s2):
    '''
    Calculating hamming distance from two strings
    from Douglas's python package: 
    https://github.com/wckdouglas/sequencing_tools/blob/master/sequencing_tools/fastq_tools/function_clip.pyx

    usage: hamming_distance(string1, string2)
    ==============================
    input parameter:
    s1, s2
    has to be same length

    return:
    edit distance: the edit distance between two string
    ===============================

    Example:
    > hamming_distance('AAA','AAC')
    # 1
    '''
    cdef:
        str i,j 
        int hamming = 0
    assert len(s1) == len(s2), 'Wrong barcode extraction: %s, %s' %(s1, s2)

    for i, j in zip(s1, s2):
        if i != j:
            hamming += 1

    return hamming


def min_dist(barcode, barcode_set):
    '''
    minumum pairwise distance compared to each of the barcode in the barcode set
    no comparison is done for exact same barcodes
    
    input params:
        barcode: string (e.g. AAAA)
        barcode_set: a set of barcodes with same lengths (e.g. {'AAAA','CCCC'})

    output:
        minumum edit distance

    example:
    > min_dist('AAAA', {'AAAA','CCCC'}) # ignoring comparison of: AAAA vs AAAA
    # 4
    '''
    cdef:
        str bc
        int min_score
    
    return min(hamming_distance(barcode, bc) for bc in barcode_set if bc != barcode)
