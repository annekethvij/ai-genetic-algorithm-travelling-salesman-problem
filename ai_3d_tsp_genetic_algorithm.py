import numpy as np
import random
import os.path

initial_population = []
initial_population_size = 0
number_of_cities_to_traverse = 0
cities_list_to_traverse = []

# input_file_path = "/Users/annekethvij/Documents/resource/input3.txt"
input_file_path = "input.txt"
# print(os.path.isfile(input_file_path))
# checking for input file before proceeding with the computation.
if os.path.isfile(input_file_path):
    inputfile = open(input_file_path).read()
    # print(inputfile)
    if inputfile is not None:
        number_of_cities_to_traverse = int(inputfile.split("\n")[0])
        cities_list_to_traverse = list(filter(None, inputfile.split("\n")[1:]))
        if(number_of_cities_to_traverse != 0 and number_of_cities_to_traverse != 1):

            # print("Number of cities in the input: ", number_of_cities_to_traverse)
            # print("List of cities to traverse: ", cities_list_to_traverse)
            initial_population_size = 2 * number_of_cities_to_traverse if number_of_cities_to_traverse < 100 else number_of_cities_to_traverse


            # print("initial_population_size is: ", initial_population_size)

            def calculate_euclidean_distance(city1, city2):
                '''
                :param city1: 3D co-ordinates x y z representing the city1
                :param city2: 3D co-ordinates x y z representing the city2
                :return: Euclidean Distance between the cities
                '''
                # print("Entering method: calculate_euclidean_distance")
                city1 = city1.split(" ")
                city2 = city2.split(" ")
                # print(f" city 1 is {city1}, is of type {type(city1)}")
                # print(f" city 2 is {city2}, is of type {type(city2)}")
                # print(f" city 1 co-ordinates are: {city1[0]}, {city1[1]}, {city1[2]}")
                # print(f" city 2 co-ordinates are: {city2[0]}, {city2[1]}, {city2[2]}")
                euclidean_distance = np.sqrt((int(city2[0]) - int(city1[0])) ** 2 + (int(city2[1]) - int(city1[1])) ** 2 + (
                        int(city2[2]) - int(city1[2])) ** 2)
                # print("Returning euclidean_distance: ", euclidean_distance)
                # print("Exiting method: calculate_euclidean_distance")
                return euclidean_distance


            def create_initial_population(initial_population_size, cities) -> list:
                '''
                helper method to create initial population for the genetic algorithm using the Nearest Neighbor heuristic.
                :param initial_population_size: The number of cities in the input population
                :param cities: List of the cities with co-ordinates x,y,z provided from input file
                :return: List of travel permutations
                '''

                # #print("Entering method: create_initial_population")
                for index in range(len(cities)):
                    unexplored_cities = cities[:]
                    # #print("unexplored_cities: ", unexplored_cities)
                    current_city = unexplored_cities.pop(index)
                    # #print("current_city: ", current_city)
                    path = [current_city]

                    while unexplored_cities:
                        nearest_city = min(unexplored_cities,
                                           key=lambda city: calculate_euclidean_distance(current_city, city))
                        path.append(nearest_city)
                        current_city = nearest_city
                        unexplored_cities.remove(nearest_city)

                    # print("path is: ", path)
                    path.append(path[0])
                    # print("path after append: ", path)
                    initial_population.append(path)
                    # print("initial_population is: ", initial_population)
                    # print("initial_population length is: ", len(initial_population))
                    # print("Exiting method: create_initial_population")

                return initial_population

                # #random creation of initial population
                # for size in range(initial_population_size):
                #     random_population = random.sample(cities, len(cities))
                #     random_population.append(random_population[0])
                #     #print("random_population:", random_population)
                #     if random_population not in initial_population:
                #         initial_population.append(random_population)
                # return initial_population
                #

            def calculate_euclidean_distance(city1, city2):
                '''
                :param city1: 3D co-ordinates x y z representing the city1
                :param city2: 3D co-ordinates x y z representing the city2
                :return: Euclidean Distance between the cities
                '''
                # print("Entering method: calculate_euclidean_distance")
                city1 = city1.split(" ")
                city2 = city2.split(" ")
                # print(f" city 1 is {city1}, is of type {type(city1)}")
                # print(f" city 2 is {city2}, is of type {type(city2)}")
                # print(f" city 1 co-ordinates are: {city1[0]}, {city1[1]}, {city1[2]}")
                # print(f" city 2 co-ordinates are: {city2[0]}, {city2[1]}, {city2[2]}")
                euclidean_distance = np.sqrt((int(city2[0]) - int(city1[0])) ** 2 + (int(city2[1]) - int(city1[1])) ** 2 + (
                        int(city2[2]) - int(city1[2])) ** 2)
                # print("Returning euclidean_distance: ", euclidean_distance)
                # print("Exiting method: calculate_euclidean_distance")
                return euclidean_distance


            def calculate_fitness(path):
                # print("Entering method: calculate_fitness")
                # print("path here is: ", path)
                total_path_cost = 0
                for city in range(len(path) - 1):
                    city1 = path[city]
                    city2 = path[city + 1]
                    total_path_cost += calculate_euclidean_distance(city1, city2)
                # print("total_path_cost: ", total_path_cost)
                # print("Exiting method: calculate_fitness")
                return total_path_cost


            def create_rank_list(population):
                '''
                helper method for creating the rank_list i.e. a list of tuples containing the index of path
                along with their fitness values from the ranked_population_list
                :param population: The initial population of paths that needs to be ranked
                :return: rank_list i.e. list of tuples with rank and fitness scores
                '''
                # print("Entering method: create_rank_list")
                ranked_population_list = [(path, calculate_fitness(path)) for path in population]
                ranked_population_list.sort(key=lambda rp_tuple: rp_tuple[1])

                rank_list = [(index, fitness) for index, (individual_path, fitness) in enumerate(ranked_population_list)]
                # print("Exiting method: create_rank_list")
                return rank_list


            def create_mating_pool(population, rank_list):
                '''
                helper method for  Roulette wheel-based selection of parents
                :param rank_list: Ranked list of populations based on their fitness scores
                :return: list of parents for genetic algorithm
                '''
                # print("Entering method: create_mating_pool")
                fitness_sum = 0
                mating_pool = []
                selection_probability_list = []

                for index, fitness in rank_list:
                    fitness_sum += fitness

                for index, fitness in rank_list:
                    selection_probability_list.append(fitness / fitness_sum)

                for _ in range(len(population)):
                    random_probability = random.random()
                    cumulative_probability = 0
                    for index, probability in enumerate(selection_probability_list):
                        cumulative_probability += probability
                        if cumulative_probability >= random_probability:
                            mating_pool.append(population[index])
                            break
                # print("Exiting method: create_mating_pool")
                return mating_pool


            def crossover(parent1, parent2, start_index, end_index):
                # print("Entering method: crossover")
                child = []
                child = parent1[start_index:end_index]
                for city in parent2:
                    if city not in child:
                        child.append(city)
                child.append(child[0])
                # print("Exiting method: crossover")
                return child


            def select_random_indices(path_length):
                # print("Entering method: select_random_indices")
                start_index, end_index = sorted(random.sample(range(int(path_length)), 2))
                # print("Exiting method: select_random_indices")
                return start_index, end_index


            def mutate(path):
                # print("Entering method: Entering mutate")
                # print("path in mutate is: ", path)
                start_index, end_index = random.sample(range(1, number_of_cities_to_traverse), 2)
                # print("start_index in mutate is: ", start_index)
                # print("end_index in mutate is: ", end_index)
                path[start_index:end_index + 1] = reversed(path[start_index:end_index + 1])
                # print("final path in mutate is: ", path)
                # print("Exiting method: mutate")
                return path


            # print("Starting TSP Solution with Genetic Algorithm")
            initial_population = create_initial_population(initial_population_size, cities_list_to_traverse)
            # print("final initial_population: ", initial_population)
            generations = initial_population_size
            ga_parameter_mutation_probability = 0.0001
            ga_parameter_crossover_probability = 0.3
            if (number_of_cities_to_traverse <= 10):
                ga_parameter_generation_size = 4 * number_of_cities_to_traverse
                # print("ga_parameter_generation_size is: ", ga_parameter_generation_size)
            elif (number_of_cities_to_traverse > 10 and number_of_cities_to_traverse <= 75):
                ga_parameter_generation_size = 2 * number_of_cities_to_traverse
                # print("ga_parameter_generation_size is: ", ga_parameter_generation_size)
            elif (number_of_cities_to_traverse > 75 and number_of_cities_to_traverse <= 200):
                ga_parameter_generation_size = 0.4 * number_of_cities_to_traverse
                # print("ga_parameter_generation_size is: ", ga_parameter_generation_size)
            else:
                ga_parameter_generation_size = 0.2 * number_of_cities_to_traverse
                # print("ga_parameter_generation_size is: ", ga_parameter_generation_size)

            population = initial_population
            for generation in range(generations):
                # print("****")
                # print("Starting with generation number", generation)
                rank_list = create_rank_list(population)
                # print("rank_list is: ", rank_list)
                mating_pool = create_mating_pool(population, rank_list)
                # print("mating_pool is:", mating_pool)

                next_generation = []

                while len(next_generation) < ga_parameter_generation_size:
                    parent1, parent2 = random.sample(mating_pool, 2)
                    # print(f"parent1 is: {parent1} and parent2 is: {parent2}")
                    if random.random() < ga_parameter_crossover_probability:
                        start_index, end_index = select_random_indices(number_of_cities_to_traverse)
                        child = crossover(parent1, parent2, start_index, end_index)
                    else:
                        child = parent1 if calculate_fitness(parent1) < calculate_fitness(parent2) else parent2

                    if random.random() < ga_parameter_mutation_probability:
                        child = mutate(child)

                    next_generation.append(child)
                # print("next_generation: ", next_generation)
                population = next_generation
                # print("population: ", population)

            final_path = min(population, key=calculate_fitness)
            final_path_cost = calculate_fitness(final_path)

            # output_file = open("/Users/annekethvij/Documents/resource/output.txt", "w")
            output_file = open("output.txt", "w")
            print(round(final_path_cost, 3), file=output_file)
            for city in final_path:
                print(city, file=output_file)
            # print("Final Path Cost is: ", round(final_path_cost, 3))
            # print("Final Path is: ", final_path)
            # print("Final Path length is: ", len(final_path))
        elif number_of_cities_to_traverse == 1:
            # output_file = open("/Users/annekethvij/Documents/resource/output.txt", "w")
            output_file = open("output.txt", "w")
            print(0, file=output_file)
            for _ in range(2):
                print(cities_list_to_traverse[0], file=output_file)
        else:
            # output_file = open("/Users/annekethvij/Documents/resource/output.txt", "w")
            output_file = open("output.txt", "w")
            print(0, file=output_file)

