import plot
import numpy as np
from math import *
import os
import errno

class Record:
    list_of_results = []
    mean_opt_time = 0
    
    def __init__(self):
        self.list_of_results = []
        self.mean_opt_time = 0

    def insert_expriment(self, experiment):
        self.list_of_results.append(experiment)
        n = len(self.list_of_results)
        self.mean_opt_time =  (self.mean_opt_time*float(n-1) + experiment[0])/float(n)

    def plot_all(self):
        neval = []
        function_value = []
        for r in self.list_of_results:
            neval.append(r[3])
            function_value.append(r[2])
        plot.line_plot(neval, function_value, xaxis='Evaluations', yaxis='f(x)')
        
    def plot_average(self, steps):
        minimum_value = 0
        maximum_value = max(self.list_of_results[0][2]) #max value from function_value

        #Calculate average values
        intermediate_values = np.linspace(minimum_value, maximum_value, steps)
        average_run = np.zeros(steps)
        for i in range(steps):
            #for each value, find the first time it was found by each iteration
            for l in self.list_of_results:
                j = 0
                nevals = l[3]
                function_value = l[2]
                while function_value[j] < intermediate_values[i]:
                    j += 1
                    if j == len(function_value) - 1:
                        break
                average_run[i] += nevals[j]
            
        average_run = np.divide(average_run, len(self.list_of_results))

        #Calculate variances
        variance = np.zeros(steps)
        for i in range(steps):
            for l in self.list_of_results:
                j = 0
                nevals = l[3]
                function_value = l[2]
                while function_value[j] < intermediate_values[i]:
                    j += 1
                    if j == len(function_value) - 1:
                        break
                variance[i] += pow((nevals[j] - average_run[i]), 2)

        variance = np.asarray([sqrt(x) for x in variance] )
        variance = np.divide(variance, len(self.list_of_results) - 1)
        #errorbar = [[average_run[i] - variance[i], average_run[i] + variance[i]] for i in range(steps)]

        time_spent = []
        for l in self.list_of_results:
            nevals = l[3]
            time_spent.append(nevals[-1])
            
        print average_run[steps-1], min(time_spent), max(time_spent)
        #plot.line_plot_error([np.asarray(intermediate_values)], [np.asarray(average_run)], [np.asarray(variance)], xaxis='f(x)', yaxis='Evaluations')


    #print the time to get to a certain value     
    def print_to_file(self, problem, size, alg, steps, extra=""):
        path = "../data/" + problem + "/"# + alg + ".txt"
        if not os.path.exists(path):
            os.makedirs(path)
        f1 = open(path + "n" + str(size) + "_" + alg + extra + "_" + problem  + ".txt", 'w+')

        minimum_value = 0
        maximum_value = max(self.list_of_results[0][2]) #max value from function_value

        #Calculate average values
        intermediate_values = np.linspace(minimum_value, maximum_value, steps)
        
        #Define the list to be printed
        lists_to_print = np.zeros([len(self.list_of_results), steps])
        
        for i in range(steps):
            #for each value, find the first time it was found by each iteration
            for (k,l) in enumerate(self.list_of_results):
                j = 0
                nevals = l[3]
                function_value = l[2]
                while function_value[j] < intermediate_values[i]:
                    j += 1
                    if j == len(function_value) - 1:
                        break
                lists_to_print[k][i] = nevals[j]

        for (k,l) in enumerate(lists_to_print):
            f1.write(' '.join(map(str, l)))
            f1.write('\n')
            
        
        

        
    
