from typing import Iterator
from dataclasses import dataclass


@dataclass
class RandomNumberGenerator:
    """
        This class represents a simple linear congruential pseudo-random number generator.
        It generates a sequence of pseudo-random integers based on the linear congruential
        formula: Xn+1 = (a * Xn + c) % m.

        Attributes:
            m (int): The modulus value for the LCG.
            a (int): The multiplier value for the LCG.
            c (int): The increment value for the LCG.
            x (int): The current state (seed) of the generator.

        Methods:
            - __iter__() -> Iterator[int]: Returns an iterator object (self) for the generator.
            - __next__() -> int: Computes the next pseudo-random integer in the sequence.
    """
    m: int
    a: int
    c: int
    x: int

    def __iter__(self) -> Iterator[int]:
        """Return an iterator object for the generator."""
        return self

    def __next__(self) -> int:
        """Compute the next pseudo-random integer in the sequence."""
        self.x = (self.a * self.x + self.c) % self.m
        return self.x


def get_period(m: int, a: int, c: int, x: int) -> int:
    """
        Calculate the period of a linear congruential pseudo-random number generator.

        Args:
            m (int): The modulus value for the LCG.
            a (int): The multiplier value for the LCG.
            c (int): The increment value for the LCG.
            x (int): The initial seed value for the LCG.

        Returns:
            int: The period (cycle length) of the LCG.
    """
    random_generator: RandomNumberGenerator = RandomNumberGenerator(m, a, c, x)
    period = 1
    initial_x = next(random_generator)
    while True:
        number = next(random_generator)
        if initial_x == number:
            break
        period += 1
    return period
