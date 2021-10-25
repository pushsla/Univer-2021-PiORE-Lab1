class Averager:
    @staticmethod
    def avg(samples: list[float]) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()


class MeanAverager(Averager):
    @staticmethod
    def avg(samples: list[float]) -> float:
        return sum(samples)/len(samples)

    @staticmethod
    def get_name() -> str:
        return "Среднее"


class MedianAverager(Averager):
    @staticmethod
    def avg(samples: list[float]) -> float:
        s = sorted(samples)
        pivot = len(s)//2
        return s[pivot] if len(s) % 2 == 1 else (s[pivot - 1] + s[pivot]) / 2

    @staticmethod
    def get_name() -> str:
        return "Медиана"


Averagers = [MedianAverager, MeanAverager]