import t_rank
import collections
import fmindex

with open('ipsum.txt') as f:
    d = f.read()
d = d.replace(' ', '_')

letters = collections.Counter(d).keys()
fm = fmindex.FMIndex(d)
ranks = t_rank.TRank(d, letters)

def test_lookup_with_no_occurences():
    assert ranks.rank_at_row('X', 10) == -1

def test_lookup_before_first_occurence():
    assert ranks.rank_at_row('s', 1) == -1

def test_lookup_at_first_occurence():
    assert ranks.rank_at_row('o', 1) == 0

def test_lookup_directly_after_first_occurence():
    assert ranks.rank_at_row('o', 2) == 0

def test_lookup_before_checkpoint():
    assert ranks.rank_at_row('m', 3) == -1

def test_lookup_at_checkpoint():
    assert ranks.rank_at_row('m', 4) == 0

def test_lookup_after_checkpoint():
    assert ranks.rank_at_row('m', 5) == 0

def test_lookup_sanity_check():
    for i in xrange(1, len(d)):
        c = d[i]
        assert ranks.rank_at_row(c, i) == 1 + ranks.rank_at_row(c, i - 1)