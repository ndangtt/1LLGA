from solution import *
import numpy as np


class setup_OneMax:
    size = None
    optimum = None
    name = None

    def __init__(self, size, name):
        self.size = size
        self.optimum = size
        self.name = name

def OneMax(solution, instance, first = False):
    flipped = solution.bits_flipped
    if first:
        return sum(solution.chromossome)
        
    return solution.parent.value + sum([solution.chromossome[i] for i in flipped]) - sum([solution.parent.chromossome[i] for i in flipped])

class setup_LeadingOnes:
    size = None
    optimum = None
    name = None

    def __init__(self, size, name):
        self.size = size
        self.optimum = size
        self.name = name

def LeadingOnes(solution, instance, first = False):
    if first:
        i = 0
        while solution.chromossome[i] != 0:
            i += 1
            if i == instance.size:
                break
        return i

    if len(solution.bits_flipped) == 0:
        return solution.parent.value

    if min(solution.bits_flipped) < solution.parent.value:
        return min(solution.bits_flipped)
    else:
        i = solution.parent.value
        increment = 0
        while solution.chromossome[i] != 0:
            i += 1
            increment += 1
            if i == instance.size:
                break
        return solution.parent.value + increment
    

class setup_Linear:
    size = None
    optimum = None
    name = None
    w = None

    def __init__(self, size, name):
        self.size = size
        self.name = name
        aux = np.ones(size)
        for i in range(size):
            aux[i] += np.random.rand()
        self.w = aux
        self.optimum = np.dot(aux, np.ones(size))

def Linear(solution, instance, first = False):
    w = instance.w
    flipped = solution.bits_flipped
    if first:
        return np.dot(w,solution.chromossome)

    #This solution is better but I'm have problems with comparing floating points
    #w_i = [w[i] for i in flipped]
    #solution_i = [solution.chromossome[i] for i in flipped]
    #solution_parent_i = [solution.parent.chromossome[i] for i in flipped]
    #return solution.parent.value + np.dot(w_i, solution_i) - np.dot(w_i, solution_parent_i)
    return np.dot(w,solution.chromossome)
    
class setup_Jump:
    size = None
    optimum = None
    name = None

    def __init__(self, size, name):
        self.size = size
        self.optimum = size
        self.name = name

def Jump(solution, instance, first = False):
    flipped = solution.bits_flipped
    if first:
        return sum(solution.chromossome)

    
    aux = solution.parent.value + sum([solution.chromossome[i] for i in flipped]) - sum([solution.parent.chromossome[i] for i in flipped])
    if aux < instance.optimum - 1:
        return aux
    elif aux == instance.optimum - 1:
        return -100
    else:
        return instance.optimum


class setup_RoyalRoad:
    size = None
    optimum = None
    name = None
    k = 0
    blocks = []

    def __init__(self, size, name):
        self.size = size
        self.k = 3
        if (size)%self.k == 0:
            self.optimum = (size)/self.k
        else:
            self.optimum = (size)/self.k + 1
        self.name = name

        
        j = 0
        self.blocks = []
        while j < self.size:
            b = []
            i = 0
            while i < self.k and j + i < self.size:
                b.append(j + i)
                i += 1
            self.blocks.append(b)
            j += self.k
        

def RoyalRoad(solution, instance, first = False):
    
    k = instance.k
    n = instance.size

    #if first:
    value = 0
    for b in instance.blocks:
        all_ones = True
        for i in b:
            if solution.chromossome[i] == 0:
                all_ones = False
        if all_ones:
            value += 1
    
    return value
    '''
    value = 0
    flip = solution.bits_flipped

    for i in flip:
        #identify the block it belongs to
        b_id = i/k
        b = instance.blocks[b_id]
        #was it all ones before?
        all_ones_before = True
        for j in b:
            if solution.parent.chromossome[i] == 0:
                all_ones_before = False
        
        
        all_ones = True
        for j in b:
            if solution.chromossome[i] == 0:
                all_ones = False

        if all_ones and not all_ones_before:
            value += 1
        if not all_ones and all_ones_before:
            value -= 1

    return solution.parent.value + value
    '''
        
    
