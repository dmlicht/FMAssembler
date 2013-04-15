import fmindex
from collections import Counter

s = "Tomorrow_and_tomorrow_and_tomorrow"

fm_index = fmindex.FMIndex(s)

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

def test_counts_from_get_occurences():
    #read in data
    with open('ipsum.txt') as f:
        s2 = f.read()
    index = fmindex.FMIndex(s2)

    distinct_words = set(s2.split())
    #count the words the old fashioned way
    counter = Counter()
    for word in distinct_words:
        i = 0
        while i < len(s2):
            i = s2.find(word, i)
            if i == -1:
                break
            counter[word] += 1
            i += 1

    #count the words using fm index
    fm_occurence_counts = {}
    for word in distinct_words:
        fm_occurence_counts[word] = len(index.occurrences(word))

    #compare!
    print counter
    for word in distinct_words:
        print word
        assert fm_occurence_counts[word] == counter[word]

test_counts_from_get_occurences()