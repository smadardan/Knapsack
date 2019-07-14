"""
tests.chromosome
~~~~~~~~~~~~~~~~
here we will write all of the unit test for the chromosome class
"""
import numpy as np

from src.chromosome import Chromosome


class LoggerMock:
    def __init__(self):
        return

    def debug(self, text):
        pass

    def info(self, test):
        pass


# initialize for all tests
logger = LoggerMock()
inst = Chromosome(5, logger)


def test_create_chromosome():
    chromosome = inst.create_chromosome(np.array([[6, 6], [2, 2], [3, 3], [7, 7]]))
    assert np.array_equal(chromosome, np.array([[2, 2], [3, 3]])) or np.array_equal(
        chromosome, np.array([[3, 3], [2, 2]]))


def test_crossover():
    child = inst.crossover(np.array([[7, 7], [3, 3]]), np.array([[2, 2], [8, 8]]))
    assert np.array_equal(child, np.array([[2, 2], [3, 3]])) or np.array_equal(
        child, np.array([[3, 3], [2, 2]]))


def test_mutation():
    mutate = inst.mutation(np.array([[1, 1]]), np.array([[2, 2]]))
    assert np.array_equal(mutate, np.array([2, 2]))
