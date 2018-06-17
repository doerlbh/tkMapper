import itertools
from collections import defaultdict

class Nerve:
    """Base class for implementations of a nerve finder to build a Mapper complex.

    __call__: Return all simplices found by the nerve finder
    """
    def __init__(self):
        pass

    def __call__(self, nodes, links):
        raise NotImplementedError()


class GraphNerve(Nerve):
    """ Creates the 1-skeleton of the Mapper complex.
    """
    def __init__(self, min_intersection=1, times=None, time_filtration=None):
        self.min_intersection = min_intersection
        self.times = times
        self.time_filtration = time_filtration

    def __call__(self, nodes, times=None, time_filtration=None):
        """Helper function to find edges of the overlapping clusters.

        Parameters
        ----------
        nodes:
            A dictionary with entires `{node id}:{list of ids in node}`

        Returns
        -------
        edges:
            A 1-skeleton of the nerve (intersecting  nodes)

        simplicies: 
            Complete list of simplices

        """

        result = defaultdict(list)
        self.times = times
        self.time_filtration = time_filtration

        # Create links when clusters from different hypercubes have members with the same sample id.
        candidates = itertools.combinations(nodes.keys(), 2)
        for candidate in candidates:
            # if there are non-unique members in the union
            if len(set(nodes[candidate[0]]).intersection(nodes[candidate[1]])) >= self.min_intersection:
                if self.times is not None and self.time_filtration is not None:
                    # print(self.times[candidate[0]])
                    # print(self.times[candidate[1]])
                    if abs(self.times[candidate[0]][0] - self.times[candidate[1]][0]) <= self.time_filtration:
                        result[candidate[0]].append(candidate[1])
                else: 
                    result[candidate[0]].append(candidate[1])

        simplices = [[n] for n in nodes] + [[x] + result[x] for x in result]
        return result, simplices

class SimplicialNerve(Nerve):
    """ Creates the entire Cech complex of the covering defined by the nodes.

    Warning: Not implemented yet.
    """
    def __call__(self, nodes, links=None):
        pass
