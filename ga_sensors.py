import random
import math

# -------------------------
# Problem parameters
# -------------------------
WIDTH = 20          # building width (x)
HEIGHT = 10         # building height (y)
NUM_SENSORS = 8     # how many sensors to place
RADIUS = 3          # coverage radius (cells)
ALPHA = 5.0         # cost weight (0 = ignore cost)

# -------------------------
# GA parameters
# -------------------------
POP_SIZE = 40       # how many candidate solutions per generation
GENERATIONS = 50    # how many generations to evolve
CROSS_RATE = 0.9    # probability of crossover
MUT_RATE = 0.1      # probability of mutating each sensor
TOURNAMENT_K = 3    # tournament size for selection


# -------------------------
# Helper: create a random individual
# -------------------------
def random_individual():
    """
    One individual = one sensor placement solution.
    Represented as a dict with:
      - 'sensors': list of (x, y) tuples
      - 'fitness': float
    """
    sensors = []
    for _ in range(NUM_SENSORS):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        sensors.append((x, y))
    return {"sensors": sensors, "fitness": None}


# -------------------------
# Compute coverage grid for one individual
# -------------------------
def compute_coverage_grid(individual):
    """
    Returns a 2D list 'grid[y][x]' = True if covered, False otherwise.
    """
    # initialize all False
    grid = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for (sx, sy) in individual["sensors"]:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - sx
                dy = y - sy
                if dx*dx + dy*dy <= RADIUS * RADIUS:
                    grid[y][x] = True
    return grid


# -------------------------
# Fitness function
# -------------------------
def compute_fitness(individual):
    """
    Fitness = coverage_score - ALPHA * sensor_cost
    coverage_score = number of covered cells
    sensor_cost = number of sensors (simple version)
    """
    grid = compute_coverage_grid(individual)

    covered = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x]:
                covered += 1

    coverage_score = covered
    sensor_cost = len(individual["sensors"])

    fitness = coverage_score - ALPHA * sensor_cost
    individual["fitness"] = fitness
    return fitness


# -------------------------
# Selection: tournament
# -------------------------
def tournament_selection(population):
    """
    Pick TOURNAMENT_K random individuals and return the best among them.
    """
    candidates = random.sample(population, TOURNAMENT_K)
    best = max(candidates, key=lambda ind: ind["fitness"])
    return best



# Individual tournamentSelection(const vector<Individual>& population) {
#     vector<Individual> candidates;
#     for(int i = 0; i < TOURNAMENT_K; i++) {
#         int idx = rand() % population.size();
#         candidates.push_back(population[idx]);
#     }

#     // find max fitness
#     Individual best = candidates[0];
#     for(auto &ind : candidates) {
#         if(ind.fitness > best.fitness)
#             best = ind;
#     }
#     return best;
# }



# -------------------------
# Crossover: one-point
# -------------------------
def crossover(parent1, parent2):
    """
    Combine sensors list of parents to make two children.
    """
    if random.random() > CROSS_RATE:
        # no crossover, just copy
        return (
            {"sensors": parent1["sensors"][:], "fitness": None},
            {"sensors": parent2["sensors"][:], "fitness": None},
        )

    point = random.randint(1, NUM_SENSORS - 1)

    child1_sensors = parent1["sensors"][:point] + parent2["sensors"][point:]
    child2_sensors = parent2["sensors"][:point] + parent1["sensors"][point:]

    child1 = {"sensors": child1_sensors, "fitness": None}
    child2 = {"sensors": child2_sensors, "fitness": None}
    return child1, child2


# -------------------------
# Mutation: random reposition
# -------------------------
def mutate(individual):
    """
    For each sensor, with probability MUT_RATE, move it to a random position.
    """
    sensors = individual["sensors"]
    new_sensors = []
    for (x, y) in sensors:
        if random.random() < MUT_RATE:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
        new_sensors.append((x, y))
    individual["sensors"] = new_sensors
    # fitness will be recomputed later


# -------------------------
# Run the genetic algorithm
# -------------------------
def run_ga():
    # 1) initial random population
    population = [random_individual() for _ in range(POP_SIZE)]

    best_overall = None
    best_fitness_history = []

    for gen in range(GENERATIONS):
        # 2) compute fitness for all
        for ind in population:
            compute_fitness(ind)

        # 3) find best in this generation
        gen_best = max(population, key=lambda ind: ind["fitness"])

        if best_overall is None or gen_best["fitness"] > best_overall["fitness"]:
            best_overall = {
                "sensors": gen_best["sensors"][:],
                "fitness": gen_best["fitness"],
            }

        best_fitness_history.append(best_overall["fitness"])
        print(f"Generation {gen}: best fitness = {best_overall['fitness']}")

        # 4) create new population
        new_population = []
        while len(new_population) < POP_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.append(child1)
            if len(new_population) < POP_SIZE:
                new_population.append(child2)

        population = new_population

    return best_overall, best_fitness_history


# -------------------------
# Simple ASCII coverage map
# -------------------------
def print_coverage_map(individual):
    """
    Print a text-based map:
        'S' = sensor
        '#' = covered cell
        '.' = not covered
    """
    grid = compute_coverage_grid(individual)

    # start with '.' or '#'
    display = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if grid[y][x]:
                row.append('#')
            else:
                row.append('.')
        display.append(row)

    # mark sensors
    for (sx, sy) in individual["sensors"]:
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            display[sy][sx] = 'S'

    print("\nCoverage map (top row printed last):")
    for y in reversed(range(HEIGHT)):   # print from top to bottom
        print("".join(display[y]))


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    best, history = run_ga()

    print("\nBest fitness:", best["fitness"])
    print("Best sensor positions (x, y):")
    for (x, y) in best["sensors"]:
        print(f"({x}, {y})")

    print_coverage_map(best)

    print("\nBest fitness over generations:")
    for i, val in enumerate(history):
        print(i, val)
