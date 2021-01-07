import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl


eggs = ctrl.Consequent(np.arange(0, 3000, 1), 'eggs')
temperature = ctrl.Antecedent(np.arange(-20, 40, 1), 'temperature')
pollen = ctrl.Antecedent(np.arange(0, 500, 1), 'pollen')
day_length = ctrl.Antecedent(np.arange(7, 18, 1), 'day_length')
bees_num = ctrl.Antecedent(np.arange(1, 80000, 1), 'bees_num')

pollen.automf(3)
temperature['low'] = fuzz.trimf(temperature.universe, [-20, -20, 0])
temperature['medium'] = fuzz.trimf(temperature.universe, [0, 10, 20])
temperature['high'] = fuzz.trimf(temperature.universe, [20, 40, 40])

day_length['short'] = fuzz.trimf(day_length.universe, [7, 7, 12])
day_length['average'] = fuzz.trimf(day_length.universe, [10, 12.5, 15])
day_length['long'] = fuzz.trimf(day_length.universe, [13, 15, 18])

bees_num['little'] = fuzz.trimf(bees_num.universe, [0, 0, 25000])
bees_num['medium'] = fuzz.trimf(bees_num.universe, [25000, 40000, 55000])
bees_num['a lot'] = fuzz.trimf(bees_num.universe, [55000, 80000, 80000])

eggs['very_little'] = fuzz.trimf(eggs.universe, [0, 0, 600])
eggs['little'] = fuzz.trimf(eggs.universe, [400, 800, 1200])
eggs['medium'] = fuzz.trimf(eggs.universe, [1000, 1500, 2000])
eggs['many'] = fuzz.trimf(eggs.universe, [1800, 2200, 2600])
eggs['a lot'] = fuzz.trimf(eggs.universe, [2400, 3000, 3000])


#bees_num.view()
#eggs.view()
#temperature.view()
#pollen.view()

rule1 = ctrl.Rule(temperature['low'] | day_length['short'] & bees_num['little'] & pollen['poor'], eggs['very_little'])
rule2 = ctrl.Rule(temperature['low'] | day_length['short'] | bees_num['little'] & pollen['poor'], eggs['little'])
rule3 = ctrl.Rule(temperature['medium'] | day_length['average'] | bees_num['medium'] & pollen['average'], eggs['medium'])
rule4 = ctrl.Rule(temperature['high'] | day_length['long'] | bees_num['a lot'] & pollen['good'], eggs['many'])
rule5 = ctrl.Rule(temperature['high'] | bees_num['a lot'] & day_length['long'] & pollen['good'], eggs['a lot'])
rule6 = ctrl.Rule(pollen['poor'], eggs['little'])
eggs_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
laying_eggs = ctrl.ControlSystemSimulation(eggs_ctrl)
laying_eggs.input['temperature'] = 20
laying_eggs.input['pollen'] = 100
laying_eggs.input['day_length'] = 10
laying_eggs.input['bees_num'] = 43000

laying_eggs.compute()
print(laying_eggs.output['eggs'])
eggs.view(sim=laying_eggs)
print("the end")










