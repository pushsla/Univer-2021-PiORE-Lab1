from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QGroupBox, QLabel, QVBoxLayout, QSpinBox, QDoubleSpinBox, QComboBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from data.density import Densities, Density
from data.generation import DataGenerator
from data.estimating import Estimators, Estimator


class EstimateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/estimate_dialog.ui', self)

        self.__samples: list[float] = None

        self.__generator: dict = None
        self.__xrange = None

        self.__estimators: list[dict] = []
        self.__current_estimator: dict = None

        self.__densities: list[dict] = []
        self.__density_selector: QComboBox = None

        self.__data_fig: plt.figure = None
        self.__data_canvas: FigureCanvas = None
        self.__ax = None

        self.__connect_data_slots()
        self.__connect_event_slots()
        self.__connect_matplotlib()

    def exec(self) -> int:
        self.reset_graph()
        return self.exec_()

    def set_samples(self, samples: list[float]):
        self.__samples = samples
        smin = int(min(samples))*100
        smax = int(max(samples))*100
        self.__xrange = [i*0.01 for i in range(smin, smax)]

    def set_generator(self, gen: dict):
        self.__generator = gen

    def add_estimator(self, est: Estimator):
        name = est.get_name()
        self.__estimators.append({
            'name': name,
            'params': est.get_params(),
            'est': est
        })

        self.comboBox_method.addItem(name)

    def add_density(self, den: Density):
        name = den.get_name()
        self.__densities.append({
            'name': name,
            'den': den
        })

    def reset_graph(self):
        if self.__generator and self.__xrange:
            y = [self.__generator['gen'].density(self.__generator['params'], t) for t in self.__xrange]

            self.__data_fig.clear()
            self.__ax = self.__data_fig.add_subplot()
            self.__ax.plot(self.__xrange, y)
            self.__data_canvas.draw()

    def draw_estimator(self):
        if self.__samples and self.__current_estimator:
            est = self.__current_estimator['est']
            y = [est.estimate(self.__current_estimator['params'], self.__samples, t) for t in self.__xrange]

            self.__ax.plot(self.__xrange, y)
            self.__data_canvas.draw()

    def __connect_data_slots(self):
        self.comboBox_method.addItem("")
        for est in Estimators:
            self.add_estimator(est)

        for den in Densities:
            self.add_density(den)

    def __connect_event_slots(self):
        self.comboBox_method.currentIndexChanged.connect(self.__event_new_estimator_selected)
        self.pushButton_clearGraph.clicked.connect(self.reset_graph)
        self.pushButton_drawEstimate.clicked.connect(self.draw_estimator)

    def __connect_density_selector(self):
        self.__density_selector = QComboBox()
        self.__density_selector.addItem("")
        for den in self.__densities:
            self.__density_selector.addItem(den['name'])

    def __event_new_estimator_selected(self):
        selection = self.comboBox_method.currentText()
        est = tuple(filter(lambda x: x['name'] == selection, self.__estimators))
        if est:
            est = est[0]
            self.__current_estimator = est
            self.__connect_current_estimator_params()

    def __connect_current_estimator_params(self):
        def lambda_hack(p, e): return lambda: params.update({p: e.value()})

        count = self.verticalLayout_methodParams.count()
        for i in reversed(range(count)):
            self.verticalLayout_methodParams.itemAt(i).widget().setParent(None)

        for param_name, param_type in (params := self.__current_estimator['params']).items():
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
            elif isinstance(param_type(), Density):
                self.__connect_density_selector()
                edit = self.__density_selector
                edit.valueChanged = edit.currentIndexChanged
                edit.value = lambda: tuple(filter(lambda x: x['name'] == edit.currentText(), self.__densities))[0]['den']

            self.verticalLayout_methodParams.addWidget(label)
            self.verticalLayout_methodParams.addWidget(edit)

            edit.valueChanged.connect(lambda_hack(param_name, edit))

    def __connect_matplotlib(self):
        self.__data_fig = plt.figure()
        self.__data_canvas = FigureCanvas(self.__data_fig)
        self.__ax = None
        self.verticalLayout_plot.addWidget(self.__data_canvas)
