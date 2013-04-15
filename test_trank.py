import t_rank
import collections

with open('ipsum.txt') as f:
    d = f.read()
d = d.replace(' ', '_')

letters = collections.Counter(d).keys()


ranks = t_rank.TRank(d, letters)
print d
# print ranks.get_char_occurences_at_row('X', 10)

def test_lookup_with_no_occurences():
    assert ranks.get_char_occurences_at_row('X', 10) == 0

def test_lookup_before_first_occurence():
    assert ranks.get_char_occurences_at_row('s', 1) == -1

def test_lookup_at_first_occurence():
    assert ranks.get_char_occurences_at_row('o', 2) == 0

def test_lookup_directly_after_first_occurence():
    assert ranks.get_char_occurences_at_row('o', 3) == 0

def test_lookup_before_checkpoint():
    assert ranks.get_char_occurences_at_row('m', 3) == -1

def test_lookup_at_checkpoint():
    assert ranks.get_char_occurences_at_row('m', 4) == 0
    print ranks.get_char_occurences_at_row('m', 4)

def test_lookup_after_checkpoint():
    assert ranks.get_char_occurences_at_row('m', 5) == 0


test_lookup_at_checkpoint()