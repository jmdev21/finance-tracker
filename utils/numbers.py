import math

def truncate(value: float, decimals: int = 2) -> float:
    factor = 10 ** decimals
    return math.trunc(value * factor) / factor
