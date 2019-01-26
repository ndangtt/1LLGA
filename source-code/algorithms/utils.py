from solution import *
import evaluate
import record
import plot
from copy import *
import time

def random_vector(n):
    x = np.zeros(n)
    for i in range(n):
        if np.random.rand() < 0.5:
            x[i] = 1
    return x

    
def mutation(parent, l):
    n = len(parent.chromossome)
    flip = np.random.choice(range(n),l, replace=False)

    offspring = copy(parent.chromossome)
    for i in flip:
        offspring[i] = (parent.chromossome[i] + 1)%2

    s = Solution(offspring, parent, flip, None)
    #s.value = getattr(evaluate, instance.name)(s,instance)
    return s
    #does not assign the value because we do not which function is being used. This has to be assigned somewhere else in the code

    
#takes element from solution1 with probability 1-c and from solution2 with probability c
def crossover(solution1, solution2, c):
    assert (len(solution1.chromossome) == len(solution2.chromossome)), "Lists do not have the same size."
    n = len(solution1.chromossome)
    offspring = copy(solution1.chromossome)
    flip = []
    evaluation = 0 #if there was an evaluation or not

    l = np.random.binomial(n,c)
    flip = np.random.choice(range(n),l, replace=False)

    for i in flip:
        offspring[i] = solution2.chromossome[i]    

    s = Solution(offspring, solution1, flip, None)

    return s


#similar to crossover, but only different bits are considered
def crossover_different_bits(solution1, solution2, c, D, nD):
    assert (len(solution1.chromossome) == len(solution2.chromossome)), "Lists do not have the same size."
    
    offspring = copy(solution1.chromossome)
    flip = []

    l = np.random.binomial(nD,c)
    while l == 0 or l == nD:
        l = np.random.binomial(nD,c)
    #if l==0:
    #    l=1

    flip = np.random.choice(range(nD),l, replace=False)

    for i in flip:
        position = D[i]
        offspring[position] = solution2.chromossome[position]    

    s = Solution(offspring, solution1, flip, None)

    return s


def compare(list_of_records, steps, algorithms):
    all_intermediate_values = []
    all_average_runs = []
    
    for record in list_of_records:
        minimum_value = 0
        maximum_value = max(record.list_of_results[0][2]) #max value from function_value
        
        intermediate_values = np.linspace(minimum_value, maximum_value, steps)
        average_run = np.zeros(steps)
        for i in range(steps):
            #for each value, find the first time it was found by each iteration
            for l in record.list_of_results:
                j = 0
                nevals = l[3]
                function_value = l[2]
                while function_value[j] < intermediate_values[i] and j < l[1]-1:
                    j += 1
                    #if j > len(function_value):
                     #   break
                average_run[i] += nevals[j]

        average_run = np.divide(average_run, len(record.list_of_results))
        all_intermediate_values.append(list(intermediate_values))
        all_average_runs.append(list(average_run))

        
    #plot.line_plot( all_intermediate_values, all_average_runs, xaxis='f(x)', yaxis='Evaluations', labels=algorithms)
    plot.scatter( all_intermediate_values, all_average_runs, xaxis='f(x)', yaxis='Evaluations', labels=algorithms) 
