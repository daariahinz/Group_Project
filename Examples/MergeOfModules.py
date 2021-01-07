from GUI.GUI_BeesDevelopment import *

##########################TODO:#############################
##Przygotowane do połączenia modelu logiki i rozwoju pszczół
simulation = Simulation()
for day in range(1, simulate_days):
    #eggs = output logika
    simulation.simple_run(eggs)

# Na koniec możliwość wyświetlenia wykresu po całej symulacji
simulation.window_to_generate_sumup()
window.mainloop()