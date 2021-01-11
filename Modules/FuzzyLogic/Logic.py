import skfuzzy as fuzz
from skfuzzy import control as ctrl
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from GUI.GUI_Logic import *

class Logic():
    def __init__(self):
        self.simulate_eggs = ctrl.Consequent(np.arange(0, 3001, 1), 'eggs')
        self.temperature = ctrl.Antecedent(np.arange(-5, 41, 1), 'temperature')
        self.pollen = ctrl.Antecedent(np.arange(0, 15, 1), 'pollen')
        self.day_length = ctrl.Antecedent(np.arange(7, 18, 1), 'day length')
        self.bees_num = ctrl.Antecedent(np.arange(1, 80001, 1), 'bees num')

        self.pollen['poor'] = fuzz.trimf(self.pollen.universe, [0, 0, 5])
        self.pollen['average'] = fuzz.trimf(self.pollen.universe, [3, 7, 11])
        self.pollen['good'] = fuzz.trimf(self.pollen.universe, [9, 14, 14])

        self.temperature['low'] = fuzz.trimf(self.temperature.universe, [-5, -5, 15])
        self.temperature['medium'] = fuzz.trimf(self.temperature.universe, [12, 19, 26])
        self.temperature['high'] = fuzz.trimf(self.temperature.universe, [23, 40, 40])

        self.day_length['short'] = fuzz.trimf(self.day_length.universe, [7, 7, 11])
        self.day_length['average'] = fuzz.trimf(self.day_length.universe, [10, 12, 14])
        self.day_length['long'] = fuzz.trimf(self.day_length.universe, [13, 17, 17])

        self.bees_num['little'] = fuzz.trimf(self.bees_num.universe, [0, 0, 30000])
        self.bees_num['medium'] = fuzz.trimf(self.bees_num.universe, [25000, 42500, 60000])
        self.bees_num['a lot'] = fuzz.trimf(self.bees_num.universe, [55000, 80000, 80000])

        self.simulate_eggs['none'] = fuzz.trimf(self.simulate_eggs.universe, [0, 0, 50])
        self.simulate_eggs['very little'] = fuzz.trimf(self.simulate_eggs.universe, [49, 250, 500])
        self.simulate_eggs['little'] = fuzz.trimf(self.simulate_eggs.universe, [450, 750, 1050])
        self.simulate_eggs['medium'] = fuzz.trimf(self.simulate_eggs.universe, [1000, 1300, 1600])
        self.simulate_eggs['many'] = fuzz.trimf(self.simulate_eggs.universe, [1500, 1900, 2300])
        self.simulate_eggs['a lot'] = fuzz.trimf(self.simulate_eggs.universe, [2200, 3000, 3000])

        rule1 = ctrl.Rule(self.day_length['short'] & self.temperature['low'], self.simulate_eggs['none'])
        rule2 = ctrl.Rule(self.day_length['short'] & self.temperature['medium'] & self.pollen['average'],
                          self.simulate_eggs['little'])
        rule3 = ctrl.Rule(
            self.day_length['short'] & self.temperature['high'] & (self.pollen['average'] | self.pollen['good']),
            self.simulate_eggs['medium'])
        rule4 = ctrl.Rule(self.day_length['short'] & self.temperature['medium'] & self.pollen['good'],
                          self.simulate_eggs['medium'])
        rule5 = ctrl.Rule(
            self.day_length['long'] & self.temperature['low'] & (self.pollen['average'] | self.pollen['good']),
            self.simulate_eggs['very little'])
        rule6 = ctrl.Rule(
            self.day_length['average'] & self.temperature['low'] & (self.pollen['average'] | self.pollen['good']),
            self.simulate_eggs['very little'])
        rule7 = ctrl.Rule(self.day_length['average'] & self.temperature['medium'] & self.pollen['average'],
                          self.simulate_eggs['little'])
        rule8 = ctrl.Rule(self.day_length['average'] & self.temperature['medium'] & self.pollen['good'],
                          self.simulate_eggs['medium'])
        rule9 = ctrl.Rule(
            self.day_length['average'] & self.temperature['high'] & (self.pollen['average'] | self.pollen['good']),
            self.simulate_eggs['many'])
        rule10 = ctrl.Rule(self.day_length['long'] & self.temperature['medium'] & (self.pollen['average']),
                           self.simulate_eggs['many'])
        rule11 = ctrl.Rule((self.day_length['average'] | self.day_length['long']) & (
                self.temperature['high'] | self.temperature['medium']) &
                           (self.pollen['average'] | self.pollen['good']) & self.bees_num['little'],
                           self.simulate_eggs['little'])
        rule12 = ctrl.Rule((self.day_length['average'] | self.day_length['long']) & (
                self.temperature['high'] | self.temperature['medium']) &
                           (self.pollen['average'] | self.pollen['good']) & self.bees_num['medium'],
                           self.simulate_eggs['medium'])
        rule13 = ctrl.Rule((self.day_length['average'] | self.day_length['long']) & (
                self.temperature['high'] | self.temperature['medium']) &
                           (self.pollen['average'] | self.pollen['good']) & self.bees_num['a lot'],
                           self.simulate_eggs['a lot'])
        rule14 = ctrl.Rule(self.day_length['long'] & self.temperature['high'] & self.pollen['average'],
                           self.simulate_eggs['many'])
        rule15 = ctrl.Rule(self.day_length['long'] & self.temperature['high'] & self.pollen['good'],
                           self.simulate_eggs['a lot'])
        rule16 = ctrl.Rule(self.bees_num['little'], self.simulate_eggs['none'])
        rule17 = ctrl.Rule(self.bees_num['little'] & self.pollen['poor'], self.simulate_eggs['none'])
        rule18 = ctrl.Rule(self.pollen['poor'], self.simulate_eggs['none'])

        eggs_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11,
                                        rule12, rule13, rule14, rule15, rule16, rule17, rule18])
        self.laying_eggs = ctrl.ControlSystemSimulation(eggs_ctrl)

    def show_inputs(self):
        self.bees_num.view()
        self.simulate_eggs.view()
        self.temperature.view()
        self.pollen.view()
        self.day_length.view()

    def simulate_logic(self):
        self.laying_eggs.input['temperature'] = 1
        self.laying_eggs.input['pollen'] = 3
        self.laying_eggs.input['day length'] = 9
        self.laying_eggs.input['bees num'] = 15000
        self.laying_eggs.compute()

        app = QApplication(sys.argv)
        clock = LogicInterface(self.laying_eggs, self.simulate_eggs, self.bees_num,
                               self.pollen, self.temperature, self.day_length)
        clock.show()
        sys.exit(app.exec_())
