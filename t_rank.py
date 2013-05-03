class TRank(object):
    """Maintains checkpoints of t-ranks for last row in BW matrix
    values of characters at checkpoint is 0 if character has not been seen at all"""

    def __init__(self, bwt, characters, cp_interval=4):
        self.checkpoints = {}
        self.characters = characters
        self.bwt = bwt
        self.cp_interval = cp_interval

        #setting all values to nergative 1, because t-rank should be 0 at first occurence
        self.char_occurences = { c: -1 for c in characters }
        self.create_checkpoints()

    def create_checkpoints(self):
        """iterates through last column of BW matrix recording num occurences of
        each character seen. Stores current counts in checkpoint rows"""
        for i, c in enumerate(self.bwt):
            self.char_occurences[c] += 1        #track occurence of letter
            if i % self.cp_interval == 0:       #at specified interval
                self.add_checkpoint(i)          #add checkpoint

    def add_checkpoint(self, checkpoint_row):
        """saves number of occurences of each character at checkpoint row"""
        self.checkpoints[checkpoint_row] = self.char_occurences.copy()

    def rank_at_row(self, char, row):
        """returns number of character occurences up to given row. 
        INCLUDING occurences at given row"""

        #save ourselves trouble if the character does not occur at all
        if char not in self.characters or row < 0:
            return -1

        distance_from_prev_cp = row % self.cp_interval
        prev_cp_index = row - distance_from_prev_cp
        t_rank_at_prev_index = self.checkpoints[prev_cp_index][char]

        #previous cp_index + 1 because the checkpoints count occurences that happen on their index
        occurences_after_checkpoint = self.count_up(char, prev_cp_index + 1, row + 1)
        # print prev_cp_index, row
        return t_rank_at_prev_index + occurences_after_checkpoint

    def count_up(self, char, from_index, to_index):
        """counts occurences of char between from_index and to_index"""
        occurences = 0
        # print 'from_index:', from_index
        # print 'to_index', to_index
        # print len(self.bwt)
        for i in xrange(from_index, to_index):
            # print char
            if self.bwt[i] == char:
                occurences += 1
        return occurences