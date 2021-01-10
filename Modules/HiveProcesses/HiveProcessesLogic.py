from GUI.GUI_Logic import *

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib

matplotlib.use('Qt5Agg')

from GUI.GUI_BeesDevelopment import *

import matplotlib.pyplot as plt
from matplotlib import pyplot


class HiveProcessesLogic:
    def __init__(self, amount_of_collectors, temperature_value, day_length_value):
        self.pollen = ctrl.Consequent(np.arange(0, 14, 1), 'pollen')
        self.temperature = ctrl.Antecedent(np.arange(0, 40, 1), 'temperature')
        self.day_length = ctrl.Antecedent(np.arange(8, 18, 1), 'day length')
        self.bees_num = ctrl.Antecedent(np.arange(1, 80000, 1), 'bees num')

        self.temperature['low'] = fuzz.trimf(self.temperature.universe, [0, 0, 15])
        self.temperature['medium'] = fuzz.trimf(self.temperature.universe, [14, 20, 26])
        self.temperature['high'] = fuzz.trimf(self.temperature.universe, [25, 40, 40])

        self.day_length['short'] = fuzz.trimf(self.day_length.universe, [8, 8, 12])
        self.day_length['average'] = fuzz.trimf(self.day_length.universe, [11, 13, 15])
        self.day_length['long'] = fuzz.trimf(self.day_length.universe, [14, 17, 17])

        self.bees_num['little'] = fuzz.trimf(self.bees_num.universe, [0, 0, 26000])
        self.bees_num['medium'] = fuzz.trimf(self.bees_num.universe, [25000, 40000, 55000])
        self.bees_num['a lot'] = fuzz.trimf(self.bees_num.universe, [54000, 80000, 80000])

        self.pollen['none'] = fuzz.trimf(self.pollen.universe, [0, 0, 3])
        self.pollen['very little'] = fuzz.trimf(self.pollen.universe, [2.5, 3, 3.5])
        self.pollen['little'] = fuzz.trimf(self.pollen.universe, [4, 5, 6])
        self.pollen['medium'] = fuzz.trimf(self.pollen.universe, [5.5, 7, 8.5])
        self.pollen['many'] = fuzz.trimf(self.pollen.universe, [8, 10, 12])
        self.pollen['a lot'] = fuzz.trimf(self.pollen.universe, [10, 14, 14])

        #self.pollen.view()

        rule1 = ctrl.Rule(self.day_length['short'] & self.temperature['low'], self.pollen['none'])
        rule2 = ctrl.Rule(self.day_length['short'] & self.temperature['medium'] & self.bees_num['little'], self.pollen['very little'])
        rule3 = ctrl.Rule(self.day_length['short'] & self.temperature['medium'] & (self.bees_num['medium'] | self.bees_num['a lot']), self.pollen['very little'])
        rule4 = ctrl.Rule(self.day_length['average'] & self.temperature['medium'] & self.bees_num['little'], self.pollen['little'])
        rule5 = ctrl.Rule(self.day_length['average'] & self.temperature['medium'] & self.bees_num['medium'], self.pollen['medium'])

        rule6 = ctrl.Rule(self.day_length['average'] & self.temperature['low'] & (self.bees_num['medium'] | self.bees_num['a lot']), self.pollen['very little'])

        rule12 = ctrl.Rule((self.day_length['average'] | self.day_length['long']) & (self.temperature['high'] | self.temperature['medium']) & self.bees_num['medium'], self.pollen['medium'])
        rule13 = ctrl.Rule((self.day_length['average'] | self.day_length['long']) & (self.temperature['high'] | self.temperature['medium']) & (self.bees_num['medium'] | self.bees_num['a lot']), self.pollen['many'])
        rule14 = ctrl.Rule(self.day_length['long'] & self.temperature['high'] & self.bees_num['medium'], self.pollen['many'])
        rule15 = ctrl.Rule(self.day_length['long'] & self.temperature['high'] & self.bees_num['a lot'], self.pollen['a lot'])
        rule16 = ctrl.Rule(self.day_length['short'], self.pollen['very little'])
        rule17 = ctrl.Rule(self.bees_num['little'] & self.temperature['medium'], self.pollen['little'])
        rule18 = ctrl.Rule(self.bees_num['little'], self.pollen['very little'])

        self.collected_pollen_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule12, rule13, rule14, rule15, rule16, rule17, rule18])
        self.collected_pollen = ctrl.ControlSystemSimulation(self.collected_pollen_ctrl)

    def simulate_process(self, amount_of_collectors, temperature_value, day_length_value):
        self.collected_pollen.input['temperature'] = temperature_value
        self.collected_pollen.input['day length'] = day_length_value
        self.collected_pollen.input['bees num'] = amount_of_collectors
        self.collected_pollen.compute()
        self.pollen.view(sim=self.collected_pollen)
        #mngr = plt.get_current_fig_manager()
        #mngr.window.setGeometry(1180, 370, 600, 435)
        #fig = pyplot.gcf()
        #fig.canvas.set_window_title('Number of pollen generated')
        #
        #plt.close('all')


if __name__ == '__main__':
    hive = HiveProcessesLogic(0, 0, 0)
    hive.simulate_process(20000, 20, 12)
