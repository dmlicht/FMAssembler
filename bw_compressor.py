class Compressor(object):
    def __init__(self):
        pass

    def bw_compress(self, s):
        self.text = s + '$'
        sa = self.create_suffix_array(self.text)
        bwt = [s[i-1] for i in sa]
        self.text = ""
        return self.compress(bwt)

    def create_suffix_array(self, text):
        """create suffix array representation of given text"""
        suffix_refs = range(len(self.text))
        return sorted(suffix_refs, cmp=self.ref_comp)

    def ref_comp(self, x, y):
        """compare two references to the text
        checks which points to a greater valued suffix"""
        i = 0
        while self.text[x+i] == self.text[y+i]:
            i += 1
            print i
        return ord(self.text[x+i]) - ord(self.text[y+i])

    def compress(self, bwt):
        compressed_bwt = []
        last_char = bwt[0]
        run = 1
        for i in range(1, len(bwt)):
            if bwt[i] == last_char:
                run += 1
            else:
                compressed_bwt.append((last_char, run))
                last_char = bwt[i]
                run = 0
        compressed_bwt.append((last_char, run))
        return compressed_bwt

c = Compressor()
s = "Tomorrow_and_tomorrow_and_tomorrow"
print len(s)
print c.bw_compress("Tomorrow_and_tomorrow_and_tomorrow")