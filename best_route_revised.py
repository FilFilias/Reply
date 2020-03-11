#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Nov 18 17:50:54 2019

@author: filip
"""


import matplotlib.pyplot as plt
#_________PLANO_________#
# 1-- FTIAXNW FUNCTION POY NA MOY DINEI TON XARTH
# 2-- FTIAXNW FUNCTION POY NA MOY FTIAXNEI POREIES
# 3-- FTIAXNW FUNCTION POY NA MOY FTIAXNEI ARXIKO PLHTHYSMO
# 4-- FTIAXNW FUNCTION GIA FITNESS
# 5-- FTIAXNW FUNCTION GIA SELECTION
# 6-- FTIAXNW FUNCTION GIA CROSSOVER
# 7-- FTIAXNW FUNCTION GIA MUTATION
import numpy as np
import pandas as pd
import seaborn as sns

"""
          ______________________________________________________
         |_________________________NEW MAP______________________|
                                                                    """

# FUNCTION POU SKIAGRAFEI TON XARTH.KATHE INDEX TOY PINAKA NxN EINAI KAI MIA POLH KAI
# KATHE STOIXEIO X_ij MOY DINEI THN APOSTASH THS POLHS I APO THN POLH J.OSES POLEIS DEN
# SYNDEONTAI METAXY TOYS EXOYN X_ij=0.EPISHS,O PINAKAS EINAI SYMMETRIKOS KATHWS H
# APOSTASH APO THN POLH I STHN POLH J EINAI IDIA ME THN APOSTASH APO THN J STHN I


def the_map(N):
    my_map = np.zeros((N, N))
    for i in range(N):
        for j in range(i):
            my_map[i][j] = np.random.random()
            my_map[j][i] = my_map[i][j]
    return my_map


"""
          ________________________________________________________
         |_________________________NEW ROUTE______________________|
                                                                   """
# Function poy dhmioyrgeia poreies oi opoies exoyn ws shmeio ekkinhshs to 0
# kai termatismo to shmeio N.


def route(my_map):
    that_map = my_map.copy()
    my_route = np.zeros(1)
    possible_values = possible_values = np.nonzero(that_map[0])
    possible_values = np.delete(possible_values, -1)
    for i in range(len(my_map) - 2):
        next_stop = np.random.choice(possible_values)
        my_route = np.append(my_route, next_stop)
        possible_values = np.delete(possible_values, np.argwhere(possible_values == next_stop))
    my_route = np.append(my_route, len(that_map) - 1)
    return my_route


"""
          _____________________________________________________________
         |_________________________INITIALIZATION______________________|
                                                                    """
# Function pou moy dinei san arxiko plhthysmo ena set diadromwn


def initialization(pop_size, my_map):
    population = []
    for i in range(pop_size):
        population.append(route(my_map))
    return population


"""
          ______________________________________________________
         |_________________________FITNESS______________________|
                                                                    """
# Function poy pairnei kathe diadromh kai ypologizei posa synolika xiliometra
# tha dianysei opoios thn akoloythisei


def fitness(my_route, my_map):
    score = 0
    for i in range(len(my_route) - 1):
        score = score + my_map[int(float(my_route[i]))][int(float(my_route[i + 1]))]
    if len(np.unique(my_route)) != len(my_map[0]):
        score = 2 * score
    if (my_route[0] != 0) or (my_route[-1] != len(my_map) - 1):
        score = 10000000
    return score


"""
         ________________________________________________________
        |_________________________CROSSOVER______________________|
                                                                    """
# Function poy kanei diastayrwsh dyo stoixeiwn.H diastayrwsh ginetai epilegontas
# ena apo ta koina shmeia twn dyo diadromwn kai diastayrwnwntas ta stoixeia apo
# to shmeio ekeino kai pera.


def crossover(chrom_1, chrom_2):
    new_chrom = []
    k = np.random.random()
    r = np.random.randint(1, len(chrom_2) - 2)
    if k < 0.5:
        new_chrom = np.append(chrom_1[:r], chrom_2[r:])
    else:
        new_chrom = np.append(chrom_2[:r], chrom_2[r:])
    return new_chrom


"""
          ________________________________________________________
         |_________________________MUTATION______________________|
                                                                    """
# Function poy kanei metallaxh se mia diadromh.Briskei to shmeio poy ginetai
# h metallaxh kai apo ekei kai pera dhmioyrgei nea diadromh.H telikh diadromh
# (metallagmenh) einai idia me thn arxikh ews to shmeio poy egine h metallaxh
# kai kainoyrgia apo ekei kai pera


def mutation(chrom, pm):
    for i in range(1, len(chrom) - 1):
        r = np.random.random()
        if r <= pm:
            chrom[i] = np.random.randint(0, len(chrom))
    return chrom


"""
          ___________________________________________________________
         |_______________Sort_Population_By_Fitness__________________|
                                                                   """


def sort_pop(pop, my_map):
    pop_sorted = {"route": [], "fitness": []}
    for item in pop:
        pop_sorted["route"].append(item)
        pop_sorted["fitness"].append(fitness(item, my_map))
    pop_sorted = pd.DataFrame(data=pop_sorted)
    # Lower index -> fitter
    pop_sorted.sort_values(by=["fitness"], inplace=True, ascending=True)
    return pop_sorted["route"].tolist(), pop_sorted["fitness"].tolist()


"""
          ___________________________________________________________
         |__________________Pop_Best_Chrom___________________________|
                                                                         """


def best(pop, my_map):
    pop_sorted, pop_fitness = sort_pop(pop, my_map)
    return pop_sorted[0], pop_fitness[0]


"""
          ___________________________________________________________
         |______________________MAIN_FUNCTION________________________|
                                                                    """


def main(N, pop_size, pm, iterations):

    # Bazoyme mia poly megalh diadromh ws kalyterh prokeimenoy na antikatastathei
    # apo thn prwth poy tha ftiaxtei.

    best_of_all = 1000000000
    best_route_of_all = []
    best_of_all_before = 0
    # Dhmeioyrgeia xarth

    my_map = the_map(N)

    # Dhmioyrgeia arxikoy plhthysmoy (diadromwn)

    current_population = initialization(pop_size, my_map)

    # To k einai to "shma" poy tha dwsei o algorythmos etsi wste an gia 20
    # synexomenes genies den exei brethei kalyterh diadromh na termatistei
    # h anazhthsh.Kathe fora poy brisketai kainoyrgia diadromh to k
    # pairnei ek neoy thn timh 0.

    # Epanalhpsh twn bhmatwn mexri na ginei o megistos arithmos epanalhpsewn h
    # na perasoun 20 genies xwris na brethei kalyterh diadromh
    k = 0
    for it in range(iterations):
        new_pop = current_population[:pop_size]
        for i in range(0, np.int(len(new_pop) * 0.15)):
            # Use top 15% to replace bottom 15%
            new_pop[len(new_pop) - i - 1] = crossover(new_pop[i], new_pop[i + 1])
        for i in range(len(new_pop)):
            # Replace every pop with a mutation of itself
            new_pop[i] = mutation(new_pop[i], pm)
        best_route, best_route_score = best(new_pop, my_map)
        if best_of_all > best_route_score:
            best_of_all = best_route_score
            best_route_of_all = best_route

        new_pop, new_pop_fitness = sort_pop(new_pop, my_map)

        current_population = new_pop.copy()

        # if best_of_all == best_of_all_before:
        #     k = k + 1
        # else:
        #     best_of_all_before = best_of_all
        #     k = 0
        # Apeikonhsh ths diadromhs
        print("Number of iteration:", it)
        print("Best score so far:", best_of_all)
        print("Number of stops:", len(best_route_of_all))
        print("Current population:", len(current_population))

        # if k == 20:
        #     break
    ax = sns.heatmap(my_map)
    x = [0.5] + [x + 0.5 for x in best_route_of_all[0:len(best_route_of_all) - 1]] + [len(my_map) - 0.5]
    y = [0.5] + [x + 0.5 for x in best_route_of_all[1:len(best_route_of_all)]] + [len(my_map) - 0.5]
    plt.plot(x, y, marker='o', linewidth=4, markersize=12, linestyle="-", color='white')
    plt.show()

    return current_population, my_map


pp, mm = main(15, 150, 0.05, 2000)
