import unittest

from libs.random_number_generator import RandomNumberGenerator, get_period


class TestRandomNumberGenerator(unittest.TestCase):

    def test_generator_iteration(self):
        generator = RandomNumberGenerator(m=536870911, a=4096, c=6567, x=23)
        result = [next(generator) for i in range(10)]
        print(result)
        expected_result = [100775, 412780967, 144348660, 157244916, 366960214, 367363222, 407471257, 407483851,
                           459068875, 224188245]
        self.assertEqual(result, expected_result)

    def test_with_equal_parameters(self):
        generator1 = RandomNumberGenerator(m=536870911, a=4096, c=6567, x=23)
        result1 = [next(generator1) for i in range(10)]
        generator2 = RandomNumberGenerator(m=536870911, a=4096, c=6567, x=23)
        result2 = [next(generator2) for i in range(10)]
        self.assertEqual(result1, result2)

    def test_with_different_parameters(self):
        generator1 = RandomNumberGenerator(m=536870911, a=4096, c=6567, x=23)
        result1 = [next(generator1) for i in range(10)]
        generator2 = RandomNumberGenerator(m=4000, a=35, c=78, x=6)
        result2 = [next(generator2) for i in range(10)]
        self.assertNotEqual(result1, result2)

    def test_get_period(self):
        m = 536870911
        a = 4096
        c = 6567
        x = 23
        period = get_period(m, a, c, x)
        expected_period = 29
        self.assertEqual(period, expected_period)
