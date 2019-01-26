#LLAll algorithms
#print("import algorithms") #DEBUG

import evaluate
import numpy as np
import utils
import time
import solution
import plot
from math import *
from copy import *
from scipy import stats
from scipy.misc import comb
import scipy.optimize as sciopt
from sympy import binomial
#from main import ioh_output


def LL_crossover_phase(x, x_prime, instance, implementation_choice, chromossome_length, n_offsprings, crossover_bias):
    y = copy(x_prime)
    T = 0

    if implementation_choice == 1: # original implementation
        for i in range(n_offsprings):
            offspring = utils.crossover(x,x_prime,crossover_bias)
            if (offspring.chromossome == x.chromossome).all():
                offspring.value = x.value
            elif (offspring.chromossome == y.chromossome).all():
                offspring.value = y.value
            else:
                offspring.value = getattr(evaluate, instance.name)(offspring,instance)
                T += 1
            if offspring.value > y.value:
                y = offspring
    
    elif implementation_choice == 2: # new implementation: only consider bits where x and x_prime are different
        D = np.arange(chromossome_length)[x!=x_prime]
        nD = len(D)
        if nD >= 2: # no crossover if x and x_prime differ in less than two bits
            for i in range(n_offsprings):
                offspring = utils.crossover_different_bits(x,x_prime,crossover_bias,D,nD)
                offspring.value = getattr(evaluate, instance.name)(offspring,instance)
                T += 1
                if offspring.value > y.value:
                    y = offspring

    elif implementation_choice == 3: # same as crossover_implementation=1, but count evaluations even if offspring==parent
        for i in range(n_offsprings):
            offspring = utils.crossover(x,x_prime,crossover_bias)
            offspring.value = getattr(evaluate, instance.name)(offspring,instance)
            T += 1
            if offspring.value > y.value:
                y = offspring

    return y,T


def LL_static(initial_solution, instance, lda1, lda2, k, c, crossover_choice, max_evaluation, ioh_output = None):
    x = initial_solution
    n = len(x.chromossome)    
    
    T = 0
    function_value = []
    neval = []
    counter = 0

    f = None
    if ioh_output is not None:
        f = open(ioh_output,'at')
        f.write('"function evaluation" "original f(x)" "best original f(x)" "transformed f(x) " "best transformed f(x)" "mutation_rate" "crossover_bias"')

    while(x.value != instance.optimum):        
        #---------- mutation phase ------------

        #sample l from the binomial
        p = k/float(n)
        l = np.random.binomial(n,p)
        while l == 0:
            l = np.random.binomial(n,p)
        
        x_prime = utils.mutation(x,l)
        x_prime.value = getattr(evaluate, instance.name)(x_prime,instance)
        T += 1
        for i in range(lda1 - 1):
            x2_prime = utils.mutation(x,l)
            x2_prime.value = getattr(evaluate, instance.name)(x2_prime,instance)
            T += 1
            if x2_prime.value > x_prime.value:
                x_prime = x2_prime
        
        #-------- crossover phase
        y, Ty = LL_crossover_phase(x=x,x_prime=x_prime,instance=instance,implementation_choice=crossover_choice,chromossome_length=n,n_offsprings=lda2,crossover_bias=c)
        T += Ty
        
        #-------- selection
        if y.value > x.value:
            x = y
	
	if f is not None:
	    ls = [T, x.value, x.value, x.value, x.value, p, c] # IOH output 
	    s = ' '.join([str(val) for val in ls])
	    f.write('\n'+s)
        
        function_value.append(x.value)
        neval.append(T)
        counter += 1

        
        if max_evaluation > 0 and T >= max_evaluation:
            break
        
    #End while

    if f is not None:
        f.write('\n'+str(T))
        f.close()

    return (T, counter, function_value, neval)


def LL_static_02(initial_solution, instance, lda, alpha, beta, crossover_choice, max_evaluation, ioh_output=None):
    x = initial_solution
    n = len(x.chromossome)    
    
    T = 0
    function_value = []
    neval = []
    counter = 0
    
    while(x.value != instance.optimum):        
        #---------- mutation phase ------------

        #sample l from the binomial
        p = alpha/float(n)
        l = np.random.binomial(n,p)
        while l == 0:
            l = np.random.binomial(n,p)
        
        x_prime = utils.mutation(x,l)
        x_prime.value = getattr(evaluate, instance.name)(x_prime,instance)
        T += 1
        for i in range(lda - 1):
            x2_prime = utils.mutation(x,l)
            x2_prime.value = getattr(evaluate, instance.name)(x2_prime,instance)
            T += 1
            if x2_prime.value > x_prime.value:
                x_prime = x2_prime
        
        #-------- crossover phase
        c = 1.0/beta
        y, Ty = LL_crossover_phase(x=x,x_prime=x_prime,instance=instance,implementation_choice=crossover_choice,chromossome_length=n,n_offsprings=lda,crossover_bias=c)
        T += Ty
        
        #-------- selection
        if y.value > x.value:
            x = y
        
        function_value.append(x.value)
        neval.append(T)
        #counter += 1

        if max_evaluation > 0 and T >= max_evaluation:
            break
        
        #if T % 1000 == 0:
        #    print(T)
        #    print(str(x.value) + '/' + str(instance.optimum))

    #End while
    return (T, counter, function_value, neval)


