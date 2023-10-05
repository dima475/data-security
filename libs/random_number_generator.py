from typing import Iterator
from dataclasses import dataclass


@dataclass
class RandomNumberGenerator:
    m: int
    a: int
    c: int
    x: int

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        self.x = (self.a * self.x + self.c) % self.m
        return self.x


def get_period(m: int, a: int, c: int, x: int) -> int:
    random_generator: RandomNumberGenerator = RandomNumberGenerator(m, a, c, x)
    period = 1
    initial_x = next(random_generator)
    while True:
        number = next(random_generator)
        if initial_x == number:
            break
        period += 1
    return period
