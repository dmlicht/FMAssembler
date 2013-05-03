import collections
import sys
import t_rank
from suffix_array import Suffix_array
# import tools


class FMIndex(object):
    def __init__(self, text):
            #handles pysuffix sorting
            self.text = text

            self.text_len = len(text)
            # text_unicode = tools.utf82unicode(text)
            sa = Suffix_array()
            sa._add_str(text)
            sa.karkkainen_sort()
            sa.str_array = "" #free up some memory
            self.suffix_array = sa.suffix_array[:-3] #for some reason pysuffix appends 3 0's at the end of the suffix array
            sa = "" #free up more mem

            # self.suffix_array = self.create_suffix_array(self.text)

            #bwt = burrows wheeler transformed string
            self.bwt = [self.text[i-1] for i in self.suffix_array]

            #occurences of lexicographically lower valued characters in text
            self.occ_lex_lower = self.calculate_occ_lex_lower(self.bwt)
            self.rank_cps = t_rank.TRank(self.bwt, self.occ_lex_lower.keys())

    #NOTE:Below two function (csa, rc) not being used
    #just temporarily kept to verify results of karkkainen sort
    #until more permanant solution in place
    def create_suffix_array(self, text):
        """create suffix array representation of given text"""
        suffix_refs = range(self.text_len)
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

    def calculate_occ_lex_lower(self, l):
        """returns a dict containing the counts of occurences of 
        lexicographically lower valued characters for a given character"""
        counter = collections.Counter(l)
        sorted_counts = sorted(counter.items())
        lower_char_count = 0
        occ_lex_lower = {}
        for (key, value) in sorted_counts:
            occ_lex_lower[key] = lower_char_count
            lower_char_count += value
        return occ_lex_lower

    def occurrences(self, p):
        """return indices of occurrences of pattern in the text"""
        start, end = self.get_range(p)
        if start < end:
            return self.suffix_array[start:end]
        else:
            return []

    def get_range(self, p):
        """get the range of rows containing indices for hits of given pattern
        returning start with value greater than end indicates no hits were found"""
        rs = reversed(p)
        start = 0
        end = self.text_len - 1
        for c in rs:
            start, end = self.backtrace_step(c, start, end)
            if start > end:     #start will be greater than end if no matches
                break
        return start, end + 1

    def backtrace_step(self, c, start, end):
        """returns start and end of range backtraced one step
        start will be greater than end if no occurences w/in range"""
        if c not in self.occ_lex_lower.keys(): 
            start = end + 1
            return start, end
        start = self.rank_cps.rank_at_row(c, start - 1) + self.occ_lex_lower[c] + 1
        end = self.rank_cps.rank_at_row(c, end) + self.occ_lex_lower[c]
        return start, end

    def contains_substring(self, p):
        """returns true is there is at least one occurence of p indexed"""
        start, end = self.get_range(p)
        return start < end

    #in this function we backtrace the given pattern through the index
    #checking for prefixes at every step (indicated by '$')
    def get_prefix_overlaps(self, p, min_overlap_len):
        """returns all strings with prefix overlap over given min_overlap_len"""
        rs = reversed(p)
        start = 0
        end = self.text_len - 1
        chars_into_p = 0
        all_overlaps = []
        for c in rs:
            start, end = self.backtrace_step(c, start, end)
            chars_into_p += 1
            if start > end:
                break
            if min_overlap_len <= chars_into_p < len(p):
                overlaps = self.elements_preceeded_by_sep(start, end)
                # if overlaps:
                #     print 'fm:', overlaps
                overlaps = [(self.get_read_at_offset(i), chars_into_p) for i in overlaps]
                all_overlaps.extend(overlaps)
        return all_overlaps
    #//NOTE: this function is very similar to get_range
    #is there some clever way to re-use this code?

    def elements_preceeded_by_sep(self, start, end):
        """return list of indices between range directly preceeded by '$' """
        indices = self.suffix_array[start:end+1]
        return [i for i in indices if self.text[i-1] == '$']
        # start, end = self.backtrace_step('$', start, end)
        #+1 because we are getting the indices of the seperators, not the first chars
        # return [i + 1 for i in self.suffix_array[start:end+1]] 

    #NOTE: This function is no longer used
    #This is left in tact for comparison to get_prefix_overlaps()
    def find_prefixes(self, p):
        occurences = self.occurrences(p)
        prefixes = [occ for occ in occurences if self.text[occ-1] == '$']
        return prefixes

    #NOTE: This method only works if multiple reads are passed as a '$' seperated txt
    #NOTE: this function does not work using pysuffix does not prioritize
    # seperator characters that occur earlier in the string
    # to get this function working again, you must roll your own suffix sorting
    def get_nth_read(self, n):
        """Gets the nth stored element
        O(|read|) runtime"""
        chars = []
        row = n
        bw_c = self.bwt[row]
        chars.append(bw_c)
        while bw_c != '$':
            row = self.rank_cps.rank_at_row(bw_c, row - 1) + self.occ_lex_lower[bw_c] + 1
            bw_c = self.bwt[row]
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
        for i in xrange(self.text_len - offset):
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