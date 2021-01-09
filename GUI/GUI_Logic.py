from GUI.GUI_BeesDevelopment import *
from Examples.SimulationConstans import *

from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout,
                             QWidget, QSlider, QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import pyqtgraph as pg
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import pyplot
from PyQt5.QtCore import Qt, pyqtSlot




def changed_value(slider, label, string, laying_eggs):
    size = slider.value()
    label.setText(str(size))
    laying_eggs.input[string] = slider.value()

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class LogicInterface(QWidget):
    def __init__(self, sim_eggs, eggs, bees, pollen, temperature, day):
        super(LogicInterface, self).__init__(None)

        grid = QGridLayout()
        self.simulation = Simulation()
        self.laying_eggs = sim_eggs
        self.eggs = eggs
        self.bees_num_value = bees
        self.pollen_value = pollen
        self.temperature_value = temperature
        self.day_length_value = day

        self.temperature = QSlider
        self.pollen = QSlider
        self.temperature = self.create_slider(0,40,1)
        self.label_temp = QLabel("0");
        self.pollen = self.create_slider(0,14,1)
        self.label_pollen = QLabel("0");
        self.bees = self.create_slider(0, 80000, 1000)
        self.label_bees = QLabel("0");
        self.day = self.create_slider(8, 18, 1)
        self.label_day = QLabel("8");

        button_generate = QPushButton('Generate', self)
        button_generate.clicked.connect(self.generate_eggs)

        button_temperature = QPushButton('Show dependence on temperature', self)
        button_temperature.clicked.connect(self.on_click_temp)

        button_day = QPushButton('Show dependence on day length', self)
        button_day.clicked.connect(self.on_click_day)

        button_pollen = QPushButton('Show dependence on pollen amount', self)
        button_pollen.clicked.connect(self.on_click_pollen)

        button_start = QPushButton('Start simulation', self)
        button_start.clicked.connect(self.on_click_start)

        button_inputs = QPushButton('Show membership function', self)
        button_inputs.clicked.connect(self.on_click_show_plots)

        self.temperature.valueChanged.connect(lambda: changed_value(self.temperature, self.label_temp, 'temperature', self.laying_eggs))
        self.pollen.valueChanged.connect(lambda: changed_value(self.pollen, self.label_pollen, 'pollen', self.laying_eggs))
        self.bees.valueChanged.connect(lambda: changed_value(self.bees, self.label_bees, 'bees num', self.laying_eggs))
        self.day.valueChanged.connect(lambda: changed_value(self.day, self.label_day, 'day length', self.laying_eggs))

        grid.addWidget(self.create_example_group("Temperatura [°C]", self.temperature, self.label_temp), 0, 0)
        grid.addWidget(self.create_example_group("Pokarm [kg]", self.pollen, self.label_pollen), 1, 0)
        grid.addWidget(self.create_example_group("Liczba pszczół [os]", self.bees, self.label_bees), 2, 0)
        grid.addWidget(self.create_example_group("Długość dnia [h]", self.day, self.label_day), 3, 0)
        grid.addWidget(button_generate, 4, 0)
        grid.addWidget(button_inputs, 5, 0)
        grid.addWidget(button_temperature, 6, 0)
        grid.addWidget(button_day, 7, 0)
        grid.addWidget(button_pollen, 8, 0)
        grid.addWidget(button_start, 9, 0)
        graphWidget = pg.PlotWidget()

        self.setLayout(grid)
        self.resize(400, 300)

    def create_example_group(self, name, slider, label):
        groupBox = QGroupBox(name)
        vbox = QVBoxLayout()
        vbox.addWidget(slider)
        vbox.addWidget(label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox

    def create_slider(self, min, max, tick):
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(tick)
        slider.setSingleStep(tick)
        slider.setMinimum(min)
        slider.setMaximum(max)
        return slider

    def on_apply(self):
        changed_value(self.temperature, self.label_temp, 'temperature', self.laying_eggs)
        changed_value(self.pollen, self.label_pollen, 'pollen', self.laying_eggs)
        changed_value(self.bees, self.label_bees, 'bees num', self.laying_eggs)
        changed_value(self.day, self.label_day, 'day length', self.laying_eggs)

    @pyqtSlot()
    def on_click_start(self):
         self.generate_eggs()
         plt.close('all')
         for day in range(1, NUM_OF_SIMULATED_DAYS):
            eggs = int(self.laying_eggs.output['eggs'])
            if DEBUG_PRINT:
                print("Number of eggs generated : " + str(eggs))
            self.simulation.simple_run(eggs)
         self.simulation.window_to_generate_sumup()
         window.mainloop()

    @pyqtSlot()
    def on_click_show_plots(self):
         plt.close('all')
         self.bees_num_value.view()
         self.temperature_value.view()
         self.pollen_value.view()
         self.day_length_value.view()

    @pyqtSlot()
    def generate_eggs(self):
        plt.close('all')
        self.on_apply()
        self.laying_eggs.compute()
        self.eggs.view(sim=self.laying_eggs)
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(1180, 370, 600, 435)
        fig = pyplot.gcf()
        fig.canvas.set_window_title('Number of eggs generated')

    @pyqtSlot()
    def on_click_temp(self):
        self.on_apply()
        plt.close('all')
        score_temp = []
        temp_sim = []
        for i in range(0, 40):
            self.laying_eggs.input['temperature'] = i
            temp_sim.append(i)
            self.laying_eggs.compute()
            y = self.laying_eggs.output['eggs']
            score_temp.append(y)
        plt.plot(temp_sim, score_temp)
        plt.show()
        mngr2 = plt.get_current_fig_manager()
        mngr2.window.setGeometry(1180, 370, 600, 435)
        fig = pyplot.gcf()
        fig.canvas.set_window_title('Temperature dependence graph')

    @pyqtSlot()
    def on_click_day(self):
        self.on_apply()
        plt.close('all')
        score_temp = []
        temp_sim = []
        for i in range(8, 18):
            self.laying_eggs.input['day length'] = i
            temp_sim.append(i)
            self.laying_eggs.compute()
            y = self.laying_eggs.output['eggs']
            score_temp.append(y)
        plt.plot(temp_sim, score_temp)
        plt.show()
        mngr2 = plt.get_current_fig_manager()
        mngr2.window.setGeometry(1180, 370, 600, 435)
        fig = pyplot.gcf()
        fig.canvas.set_window_title('Day Length dependence graph')

    @pyqtSlot()
    def on_click_pollen(self):
        self.on_apply()
        plt.close('all')
        score_temp = []
        temp_sim = []
        for i in range(0, 14):
            self.laying_eggs.input['pollen'] = i
            temp_sim.append(i)
            self.laying_eggs.compute()
            y = self.laying_eggs.output['eggs']
            score_temp.append(y)
        plt.plot(temp_sim, score_temp)
        plt.show()
        mngr2 = plt.get_current_fig_manager()
        mngr2.window.setGeometry(1180, 370, 600, 435)
        fig = pyplot.gcf()
        fig.canvas.set_window_title('Day Length dependence graph')
