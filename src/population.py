"""
src.population
~~~~~~~~~~~~~~~
deals with all population operations like create population of some specific size,
select the best chromosomes out of a populations and save all of the best scores out of all rounds,
new_population creates new improved population and circle of life just calls every function by order
in correlation of how many rounds we decided to perform and prints the best score by the help of func
top_of_the_top
"""

import numpy as np

from src.gene import Gene
from src.chromosome import Chromosome
import config.conf_file as cnf


class Population(object):

    def __init__(self, population_size, filename_of_genes, max_weight, logger):
        self.population_size = population_size
        self.genes = Gene(filename_of_genes, logger)
        self.max_weight = max_weight
        self.max_score_for_run = None
        self.logger = logger
        self.best_chromosome = np.array([0, 0])
        return

    def natural_population(self, list_of_genes, amount_of_chroms):
        """
        makes new population with given set genes and desired size for the population
        :param list_of_genes: list of ints, the items (0: weight, 1: value)
        :param amount_of_chroms: int, number of chromosomes
        :return:
        """
        population = []
        for i in range(amount_of_chroms):
            inst = Chromosome(self.max_weight, self.logger)
            population.append(inst.create_chromosome(list_of_genes))
        self.logger.debug('population: %s' % population)
        self.logger.debug('length of population: %s' % len(population))
        return population

    def selection(self, population):
        """
        finds the best score of each chromosome in population, returns half of the population with the best
        scores
        :param population: list of lists. combination of chromosomes
        :return: best: list, best chromosome, scores_of_chromosomes: , rank:
        """
        scores_of_chromosomes = self.calc_scores(population)
        rank, best = self.rank_and_find_best(scores_of_chromosomes, population)
        self.logger.debug('scores of all chromosomes by order: %s' % scores_of_chromosomes)
        self.logger.debug('best chromosomes in population: %s' % best)
        return best, scores_of_chromosomes, rank

    def calc_scores(self, population):
        """
        calculates the score of each chromosome in the population
        :param population: list of chromosomes
        :return: scores_of_chromosomes: np.array of score for each chromosome
        """
        scores_of_chromosomes = None
        for count, chromosome in enumerate(population):
            self.logger.debug('chromosome: %s' % chromosome)
            # sum values and weights of each chromosome
            if len(chromosome.shape) == 1:  # if there is only one gene in the chromosome
                chromosome = np.array([chromosome])
            chrom_sum = np.sum(chromosome, axis=0)
            if count == 0:
                scores_of_chromosomes = chrom_sum
            else:
                scores_of_chromosomes = np.vstack((scores_of_chromosomes, chrom_sum))
        return scores_of_chromosomes

    def rank_and_find_best(self, scores_of_chromosomes, population):
        """
        create rank of the chromosomes from best o worst and find the best one
        :param scores_of_chromosomes: list of scores for all the chromosomes in the population
        :param population: list of genes
        :return: rank: the ranking of each chromosome, best: list, the best chromosome
        """
        rank = scores_of_chromosomes[:, cnf.VALUE].argsort()
        best = []
        self.logger.debug('length of population: %s' % len(population))
        for i in range(len(rank)):
            if i >= cnf.TOP_PERCENT * len(population):
                best.append(population[rank[i]])
        current_best = np.sum(self.calc_scores(np.array(self.best_chromosome)), axis=0)
        up_runner_best = np.sum(self.calc_scores(np.array([population[rank[-1]]])), axis=0)
        if up_runner_best > current_best:  # save the best chromosome
            self.best_chromosome = [population[rank[-1]]]
        return rank, best

    def find_best_score(self, scores_of_population, rank):
        """
        given a rank of chromosomes in population and the list of chromosomes find the best chromosome
        of each round and save in a global variable
        :param scores_of_population: np.array score for each population
        :param rank: list of chromosomes ordered
        :return:
        """
        for chrom in range(len(scores_of_population)):
            if rank[chrom] == 0:
                if self.max_score_for_run is not None:
                    self.max_score_for_run = np.vstack((self.max_score_for_run, scores_of_population[chrom]))
                else:
                    self.max_score_for_run = scores_of_population[chrom]
        return

    def new_population(self, best, list_of_genes):
        """
        creates improved population:
         1. takes the 50% best chromosomes from previous population and divide them by half:
         1.a half of the best are parent - each couple will create one child
         1.b half of the best will be mutated and continue to the second population
         2. the rest will be new neutral chromosomes from the entire list of genes to return to the
         the given size of population (we keep population size as constant
        :param best: list of best chromosomes in the population
        :param list_of_genes: list of extra genes to insert to chromosome
        :return:
        """
        new_population = self.create_new_population(best, list_of_genes)
        parents, mutants = Population.create_parents_and_mutants(best)

        # new children (mix of parents)
        for i in range(0, len(parents) - 1, cnf.CUT_BY):
            inst = Chromosome(self.max_weight, self.logger)
            new_population.append(inst.crossover(parents[i], parents[i+1]))

        # new mutations size of whats is left of the best after allocation of parents
        for mutant in mutants:
            inst = Chromosome(self.max_weight, self.logger)
            new_population.append(inst.mutation(mutant, list_of_genes))
        self.logger.debug('new population: %s' % new_population)
        return new_population

    def create_new_population(self, best, list_of_genes):
        """
        creates new population by creating new unrelated chromosomes as half of the population
         and adding one quarter of previous population
        :param best: list, best chromosomes from previous round
        :param list_of_genes: list, extra genes
        :return: new_population: the new mix of genes
        """
        np.random.shuffle(best)
        # new unrelated chromosomes as half + one quarter of previous population
        new_population = [self.natural_population(
            list_of_genes, int(len(best) + (len(best) / cnf.CUT_BY * cnf.CUT_BY)))]
        new_population = new_population[0]
        return new_population

    @staticmethod
    def create_parents_and_mutants(best):
        """
        creates from the best chromosomes of previous population allocation for half to be parents and half mutants
        :param best: list of lists, top chromosomes from previous population
        :return: parents: chromosomes that will become parents (have to be even number), mutants: the rest
        of the chromosomes will become mutants
        """
        if len(best) % cnf.CUT_BY == 0:
            parents = best[:int(len(best) / cnf.CUT_BY)]
            mutants = best[int(len(best) / cnf.CUT_BY):]
        else:
            parents = best[:int(len(best) / cnf.CUT_BY + 1)]
            mutants = best[int(len(best) / cnf.CUT_BY + 1):]
        return parents, mutants

    def circle_of_life(self, number_of_iterations):
        """
        will initiate the whole process and create improved populations by the number of iterations given
        :param number_of_iterations: int, number of iterations
        :return:
        """
        population = self.natural_population(self.genes.items, self.population_size)
        # print(len(population))
        for i in range(number_of_iterations):
            best, scores_for_round, rank_for_round = self.selection(population)
            self.logger.debug('population in round %s: %s' % (i, population))
            self.logger.debug('best chromosomes: %s' % best)
            self.logger.debug('scores of all chromosomes in round: %s' % scores_for_round)

            self.find_best_score(scores_for_round, rank_for_round)
            self.logger.debug('best scores so far: %s' % self.max_score_for_run)

            new_population = self.new_population(best, self.genes.items)
            self.logger.debug('new and improved population: %s' % new_population)

            population = new_population

        self.top_of_the_top()
        return

    def top_of_the_top(self):
        """
        after all of the iterations finds the best chromosome from all populations
        :return:
        """
        rank = np.argsort(self.max_score_for_run[:, cnf.VALUE])
        answer = self.max_score_for_run[rank[-1]]
        self.logger.info('best value for knapsack is: %s' % answer)
        self.logger.info('best combination for knapsack is: %s' % self.best_chromosome)
        return
