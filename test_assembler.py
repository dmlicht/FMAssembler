import assembler
import random
import fmindex
import time
import pprint

READ_SIZE = 40
COVERAGE = 5
INCREMENT = 10

def split_into_reads(seq, cov=10, read_len=20, skip_size=5):
    """returns an array of simulated reads from genome sequence"""
    generated_reads = [seq[i:i+read_len] for i in xrange(0,len(seq)-read_len, 5) for j in xrange(cov)]
    random.shuffle(generated_reads)
    return generated_reads

with open('test_files/phiX174_genome.txt') as f:
    data = f.read()

reads = split_into_reads(data, COVERAGE, READ_SIZE, INCREMENT)

joined_reads = '$'.join(reads) + '$'

start_time = time.time()
fmi = fmindex.FMIndex(joined_reads)
end_time = time.time()
print 'index build time', end_time - start_time
#filter index

start_time = time.time()
fmi = assembler.filter_index(reads, fmi)
end_time = time.time()
print 'index filter time', end_time - start_time

# print len(reads)

# start_time = time.time()
# for read in reads:
#     assembler.find_overlaps(read, fmi)
# end_time = time.time()
# print end_time - start_time

# start_time = time.time()
# total_overlaps = 0
# for read in reads:
#     # total_overlaps += len(fmi.get_prefix_overlaps(read, 10))
#     fmi.get_prefix_overlaps(read, 10)
# end_time = time.time()
# print 'overlap detection time:', end_time - start_time
# print total_overlaps / len(reads)

#//NOTE: REMOVE ONLY FOR TESTING

for read in reads[:10]:
#     o1 = assembler.find_irreducible_overlaps(read, fmi)
    o2 = assembler.find_irreducible_overlaps2(read, fmi)
#     print 'o1'
#     pprint.pprint(o1)
    # print 'o2'
    # pprint.pprint(o2)
#     if o1 != o2:
#         print "problemo: irreducible 2 isn't working"

# start_time = time.time()
# for read in reads:
#      assembler.find_irreducible_overlaps(read, fmi)
# end_time = time.time()
# print 'find irreducible:', end_time - start_time

# start_time = time.time()
# for read in reads:
#      assembler.find_irreducible_overlaps(read, fmi)
# end_time = time.time()
# print 'find irreducible2:', end_time - start_time

# exit(0)
overlap_graph = assembler.build_overlap_graph(reads, fmi)
contigs = overlap_graph.get_contigs()
print len(contigs)
for contig in contigs:
    print contig

