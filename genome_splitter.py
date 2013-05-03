import random
import sys

READ_SIZE = 40
COVERAGE = 5
INCREMENT = 10

def split_into_reads(seq, cov=10, read_len=20, skip_size=5):
    """returns an array of simulated reads from genome sequence"""
    generated_reads = [seq[i:i+read_len] for i in xrange(0,len(seq)-read_len, 5) for j in xrange(cov)]
    random.shuffle(generated_reads)
    return generated_reads

def main():
    if len(sys.argv) != 5:
        print "Please call script in the following format: python fm_index.py file_to_build_index_of.txt"
        exit()
    data = ""

    f_name, read_size, cov, inc = sys.argv[1:5]
    with open(f_name) as f:
        data = f.read()

    reads = split_into_reads(data, cov, read_size, inc)
    print '\n'.join(reads)

if __name__ == "__main__":
    main()