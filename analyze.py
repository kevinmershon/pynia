import math
import random
import redis as Redis

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

if __name__ == "__main__":
    c = Chromosome()
    print c
