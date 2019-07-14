"""
src.chromosome
~~~~~~~~~~~~~~~
make all of the chromosome related operations such as create new chromosome from
    list of genes with constrains, create crossover and create mutation
"""

import numpy as np

import config.conf_file as cnf


class Chromosome(object):
    def __init__(self, max_weight, logger):
        self.max_weight = max_weight
        self.logger = logger
        return

    def create_chromosome(self, list_of_genes, sum_of_weights=0, chromosome=None):
        """
        given constrains of maximal weight and specific genes (no duplicates) the func creates new chromosome.
        if we want just to add one chromosome like in mutation we can do that by
        mentioning previous some of weights and the genes that are already in the chromosome
        :param list_of_genes: list, all of the genes we have
        :param sum_of_weights: int, how much weight we have it the chromosome so far
        :param chromosome: list, if we already have some genes in the chromosome
        :return: chromosome: list, the new chromosome
        """
        np.random.shuffle(list_of_genes)

        for gene in list_of_genes:
            self.logger.debug('gene: %s' % gene)
            if sum_of_weights == 0 and gene[cnf.WEIGHT] <= self.max_weight:
                chromosome = gene
                sum_of_weights += gene[cnf.WEIGHT]
            elif sum_of_weights < self.max_weight and int(sum_of_weights) + gene[cnf.WEIGHT] <= self.max_weight \
                    and gene not in chromosome:
                chromosome = np.vstack((chromosome, gene))
                sum_of_weights += gene[cnf.WEIGHT]

        self.logger.debug('chromosome: %s' % chromosome)
        return chromosome

    def crossover(self, chrom1, chrom2):
        """
        takes two parents. mix the genes and create child with the known constrains
        :param chrom1: list, chromosome one to mix from
        :param chrom2: list, chromosome 2 to mix from
        :return: child: list, new chromosome that is a mix of chrom1 and chrom2
        """
        parents = np.vstack((chrom1, chrom2))
        self.logger.debug('parents: %s' % parents)

        np.random.shuffle(parents)
        child = Chromosome.create_chromosome(self, parents)
        self.logger.debug('child: %s' % child)
        return child

    def mutation(self, chromosome, list_of_genes):
        """
        takes chromosome, removes the first gene (after shuffling) and try to add new chromosome
        instead of the old chromosome to improve value
        :param chromosome: list, combination of genes
        :param list_of_genes: list, list of extra genes to append to or not the chromosome
        :return:
        """
        np.random.shuffle(chromosome)
        # get rid of one gene
        takeout_gene = chromosome[cnf.WEIGHT:]
        current_weight = np.sum(takeout_gene[:, cnf.WEIGHT], axis=0)

        # try and add new gene
        mutant = Chromosome.create_chromosome(self, list_of_genes,
                                              sum_of_weights=int(current_weight), chromosome=chromosome[cnf.WEIGHT:])
        self.logger.debug('mutant: {}'.format(mutant))

        return mutant
