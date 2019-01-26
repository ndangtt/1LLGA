This repository contains all data and results for the paper ***Hyper-Parameter Tuning for the (1 + (λ, λ)) GA***

Structure:

* ```source-code```: source code of the (1 + (λ, λ)) GA algorithm used in the paper

* ```irace-and-fanova-results```: results obtained from
	- tuning experiments using the [irace](http://iridia.ulb.ac.be/irace/) software 
	- post analysis on the performance data returned by irace, using the *functional ANOVA (Hutter, Hoos and Leyton-Brown, 2014)* provided in the [PyImp](https://github.com/automl/ParameterImportance) package .

* ```test-performance```: performance of all configurations shown in the paper over 500 runs on each problem dimension. Notes that for RLS, results for n=20,000 and n=30,000 are on 100 runs only.

* ```heapmaps```: heatmaps and the corresponding relevant performance datassssss

* ```IOHProfiler-analyses```: data for [IOHProfiler](http://iohprofiler.liacs.nl/) analyses 
