import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rc('xtick', labelsize=40) 
matplotlib.rc('ytick', labelsize=40) 
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 30}
axis_font = {'size':'30'}
matplotlib.rc('font', **font)
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from math import *

linestyles = ['solid', 'dashed', 'dashdot', 'dotted', '-', '--', '-.', ':']
markers = ['d' , '^' , 'o', 's', 'p', 'd', '*' ]
algos_dict = {
    'RLS': r'~RLS',
    'RLS_opt_OM': r'~RLS$_{opt,OM}$',
    'OPOEA': r'$(1 + 1)$~EA',
    'OPOEA_resampling': r'$(1 + 1)$~EA$_{>0}$',
    'OPOEA_alpha': r'$(1 + 1)$~EA$_{\alpha}$',
    'OPOEA_alpha_mod': r'$(1 + 1)$~EA$_{\alpha,mod}$',
    'OPOEA_opt_LO': r'$(1 + 1)$~EA$_{opt, LO}$',
    'OPOEA_shift': r'$(1 + 1)$~EA$_{0 \rightarrow 1}$',
    'LL': r'$(1 + (\lambda, \lambda))$~GA',
    'LL_opt': r'$(1 + (\lambda,\lambda))$~GA$_{mod}$',
    'LL_mod': r'$(1 + (\lambda,\lambda))$~GA$_{mod_2}$',
    'LL_alpha': r'$(1 + (\lambda,\lambda))$~GA$_{\alpha}$',
    'TPOEA': r'$(2+1)$~GA',
    'TPOEA_resampling': r'$(2+1)$~GA$_{mod,p=0.77\dots/n}$',
    'TPOEA_resampling_2': r'$(2+1)$~GA$^2_{mod}$',
    'TPOEA_1_p1sqrt5o2': r'$(2+1)$~GA$_{mod,p=(1+\sqrt{5})/(2n)}$',
    'RLS_opt_LO': r'~RLS$_{opt,LO}$'
}

def regression(x,y,xaxis = 'n', yaxis = 'Length'):
    colors = ['k', 'b', 'c', 'g', 'r', 'm', 'y']
    c = 0

    for i in range(len(x)):
        x[i] = np.reshape(x[i], (len(x[i]),1))
    
    for j in range(len(y)):
        y[j] = np.reshape(y[j], (len(x[j]),1))


    xmin = min(x[0])
    xmax = max(x[0])
    ymin = min(y[0])
    ymax = max(y[0])
    
    for (u,v) in zip(x,y):
        #Update the global minimum and maximum
        local_xmin = min(u)
        local_xmax = max(u)
        local_ymin = min(v)
        local_ymax = max(v)
        if local_xmin < xmin:
            xmin = local_xmin
        if local_xmax > xmax:
            xmax = local_xmax
        if local_ymin < ymin:
            ymin = local_ymin
        if local_ymax > ymax:
            ymax = local_ymax

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(u, v)

        # The coefficients
        print('Coefficients: \n', regr.coef_)

        # Plot outputs
        plt.scatter(u, v,  color=colors[c])
        plt.plot(u, regr.predict(u), color=colors[c%7], linewidth=2)
        c += 1

        #plt.xticks(())
        #plt.yticks(())
        eq = 'y = ' + str("%.2f" % regr.coef_[0][0]) + 'x + ' + str("%.2f" % regr.intercept_[0]) 
        plt.annotate(eq, xy=(u[-1] - 1, v[-1] + 1))
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        
    plt.axis([0.85*xmin,1.15*xmax, 0.85*ymin, 1.15*ymax])
    plt.grid()
    plt.show()

