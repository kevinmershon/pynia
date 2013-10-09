import math
import random
import redis as Redis

redis = None
population_size = 100
crossover_rate = 0.7
mutation_rate = 0.001

class Chromosome:
    CHROMOSOME_SIZE = 128
    GENE_CODES = [
        "0.01",                     # 00 = 0
        "10",                       # 01 = 10
        "alpha[0]",                 # 02 = alpha low
        "alpha[1]",                 # 03 = alpha medium
        "alpha[2]",                 # 04 = alpha high
        "beta[0]",                  # 05 = beta low
        "beta[1]",                  # 06 = beta medium
        "beta[2]",                  # 07 = beta high
        str((1+math.sqrt(5))/2),    # 08 = phi
        str(1j),                    # 09 = i
        str(math.e),                # 10 = e
        "+",                        # 11 = +
        "-",                        # 12 = -
        "*",                        # 13 = *
        "/",                        # 14 = /
        "NaN"                       # 15 = not a number (unassigned)
    ]
    NUMBER_GENES = range(0, 11)
    MATH_GENES = range(11, 15)

    def __init__(self):
        """
            Create a Chromosome with random genes
        """
        self.genes = [random.randint(0, len(Chromosome.GENE_CODES)-1)
                          for x in range(Chromosome.CHROMOSOME_SIZE)]

    def get_valid_genes(self):
        """
            Get the valid genetic components of this Chromosome. Alternate
            taking the next valid number, then the next valid math operation.
        """
        valid_genes = []
        for i in range(len(self.genes)):
            if len(valid_genes) % 2 == 0:
                # we need a number
                if self.genes[i] in Chromosome.NUMBER_GENES:
                    valid_genes.append(self.genes[i])
            else:
                # we need a math operation
                if self.genes[i] in Chromosome.MATH_GENES:
                    valid_genes.append(self.genes[i])

        # if we ended with a math operation, drop it
        if valid_genes[len(valid_genes)-1] in Chromosome.MATH_GENES:
            valid_genes.pop()

        return valid_genes

    def __str__(self):
        return " ".join([Chromosome.GENE_CODES[x]
                             for x in self.get_valid_genes()])

def get_last_event(event_type):
    last_events = redis.zrevrange(event_type, 0, 0)
    if len(last_events) == 0:
        return None

    return eval(last_events[0])

def get_chromosomes(event_type):
    chromosomes = redis.zrevrange("chromosomes." + event_type, 0, 0)
    if len(chromosomes) == 0:
        return []

    return eval(chromosomes[0])

def get_probability_ranges_for_chromosomes(chromosomes, scores):
    """
        Compute interval ranges from 0 to 1.0 for the fitness of each chromosome
        relative to the overall fitness of the batch based on their total
        scores.
    """
    total_fitness = float(sum(scores))
    relative_fitnesses = [s/total_fitness
                              for s in scores]
    probabilities = [sum(relative_fitnesses[:i+1])
                         for i in range(population_size)]

    return probabilities

def get_weighted_random_chromosome(chromosomes, probabilities):
    """
        Get a random chromosome based on the specified probability intervals
    """
    # choose a random number
    randomness = random.random()

    # find the chromosome which falls within the probability range of randomness
    random_index = [i for i in range(0, population_size)
                          if (probabilities[i] <= randomness and
                              (i+1 == population_size or
                               probabilities[i+1] > randomness))][0]
    # print("random:", randomness,
    #       ", index:", random_index,
    #       ", probability:", probabilities[random_index])

    return chromosomes[random_index], random_index

def evolve(event_type):
    # find all events from redis for the specified event type
    event = get_last_event(event_type)

    # try to get the last batch of chromosomes from redis if we have them
    chromosomes = get_chromosomes(event_type)

    # if no chromosomes exist, generate chromosomes at random
    if (len(chromosomes) == 0):
        chromosomes = []
        for x in range(population_size):
            chromosomes.append(Chromosome())

    # compute the scores for each chromosome (and throw away imaginary parts)
    scores = [compute_chromosome_score(x, event).real
                  for x in chromosomes]

    # compute probability ranges for each chromosome in the population based on
    # its fitness relative to the fitness of the entire population
    probabilities = get_probability_ranges_for_chromosomes(chromosomes, scores)
    for i in range(population_size):
        # select two chromosomes from the old population proportionally relative
        # to how fit they are
        c_a, idx_a = get_weighted_random_chromosome(chromosomes, probabilities)
        c_b, idx_b = get_weighted_random_chromosome(chromosomes, probabilities)
        print "a:", scores[idx_a], ", b:", scores[idx_b]

        # TODO -- crossover and mutate the chromosomes and add both to the new
        # population


def eval_chromosome(chromosome, dataset):
    """
        Compute the score of this chromosome against the specified dataset
    """
    chromosome_str = str(chromosome)
    alpha = dataset[0:3]
    beta = dataset[3:6]

    try:
        dataset_score = eval(chromosome_str, { "alpha": alpha, "beta": beta })
        return dataset_score
    except Exception, ex:
        return 0

def compute_chromosome_score(chromosome, event):
    """
        Compute the score of this chromosome against all datasets associated
        with this event, match or non-match
    """
    # Ideally we want the lowest latency we can get for interpreting signals.
    # This means we want to favor chromosomes which eval highly on the 0th match
    # (the most recent) and decreasingly favor older matches.
    score = (50 * eval_chromosome(chromosome, eval(event["matches"][0])) +
             30 * eval_chromosome(chromosome, eval(event["matches"][1])) +
             15 * eval_chromosome(chromosome, eval(event["matches"][2])) +
             05 * eval_chromosome(chromosome, eval(event["matches"][3])))

    # Additionally, to rule out chromosomes which yield false positives, we want
    # to also favor chromosomes which eval minimally on all the non-matches
    # test each chromosome to see how good it is at solving the problem
    for i in range(len(event["non_matches"])):
        score -= eval_chromosome(chromosome, eval(event["non_matches"][i]))

    return score

if __name__ == "__main__":
    redis = Redis.StrictRedis(host='localhost', port=6379, db=0)
    c = Chromosome()
    print c
