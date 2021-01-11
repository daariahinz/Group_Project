import pandas as pd
import numpy as np

from Modules.BeesDevelopment.BeesDevelopment import BeesDevelopment
from Modules.BeesDevelopment.Defines import *
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math


class Simulation():
    def __init__(self):
        #### wartości startowe ####
        eggs_start = EGGS_START
        larvas_start = LARVAS_START
        before_pupas_start = BFORE_PUPAS_START
        pupas_start = PUPAS_START
        imagos_start = IMAGOS_START
        workers = WORKERS
        self.names = ["Eggs", "Larvas", "Before pupas", "Before pupas drone", "Pupas", "Pupas drone", "Imago young workers",
         "Imago workers nectar collectors", "Imago workers pollen collectors", "Imago drones"]
        self.bee_hive = BeesDevelopment(eggs_start, larvas_start, before_pupas_start, pupas_start, imagos_start,workers)
        self.eggs =[self.bee_hive.eggs_counter]
        self.income_eggs =[]
        self.larvas=[self.bee_hive.larva_counter]
        self.before_pupas=[self.bee_hive.before_pupa_counter]
        self.before_pupas_drone =[self.bee_hive.before_pupa_drone_counter]
        self.pupas=[self.bee_hive.pupa_counter]
        self.pupas_drone=[self.bee_hive.pupa_drone_counter]
        self.imago_young = [self.bee_hive.imago_worker_young_counter]
        self.imago_nectar=[self.bee_hive.nectar_collectors]
        self.imago_pollen=[self.bee_hive.pollen_collectors]
        self.imago_drone=[self.bee_hive.imago_drone_counter]
        self.prev_count=[]
        self.current_count=[]
        self.fig1 = plt.Figure()
        self.fig2 = plt.Figure()
        self.fig3 = plt.Figure()
        self.fig4 = plt.Figure()
        self.fig5 = plt.Figure()
        self.fig6 = plt.Figure()
        self.fig7 = plt.Figure()
        self.fig8 = plt.Figure()
        self.fig9 = plt.Figure()
        self.fig10 = plt.Figure()
        self.fig11 = plt.Figure()
        self.fig12 = plt.Figure()

    def init_GUI(self):
        self.eggs_label = tk.Label(window, text="Puts number of new eggs:")
        self.eggs_label.grid(column=0, row=0)
        self.eggs_entry = tk.Entry(window, width=8)
        self.eggs_entry.grid(column=1, row=0, sticky="W")
        self.init_checkboxes_interface()
        generate_btn = tk.Button(window, text="Generate", command=self.generate_plot_with_entry)
        generate_btn.grid(column=1, row=15)

    def init_checkboxes_interface(self):
        row = 1
        self.gen_label = tk.Label(window, text="Choose to generate:")
        self.gen_label.grid(column=0, row=row, sticky="W")

        self.chk_eggs = tk.BooleanVar()
        self.chk_eggs.set(False)  # set check state
        chk1 = tk.Checkbutton(window, text='eggs chart', var=self.chk_eggs)
        chk1.grid(column=1, row=row + 1, sticky="W")

        self.chk_larvas = tk.BooleanVar()
        self.chk_larvas.set(False)  # set check state
        chk2 = tk.Checkbutton(window, text='larvas chart', var=self.chk_larvas)
        chk2.grid(column=1, row=row + 2, sticky="W")

        self.chk_larvas_drone = tk.BooleanVar()
        self.chk_larvas_drone.set(False)  # set check state
        chk3 = tk.Checkbutton(window, text='larvas drone chart', var=self.chk_larvas_drone)
        chk3.grid(column=1, row=row + 3, sticky="W")

        self.chk_before_pupa = tk.BooleanVar()
        self.chk_before_pupa.set(False)  # set check state
        chk4 = tk.Checkbutton(window, text='before pupa chart', var=self.chk_before_pupa)
        chk4.grid(column=1, row=4, sticky="W")

        self.chk_before_pupa_drone = tk.BooleanVar()
        self.chk_before_pupa_drone.set(False)  # set check state
        chk5 = tk.Checkbutton(window, text='before pupa drone chart', var=self.chk_before_pupa_drone)
        chk5.grid(column=1, row=row + 5, sticky="W")

        self.chk_pupa = tk.BooleanVar()
        self.chk_pupa.set(False)  # set check state
        chk6 = tk.Checkbutton(window, text='pupa chart', var=self.chk_pupa)
        chk6.grid(column=1, row=row + 6, sticky="W")

        self.chk_pupa_drone = tk.BooleanVar()
        self.chk_pupa_drone.set(False)  # set check state
        chk7 = tk.Checkbutton(window, text='pupa drone chart', var=self.chk_pupa_drone)
        chk7.grid(column=1, row=row + 7, sticky="W")

        self.chk_imago_worker_young = tk.BooleanVar()
        self.chk_imago_worker_young.set(False)  # set check state
        chk8 = tk.Checkbutton(window, text='imago worker young chart', var=self.chk_imago_worker_young)
        chk8.grid(column=1, row=row + 8, sticky="W")

        self.chk_imago_worker_nectar_collectors = tk.BooleanVar()
        self.chk_imago_worker_nectar_collectors.set(False)  # set check state
        chk9 = tk.Checkbutton(window, text='imago worker nektar collectors chart',
                              var=self.chk_imago_worker_nectar_collectors)
        chk9.grid(column=1, row=row + 9, sticky="W")

        self.chk_imago_drone = tk.BooleanVar()
        self.chk_imago_drone.set(False)  # set check state
        chk10 = tk.Checkbutton(window, text='imago drone chart', var=self.chk_imago_drone)
        chk10.grid(column=1, row=row + 10, sticky="W")

        self.chk_imago_worker_pollen_collectors = tk.BooleanVar()
        self.chk_imago_worker_pollen_collectors.set(False)  # set check state
        chk11 = tk.Checkbutton(window, text='imago worker pollen collectors chart',
                               var=self.chk_imago_worker_pollen_collectors)
        chk11.grid(column=1, row=row + 11, sticky="W")

        self.chk_change = tk.BooleanVar()
        self.chk_change.set(False)  # set check state
        chk12 = tk.Checkbutton(window, text='change view', var=self.chk_change)
        chk12.grid(column=1, row=row + 12, sticky="W")

        e = tk.Label(window, text="")
        e.grid(column=0, row=row + 13)
        
    def update_tables(self):
        self.eggs.append(self.bee_hive.eggs_counter)
        self.larvas.append(self.bee_hive.larva_counter)
        self.before_pupas.append(self.bee_hive.before_pupa_counter)
        self.before_pupas_drone.append(self.bee_hive.before_pupa_drone_counter)
        self.pupas.append(self.bee_hive.pupa_counter)
        self.pupas_drone.append(self.bee_hive.pupa_drone_counter)
        self.imago_young.append(self.bee_hive.imago_worker_young_counter)
        self.imago_nectar.append(self.bee_hive.nectar_collectors)
        self.imago_pollen.append(self.bee_hive.pollen_collectors)
        self.imago_drone.append(self.bee_hive.imago_drone_counter)
    def xlabel(self, max):
        xlabel = []
        shift = math.ceil(max/XSHIFT)
        for i in range(0,XSHIFT):
            xlabel.append(i*shift)
        return xlabel

    def generate_eggs_chart(self):
        plt.close(self.fig1)
        self.fig1 = plt.figure(1)
        plt.title("Eggs")
        freq_series = pd.Series(self.eggs)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.eggs)) ,rotation=90)
        plt.show(block=False)
        plt.close(self.fig12)
        self.fig12 = plt.figure(12)
        plt.title("Generated eggs per day")
        freq_series = pd.Series(self.income_eggs)
        plt.xticks(self.xlabel(len(self.income_eggs)) ,rotation=90)
        ax = freq_series.plot(kind='bar')
        plt.savefig("generated_eggs_plot.png")


    def generate_larvas_chart(self):
        plt.close(self.fig2)
        self.fig2 = plt.figure(2)
        plt.title("Larvas")
        freq_series = pd.Series(self.larvas)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.larvas)), rotation=90)
        # plt.savefig("Plots/larvas_plot.png")
        plt.show(block=False)
        
    def generate_before_pupa_chart(self):
        plt.close(self.fig3)
        self.fig3 = plt.figure(3)
        plt.title("Before pupas")
        freq_series = pd.Series(self.before_pupas)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.before_pupas)), rotation=90)
        # plt.savefig("Plots/before_pupas_plot.png")
        plt.show(block=False)
        
    def generate_before_pupa_drone_chart(self):
        plt.close(self.fig4)
        self.fig4 = plt.figure(4)
        plt.title("Before pupas drone")
        freq_series = pd.Series(self.before_pupas_drone)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.before_pupas_drone)), rotation=90)
        # plt.savefig("Plots/before_pupas_drone_plot.png")
        plt.show(block=False)
        
    def generate_pupa_chart(self):
        plt.close(self.fig5)
        self.fig5 = plt.figure(5)
        plt.title("Pupas")
        freq_series = pd.Series(self.pupas)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.pupas)), rotation=90)
        # plt.savefig("Plots/pupas_plot.png")
        plt.show(block=False)
        
    def generate_pupa_chart(self):
        plt.close(self.fig6)
        self.fig6 = plt.figure(6)
        plt.title("Pupas drone")
        freq_series = pd.Series(self.pupas_drone)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.pupas_drone)), rotation=90)
        # plt.savefig("Plots/pupas_drone_plot.png")
        plt.show(block=False)
        
    def generate_imago_young_chart(self):
        plt.close(self.fig7)
        self.fig7 = plt.figure(7)
        plt.title("Imago young")
        freq_series = pd.Series(self.imago_young)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.imago_young)), rotation=90)
        # plt.savefig("Plots/imago_young_plot.png")
        plt.show(block=False)
        
    def generate_imago_nectar_chart(self):
        plt.close(self.fig8)
        self.fig8 = plt.figure(8)
        plt.title("Imago nectar collectors")
        freq_series = pd.Series(self.imago_nectar)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.imago_nectar)), rotation=90)
        # plt.savefig("Plots/imago_nectar_plot.png")
        plt.show(block=False)
        
    def generate_imago_pollen_chart(self):
        plt.close(self.fig9)
        self.fig9 = plt.figure(9)
        plt.title("Imago pollen collectors")
        freq_series = pd.Series(self.imago_pollen)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.imago_pollen)), rotation=90)
        # plt.savefig("Plots/imago_pollen_plot.png")
        plt.show(block=False)
        
    def generate_imago_drone_chart(self):
        plt.close(self.fig10)
        self.fig10 = plt.figure(10)
        plt.title("Imago drone")
        freq_series = pd.Series(self.imago_drone)
        ax = freq_series.plot(kind='bar')
        plt.xticks(self.xlabel(len(self.drone)), rotation=90)
        # plt.savefig("Plots/imago_drone_plot.png")
        plt.show(block=False)
        
    def generate_change_view(self):
        X = np.arange(10)
        plt.close(self.fig11)
        self.fig11 = plt.figure(11, figsize=(10,8))
        ax = plt.subplot(1,1,1)
        plt.title("Comparision day "+str(len(self.imago_drone)-1)+" with day "+str(len(self.imago_drone)-2))
        ax.bar(X + 0.00, self.prev_count, color='b', width=0.20)
        ax.bar(X + 0.20, self.current_count, color='g', width=0.20)
        plt.xticks(X, self.names, rotation='vertical')
        plt.subplots_adjust(bottom=0.30)
        blue_patch = mpatches.Patch(color='b', label='Day '+str(len(self.imago_drone)-2))
        green_patch = mpatches.Patch(color='g', label='Day '+str(len(self.imago_drone)-1) )
        plt.legend(handles=[blue_patch,green_patch])
        plt.show(block=False)
            
    def generate_plot_with_entry(self):
        en =self.eggs_entry.get()
        if en != "":
            self.prev_count = [self.bee_hive.eggs_counter,self.bee_hive.larva_counter,self.bee_hive.before_pupa_counter,self.bee_hive.before_pupa_drone_counter,self.bee_hive.pupa_counter,self.bee_hive.pupa_drone_counter,self.bee_hive.imago_worker_young_counter,self.bee_hive.nectar_collectors,self.bee_hive.pollen_collectors,self.bee_hive.imago_drone_counter]
            self.bee_hive.simulate_day(int(en))
            self.current_count = [self.bee_hive.eggs_counter,self.bee_hive.larva_counter,self.bee_hive.before_pupa_counter,self.bee_hive.before_pupa_drone_counter,self.bee_hive.pupa_counter,self.bee_hive.pupa_drone_counter,self.bee_hive.imago_worker_young_counter,self.bee_hive.nectar_collectors,self.bee_hive.pollen_collectors,self.bee_hive.imago_drone_counter]
            self.update_tables()
            self.check_checkboxes()
    
    def check_checkboxes(self):
        if(self.chk_eggs.get() == True):
                self.generate_eggs_chart()
        if(self.chk_larvas.get()==True):
            self.generate_larvas_chart()
        if(self.chk_before_pupa.get()==True):
            self.generate_before_pupa_chart()
        if(self.chk_before_pupa_drone.get()==True):
            self.generate_before_pupa_drone_chart()
        if(self.chk_pupa.get()==True):
            self.generate_pupa_chart()
        if(self.chk_pupa_drone.get()==True):
            self.generate_pupa_chart()
        if(self.chk_imago_worker_young.get()==True):
            self.generate_imago_young_chart()
        if(self.chk_imago_worker_nectar_collectors.get()==True):
            self.generate_imago_nectar_chart()
        if(self.chk_imago_worker_pollen_collectors.get()==True):
            self.generate_imago_pollen_chart()
        if(self.chk_imago_drone.get()==True):
            self.generate_imago_drone_chart()
        if(self.chk_change.get()==True):
            self.generate_change_view()
                
    def simple_run(self, eggs):
        self.income_eggs.append(eggs)
        self.prev_count = [self.bee_hive.eggs_counter,self.bee_hive.larva_counter,self.bee_hive.before_pupa_counter,self.bee_hive.before_pupa_drone_counter,self.bee_hive.pupa_counter,self.bee_hive.pupa_drone_counter,self.bee_hive.imago_worker_young_counter,self.bee_hive.nectar_collectors,self.bee_hive.pollen_collectors,self.bee_hive.imago_drone_counter]
        self.bee_hive.simulate_day(int(eggs))
        self.current_count = [self.bee_hive.eggs_counter,self.bee_hive.larva_counter,self.bee_hive.before_pupa_counter,self.bee_hive.before_pupa_drone_counter,self.bee_hive.pupa_counter,self.bee_hive.pupa_drone_counter,self.bee_hive.imago_worker_young_counter,self.bee_hive.nectar_collectors,self.bee_hive.pollen_collectors,self.bee_hive.imago_drone_counter]
        self.update_tables()
        
    def window_to_generate_sumup(self):
        self.init_checkboxes_interface()
        generate_btn = tk.Button(window, text="Generate", command=self.generate_plot)
        generate_btn.grid(column=1, row=15)
    
    def generate_plot(self):
        self.check_checkboxes()

def update_defines(bees_onstart):
    LARVAS_START = int(0.25 * bees_onstart)
    BFORE_PUPAS_START = int(0.25 * bees_onstart)
    PUPAS_START = int(0.15 * bees_onstart)
    IMAGOS_START = int(0.2 * bees_onstart)
    WORKERS = int(0.15 * bees_onstart)

window = tk.Tk()
window.title("Bees development module")
window.geometry('400x400')
