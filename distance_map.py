"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict, Tuple


class DistanceMap:
    """
    A distance map for storing distances between locations.

    === Private Attributes ===
    _distances: A dictionary that stores the distances between locations
    for this distance map.

    === Sample Usage ===
    >>> dmap = DistanceMap()
    >>> dmap.add_distance('Toronto', 'Vancouver', 40, 50)
    >>> dmap.distance('Toronto', 'Vancouver')
    40
    >>> dmap.distance('Vancouver', 'Toronto')
    50
    """
    _distances: Dict[Tuple, int]

    def __init__(self) -> None:
        """Initialize this Distance Map.
        A distance map has no stored distances when it is first created.
        """
        self._distances = {}

    def add_distance(self, c1: str, c2: str, distance1: int,
                     distance2: int = -1) -> None:
        """ Add the distance between <c1> and <c2> into this Distance Map.

        If distance2 is provided, distance1 is recorded as the distance from
        <c1> to <c2>, and distance2 is recorded as the distance from <c2> to
        <c1>.
        If distance2 is not provided, the distance from <c1> to <c2> and the
        distance from <c2> to <c1> is recorded as distance1.

        Precondition: distance1 and distance2 (if provided) are positive
        integers.

        >>> dmap = DistanceMap()
        >>> dmap.add_distance('Toronto', 'London', 3)
        >>> dmap.distance('London', 'Toronto')
        3
        >>> dmap.add_distance('Toronto', 'Hamilton', 2, 4)
        >>> dmap.distance('Hamilton', 'Toronto')
        4
        """

        self._distances[(c1, c2)] = distance1
        if distance2 != -1:
            self._distances[(c2, c1)] = distance2
        else:
            self._distances[(c2, c1)] = distance1

    def distance(self, c1: str, c2: str) -> int:
        """Return the distance from <c1> to <c2>.
        If the distance from <c1> to <c2> is not stored in the distance map,
        return -1.

        >>> dmap = DistanceMap()
        >>> dmap.add_distance('Toronto', 'London', 4)
        >>> dmap.distance('Toronto', 'Hamilton')
        -1
        """
        if (c1, c2) in self._distances:
            return self._distances[(c1, c2)]
        return -1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
