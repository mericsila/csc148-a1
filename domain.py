"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """ A parcel to be delivered.

    === Public Attributes ===
    parcel_id: The specific identification number of this parcel.
    volume: Volume of this parcel.
    start: Source location of the parcel.
    end: The parcel's destination location.

    === Representation invariants ===
    - Volume is a positive integer.

    === Sample Usage ===
    >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
    >>> p1.parcel_id
    1
    >>> p1.volume
    5
    >>> p1.start
    'Buffalo'
    >>> p1.end
    'Hamilton'
    """
    parcel_id: int
    volume: int
    start: str
    end: str

    def __init__(self, parcel_id: int, volume: int, start: str, end: str) \
            -> None:
        """Initialize this parcel.

        Precondition: volume is a positive integer.
        """
        self.parcel_id = parcel_id
        self.volume = volume
        self.start = start
        self.end = end


class Truck:
    """ A truck for making deliveries.

    === Public Attributes ===
    truck_id: The specific identification number of this truck.
    capacity: The maximum capacity of this truck.
    route: The truck's route.
    available_space: Available space in the truck.
    parcels: A list of all the parcels in this truck.
    packed_p: A list of the IDs of the parcels in this truck.

    === Representation invariants ===
    - capacity is a positive integer.
    - available_space is between 0 and capacity, inclusive.
    """
    truck_id: int
    capacity: int
    route: List[str]
    available_space: int
    parcels: List[Parcel]
    packed_p: List[int]

    def __init__(self, truck_id: int, capacity: int, depot: str) -> None:
        """Initialize this truck.

        A truck is empty when it is created; its available space is equal to
        its capacity. It has no parcels inside it initially.
        The route of the truck is only <depot> before any parcels are packed
        into it.
        """
        self.truck_id = truck_id
        self.capacity = capacity
        self.route = [depot]
        self.available_space = capacity
        self.packed_p = []
        self.parcels = []

    def pack(self, p: Parcel) -> bool:
        """Packs parcel <p> into the truck if there is enough available space.

        Return True if parcel is packed into the truck successfully, return
        False if unable to pack.

        Assume the parcel has been already shipped to the depot of the truck.
        Add the destination of the parcel to the truck's route.
        Subtract the parcel's volume from the truck's available space.

        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.route
        ['Toronto', 'Hamilton']
        """
        if p.volume <= self.available_space:
            self.available_space -= p.volume
            self.packed_p.append(p.parcel_id)
            self.parcels.append(p)
            if p.end != self.route[-1]:
                self.route.append(p.end)
            return True
        return False

    def fullness(self) -> float:
        """ Return the truck's fullness in percentage points.

        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        """
        return 100 - self.available_space / self.capacity * 100


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        truck id eklenebilir
        """
        return f'number of trucks: {self.num_trucks()}, ' \
               f'unused trucks: ' \
               f'{(self.num_trucks() - self.num_nonempty_trucks())}, ' \
               f'avg fullness: {self.average_fullness()}, ' \
               f'unused space: {self.total_unused_space()} ' \


    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        num_non_empty = 0
        for truck in self.trucks:
            if truck.fullness() > 0:
                num_non_empty += 1
        return num_non_empty

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        fleet_track = {}
        for truck in self.trucks:
            fleet_track[truck.truck_id] = truck.packed_p
        return fleet_track

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        empty_space = 0
        for truck in self.trucks:
            if truck.fullness() > 0:
                empty_space += truck.available_space
        return empty_space

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        total_fullness = 0
        for truck in self.trucks:
            if truck.fullness() > 0:
                total_fullness += truck.fullness()
        return total_fullness

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        fullness_avg = 0
        for truck in self.trucks:
            if truck.fullness() > 0:
                fullness_avg += truck.fullness() / len(self.trucks)
        return fullness_avg

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        total_distance = 0

        for truck in self.trucks:
            if len(truck.route) > 1:
                tuple_route = []  # make a list w tuples for dmap usage
                i = 1
                while i < len(truck.route):
                    tuple_route.append((truck.route[i - 1], truck.route[i]))
                    i += 1
                tuple_route.append((truck.route[-1], truck.route[0]))
                for tup in tuple_route:
                    total_distance += dmap.distance(tup[0], tup[1])

        return total_distance

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        total_distance = self.total_distance_travelled(dmap)
        valid_trucks = 0
        for truck in self.trucks:
            if len(truck.route) > 1:
                valid_trucks += 1
        return total_distance / valid_trucks


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
