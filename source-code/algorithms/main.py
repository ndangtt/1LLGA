# (Nguyen) Syntax: python2 main.py --problem <problem> --size <size> --algorithm <algorithm> <parameters> [--random_seed <random_seed>] [--max_evaluation <max_evaluation>] [--it <number of runs>]

# Examples:

# ----- static LL, one run, without bound
# python2 main.py --problem OneMax --size 500 --algorithm "['LL_static']" --LL_static_lambda1 4 --LL_static_lambda2 4 --LL_static_lda 3 --LL_static_crossOverBias 0.3 --random_seed 11

# ----- static LL, one run, with bound
# python2 main.py --problem OneMax --size 500 --algorithm "['LL_static']" --LL_static_lambda1 4 --LL_static_lambda2 4 --LL_static_lda 3 --LL_static_crossOverBias 0.3 --random_seed 11 --max_evaluation 100000

# ----- static LL, 10 runs
# python2 main.py --problem OneMax --size 500 --algorithm "['LL_static']" --LL_static_lambda1 4 --LL_static_lambda2 4 --LL_static_lda 3 --LL_static_crossOverBias 0.3 --it 10

# ----- dynamic LL, 2 parameters
# python2 main.py --problem OneMax --size 500 --algorithm "['LL_dynamic_01']" --LL_dynamic_01_a 1.1 --LL_dynamic_01_b 0.7 --random_seed 123

# ----- dynamic LL, 5 parameters
# python2 main.py --problem OneMax --size 500 --algorithm "['LL_dynamic_02']" --LL_dynamic_02_alpha 0.7 --LL_dynamic_02_beta 3 --LL_dynamic_02_gamma 0.3 --LL_dynamic_02_a 1.1 --LL_dynamic_02_b 0.7 --random_seed 123

from solution import *
#from tqdm import tqdm
import evaluate
import utils
import algorithms
import plot
import record

import numpy as np
import sys, argparse
import time
import os

import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--problem', help='Available problems: OneMax, LeadingOnes, Jump, Linear, RoyalRoad.')
parser.add_argument('--size', help='Size of the search space.')
parser.add_argument('--algorithm', help='Format: \"[\'RLS\', \'OPOEA\']\"; Available algorithms: OPOEA, OPOEA_shift, OPOEA_resampling, OPOEA_alpha, RLS, LL, LL_opt, LL_shift, RLS_LL, LL_static, LL_dynamic_01, LL_dynamic_02')
parser.add_argument('--it', help='Number of iterations from the same algorithm.')
parser.add_argument('--steps')
parser.add_argument('--save')
parser.add_argument('--test')
parser.add_argument('--extra_name')
parser.add_argument('--random_seed')
parser.add_argument('--max_evaluation',type=float,default=-1)

# LL_static
parser.add_argument("--LL_static_lambda1")
parser.add_argument("--LL_static_lambda2")
parser.add_argument("--LL_static_lda")
parser.add_argument("--LL_static_crossOverBias")

# LL_static_02
parser.add_argument("--LL_static_02_lda")
parser.add_argument("--LL_static_02_alpha")
parser.add_argument("--LL_static_02_beta")

# LL_dynamic_01
parser.add_argument("--LL_dynamic_01_a")
parser.add_argument("--LL_dynamic_01_b")

# LL_dynamic_02
parser.add_argument("--LL_dynamic_02_alpha")
parser.add_argument("--LL_dynamic_02_beta")
parser.add_argument("--LL_dynamic_02_gamma")
parser.add_argument("--LL_dynamic_02_a")
parser.add_argument("--LL_dynamic_02_b")

# for LL algorithms
parser.add_argument("--crossover_choice",type=int,default=1)
parser.add_argument("--ioh_output",type=str,default=None)

#ioh_output = 0

#DEBUG
def mytest():
    global ioh_output
    print("test: " + str(ioh_output))


