import math
import random


class DataGenerator:

    base_random = random.SystemRandom()
    bootstrap = lambda x: x

    @classmethod
    def generate(cls, params: dict, amount: int) -> list[float]:
        result = []
        for _ in range(amount):
            base = cls.bootstrap(cls.base_random.random())
            result.append(cls.f(params, base))

        return result

    @staticmethod
    def f(params: dict, base: float) -> float:
        raise NotImplementedError()

    @staticmethod
    def density(params: dict, n: float) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_params() -> dict:
        raise NotImplementedError()

    @staticmethod
    def get_name():
        raise NotImplementedError()


class LinearGenerator(DataGenerator):

    @staticmethod
    def f(params: dict, base: float) -> float:
        pmin = params['min']
        pmax = params['max']

        return pmin + base*(pmax-pmin)

    @staticmethod
    def density(params: dict, n: float) -> float:
        pmin = params['min']
        pmax = params['max']

        return 1/(pmax-pmin) if pmax >= n >= pmin else 0

    @staticmethod
    def get_params() -> dict:
        return {
            'min': -5.0,
            'max': 5.0
        }

    @staticmethod
    def get_name():
        return "Равномерное"


class ExponentialGenerator(DataGenerator):

    lmin = 0.00001
    lmax = 1

    @classmethod
    def f(cls, params: dict, base: float) -> float:
        lamb = params['lambda']

        return math.log(1-base)/(-lamb)

    @staticmethod
    def density(params: dict, n: float) -> float:
        lamb = params['lambda']

        return lamb*math.e**(-lamb*n) if n >= 0 else 0

    @staticmethod
    def get_params() -> dict:
        return {
            'lambda': 1.0,
        }

    @staticmethod
    def get_name():
        return "Экспоненциальное"


class NormalGenerator(DataGenerator):

    second_random = random.SystemRandom()

    @staticmethod
    def f(params: dict, base: float) -> float:

        sigma = params['sigma']
        median = params['median']

        base2 = NormalGenerator.second_random.random()
        nx = math.sqrt(-2*math.log(base))*math.cos(2*math.pi*base2)

        return median + nx*sigma

    @staticmethod
    def density(params: dict, n: float) -> float:
        sigma = params['sigma']
        median = params['median']

        return (1/(sigma*math.sqrt(2*math.pi)))*math.e**(-(((n-median)/sigma)**2)*0.5)

    @staticmethod
    def get_params() -> dict:
        return {
            'sigma': 0.3,
            'median': 1.0,
        }

    @staticmethod
    def get_name():
        return "Нормальное"


Generators = [LinearGenerator, ExponentialGenerator, NormalGenerator]
