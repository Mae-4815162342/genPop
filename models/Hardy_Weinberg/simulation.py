import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
import ipywidgets as iw

#Hardy-Weinberg
def simulate_HW(p, pop, gens):
    
    # inits
    frequences = np.zeros((gens, 3))
    new_p = p
    
    # run generations
    for gen in range(gens):
        current_pop = np.zeros(3)
        
        # run population
        for x in range(pop):
            
            # allele 1
            allele_1 = 0
            n = random.random()
            if n > p:
                allele_1 = 1
                
            # allele 2
            allele_2 = 0
            m = random.random()
            if m > p:
                allele_2 = 1
            
            # add to population
            current_pop[allele_1 + allele_2] += 1
        
        frequences[gen] = current_pop/pop
        
        # compute new p
        new_p = (current_pop[0] + current_pop[1] / 2) / pop
    return frequences    


pop = 10000
gens = 20
p_it = 20

p_results = np.zeros((p_it - 1, gens, 3))
for p_mille in range(1, p_it):
    p = p_mille / p_it
    
    res = simulate_HW(p, pop, gens)
    p_results[p_mille - 1] = res


def plot_sumup(gen):
    title = 'Genotypes frequences after ' + str(gen) + ' generations'
    plt.title(title)
    plt.xlabel('p')
    plt.ylabel('genotype frequence')
    for p_mille in range(1, p_it):
        p = p_mille / p_it
        plt.scatter(p, p_results[p_mille - 1][gen - 1][0], color='b', label='AA')
        plt.scatter(p, p_results[p_mille - 1][gen - 1][1], color='r', label='Aa')
        plt.scatter(p, p_results[p_mille - 1][gen - 1][2], color='g', label='aa')
    plt.axvline(0.5, label='x=0.5', color='red', linestyle='dashed')
    plt.axhline(0.25, label='y=0.25', linestyle='dashed')
    ax = plt.gca()  
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    plt.legend(handle_list, label_list)
    
iw.interact(plot_sumup, gen=(1,gens))  

def plot_results(p, gen):
    plt.title('Genotype frequences for p=' + str(round(p, 2)) + ' after ' + str(gen) + ' generations')
    plt.bar(['AA', 'Aa', 'aa'], p_results[math.floor(p*p_it) - 1][gen - 1], color=['b', 'r', 'g'])
    
iw.interact(plot_results, p=(1/p_it, (p_it - 1)/p_it), gen=(1,gens))