def scatter(x,y,xaxis = 'n', yaxis = 'Length', labels = None, s = 100):
    colors = ['k', 'b', 'c', 'g', 'r', 'm', 'y'] 
    c = 0
    
    for i in range(len(x)):
        x[i] = np.reshape(x[i], (len(x[i]),1))


    for j in range(len(y)):
        y[j] = np.reshape(y[j], (len(x[j]),1))


    xmin = min(x[0])
    xmax = max(x[0])
    ymin = min(y[0])
    ymax = max(y[0])
        
    
    for (u,v) in zip(x,y):
        #Update the global minimum and maximum
        local_xmin = min(u)
        local_xmax = max(u)
        local_ymin = min(v)
        local_ymax = max(v)
        if local_xmin < xmin:
            xmin = local_xmin
        if local_xmax > xmax:
            xmax = local_xmax
        if local_ymin < ymin:
            ymin = local_ymin
        if local_ymax > ymax:
            ymax = local_ymax
        
        # Plot outputs
        if labels[c] in algos_dict:
            label = algos_dict[labels[c]]
        else:
            label = r'$' + labels[c] + '$'
        plt.scatter(u, v,  color=colors[c%7], label=label, s=s, marker=markers[c%7])
        c += 1
        
    #plt.xticks(())
    #plt.yticks(())
    plt.xlabel(xaxis, **axis_font)
    plt.ylabel(yaxis, **axis_font)

    plt.axis([0.85*xmin,1.15*xmax, 0.85*ymin, 1.15*ymax])
    plt.legend(loc='upper left', shadow=True, fontsize='x-large')
    #plt.grid()
    plt.show()

def line_plot(x,y, xaxis = 'n', yaxis = 'Length', labels = None):
    colors = ['k', 'b', 'c', 'g', 'r', 'm', 'y'] 
    c = 0
    
    for i in range(len(x)):
        x[i] = np.reshape(x[i], (len(x[i]),1))


    for j in range(len(y)):
        y[j] = np.reshape(y[j], (len(x[j]),1))


    xmin = min(x[0])
    xmax = max(x[0])
    ymin = min(y[0])
    ymax = max(y[0])
        
    
    for (u,v) in zip(x,y):
        #Update the global minimum and maximum
        local_xmin = min(u)
        local_xmax = max(u)
        local_ymin = min(v)
        local_ymax = max(v)
        if local_xmin < xmin:
            xmin = local_xmin
        if local_xmax > xmax:
            xmax = local_xmax
        if local_ymin < ymin:
            ymin = local_ymin
        if local_ymax > ymax:
            ymax = local_ymax
        
        # Plot outputs
        plt.plot(u, v, color=colors[c%7], label = algos_dict[labels[c]], linestyle = linestyles[c%7], linewidth = 2.0)
        c += 1
        
        #plt.xticks(())
        #plt.yticks(())
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)

    plt.axis([0.85*xmin,1.15*xmax, 0.85*ymin, 1.15*ymax])
    #plt.grid()
    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.show()

    
def line_plot_error(x,y, error, xaxis = 'n', yaxis = 'Length'):
    colors = ['k', 'b', 'c', 'g', 'r', 'm', 'y'] 
    c = 0
        
    for i in range(len(x)):
        x[i] = np.reshape(x[i], (len(x[i]),1))


    for j in range(len(y)):
        y[j] = np.reshape(y[j], (len(x[j]),1))


    xmin = min(x[0])
    xmax = max(x[0])
    ymin = min(y[0])
    ymax = max(y[0])
        
    
    for (u,v,e) in zip(x,y,error):
        #Update the global minimum and maximum
        local_xmin = min(u)
        local_xmax = max(u)
        local_ymin = min(v)
        local_ymax = max(v)
        if local_xmin < xmin:
            xmin = local_xmin
        if local_xmax > xmax:
            xmax = local_xmax
        if local_ymin < ymin:
            ymin = local_ymin
        if local_ymax > ymax:
            ymax = local_ymax
        
        # Plot outputs
        
        plt.errorbar(u.flatten(), v.flatten(), yerr=e.flatten(), fmt = 'o')
        c += 1
        
        #plt.xticks(())
        #plt.yticks(())
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)

    plt.axis([0.85*xmin,1.15*xmax, 0.85*ymin, 1.15*ymax])
    #plt.grid()
    plt.show()
