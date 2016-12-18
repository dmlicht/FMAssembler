# FMAssembler

A tool to efficiently assemble large datasets of overlapping strings (like genomes!). 
This project is a python implementation of an overlap graph based assembler that uses the FM-Index compressed data structure.

# David Lichtenberg
# hello [at] davidlichtenberg [dot] com

to run assembler:

    python assembler.py /path/to/file_containing_newline_seperated_reads.txt

to run index on arbitrary text:

    python fmindex.py /path/to/file_containing_text_to_index.txt

## Overview

- assembler.py
    Takes a set of reads from user and passes them to index. Then uses the index to query for overlap edges to pass to the overlap graph

- fmindex.py 
    builds compressed index of a given text and allows a user to search for occurences of the text. This uses pysuffix library for Karkainnen suffix sorting.

- overlap_graph.py
    maintains data structure of edges and travelsal algorithm to return contigs implied by reads.

- t_rank.py 
    contains the checkpoint data structure for t_rank lookup with sublinear memory footprint (sublinear memory footprint not yet implemented - see below)

- genome_splitter.py
    takes a genome sequences and cuts it up to simulate lots of reads for testing

- bw_compressor.py (incomplete)
    contains testing algorithms for compressing the text, decompressing the text, and searching compressed text. (see below for what is incomplete)

- ukkonen.py (incomplete)
    toy implementation of ukkonen's algorithm for suffix sorting.


## Notes

suffix_array.py and tools.py taken directly from pysuffix library: https://code.google.com/p/pysuffix/ I take no credit for anything in those two files (except the comments saying that they aren't mine :P)


## TODO                                                                     time est
- Run Length Encoding Burrows Wheeler Transform                             20-30 m
- sort seperator chars in burrows wheeler transform (hackish fix)           10-20 m
- backwards search star (allows for any char matching in backwards search)  1-2 h
- contig graph                                                              .5 - 2 h
- more efficient transitive edge reduction                                  2+ h
- read error correction                                                     not sure
- fm-index merge algorithm                                                  not sure
- re-implement fm index in c (port using cython) to save memory             not sure
