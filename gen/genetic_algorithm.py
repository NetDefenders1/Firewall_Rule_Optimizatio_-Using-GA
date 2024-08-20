import pygad
import numpy as np
from deap import base, creator, tools, algorithms
from fitness_functions import pygad_fitness, deap_fitness

def pygad_genetic_algorithm(rules, constraints, population_size, generations, mutation_rate, progress_bar):
    def fitness_function(ga_instance, solution, solution_idx):
        return pygad_fitness(ga_instance, solution, solution_idx, constraints, rules)

    ga_instance = pygad.GA(
        num_generations=generations,
        num_parents_mating=population_size // 2,
        fitness_func=fitness_function,
        sol_per_pop=population_size,
        num_genes=len(rules),
        mutation_percent_genes=int(mutation_rate * 100),
        on_generation=lambda ga_instance: progress_bar.progress(ga_instance.generations_completed / ga_instance.num_generations)
    )
    ga_instance.run()
    return ga_instance.best_solution(), ga_instance.population

def deap_genetic_algorithm(population, constraints, population_size, generations, mutation_rate, rules):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attribute", np.random.permutation, len(rules))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attribute)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", deap_fitness, constraints=constraints, rules=rules)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutation_rate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=population_size)
    fitness_values = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitness_values):
        ind.fitness.values = fit

    for gen in range(generations):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if np.random.rand() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if np.random.rand() < mutation_rate:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitness_values = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitness_values):
            ind.fitness.values = fit

        population[:] = offspring

    return tools.selBest(population, 1)[0], population

def sgg_ga(rules, constraints, population_size, generations, mutation_rate, progress_bar):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attribute", np.random.permutation, len(rules))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attribute)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", deap_fitness, constraints=constraints, rules=rules)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutation_rate)
    toolbox.register("select", tools.selBest)

    population = toolbox.population(n=population_size)
    fitness_values = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitness_values):
        ind.fitness.values = fit

    for gen in range(generations):
        for ind in population:
            offspring = toolbox.clone(ind)
            if np.random.rand() < mutation_rate:
                toolbox.mutate(offspring)
                del offspring.fitness.values
            if not offspring.fitness.valid:
                offspring.fitness.values = toolbox.evaluate(offspring)
            if offspring.fitness > ind.fitness:
                ind[:] = offspring[:]
        progress_bar.progress(gen / generations)

    return tools.selBest(population, 1)[0], population

def plus_ga(rules, constraints, population_size, generations, mutation_rate, progress_bar):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attribute", np.random.permutation, len(rules))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attribute)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", deap_fitness, constraints=constraints, rules=rules)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutation_rate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=population_size)
    fitness_values = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitness_values):
        ind.fitness.values = fit

    for gen in range(generations):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if np.random.rand() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if np.random.rand() < mutation_rate:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitness_values = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitness_values):
            ind.fitness.values = fit

        population[:] = toolbox.select(population + offspring, population_size)
        progress_bar.progress(gen / generations)

    return tools.selBest(population, 1)[0], population

def combined_genetic_algorithm(rules, constraints, population_size, generations, mutation_rate, progress_bar):
    pygad_best_ordering, pygad_population = pygad_genetic_algorithm(rules, constraints, population_size, generations, mutation_rate, progress_bar)
    sgg_best_ordering, sgg_population = sgg_ga(rules, constraints, population_size, generations, mutation_rate, progress_bar)
    plus_best_ordering, plus_population = plus_ga(rules, constraints, population_size, generations, mutation_rate, progress_bar)
    return sgg_best_ordering, plus_best_ordering
