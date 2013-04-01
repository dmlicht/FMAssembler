class TRank(object):
    """Maintains checkpoints of t-ranks for last row in BW matrix
    values of characters at checkpoint is 0 if character has not been seen at all"""

    def __init__(self, last_column, characters, cp_interval=4):
        self.checkpoints = {}
        self.last_column = last_column
        self.cp_interval = cp_interval

        #setting all values to nergative 1, because t-rank should be 0 at first occurence
        self.char_occurences = { c: -1 for c in characters }
        self.create_checkpoints()

    def create_checkpoints(self):
        """iterates through last column of BW matrix recording num occurences of
        each character seen. Stores current counts in checkpoint rows"""
        for i, c in enumerate(self.last_column):
            self.char_occurences[c] += 1        #track occurence of letter
            if i % self.cp_interval == 0:       #at specified interval
                self.add_checkpoint(i)          #add checkpoint

    def add_checkpoint(self, checkpoint_row):
        """saves number of occurences of each character at checkpoint row"""
        self.checkpoints[checkpoint_row] = self.char_occurences.copy()

    def get_char_occurences_at_row(self, char, row):
        """returns number of character occurences up to given row. Includes occurences at row"""
        distance_from_prev_cp = row % self.cp_interval
        prev_cp_index = row - distance_from_prev_cp
        t_rank_at_prev_index = self.checkpoints[prev_cp_index][char]
        occurences_after_checkpoint = self.count_up(char, prev_cp_index, row+1)
        return t_rank_at_prev_index + occurences_after_checkpoint

    def count_up(self, char, from_index, to_index):
        """counts occurences of char between from_index and to_index"""
        occurences = 0
        for i in xrange(from_index, to_index):
            if self.last_column[i] == char:
                occurences += 1
        return occurences