def main(argv):
    #get arguments
    args = parser.parse_args()
    if args.problem != None:
        problem = args.problem
    else:
        problem = "OneMax"
    if args.size != None:
        size = int(args.size)
    else:
        size = 100
    if args.algorithm != None:
        algorithm = eval(args.algorithm)
    else:
        algorithm = ["OPOEA"]
    if args.it != None:
        it = int(args.it)
    else:
        it = 1
    if args.steps != None:
        steps = int(args.steps)
    else:
        steps = int(size)
    if args.save != None:
        save = bool(args.save)
    else:
        save = False
    if args.test != None:
        test = bool(args.test)
    else:
        test = False
    if args.extra_name != None:
        extra_name = str(args.extra_name)
    else:
        extra_name = ""
    if args.random_seed != None:
        random_seed = int(args.random_seed)
        if it > 1:
            print("Error: it must be equal to 1 when random_seed is specified")
            return 1    
    else:
        random_seed = None
    crossover_choice = args.crossover_choice
    max_evaluation = int(args.max_evaluation)

    #global ioh_output
    ioh_output = args.ioh_output

    #DEBUG
    #print("args.ioh_output: " + str(args.ioh_output))
    #print("ioh_output: " + str(ioh_output))

    if 'LL_static' in algorithm:
        LL_static_lambda1 = int(args.LL_static_lambda1)
        LL_static_lambda2 = int(args.LL_static_lambda2)
        LL_static_lda = int(args.LL_static_lda)
        LL_static_crossOverBias = float(args.LL_static_crossOverBias)
    if 'LL_static_02' in algorithm:
        LL_static_02_lda = int(args.LL_static_02_lda)
        LL_static_02_alpha = int(args.LL_static_02_alpha)
        LL_static_02_beta = int(args.LL_static_02_beta)
    if 'LL_dynamic_01' in algorithm:
        LL_dynamic_01_a = float(args.LL_dynamic_01_a)
        LL_dynamic_01_b = float(args.LL_dynamic_01_b)
    if 'LL_dynamic_02' in algorithm:
        LL_dynamic_02_alpha = float(args.LL_dynamic_02_alpha)
        LL_dynamic_02_beta = float(args.LL_dynamic_02_beta)
        LL_dynamic_02_gamma = float(args.LL_dynamic_02_gamma)
        LL_dynamic_02_a = float(args.LL_dynamic_02_a)
        LL_dynamic_02_b = float(args.LL_dynamic_02_b)

    results = {}
    for alg in algorithm:
        results[alg] = record.Record()
       
    #import algorithms
    
    #mytest() #DEBUG

    if ioh_output is not None:
        if os.path.isfile(ioh_output):
            os.remove(ioh_output)
            with open(ioh_output,'wt') as f:
                f.write('')
    
    for i in range(it):
    #for i in tqdm(range(it)):
        print('Run number ' + str(i))
        
        #set the instance for given problem
        instance = eval('evaluate.setup_' + problem + '(size, problem)')

        if random_seed is not None:
            np.random.seed(random_seed)
        
        #initial solution
        initial_solution = Solution(utils.random_vector(size), None, None, 0)
        initial_solution.value = getattr(evaluate, problem)(initial_solution, instance, True)
        
        #Solve the problem
        for alg in algorithm:
            algFunc = getattr(algorithms,alg)
            
            if alg == 'LL_static':
                experiment = algFunc(initial_solution, instance, LL_static_lambda1, LL_static_lambda2, LL_static_lda, LL_static_crossOverBias, crossover_choice, max_evaluation, ioh_output)
            elif alg == 'LL_static_02':                
                experiment = algFunc(initial_solution, instance, LL_static_02_lda, LL_static_02_alpha, LL_static_02_beta, crossover_choice, max_evaluation, ioh_output)
            elif alg == 'LL_dynamic_01':
                experiment = algFunc(initial_solution, instance, LL_dynamic_01_a, LL_dynamic_01_b, crossover_choice, max_evaluation, ioh_output)               
            elif alg == 'LL_dynamic_02':
                experiment = algFunc(initial_solution, instance, LL_dynamic_02_alpha, LL_dynamic_02_beta, LL_dynamic_02_gamma, LL_dynamic_02_a, LL_dynamic_02_b, crossover_choice, max_evaluation, ioh_output)
            else:
                experiment = getattr(algorithms, alg)(initial_solution, instance)
            #print(alg)
            print(experiment[0])
            results[alg].insert_expriment(experiment)

         
            
    list_of_records = [results[alg] for alg in algorithm]
    if save:
        for (l,alg) in zip(list_of_records, algorithm):
            l.print_to_file(problem, size, alg, steps, extra_name)
            
    if test:
        for (l,alg) in zip(list_of_records, algorithm):
            l.plot_average(steps)        
        utils.compare(list_of_records, steps, algorithm)

    if it > 1:
        print("\n------------------- Summarised results ------------------")
        for alg in algorithm:            
            lsVals = [e[0] for e in results[alg].list_of_results]
            print(alg + ', mean: ' + str(results[alg].mean_opt_time))
            print(alg + ', min: ' + str(np.min(lsVals)))
            print(alg + ', max: ' + str(np.max(lsVals)))
            
    
    return 0

    
if __name__ == "__main__":
    print(' '.join(sys.argv))
    main(sys.argv[1:])
