import random

class Individual:
    def __init__(self, genes):
        self.genes = genes
        self.value = 0
        self.weight = 0

def fitness(individual, items, max_weight):
    total_value = 0
    total_weight = 0

    for i in range(len(individual.genes)):
        if individual.genes[i] == 1:
            total_value += items[i][1]
            total_weight += items[i][0]

    if total_weight > max_weight:
        return 0
    else:
        individual.value = total_value
        individual.weight = total_weight
        return total_value

def print_best_value(generation, best_value):
    print(f"Generation {generation}, Best Value: {best_value}")

def read_input(file_path):
    with open(file_path, 'r') as file:
        M, N = map(int, file.readline().split())
        items = [list(map(int, file.readline().split())) for _ in range(N)]
    return M, N, items

def genetic_algorithm(M, N, items, max_iterations):
    population_size = 10
    mutation_rate = 0.1
    max_weight = M

    population = [Individual([random.randint(0, 1) for _ in range(N)]) for _ in range(population_size)]

    for generation in range(1, max_iterations + 1):
        population.sort(key=lambda x: fitness(x, items, max_weight), reverse=True)
        best_value = fitness(population[0], items, max_weight)
        print_best_value(generation, best_value)

        next_gen = []

        for _ in range(population_size // 2):
            parent1 = random.choice(population[:population_size // 2])
            parent2 = random.choice(population[:population_size // 2])

            crossover_point = random.randint(0, N - 1)
            child1 = Individual(parent1.genes[:crossover_point] + parent2.genes[crossover_point:])
            child2 = Individual(parent2.genes[:crossover_point] + parent1.genes[crossover_point:])

            if random.random() < mutation_rate:
                mutation_point = random.randint(0, N - 1)
                child1.genes[mutation_point] = 1 - child1.genes[mutation_point]
                child2.genes[mutation_point] = 1 - child2.genes[mutation_point]

            next_gen.extend([child1, child2])

        population = next_gen

    return best_value

if __name__ == "__main__":
    file_path = "KP short test data.txt"
    M, N, items = read_input(file_path)
    max_iterations = 10

    # Note: Optimal knapsack values are 1130 and 5119 for the provided datasets.
    result = genetic_algorithm(M, N, items, max_iterations)
    print(result)
