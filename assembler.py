import fmindex
import sys
import pprint
from overlap_graph import OverlapGraph

#parameter for overlapping sequence
MIN_OVERLAP = 20

def filter_index(reads, index, min_occ=2):
    """this function returns a new fm index with removed duplicates and 
    likely error sequences"""
    uniques = set([])
    for read in reads:
        if len(index.occurrences(read)) >= min_occ:
            uniques.add(read)
    joined_uniques = '$'.join(list(uniques)) + '$'
    return fmindex.FMIndex(joined_uniques)

#NOTE: this function is no longer used
#This is left in tact for comparison to more efficient member function
#of FMIndex - get_prefix_overlaps()
def find_overlaps(read, index):
    """returns list of tuples containing sequence and number of letters overlapped"""
    hits = []
    # print 'called'
    for i in range(MIN_OVERLAP, len(read))[::-1]:
        pref_found = index.find_prefixes(read[-1 * i:])
        hits.extend([(pref, i) for pref in pref_found])
    # if hits:
    #     print 'assem:', hits
    return [(index.get_read_at_offset(hit[0]),hit[1]) for hit in hits]

def find_irreducible_overlaps(read, index):
    """find the set of irreducible overlaps
    overlaps contain sequence and number of letters overlapped"""
    overlaps = index.get_prefix_overlaps(read, MIN_OVERLAP)
    overlaps = sorted(overlaps, key=lambda x: x[1])[::-1]
    # if overlaps:
    #     return [ overlaps[0] ]
    # else:
    #     return []
    i = 0
    while i < len(overlaps):
        overlap_seqs = [o[0] for o in overlaps]
        co = overlap_seqs[0] #current overlap
        co_overlaps = [o[0] for o in index.get_prefix_overlaps(co, MIN_OVERLAP)]
        trans_edges = list(set(overlap_seqs) & set(co_overlaps))
        for trans_edge in trans_edges:
            j = i
            while j < len(overlaps):
                if overlaps[j][0] == trans_edge:
                    overlaps.pop(j)
                j += 1
        i += 1
    if len(overlaps) == 2:
        print read
        print overlaps
    return overlaps


def find_irreducible_overlaps2(read, index):
    """find the set of irreducible overlaps
    overlaps contain sequence and number of letters overlapped"""
    overlaps = index.get_prefix_overlaps(read, MIN_OVERLAP)
    # overlaps2 = find_overlaps(read, index)
    # if set(overlaps) != set(overlaps2):
    #     print "problem"
    #     print overlaps
    #     print overlaps2
    # print read
    # print 'all', overlaps
    overlap_seqs = [o[0] for o in sorted(overlaps, key=lambda x: x[1])[::-1]]
    overlap_lens = dict(overlaps)
    i = 0
    while i < len(overlap_seqs):
        co = overlap_seqs[i] #current overlap
        co_overlaps = [o[0] for o in index.get_prefix_overlaps(co, MIN_OVERLAP)]
        overlap_seqs = list(set(overlap_seqs) - set(co_overlaps))
        i += 1
    overlaps_with_len = [(o, overlap_lens[o]) for o in overlap_seqs]
    # print 'reduced', overlaps_with_len
    return overlaps_with_len

def build_overlap_graph(reads, index):
    """returns overlap graph from list and index of reads"""
    overlap_graph = OverlapGraph()
    for read in reads:
        overlaps = find_irreducible_overlaps2(read, index)
        # print overlaps
        for overlap in overlaps:
            seq_overlapped, len_of_overlap = overlap
            overlap_graph.add_edge(read, seq_overlapped, len_of_overlap)
    return overlap_graph

def assemble(reads):
    """takes a list of reads builds generalized fm-index and overlap graph
    returns set of contigs implied by overlap graph"""
    joined_reads = '$'.join(reads) + '$'
    fmi = fmindex.FMIndex(joined_reads)
    fmi = filter_index(reads, fmi)
    overlap_graph = build_overlap_graph(reads, fmi)
    return overlap_graph.get_contigs()

def main():
    if len(sys.argv) != 2:
        print "Please call script in the following format: python assembler.py file_with_reads_to_assemble.txt"
        print "expects file with newline seperated list of reads"
    data = ""
    with open(sys.argv[1]) as f:
         data = f.read()
    reads = data.split('\n')
    contigs = assemble(reads)
    pprint.pprint(contigs)
    exit(0)

if __name__ == "__main__":
    main()