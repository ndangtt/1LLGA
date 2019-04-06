This repository contains all data and results for the paper 
***Nguyen Dang, Carola Doerr (2019) Hyper-Parameter Tuning for the (1 + (λ, λ)) GA, accepted at GECCO 2019*** 
(an extended version with additional performance statistics is available on arxiv)

Structure:

* ```source-code```: source code of the (1 + (λ, λ)) GA algorithm used in the paper. This code is based upon previous work of Eduardo Carvalho Pinto.

* ```irace-and-fanova-results```: results obtained from
	- tuning experiments using the [irace](http://iridia.ulb.ac.be/irace/) software 
	- post analysis on the performance data returned by irace, using the *functional ANOVA (Hutter, Hoos and Leyton-Brown, 2014)* provided in the [PyImp](https://github.com/automl/ParameterImportance) package .

* ```test-performance```: performance of all configurations shown in the paper over 500 runs on each problem dimension. (The only exception is RLS, for which the results for n=20,000 and n=30,000 are based on 100 runs only.)

* ```heatpmaps```: heatmaps and the corresponding relevant performance data

* ```IOHProfiler-analyses```: data for [IOHProfiler](https://github.com/IOHprofiler) analyses. These files can be analyzed with the [IOHProfiler post-processing tool](http://iohprofiler.liacs.nl/) 
