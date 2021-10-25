from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QSpinBox, QDoubleSpinBox, QComboBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from data.histogram import Histogrators, Histogrator
from data.averaging import Averagers, Averager


class HistogramDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/histogram_dialog.ui', self)

        self.__samples: list[float] = None
        self.__current_histo_data = None

        self.__histogrators = []
        self.__current_histogrator = None

        self.__averagers = []
        self.__averager_selector: QComboBox = None

        self.__data_fig: plt.figure = None
        self.__data_canvas: FigureCanvas = None

        self.__connect_data_slots()
        self.__connect_event_clost()
        self.__connect_matplotlib()

    def set_samples(self, samples: list[float]):
        self.__samples = samples

    def add_histogrator(self, hgt: Histogrator):
        params = hgt.get_params()
        name = hgt.get_name()
        self.__histogrators.append({
            'name': name,
            'params': params,
            'hgt': hgt
        })

        self.comboBox_intervalsType.addItem(name)

    def add_averager(self, avg: Averager):
        name = avg.get_name()
        self.__averagers.append({
            'name': name,
            'avg': avg
        })

    def create_histogram(self):
        if self.__samples:
            hgt = self.__current_histogrator['hgt']
            params = self.__current_histogrator['params']
            self.__current_histo_data = hgt.split(self.__samples, params)

            self.draw_histogram()

    def draw_histogram(self):
        if self.__current_histo_data:

            labels = [str(x[1]) for x in self.__current_histo_data]
            values = [x[0] for x in self.__current_histo_data]

            self.__data_fig.clear()
            ax = self.__data_fig.add_subplot()
            ax.bar(labels, values)
            self.__data_canvas.draw()

    def __connect_data_slots(self):
        self.comboBox_intervalsType.addItem('')
        for hgt in Histogrators:
            self.add_histogrator(hgt)

        for avg in Averagers:
            self.add_averager(avg)

    def __connect_event_clost(self):
        self.comboBox_intervalsType.currentIndexChanged.connect(self.__event_new_histogrator_selected)
        self.pushButton_genIntervals.clicked.connect(self.create_histogram)

    def __connect_averager_selector(self):
        self.__averager_selector = QComboBox()
        self.__averager_selector.addItem('')
        for avg in self.__averagers:
            self.__averager_selector.addItem(avg['name'])

    def __event_new_histogrator_selected(self):
        selection = self.comboBox_intervalsType.currentText()
        hgt = tuple(filter(lambda x: x['name'] == selection, self.__histogrators))
        if hgt:
            hgt = hgt[0]
            self.__current_histogrator = hgt
            self.__connect_current_histogrator_params()

    def __connect_current_histogrator_params(self):
        def lambda_hack(p, e): return lambda: params.update({p: e.value()})

        count = self.verticalLayout_histogratorParams.count()
        for i in reversed(range(count)):
            self.verticalLayout_histogratorParams.itemAt(i).widget().setParent(None)

        for param_name, param_type in (params := self.__current_histogrator['params']).items():
            label = QLabel(param_name)
            edit = QLabel("#Unsupported: {}".format(type(param_type)))
            edit.valueChanged = edit.objectNameChanged  # dirty hack
            edit.value = edit.text()  # dirty hack
            if isinstance(param_type, int):
                edit = QSpinBox()
                edit.setValue(param_type)
                edit.setMinimum(-100)
                edit.setMaximum(100)
                edit.setSingleStep(1)
            elif isinstance(param_type, float):
                edit = QDoubleSpinBox()
                edit.setValue(param_type)
                edit.setMinimum(-100.0)
                edit.setMaximum(100.0)
                edit.setSingleStep(0.1)
            elif isinstance(param_type(), Averager):
                self.__connect_averager_selector()
                edit = self.__averager_selector
                edit.valueChanged = edit.currentIndexChanged
                edit.value = lambda: tuple(filter(lambda x: x['name'] == edit.currentText(), self.__averagers))[0]['avg']

            self.verticalLayout_histogratorParams.addWidget(label)
            self.verticalLayout_histogratorParams.addWidget(edit)

            edit.valueChanged.connect(lambda_hack(param_name, edit))

    def __connect_matplotlib(self):
        self.__data_fig = plt.figure()
        self.__data_canvas = FigureCanvas(self.__data_fig)
        self.verticalLayout_histogram.addWidget(self.__data_canvas)
