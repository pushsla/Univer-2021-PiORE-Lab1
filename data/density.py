import math


class Density:
    @staticmethod
    def density(x: float) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()


class LinearDensity(Density):
    @staticmethod
    def density(x: float) -> float:
        return 0.5 if abs(x) <= 1 else 0

    @staticmethod
    def get_name() -> str:
        return "Линейное"


class GaussDensity(Density):

    multiplier = 1/(math.sqrt(math.pi*2))

    @staticmethod
    def density(x: float) -> float:
        return GaussDensity.multiplier*math.exp((x**2)/-2)

    @staticmethod
    def get_name() -> str:
        return "Гауссово"


class BiQuadroDensity(Density):
    multiplier = 15/16

    @staticmethod
    def density(x: float) -> float:
        return BiQuadroDensity.multiplier*((1-x**2)*2) if abs(x) <= 1 else 0

    @staticmethod
    def get_name() -> str:
        return "Биквадратное"


class SigmoidDensity(Density):

    multiplier = 2/math.pi

    @staticmethod
    def density(x: float) -> float:
        return SigmoidDensity.multiplier*(1/(math.exp(x)+math.exp(-x)))

    @staticmethod
    def get_name() -> str:
        return "Сигмоидальное"


Densities = [LinearDensity, GaussDensity, BiQuadroDensity, SigmoidDensity]