# with open('complete_works.txt', 'r') as f:
#   txt = f.read()
import collections

class FMIndex(object):
  def __init__(self, t):
    self.f, self.offsets = self.BW_transform(t + "$")
    self.l, self.letter_counts = self.count_letters(self.f)

  def BW_transform(self, t):
    rotations = []
    for rot, index in self.generate_rotations(t):
      rotations.append((rot, index))
    rotations.sort()
    f = [rot[0][-1] for rot in rotations]
    offsets = [rot[1] for rot in rotations]
    return f, offsets

  def generate_rotations(self, t):
    """returns generator for all rotations of given string t"""
    for i in range(len(t)):
      yield t[i:] + t[:i], (i - 1 % len(t))

  def count_letters(self, l):
    """calculated the offset of each letter beginning to appear in left column"""
    letter_counts = collections.defaultdict(int)
    count_at_position_array = []
    for letter in l:
      count_at_position_array.append(letter_counts[letter])
      letter_counts[letter] += 1
    sorted_counts = sorted(letter_counts.items())
    current_cumulative_position = 0
    cumulative_index = {}
    for (key, value) in sorted_counts:
      cumulative_index[key] = current_cumulative_position
      current_cumulative_position += value
    return cumulative_index, count_at_position_array

    


fm_index = FMIndex("How do you say, hey there, how are you friend? It seems so simple, however it's not.$")
# print fm_index.offsets

# print sorted(rotations)