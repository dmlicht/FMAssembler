import fmindex
import random
from overlap_graph import OverlapGraph

MIN_OVERLAP = 10

def test_get_read_at_offset():
    read_starts_at = 0
    read_ends_at = -1
    for i in xrange(len(reads)):
        read_ends_at = read_ends_at + len(reads[i]) + 1
        rand_pos_in_read = random.randint(read_starts_at, read_ends_at)
        ith_read_from_fm = fmi.get_read_at_offset(rand_pos_in_read)
        if reads[i] != ith_read_from_fm:
            print 'in test get at offset'
            print "problem with read " + str(i) + ":"
            print reads[i], '\n', ith_read_from_fm
            break
        read_starts_at = read_starts_at + len(reads[i]) + 1

def test_get_nth_read():
    for i in xrange(len(reads)):
        ith_read_from_fm = fmi.get_nth_read(i)
        if  ith_read_from_fm != reads[i]:
            print 'in get nth read'
            print "problem with read " + str(i) + ":"
            print reads[i], '\n' ,ith_read_from_fm


def split_into_reads(seq, cov=10, read_len=20, skip_size=5):
    """returns an array of simulated reads from genome sequence"""
    generated_reads = [seq[i:i+read_len] for i in xrange(0,len(seq)-read_len, 5) for j in xrange(cov)]
    random.shuffle(generated_reads)
    return generated_reads
    # pprint.pprint(generated_reads)

def filter_index(reads, index, min_occ=2):
    """this function returns a new fm index with removed duplicates and 
    likely error sequences"""
    uniques = set([])
    for read in reads:
        if len(index.occurrences(read)) >= min_occ:
            uniques.add(read)
    joined_uniques = '$'.join(list(uniques)) + '$'
    return fmindex.FMIndex(joined_uniques)

def find_overlaps(read, index):
    """returns list of tuples containing sequence and number of letters overlapped"""
    hits = []
    # print 'called'
    for i in range(MIN_OVERLAP, len(read))[::-1]:
        pref_found = index.find_prefixes(read[-1 * i:])
        # print 'pref found'
        # print pref_found
        hits.extend([(pref, i) for pref in pref_found])
        # print pref_found
    return [(index.get_read_at_offset(hit[0]),hit[1]) for hit in hits]

#TODO: FIX THIS FUNCTION
def find_irreducible_overlaps(read, index):
    """find the set of irreducible overlaps
    overlaps contain sequence and number of letters overlapped"""
    overlaps = find_overlaps(read, index)
    # print overlaps
    overlaps = sorted(overlaps, key=lambda x: x[1])[::-1]
    i = 0
    while i < len(overlaps):
        overlap_seqs = [o[0] for o in overlaps]
        trans_edge_overlap = [o[0] for o in find_overlaps(overlaps[i][0], index)]
        nontrans = list(set(overlap_seqs) & set(trans_edge_overlap))
        for nontran in nontrans:
            j = i
            while j < len(overlaps):
                if overlaps[j][0] == nontran:
                    overlaps.pop(j)
                j += 1
        i += 1
    return overlaps

def build_overlap_graph(reads, index):
    """returns overlap graph from list and index of reads"""
    overlap_graph = OverlapGraph()
    for read in reads:
        overlaps = find_irreducible_overlaps(read, index)
        # print overlaps
        for overlap in overlaps:
            seq_overlapped, len_of_overlap = overlap
            overlap_graph.add_edge(read, seq_overlapped, len_of_overlap)
    return overlap_graph


with open('phiX174_genome.txt') as f:
    data = f.read()

reads = split_into_reads(data, 2, 30, 10)
joined_reads = '$'.join(reads) + '$'
fmi = fmindex.FMIndex(joined_reads)

#run tests on index before filtering
test_get_read_at_offset()
# test_get_nth_read()

#filter index
fmi = filter_index(reads, fmi)
overlap_graph = build_overlap_graph(reads, fmi)
for contig in overlap_graph.get_contigs():
    print contig

#try to find an overlap
# find_irreducible_overlaps(reads[0], fmi)