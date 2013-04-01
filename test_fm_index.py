import fmindex

s = "Tomorrow_and_tomorrow_and_tomorrow"
fm_index = fmindex.FMIndex("Tomorrow_and_tomorrow_and_tomorrow")

def test_bw_transform():
    assert ''.join(fm_index.l) == "w$wwdd__nnoooaattTmmmrrrrrrooo__ooo"

def test_sanity():
    assert s == fm_index.reverse()



# def test_letter_counts():
    # counter = collections.Counter('Tomorrow_and_tomorrow_and_tomorrow')
    # print fm_index.letter_counts
    # for (k, v) in counter.items():
    #     print k
    #     assert fm_index.l[k] == v 