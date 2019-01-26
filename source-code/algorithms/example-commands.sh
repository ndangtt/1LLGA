#python2 main.py --problem OneMax --size 500 --algorithm "['LL_static']" --LL_static_lambda1 4 --LL_static_lambda2 4 --LL_static_lda 4 --LL_static_crossOverBias 0.25 --crossover_choice 2 --random_seed 123

#python2 main.py --problem OneMax --size 500 --algorithm "['LL_static_02']" --LL_static_02_lda 4 --LL_static_02_alpha 1 --LL_static_02_beta 1 --it 20 --crossover_choice 1

#python2 main.py --problem OneMax --size 500 --algorithm "['LL_dynamic_01']" --LL_dynamic_01_a 1.5 --LL_dynamic_01_b 0.5 --crossover_choice 1 --random_seed 123

python2 main.py --problem OneMax --size 500 --algorithm "['LL_dynamic_02']" --LL_dynamic_02_alpha 1.0 --LL_dynamic_02_beta 1.0 --LL_dynamic_02_gamma 1.0 --LL_dynamic_02_a 1.1 --LL_dynamic_02_b 0.7 --crossover_choice 1 --random_seed 123 --ioh_output ioh.out

#python2 main.py --problem OneMax --size 10000 --algorithm "['LL_dynamic_02']" --random_seed 154580985 --max_evaluation 2000 --LL_dynamic_02_alpha 6.515 --LL_dynamic_02_beta 4 --LL_dynamic_02_gamma 3.2044 --LL_dynamic_02_a 1.9748 --LL_dynamic_02_b 0.4837
