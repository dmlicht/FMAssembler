import fmindex
from collections import Counter

s = "Tomorrow_and_tomorrow_and_tomorrow"
fm_index = fmindex.FMIndex(s)

def test_get_range():
    print fm_index.get_range('om')
    print sorted(fm_index.cumulative_index.items(), key=lambda x: x[1])

def test_calculate_cumulative_index():
    counter = Counter(s)
    cumulative_index = fm_index.calculate_cumulative_index(s)
    sorted_counts = sorted(counter.items())
    for i in xrange(len(sorted_counts)-1):
        current_letter = sorted_counts[i][0]
        next_letter = sorted_counts[i+1][0]
        current_letter_count = sorted_counts[i][1]
        diff = cumulative_index[next_letter] - cumulative_index[current_letter]
        assert current_letter_count == diff

test_calculate_cumulative_index()