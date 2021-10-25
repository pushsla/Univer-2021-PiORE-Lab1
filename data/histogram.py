from data.averaging import Averager


class Histogrator:

    @staticmethod
    def split(samples: list, params: dict) -> list[tuple]:
        raise NotImplementedError()

    @staticmethod
    def get_name() -> str:
        raise NotImplementedError()

    @staticmethod
    def get_params() -> dict:
        raise NotImplementedError()


class FreqHistogrator(Histogrator):

    @staticmethod
    def split(samples: list[float], params: dict) -> list[tuple]:

        amount = params['amount']

        s = sorted(samples)
        interval = (s[-1]-s[0])/amount

        result = []  # [(frequency, interval)]
        interval_number = 1
        current_interval = []
        for i in s:
            if i <= s[0]+interval_number*interval:
                current_interval.append(i)
            else:
                result.append((len(current_interval), s[0]+interval_number*interval/2))
                current_interval = []
                interval_number += 1

        return result

    @staticmethod
    def get_name() -> str:
        return "Гистограмма частот"

    @staticmethod
    def get_params() -> dict:
        return {
            'amount': 50,
        }


class RelativeFreqHistogrator(Histogrator):

    @staticmethod
    def split(samples: list, params: dict) -> list[tuple]:
        n = len(samples)
        freq_hist = FreqHistogrator.split(samples, params)

        return [(x[0]/n, x[1]) for x in freq_hist]

    @staticmethod
    def get_name() -> str:
        return "Гистограмма относительных"

    @staticmethod
    def get_params() -> dict:
        return {
            'amount': 50,
        }


Histogrators = [FreqHistogrator, RelativeFreqHistogrator]
