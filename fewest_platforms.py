"""Given arrival and departure times of all trains that reach a railway station, 
the task is to find the minimum number of platforms required for the railway station so that no train waits.

We are given two arrays which represent arrival and departure times of trains that stop.

Examples:

Input: arr[] = {9:00, 9:40, 9:50, 11:00, 15:00, 18:00}
dep[] = {9:10, 12:00, 11:20, 11:30, 19:00, 20:00}
Output: 3
There are at most three trains at a time (time between 11:00 to 11:20)

https://www.geeksforgeeks.org/minimum-number-platforms-required-railwaybus-station/
"""
from itertools import chain
from typing import List


def search(arr: List[int], dep: List[int]) -> int:
    assert len(arr) == len(dep)
    arr = ((x, True) for x in arr)
    dep = ((x, False) for x in dep)
    n = n_max = 0
    for _, x in sorted(chain(arr, dep)):
        if x:
            n += 1
            n_max = max(n, n_max)
        else:
            n -= 1
    return n_max


if __name__ == '__main__':
    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]
    assert search(arrivals, departures) == 3
