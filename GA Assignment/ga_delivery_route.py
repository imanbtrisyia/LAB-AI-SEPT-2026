import random

# Distance matrix (symmetric, in kilometres)
LOCATIONS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
DISTANCE_MATRIX = {
    'A': {'A': 0, 'B': 4, 'C': 8, 'D': 6, 'E': 7, 'F': 9, 'G': 5},
    'B': {'A': 4, 'B': 0, 'C': 5, 'D': 7, 'E': 3, 'F': 8, 'G': 6},
    'C': {'A': 8, 'B': 5, 'C': 0, 'D': 4, 'E': 6, 'F': 3, 'G': 7},
    'D': {'A': 6, 'B': 7, 'C': 4, 'D': 0, 'E': 5, 'F': 6, 'G': 8},
    'E': {'A': 7, 'B': 3, 'C': 6, 'D': 5, 'E': 0, 'F': 4, 'G': 6},
    'F': {'A': 9, 'B': 8, 'C': 3, 'D': 6, 'E': 4, 'F': 0, 'G': 5},
    'G': {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 5, 'G': 0},
}

DEPOT = 'A'
DELIVERY_STOPS = ['B', 'C', 'D', 'E', 'F', 'G']


def calculate_route_distance(chromosome):
    """Calculate total distance starting at depot A, visiting all stops, and returning to A."""
    full_route = [DEPOT] + chromosome + [DEPOT]
    total_distance = 0
    for i in range(len(full_route) - 1):
        current_stop = full_route[i]
        next_stop = full_route[i + 1]
        total_distance += DISTANCE_MATRIX[current_stop][next_stop]
    return total_distance


def create_initial_population(pop_size):
    """Generate an initial population of valid random permutations of delivery stops."""
    population = []
    for _ in range(pop_size):
        route = DELIVERY_STOPS[:]
        random.shuffle(route)
        population.append(route)
    return population


def tournament_selection(population, tournament_size=3):
    """Select the best route from a random subset of the population."""
    candidates = random.sample(population, tournament_size)
    return min(candidates, key=calculate_route_distance)


def order_crossover(parent1, parent2):
    """Order Crossover (OX1) to create a valid child without duplicate or missing stops."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size

    # Copy slice from parent1
    child[start:end + 1] = parent1[start:end + 1]

    # Fill remaining positions with unused stops from parent2 in order
    p2_remaining = [stop for stop in parent2 if stop not in child]
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            child[i] = p2_remaining[p2_index]
            p2_index += 1

    return child


def swap_mutation(chromosome, mutation_rate=0.2):
    """Randomly swap two delivery locations in the route based on mutation rate."""
    mutated = chromosome[:]
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated


def run_genetic_algorithm(
    seed=42,
    pop_size=30,
    generations=100,
    crossover_rate=0.85,
    mutation_rate=0.2,
    elitism_count=2
):
    """Run the Genetic Algorithm to find the shortest delivery route."""
    random.seed(seed)
    population = create_initial_population(pop_size)

    best_chromosome = min(population, key=calculate_route_distance)
    best_distance = calculate_route_distance(best_chromosome)

    for gen in range(1, generations + 1):
        # Sort population by distance (ascending: shorter distance = better fitness)
        population.sort(key=calculate_route_distance)

        # Elitism: preserve the top routes unchanged
        next_population = [route[:] for route in population[:elitism_count]]

        # Generate remaining offspring
        while len(next_population) < pop_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]

            child = swap_mutation(child, mutation_rate)
            next_population.append(child)

        population = next_population

        # Track overall best route
        current_best = min(population, key=calculate_route_distance)
        current_distance = calculate_route_distance(current_best)
        if current_distance < best_distance:
            best_chromosome = current_best[:]
            best_distance = current_distance

    full_best_route = [DEPOT] + best_chromosome + [DEPOT]
    return full_best_route, best_distance


if __name__ == "__main__":
    best_route, min_distance = run_genetic_algorithm(
        seed=42,
        pop_size=30,
        generations=100,
        crossover_rate=0.85,
        mutation_rate=0.2,
        elitism_count=2
    )

    print("=== Genetic Algorithm Delivery Route Optimisation ===")
    print(f"Random Seed      : 42")
    print(f"Population Size  : 30")
    print(f"Generations      : 100")
    print(f"Best Route Found : {' -> '.join(best_route)}")
    print(f"Total Distance   : {min_distance} km")