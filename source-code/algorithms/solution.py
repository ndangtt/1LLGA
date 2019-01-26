import numpy as np

class Solution:
    chromossome = np.zeros(0)
    parent = None
    bits_flipped = []
    value = 0
    

    def __init__(self, chromossome, parent, bits_flipped, value):
        self.chromossome = chromossome
        self.parent = parent
        self.bits_flipped = bits_flipped
        self.value = value
