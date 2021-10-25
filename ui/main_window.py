import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel, QSpinBox, QDoubleSpinBox

from data.generation import Generators, DataGenerator
from ui.histogram_dialog import HistogramDialog
from ui.metrics_dialog import MetricsDialog
from ui.estimate_dialog import EstimateDialog


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/main_window.ui', self)

        self.__generators = []
        self.__current_samples = []
        self.__current_generator: dict = None

        self.__data_fig: plt.figure = None
        self.__data_canvas: FigureCanvas = None

        self.__connect_data_slots()
        self.__connect_event_slots()
        self.__connect_matplotlib()

    def add_generator(self, gen: DataGenerator):
        params = gen.get_params()
        name = gen.get_name()
        self.__generators.append({
            'name': name,
            'params': params,
            'gen': gen,
        })

        self.comboBox_dataGenerator.addItem(name)

    def generate_samples(self):
        if self.__current_generator:
            gen = self.__current_generator['gen']
            params = self.__current_generator['params']
            amount = self.spinBox_dataAmount.value()
            self.__current_samples = gen.generate(params, amount)

            self.groupBox_dataInspection.setEnabled(True)
            self.draw_samples()

    def draw_samples(self):
        if self.__current_samples:
            self.__data_fig.clear()
            ax = self.__data_fig.add_subplot()
            ax.get_xaxis().set_visible(False)
            ax.violinplot(sorted(self.__current_samples))
            self.__data_canvas.draw()

    def inspect_histogram(self):
        dlg = HistogramDialog(self)
        dlg.set_samples(self.__current_samples)
        dlg.exec()

    def inspect_metrics(self):
        dlg = MetricsDialog(self)
        dlg.set_samples(self.__current_samples)
        dlg.exec()

    def inspect_estimate(self):
        dlg = EstimateDialog(self)
        dlg.set_samples(self.__current_samples)
        dlg.set_generator(self.__current_generator)
        dlg.exec()

    def __connect_data_slots(self):
        self.comboBox_dataGenerator.addItem('')
        for gen in Generators:
            self.add_generator(gen)

    def __connect_event_slots(self):
        self.comboBox_dataGenerator.currentIndexChanged.connect(self.__event_new_generator_selected)
        self.pushButton_dataGenerate.clicked.connect(self.generate_samples)
        self.pushButton_inspectionHistogram.clicked.connect(self.inspect_histogram)
        self.pushButton_inspectionMetrics.clicked.connect(self.inspect_metrics)
        self.pushButton_inspectionEstimate.clicked.connect(self.inspect_estimate)

    def __event_new_generator_selected(self):
        selection = self.comboBox_dataGenerator.currentText()
        gen = tuple(filter(lambda x: x['name'] == selection, self.__generators))
        if gen:
            gen = gen[0]
            self.__current_generator = gen
            self.__connect_current_generator_params()

    def __connect_current_generator_params(self):
        def lambda_hack(p, e): return lambda: params.update({p: e.value()})

        count = self.verticalLayout_DataParams.count()
        for i in reversed(range(count)):
            self.verticalLayout_DataParams.itemAt(i).widget().setParent(None)

        for param_name, param_type in (params := self.__current_generator['params']).items():
            label = QLabel(param_name)
            edit = QLabel("#Unsupported: {}".format(type(param_type)))
            edit.value = edit.text  # dirty hack
            edit.valueChanged = edit.objectNameChanged  # dirty hack
            if isinstance(param_type, int):
                edit = QSpinBox()
                edit.setMinimum(-100)
                edit.setMaximum(100)
                edit.setValue(param_type)
                edit.setSingleStep(1)
            elif isinstance(param_type, float):
                edit = QDoubleSpinBox()
                edit.setMinimum(-100.0)
                edit.setMaximum(100.0)
                edit.setValue(param_type)
                edit.setSingleStep(0.1)

            self.verticalLayout_DataParams.addWidget(label)
            self.verticalLayout_DataParams.addWidget(edit)

            edit.valueChanged.connect(lambda_hack(param_name, edit))

    def __connect_matplotlib(self):
        self.__data_fig = plt.figure()
        self.__data_canvas = FigureCanvas(self.__data_fig)
        self.verticalLayout_dataDiagram.addWidget(self.__data_canvas)
