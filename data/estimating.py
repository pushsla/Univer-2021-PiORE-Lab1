import math

from data.density import Density


class Estimator:
    @staticmethod
    def estimate(params: dict, samples: list[float], x: float) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_params() -> dict:
        raise NotImplementedError()

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()


class RosenEstimator:
    @staticmethod
    def estimate(params: dict, samples: list[float], x: float) -> float:
        Hn = params['Hn']
        core_f = params['core_f']

        N = len(samples)
        result = 1/(N*Hn)
        result *= sum([core_f.density((x - i)/Hn) for i in samples])

        return result

    @staticmethod
    def get_params() -> dict:
        return {
            'Hn': 1.0,
            'core_f': Density
        }

    @staticmethod
    def get_name() -> str:
        return "Розенблатта-Парсена"


Estimators = [RosenEstimator]