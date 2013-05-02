import assembler
import random
import fmindex

def split_into_reads(seq, cov=10, read_len=20, skip_size=5):
    """returns an array of simulated reads from genome sequence"""
    generated_reads = [seq[i:i+read_len] for i in xrange(0,len(seq)-read_len, 5) for j in xrange(cov)]
    random.shuffle(generated_reads)
    return generated_reads

with open('test_files/phiX174_genome.txt') as f:
    data = f.read()

reads = split_into_reads(data, 2, 20, 10)
joined_reads = '$'.join(reads) + '$'
fmi = fmindex.FMIndex(joined_reads)

#filter index
fmi = assembler.filter_index(reads, fmi)

overlap_graph = assembler.build_overlap_graph(reads, fmi)
for contig in overlap_graph.get_contigs():
    print contig