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
        "0",                        # 00 = 0
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


def evolve(event_type):
    # find all events from redis for the specified event type
    event = get_last_event(event_type)

    # try to get the last batch of chromosomes from redis if we have them
    chromosomes = get_chromosomes(event_type)

    # if no chromosomes exist, generate chromosomes at random
    if (len(chromosomes) == 0):
        chromosomes = [Chromosome()
                           for x in range(population_size)]

    # compute the scores for each chromosome
    scores = [compute_chromosome_score(x, eval(event))
                  for x in chromosomes]
    return scores

def eval_chromosome(chromosome, dataset):
    chromosome_str = str(chromosome)
    alpha = dataset[0:3]
    beta = dataset[3:6]

    try:
        score = eval(chromosome_str, { "alpha": alpha, "beta": beta })
        print score
        return score
    except Exception, ex:
        return 0

def compute_chromosome_score(chromosome, event):
    print "evaluating chromosome:", chromosome

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
