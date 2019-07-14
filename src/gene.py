import numpy as np


class Gene(object):
    """
    creates lise of genes out of files and can display them in log
    """
    def __init__(self, items_file, logger):
        self.items = np.loadtxt(items_file)
        self.logger = logger
        self.logger.debug('list of items: %s' % self.items)
        return
