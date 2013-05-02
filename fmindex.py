import collections
import sys
import t_rank
from suffix_array import Suffix_array
# import tools


class FMIndex(object):
    def __init__(self, text):
            #handles pysuffix sorting
            self.text = text

            # text_unicode = tools.utf82unicode(text)
            sa = Suffix_array()
            sa._add_str(text)
            sa.karkkainen_sort()
            sa.str_array = "" #free up some memory
            self.suffix_array = sa.suffix_array[:-3] #for some reason pysuffix appends 3 0's at the end of the suffix array
            sa = "" #free up more mem

            # self.suffix_array = self.create_suffix_array(self.text)
            self.last_column = [self.text[i-1] for i in self.suffix_array]
            self.cumulative_index = self.calculate_cumulative_index(self.last_column)
            self.rank_cps = t_rank.TRank(self.last_column, self.cumulative_index.keys())

    #TODO: implement linear time suffix array creation algorithm
    def create_suffix_array(self, text):
        """create suffix array representation of given text"""
        suffix_refs = range(len(self.text))
        return sorted(suffix_refs, cmp=self.ref_comp)

    def ref_comp(self, x, y):
        """compare two references to the text
        checks which points to a greater valued suffix"""
        i = 0
        while self.text[x+i] == self.text[y+i]:
            if self.text[x+i] == '$':
                return x - y
            i += 1
        return ord(self.text[x+i]) - ord(self.text[y+i])

    def calculate_cumulative_index(self, l):
        """create array of t-rank values of characters in 
        the last column of the bw matrix"""
        counter = collections.Counter(l)
        sorted_counts = sorted(counter.items())
        current_cumulative_position = 0
        cumulative_index = {}
        for (key, value) in sorted_counts:
            cumulative_index[key] = current_cumulative_position
            current_cumulative_position += value
        return cumulative_index

    def get_range(self, p):
        """get the range of rows containing indices for hits of given pattern
        returning start with value greater than end indicates no hits were found"""
        rs = reversed(p)
        start = 0
        end = len(self.text) - 1
        for c in rs:

            #if query contains character not present anywhere in the text
            #return immmediate with values that indicate there are no hits
            if c not in self.cumulative_index.keys(): 
                start = end + 1
                break

            start = self.rank_cps.rank_at_row(c, start - 1) + self.cumulative_index[c] + 1
            end = self.rank_cps.rank_at_row(c, end) + self.cumulative_index[c]

            if start > end:     #if there are no matches
                break
        return start, end + 1

    def contains_substring(self, p):
        """the range of indices pointing the the substring
        will contain some elements if the pattern is present in the text"""
        start, end = self.get_range(p)
        return start < end

    def occurrences(self, p):
        """return indices of occurrences of pattern in the text"""
        start, end = self.get_range(p)
        # print start, end
        if start < end:
            return self.suffix_array[start:end]
        else:
            return []

    def find_prefixes(self, p):
        occurences = self.occurrences(p)
        prefixes = [occ for occ in occurences if self.text[occ-1] == '$']
        # prefix_strings = 
        return prefixes

    #NOTE: This method only works if multiple reads are passed as a '$' seperated txt
    def get_nth_read(self, n):
        """Gets the nth stored element
        O(|read|) runtime"""
        chars = []
        row = n
        bw_c = self.last_column[row]
        chars.append(bw_c)
        while bw_c != '$':
            row = self.rank_cps.rank_at_row(bw_c, row - 1) + self.cumulative_index[bw_c] + 1
            bw_c = self.last_column[row]
            chars.append(bw_c)
        return ''.join(reversed(chars))[1:]

    #NOTE: Refactor when text is no longer saved
    def get_read_at_offset(self, offset):
        """returns the read that occurs at given offset
        O(|read|) runtime"""
        before = []
        after = []

        #get all characters up to previous seperator
        for i in xrange(1, offset + 1):
            prev_char = self.text[offset - i]
            if prev_char == '$':
                break
            else:
                before.append(prev_char)

        #get all character up to next seperator
        for i in xrange(len(self.text) - offset):
            next_char = self.text[offset + i]
            if next_char == '$':
                break
            else:
                after.append(next_char)

        before = ''.join(reversed(before))
        after = ''.join(after)
        return before + after


def main():
    if len(sys.argv) != 2:
        print "Please call script in the following format: python fm_index.py file_to_build_index_of.txt"
        exit()
    t = ""
    with open(sys.argv[1]) as f:
        t = f.read()

    fm_index = FMIndex(t + '$')
    # exit(0)


    print "text processed, enter EOF when done."
    try:
        while True:
            p = raw_input("Enter string to search for occurences: ")
            occurences = fm_index.occurrences(p)
            print sorted(occurences)
            print [fm_index.text[i:i+len(p)] for i in occurences]
            print len(occurences)
    except(EOFError):
        print ""
        exit(0)

if __name__ == "__main__":
    main()