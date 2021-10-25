import math


class Metric:
    @staticmethod
    def calculate(params: dict, samples: list[float]) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_params() -> dict:
        raise NotImplementedError()

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()


class MeanMetric(Metric):
    @staticmethod
    def calculate(params: dict, samples: list[float]) -> float:
        return sum(samples)/len(samples)

    @staticmethod
    def get_params() -> dict:
        return {}

    @staticmethod
    def get_name() -> str:
        return "Выборочное среднее"


class DispersionMetric(Metric):
    @staticmethod
    def calculate(params: dict, samples: list[float]) -> float:
        mean_metric = MeanMetric.calculate(params, samples)
        return sum([(x - mean_metric)**2 for x in samples])/(len(samples)-1)

    @staticmethod
    def get_params() -> dict:
        return {}

    @staticmethod
    def get_name() -> str:
        return "Выборочная дисперсия"


class StandardDeviationMetrics(Metric):
    @staticmethod
    def calculate(params: dict, samples: list[float]) -> float:
        return math.sqrt(DispersionMetric.calculate(params, samples))

    @staticmethod
    def get_params() -> dict:
        return {}

    @staticmethod
    def get_name() -> str:
        return "Стандартное отклонение"


class WidthMetrics(Metric):
    @staticmethod
    def calculate(params: dict, samples: list[float]) -> float:
        return max(samples) - min(samples)

    @staticmethod
    def get_params() -> dict:
        return {}

    @staticmethod
    def get_name() -> str:
        return "Размах выборки"


Metrics = [MeanMetric, DispersionMetric, StandardDeviationMetrics, WidthMetrics]