import fmindex
import random
import test_assembler

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

with open('test_files/phiX174_genome.txt') as f:
    data = f.read()

reads = test_assembler.split_into_reads(data, 2, 30, 10)
joined_reads = '$'.join(reads) + '$'
fmi = fmindex.FMIndex(joined_reads)

test_get_read_at_offset()
test_get_nth_read()