def LL_dynamic_01(initial_solution, instance, a, b, crossover_choice, max_evaluation, ioh_output=None):
    x = initial_solution
    n = len(x.chromossome)
    
    lda = float(1)
    
    T = 0
    #ldas = []
    function_value = []
    neval = []
    counter = 0

    f = None
    if ioh_output is not None:
        f = open(ioh_output,'at')
        f.write('"function evaluation" "original f(x)" "best original f(x)" "transformed f(x) " "best transformed f(x)" "mutation_rate" "crossover_bias" "lambda" "iteration"')

    while(x.value != instance.optimum):
        p = lda/float(n)
        c = 1.0/lda
        
        #----------- mutation phase

        #print("Mutation phase: lda="+str(lda)+'; T='+str(T)) #DEBUG
        l = np.random.binomial(n,p)
        while l == 0:
            l = np.random.binomial(n,p)
        
        x_prime = utils.mutation(x,l)
        x_prime.value = getattr(evaluate, instance.name)(x_prime,instance)
        T += 1
        for i in range(int(round(lda) - 1)):
            x2_prime = utils.mutation(x,l)
            x2_prime.value = getattr(evaluate, instance.name)(x2_prime,instance)
            T += 1
            if x2_prime.value > x_prime.value:
                x_prime = x2_prime
        
        #---------- crossover phase
        y, Ty = LL_crossover_phase(x=x,x_prime=x_prime,instance=instance,implementation_choice=crossover_choice,chromossome_length=n,n_offsprings=int(round(lda)),crossover_bias=c)
        T += Ty
        #print("Crossover phase: lda="+str(lda)+'; T='+str(T)) #DEBUG
    
        #---------- selection and update phase        
        if (y.value <= x.value):
            #x = y
            lda = min([lda * a,n-1])

	if (y.value > x.value):
            x = y
            lda = max([lda * b,1])

	if f is not None:
	    ls = [T, x.value, x.value, x.value, x.value, p, c, lda, counter] # IOH output
	    s = ' '.join([str(val) for val in ls])
	    f.write('\n'+s)
                                
        #ldas.append(lda)
        function_value.append(x.value)
        neval.append(T)
        counter += 1

        if max_evaluation > 0 and T >= max_evaluation:
            break

    #End while
    if f is not None:    
        f.write('\n'+str(T))
        f.close()
    return (T, counter, function_value, neval)


def LL_dynamic_02(initial_solution, instance, alpha, beta, gamma, a, b, crossover_choice, max_evaluation, ioh_output=None):
    x = initial_solution
    n = len(x.chromossome)
    
    lda = float(1)
    
    T = 0
    ldas = []
    function_value = []
    neval = []
    counter = 0

    min_prob = 1.0/n
    max_prob = 0.99

    f = None
    if ioh_output is not None:
        f = open(ioh_output,'at')
        f.write('"function evaluation" "original f(x)" "best original f(x)" "transformed f(x) " "best transformed f(x)" "mutation_rate" "crossover_bias" "n_mutations" "n_offsprings" "iteration"')


    while(x.value != instance.optimum):
        p = max([min([alpha * lda/float(n),max_prob]), min_prob])
        lda1 = int(round(lda))
        lda2 = int(round(beta * lda))
        c = max([min([gamma/lda,max_prob]), min_prob])
        
        #----------- mutation phase

        l = np.random.binomial(n,p)
        while l == 0:
            l = np.random.binomial(n,p)
        
        x_prime = utils.mutation(x,l)
        x_prime.value = getattr(evaluate, instance.name)(x_prime,instance)
        T += 1
        for i in range(int(round(lda1) - 1)):
            x2_prime = utils.mutation(x,l)
            x2_prime.value = getattr(evaluate, instance.name)(x2_prime,instance)
            T += 1
            if x2_prime.value > x_prime.value:
                x_prime = x2_prime
        
        #---------- crossover phase
        y, Ty = LL_crossover_phase(x=x,x_prime=x_prime,instance=instance,implementation_choice=crossover_choice,chromossome_length=n,n_offsprings=lda2,crossover_bias=c)
        T += Ty
    
        #---------- selection and update phase            
        if (y.value <= x.value):
            #x = y
            lda = min([lda * a,n-1])

        if (y.value > x.value):
            x = y
            lda = max([lda * b,1])

	if f is not None:
	    ls = [T, x.value, x.value, x.value, x.value, p, c, lda1, lda2, counter] # IOH output
	    s = ' '.join([str(val) for val in ls])
	    f.write('\n'+s)
                    
        ldas.append(lda)
        function_value.append(x.value)
        neval.append(T)
        counter += 1

        if max_evaluation > 0 and T >= max_evaluation:
            break
        
    #End while
    if f is not None:
        f.write('\n'+str(T))
        f.close()
    return (T, counter, function_value, neval)
