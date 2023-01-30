from math import sqrt
from typing import Optional
from returns.maybe import Maybe, maybe

@maybe
def get_root(square: float) -> Optional[float]:
    if square >= 0:
        return sqrt(square)

@maybe
def divide(numerator: float, denominator: float) -> Optional[float]: 
    if denominator != 0:
        return (numerator/denominator)
