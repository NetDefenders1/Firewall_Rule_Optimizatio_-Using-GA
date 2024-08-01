def pygad_fitness(ga_instance, solution, solution_idx, constraints, rules):
    rule_positions = {tuple(rules[int(i)].items()): idx for idx, i in enumerate(solution)}
    fitness = 0
    for rule1, rule2 in constraints:
        rule1_tuple = tuple(rule1.items())
        rule2_tuple = tuple(rule2.items())
        if rule1_tuple not in rule_positions or rule2_tuple not in rule_positions:
            continue
        if rule_positions[rule1_tuple] < rule_positions[rule2_tuple]:
            fitness += 1
    return fitness

def deap_fitness(individual, constraints, rules):
    rule_positions = {tuple(rules[int(i)].items()): idx for idx, i in enumerate(individual)}
    fitness = 0
    for rule1, rule2 in constraints:
        rule1_tuple = tuple(rule1.items())
        rule2_tuple = tuple(rule2.items())
        if rule1_tuple not in rule_positions or rule2_tuple not in rule_positions:
            continue
        if rule_positions[rule1_tuple] < rule_positions[rule2_tuple]:
            fitness += 1
    return fitness,
