# with open('complete_works.txt', 'r') as f:
#   txt = f.read()
import collections
import sys
import t_rank

class FMIndex(object):
    def __init__(self, text):
        self.text = text + "$"

        self.suffix_array = self.create_suffix_array(self.text)
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
                return start, end


            #TODO: figure out why start index is on~e behind 
            start = self.rank_cps.rank_at_row(c, start - 1) + self.cumulative_index[c] + 1
            end = self.rank_cps.rank_at_row(c, end) + self.cumulative_index[c]
            # print c, start, end

            if start > end:     #if there are no matches
                return start, end + 1
        return start, end + 1

    # def get_rank(self, char, row, direction):
    #     """get the t rank of given character with respect to row.
    #     that is, number of times the character has occured up to that row"""
    #     i = row
    #     while self.last_column[i] != char and i > 0:
    #         if direction == "up":
    #             i += 1
    #         elif direction == "down":
    #             i -= 1
    #     return self.t_ranks[i]

    #NOTE: this method is currently pointless because original text is still being stored
    #as of now, it functions as a sanity check to see if the index is working properly
    #it will be more useful when we compress the text.
    # def reverse(self, reversal_start_index=0):
    #     """retrieves the text from the bwt"""
    #     word = ""
    #     current_string_index = reversal_start_index
    #     while self.last_column[current_string_index] != '$':
    #         current_letter = self.last_column[current_string_index]
    #         word = current_letter + word
    #         current_letter_t_rank = self.t_ranks[current_string_index]
    #         current_string_index = self.cumulative_index[current_letter] + current_letter_t_rank
    #     return word

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

def main():
    if len(sys.argv) != 2:
        print "Please call script in the following format: python fm_index.py file_to_build_index_of.txt"
        exit()
    t = ""
    with open(sys.argv[1]) as f:
        t = f.read()

    fm_index = FMIndex(t)
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

# fm_index = FMIndex("Tomorrow and tomorrow and tomorrow")
# print ''.join(fm_index.l) == "w$wwdd__nnoooaattTmmmrrrrrrooo__ooo"
# print fm_index.l
# print fm_index.reverse()
# print fm_index.occurrences("row")