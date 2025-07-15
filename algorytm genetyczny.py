import random
import pandas as pd

items = [(97, 13), (86, 76), (81, 76), (23, 92), (51, 97), (9, 40), (97, 27), (6, 4), (89, 71), (44, 12),   (1, 15), (77, 90), (40, 27), (22, 52), (56, 4), (3, 36), (88, 67), (84, 2), (61, 63), (93, 80)]


items = pd.DataFrame(items, columns=['weight', 'value'])
items.index.name = "items"

total_weight_limit = 200
genome = [random.randint(0, 5) == 0 for _ in range(len(items))]

def create_population(population_size: int):
    return [[random.randint(0, 5) == 0 for _ in range(len(items))] for _ in range(population_size)]

def fitness(genes: list):
    total_weight = 0
    total_value = 0
    for idx, gene in enumerate(genes):
        if gene:
            total_weight += items["weight"][idx]
            total_value += items["value"][idx]

    if total_weight > total_weight_limit:
        return 0
    else:
        return total_value

def select_winners(population: list):
    population_values = []
    for genes in population:
        value = fitness(genes=genes)
        if value > 0:
            population_values.append((value, genes))

    return [genes for value, genes in sorted(population_values, key=lambda x: x[0], reverse=True)]

def select_best(winners: list, population: list, percentage=0.2):
    limit = int(percentage * len(population))
    if len(winners) > limit:
        best = winners[:limit]
    else:
        best = winners
    return best

def crossover(genes1: list, genes2: list):
    crossover_point = random.randint(1, len(genes1) - 1)
    new_genes = genes1[:crossover_point] + genes2[crossover_point:]
    return new_genes

def mutate(genes: list):
    new_genes = list(genes)
    idx = random.randint(0, len(genes) - 1)
    new_genes[idx] = not bool(genes[idx])
    return new_genes

def random_mutation(genes: list, probability: int = 100):
    if random.randint(0, probability) == 0:
        return mutate(genes)
    else:
        return list(genes)

def next_generation(population: list):
    new_population = []
    winners = select_winners(population)

    if len(winners) > 0:
        winners = select_best(winners, population, 0.2)
        for _ in range(len(population)):
            new_genes = crossover(random.choice(winners), random.choice(winners))
            new_population.append(random_mutation(new_genes))
    else:
        new_population = create_population(len(population))

    return new_population

population = create_population(1000)
for i in range(20):
    new_population = next_generation(population)
    population = new_population

results = pd.concat([pd.DataFrame(population).mean() * 100, items], axis=1)
results.columns = ["selection_percentage"] + list(items.columns)
results.index.name = items.index.name
print(results)