"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Union
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


def _decreasing_volume_parcel(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a> has more volume than <b>.
    """
    return a.volume > b.volume


def _increasing_volume_parcel(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <b> has more volume than <a>.
    """
    return a.volume < b.volume


def _decreasing_volume_truck(a: Truck, b: Truck) -> bool:
    """
    Return True if <a> has more available space than <b>.
    """
    return a.available_space > b.available_space


def _increasing_volume_truck(a: Truck, b: Truck) -> bool:
    """
    Return True if <b> has more available space than <a>.
    """
    return a.available_space < b.available_space


def _comes_before(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a>'s destination comes before <b> alphabetically.
    """
    return a.end < b.end


def _comes_after(a: Parcel, b: Parcel) -> bool:
    """
    Return True if <a>'s destination comes after <b> alphabetically.
    """
    return a.end > b.end


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """A random scheduler that packs parcels onto trucks randomly.
    """
    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the parcels in <parcels> onto trucks in <trucks> randomly,
        considering only trucks with enough available space for each parcel.

        Return a list containing the parcels that could not be scheduled.
        """
        not_scheduled_parcels = []
        shuffle(parcels)
        for parcel in parcels:
            trucks_available = []
            for truck in trucks:
                if parcel.volume <= truck.available_space:
                    trucks_available.append(truck)
            shuffle(trucks_available)
            if not trucks_available:
                not_scheduled_parcels.append(parcel)
            else:
                t = choice(trucks_available)
                t.pack(parcel)
        return not_scheduled_parcels


class GreedyScheduler(Scheduler):
    """A scheduler that packs parcels into trucks strategically, depending on
    given parcel priority, parcel order and truck order.

    Parcel priority can be either by volume or destination.
    Parcel order can be either non-decreasing or non-increasing.
    Truck orders are by capacity and can be either non-decreasing or
    non-increasing.

    A parcel priority of non-decreasing destination means parcels are considered
    starting with the one with destination that comes first in the dictionary.

    When a parcel is processed, only the trucks with enough available space are
    considered. Among these eligible trucks, if there is one that has the
    parcel's destination at the end of its route, then the parcel is packed
    into that truck. If not, then the truck with either the most or least
    available space is chosen, depending on the given truck order.

    Ties are broken using the order in which the parcels and trucks are read
    from the data file.


    === Private Attributes ===
    _parcel_priority: The parcel priority for this scheduler. This is either
    volume or destination.
    _parcel_order: The order in which the parcels will be packed by their parcel
    priority.
    _truck_order: The order in which trucks will be considered by their
    available spaces.

    """
    _parcel_priority: str
    _parcel_order: str
    _truck_order: str

    def __init__(self, config: Dict[str, Union[str, bool]]) -> None:

        self._parcel_priority = config['parcel_priority']
        self._parcel_order = config['parcel_order']
        self._truck_order = config['truck_order']

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the parcels in <parcels> onto trucks in <trucks> with
        respect to the scheduler's parcel priority, parcel order and truck
        order.

        Return a list containing the parcels that could not be scheduled.
        """

        if self._parcel_priority == 'volume':
            if self._parcel_order == 'non-decreasing':
                if self._truck_order == 'non-decreasing':
                    func = _inc_inc
                else:
                    func = _inc_dec
            else:
                if self._truck_order == 'non-decreasing':
                    func = _dec_inc
                else:
                    func = _dec_dec
        else:
            if self._parcel_order == 'non-decreasing':
                if self._truck_order == 'non-decreasing':
                    func = _incdest_inc
                else:
                    func = _incdest_dec
            else:
                if self._truck_order == 'non-decreasing':
                    func = _decdest_inc
                else:
                    func = _decdest_dec

        return func(parcels, trucks)

# ----- Helper functions -----


def _inc_inc(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-decreasing volume
    truck priority: non-decreasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_increasing_volume_parcel)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _inc_dec(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-decreasing volume
    truck priority: non-increasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_increasing_volume_parcel)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _dec_inc(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-increasing volume
    truck priority: non-decreasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_decreasing_volume_parcel)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _dec_dec(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """
    A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-increasing volume
    truck priority: non-increasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_decreasing_volume_parcel)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _incdest_inc(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-decreasing destination
    truck priority: non-decreasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_comes_before)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _incdest_dec(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-decreasing destination
    truck priority: non-increasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_comes_before)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _decdest_inc(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-increasing destination
    truck priority: non-decreasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_comes_after)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_increasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


def _decdest_dec(parcels: List[Parcel], trucks: List[Truck]) -> List[Parcel]:
    """A helper function for the GreedyScheduler class. Schedules parcels
    onto trucks for a scheduler with:

    parcel priority: non-increasing destination
    truck priority: non-increasing available space
    """
    not_scheduled = []

    p = PriorityQueue(_comes_after)

    for parcel in parcels:
        p.add(parcel)

    while not p.is_empty():
        box = p.remove()
        eligible = []
        eligible_2 = []
        for truck in trucks:
            if truck.available_space >= box.volume:
                eligible.append(truck)
        for e in eligible:
            if e.route[-1] == box.end:
                eligible_2.append(e)
        if eligible_2 != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible_2:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        elif eligible != []:
            pq = PriorityQueue(_decreasing_volume_truck)
            for e in eligible:
                pq.add(e)
            chosen_truck = pq.remove()
            chosen_truck.pack(box)
        else:
            not_scheduled.append(box)

    return not_scheduled


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
