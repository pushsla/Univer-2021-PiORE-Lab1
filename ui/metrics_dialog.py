from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QGroupBox, QLabel, QVBoxLayout

from data.metrics import Metrics, Metric


class MetricsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/metrics_dialog.ui', self)

        self.__samples: list[float] = None

        self.__connect_data_slots()
        self.__connect_event_slots()

    def exec(self) -> int:
        self.calculate_metrics()
        return self.exec_()

    def set_samples(self, samples: list[float]):
        self.__samples = samples

    def calculate_metrics(self):
        if self.__samples:
            for mtr in Metrics:
                name = mtr.get_name()
                params = mtr.get_params()
                if params:
                    raise NotImplementedError()

                box = QGroupBox()
                box.setTitle(name)

                value = QLabel(parent=box)
                value.setMargin(30)
                font = value.font()
                font.setPointSize(16)
                value.setFont(font)
                value.setText(str(mtr.calculate(params, self.__samples)))

                self.verticalLayout_metrics.addWidget(box)

    def __connect_data_slots(self):
        pass

    def __connect_event_slots(self):
        pass

