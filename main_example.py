from BeeDevelopmentModule import BeeDevelopmentModule
from Defines import DEBUG_PRINT

simulate_days = 365  # zasieg dni symulacji

# wartości startowe
eggs_start = 1000
larvas_start = 1000
before_pupas_start = 1000
pupas_start = 1000
imagos_start = 1000

new_eggs = 1000  # tylko dla przykładu

bee_hive = BeeDevelopmentModule(eggs_start, larvas_start, before_pupas_start, pupas_start, imagos_start)
for day in range(1, simulate_days):
    bee_hive.simulate_day(new_eggs)  # docelowo to bedzie tutaj output z logiki rozmytej
    if DEBUG_PRINT:
        print(str(day) + "------------------------------")
