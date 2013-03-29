# with open('complete_works.txt', 'r') as f:
#   txt = f.read()
import collections
import sys

class FMIndex(object):
    def __init__(self, text):
        self.text = text + "$"

        self.suffix_array = self.create_suffix_array(self.text)
        self.l = self.BW_transform(self.suffix_array)
        self.t_ranks, self.cumulative_index = self.calculate_t_ranks_and_cumulative_index(self.l)
        # self.checkpoint_spacing = 4
        # self.checkpoints = self.calculate_checkpoints(self.l)

    #TODO implement linear time suffix array creation algorithm
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

    def BW_transform(self, suffix_array):
        """burrows wheeler transform uses suffix array to get character that occurs
        right before the suffix to find the character that would be in the last column
        of a BW matrix"""
        return [self.text[i-1] for i in suffix_array]

    def calculate_t_ranks_and_cumulative_index(self, l):
        """create array of t-rank values of characters in 
        the last column of the bw matrix"""
        letter_counts = collections.defaultdict(int)
        t_ranks = []
        for letter in l:
            t_ranks.append(letter_counts[letter])
            letter_counts[letter] += 1
        sorted_counts = sorted(letter_counts.items())
        current_cumulative_position = 0
        cumulative_index = {}
        for (key, value) in sorted_counts:
            cumulative_index[key] = current_cumulative_position
            current_cumulative_position += value
        return t_ranks, cumulative_index

    # def calculate_checkpoints(self, l):
    #     checkpoints = {}
    #     counts = {}
    #     for i, char in enumerate(l):
    #         if counts.get(char) == None:
    #             counts[char] = 0
    #             checkpoints[char] = []
    #         else:
    #             counts[char] += 1
    #             if i % self.checkpoint_spacing == 0:
    #                 for c in checkpoints.keys():
    #                     checkpoints[c].append(counts[c])
    #     return checkpoints

    #TODO implement checkpoint table to save memory
    #TODO refactor t rank checkpoints and calculation to seperate class
    def get_rank(self, char, row):
        """get the t rank of given character with respect to row.
        that is, number of times the character has occured"""
        i = row
        while self.l[i] != char and i > 0:
            i -= 1
        return self.t_ranks[i]

    def get_range(self, p):
        """get the range of indices for matches of given string p"""
        rs = reversed(p)
        start = 0
        end = len(self.text) - 1
        for c in rs:
            #TODO figure out cleaner fix
            if c not in self.cumulative_index.keys():
                start = end + 1
                return start, end
            start = self.get_rank(c, start) + self.cumulative_index[c]
            end = self.get_rank(c, end) + self.cumulative_index[c]
            #if there are no matches
            if start > end:
                return start, end
        return start, end + 1

    #note this is currently somewhat pointless, the original t is still being stored
    def reverse(self, reversal_start_index=0):
        """retrieves the text from the bwt"""
        word = ""
        current_string_index = reversal_start_index
        while self.l[current_string_index] != '$':
            current_letter = self.l[current_string_index]
            word = current_letter + word
            current_letter_t_rank = self.t_ranks[current_string_index]
            current_string_index = self.cumulative_index[current_letter] + current_letter_t_rank
        return word

    def contains_substring(self, p):
        """the range of indices pointing the the substring
        will contain some elements if the pattern is present in the text"""
        start, end = self.get_range(p)
        return start < end

    def occurrences(self, p):
        """return indices of occurrences of pattern in the text"""
        start, end = self.get_range(p)
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
            print p
            print sorted(fm_index.occurrences(p))
            print [fm_index.text[i:i+len(p)] for i in fm_index.occurrences(p)]
    except(EOFError):
        print
        exit(0)

if __name__ == "__main__":
    main()

# fm_index = FMIndex("Tomorrow and tomorrow and tomorrow")
# print ''.join(fm_index.l) == "w$wwdd__nnoooaattTmmmrrrrrrooo__ooo"
# print fm_index.l
# print fm_index.reverse()
# print fm_index.occurrences("row")