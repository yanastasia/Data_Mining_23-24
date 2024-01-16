import random
import math

def read_city_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if not line.startswith("#")]

def read_distances(file_path):
    distances = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith("#"):
                distances.append(list(map(int, line.strip().split())))
    return distances

class Individual:
    def __init__(self, genes):
        self.genes = genes
        self.result = 0

    def find_result(self, distances):
        # Calculate the total distance of the route
        for i in range(len(self.genes) - 1):
            a = self.genes[i]
            b = self.genes[i + 1]
            self.result += distances[a][b]

def mutate(individual):
    # Swap two genes in the individual's route to introduce variation
    rand_gene1 = random.randint(0, len(individual.genes) - 1)
    rand_gene2 = random.randint(0, len(individual.genes) - 1)
    individual.genes[rand_gene1], individual.genes[rand_gene2] = individual.genes[rand_gene2], individual.genes[rand_gene1]

def cross(p1, p2, next_gen):
    # Perform crossover between two parents to generate two children
    stopper = random.randint(0, len(p1.genes) - 1)
    c1_genes = p1.genes[:stopper] + [g for g in p2.genes if g not in p1.genes[:stopper]]
    c2_genes = p2.genes[:stopper] + [g for g in p1.genes if g not in p2.genes[:stopper]]

    c1 = Individual(c1_genes)
    c2 = Individual(c2_genes)

    mutate(c1)
    mutate(c2)

    c1.find_result(distances)
    c2.find_result(distances)

    next_gen.extend([c1, c2])

def reproduce(population, next_gen):
    # Create the next generation through selection, crossover, and mutation
    init_size = len(population)
    while len(population) > init_size // 2:
        p1 = min(population, key=lambda x: x.result)
        population.remove(p1)
        p2 = min(population, key=lambda x: x.result)
        population.remove(p2)
        cross(p1, p2, next_gen)

def init_next_gen(population, next_gen):
    # Initialize the next generation
    population.extend(next_gen)
    next_gen.clear()

def print_individual(individual, city_names):
    # Print the result of the current best individual
    print("The shortest path is:")
    path = " -> ".join([city_names[city] for city in individual.genes])
    print(path)

    reversed_path = " -> ".join([city_names[city] for city in reversed(individual.genes)])
    print("\nReversed path is:")
    print(reversed_path)

    print("\nThe total distance is:")
    print(individual.result)

    print("\n|{:<20}|{:<20}|".format(city_names[individual.genes[0]], city_names[individual.genes[-1]]))
    for i in range(len(individual.genes) - 1):
        start_city = city_names[individual.genes[i]]
        end_city = city_names[individual.genes[i + 1]]
        print("|{:<20}|{:<20}|".format(start_city, end_city))
    print("|{:<20}|{:<20}|".format(city_names[individual.genes[-1]], city_names[individual.genes[0]]))
    print("|{:<20}|{:<20}|".format(individual.result, individual.result))

def main(N, max_iterations):
    global distances
    city_names = read_city_names("uk12_name.txt")
    distances = read_distances("uk12_dist.txt")

    # Ensure that the first city in uk12_name.txt is always the starting city
    initial_city = city_names[0]

    population = [Individual(random.sample(range(N), N)) for _ in range(10)]
    next_gen = []

    iter = 0
    best = None

    while iter <= max_iterations:
        if iter == 1 or iter == 8 or iter == 100 or iter == 1000 or iter == 5000 or iter == max_iterations:
            print("Iteration", iter, end=": ")
            best = min(population, key=lambda x: x.result)
            print_individual(best, city_names)

        reproduce(population, next_gen)
        init_next_gen(population, next_gen)
        iter += 1

    return best.result

if __name__ == "__main__":
    N = 12  # Number of cities in files
    max_iterations = 5000
    result = main(N, max_iterations)
    print("Shortest path:", result)

