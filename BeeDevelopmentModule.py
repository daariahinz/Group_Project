import random
from Defines import *

class BeeDevelopmentModule:
    def __init__(self, eggs, larva, before_pupa, pupa, imago):
        self.stage_eggs = [eggs]  # 3 dniowy etap jaj
        self.eggs_counter = eggs

        temp = int(larva * PERCENT_OF_WORKER)
        self.stage_larva = [temp]  # 8 dniowy etap larwy robotnicy
        self.larva_counter = temp
        self.stage_larva_drone = [larva - temp]  # 10 dniowy etap larwy trutnia
        self.larva_drone_counter = larva - temp

        temp = int(before_pupa * PERCENT_OF_WORKER)
        self.stage_before_pupa = [temp]  # 2 dniowy etap przedpoczwarki robotnicy
        self.before_pupa_counter = temp
        self.stage_before_pupa_drone = [before_pupa - temp]  # 4 dniowy etap przedpoczwarki trutnia
        self.before_pupa_drone_counter = before_pupa - temp

        temp = int(pupa * PERCENT_OF_WORKER)
        self.stage_pupa = [temp]  # 8 dniowy etap poczwarki robotnicy
        self.pupa_counter = temp
        self.stage_pupa_drone = [pupa - temp]  # 7 dniowy etap poczwarki trutnia
        self.pupa_drone_counter = pupa - temp

        temp = int(imago * PERCENT_OF_WORKER)
        self.imago_worker_young = [temp]  # dorosly osobnik robotnicy do 10dni
        self.imago_worker_young_counter = temp
        self.imago_worker_nectar_collectors = []  # dorosly osobnik robotnicy powyżej 10dni (80%% zbiera nektar, 20% zbiera pyłek)
        self.nectar_collectors = 0
        self.imago_worker_pollen_collectors = []
        self.pollen_collectors = 0
        self.imago_drone = [imago - temp]  # dorosły osobnik truteń
        self.imago_drone_counter = imago - temp

    def new_fertility_of_bee_mother(self, new_eggs):
        self.stage_eggs.append(new_eggs)
        self.eggs_counter += new_eggs
        if len(self.stage_eggs) > 3:
            new_stage = self.stage_eggs.pop(0)
            self.eggs_counter -= new_stage
            self.update_larva(new_stage)
        else:
            self.update_larva(0)
        if DEBUG_PRINT:
            print("Eggs: " + ", ".join(map(str,self.stage_eggs)))

    def update_larva(self, new_larvas):
        new_larvas_worker = int(PERCENT_OF_WORKER * new_larvas)
        new_larvas_drone = int(PERCENT_OF_DRONE * new_larvas)
        self.stage_larva.append(new_larvas_worker)
        self.larva_counter += new_larvas_worker
        self.stage_larva_drone.append(new_larvas_drone)
        self.larva_drone_counter += new_larvas_drone
        if len(self.stage_larva) > 3:
            new_stage_worker = self.stage_larva.pop(0)
            self.larva_counter -= new_stage_worker
            self.update_before_pupa(new_stage_worker)
        else:
            self.update_before_pupa(0)
        if len(self.stage_larva_drone) > 3:
            new_stage_drone = self.stage_larva_drone.pop(0)
            self.larva_drone_counter -= new_stage_drone
            self.update_before_pupa_drone(new_stage_drone)
        else:
            self.update_before_pupa_drone(0)
        if DEBUG_PRINT:
            print("Larvas: " + ", ".join(map(str,self.stage_larva)))
            print("Larvas drone: " + ", ".join(map(str,self.stage_larva_drone)))

    def update_before_pupa_drone(self, new_before_pupa):
        self.stage_before_pupa_drone.append(new_before_pupa)
        self.before_pupa_drone_counter += new_before_pupa
        if len(self.stage_before_pupa_drone) > 4:
            new_stage = self.stage_before_pupa_drone.pop(0)
            self.before_pupa_drone_counter -= new_stage
            self.update_pupa_drone(new_stage)
        else:
            self.update_pupa_drone(0)
        if DEBUG_PRINT:
            print("Before pupa drone: " + ", ".join(map(str,self.stage_before_pupa_drone)))

    def update_before_pupa(self, new_before_pupa):
        self.stage_before_pupa.append(new_before_pupa)
        self.before_pupa_counter += new_before_pupa
        if len(self.stage_before_pupa) > 2:
            new_stage = self.stage_before_pupa.pop(0)
            self.before_pupa_counter -= new_stage
            self.update_pupa(new_stage)
        else:
            self.update_pupa(0)
        if DEBUG_PRINT:
            print("Before pupa: " + ", ".join(map(str,self.stage_before_pupa)))

    def update_pupa_drone(self, new_pupa):
        self.stage_pupa_drone.append(new_pupa)
        self.pupa_drone_counter += new_pupa
        if len(self.stage_pupa) > 8:
            new_stage = self.stage_pupa_drone.pop(0)
            self.pupa_drone_counter -= new_stage
            self.update_imago_drone(new_stage)
        else:
            self.update_imago_drone(0)
        if DEBUG_PRINT:
            print("Pupa drone: " + ", ".join(map(str,self.stage_pupa_drone)))

    def update_pupa(self, new_pupa):
        self.stage_pupa.append(new_pupa)
        self.pupa_counter += new_pupa
        if len(self.stage_pupa) > 8:
            new_stage = self.stage_pupa.pop(0)
            self.pupa_counter -= new_stage
            self.update_imago(new_stage)
        else:
            self.update_imago(0)
        if DEBUG_PRINT:
            print("Pupa: " + ", ".join(map(str,self.stage_pupa)))

    def update_imago_drone(self, new_imago):
        self.imago_drone.append(new_imago)
        self.imago_drone_counter += new_imago
        if len(self.imago_drone) > TO_OLD_DRONE:  # usuwanie za starych osobników
            self.imago_drone.pop(0)
        if DEBUG_PRINT:
            print("Imago drone: " + ", ".join(map(str,self.imago_drone)))

    def update_imago(self, new_imago):
        self.imago_worker_young.append(new_imago)
        self.imago_worker_young_counter += new_imago
        if len(self.imago_worker_young) > 10:
            new_adult_imago = self.imago_worker_young.pop(0)
            self.imago_worker_young_counter -= new_adult_imago
            nectar =int(0.8 * new_adult_imago)
            pollen =int(0.2 * new_adult_imago)
            self.imago_worker_nectar_collectors.append(nectar)
            self.imago_worker_pollen_collectors.append(pollen)
            self.nectar_collectors += nectar
            self.pollen_collectors += pollen
        else:
            self.imago_worker_nectar_collectors.append(0)
            self.imago_worker_pollen_collectors.append(0)
        if len(self.imago_worker_nectar_collectors) > TO_OLD_WORKER:  # usuwanie za starych osobników
            self.imago_worker_nectar_collectors.pop(0)
            self.imago_worker_pollen_collectors.pop(0)
        if DEBUG_PRINT:
            print("Young imago: " + ", ".join(map(str, self.imago_worker_young)))
            print("Nectar collectors: " + ", ".join(map(str,self.imago_worker_nectar_collectors)))
            print("Pollen collectors: " + ", ".join(map(str,self.imago_worker_pollen_collectors)))

    def simulate_natural_process_of_dying(self):
        loop =self.eggs_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_EGGS_DIE:
                old = random.randint(0, len(self.stage_eggs) - 1)
                if self.stage_eggs[old] > 0:
                    self.stage_eggs[old] -=1
                    self.eggs_counter -= 1
        if DEBUG_PRINT:
            print("After die process eggs: " + ", ".join(map(str,self.stage_eggs)))
        loop =self.larva_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_LARVE_DIE:
                old = random.randint(0, len(self.stage_larva) - 1)
                if self.stage_larva[old] > 0:
                    self.stage_larva[old] -= 1
                    self.larva_counter -= 1
        if DEBUG_PRINT:
            print("After die process larvas: " + ", ".join(map(str,self.stage_larva)))
        loop =self.larva_drone_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_LARVE_DIE:
                old = random.randint(0, len(self.stage_larva_drone) - 1)
                if self.stage_larva_drone[old] > 0:
                    self.stage_larva_drone[old] -= 1
                    self.larva_drone_counter -= 1
        if DEBUG_PRINT:
            print("After die process larvas drone: " + ", ".join(map(str,self.stage_larva_drone)))
        loop = self.before_pupa_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_BEFORE_PUPA_DIE:
                old = random.randint(0, len(self.stage_before_pupa) - 1)
                if self.stage_before_pupa[old] > 0:
                    self.stage_before_pupa[old] -= 1
                    self.before_pupa_counter -= 1
        if DEBUG_PRINT:
            print("After die process before pupa: " + ", ".join(map(str,self.stage_before_pupa)))
        loop = self.before_pupa_drone_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_BEFORE_PUPA_DIE:
                old = random.randint(0, len(self.stage_before_pupa_drone) - 1)
                if self.stage_before_pupa_drone[old] > 0:
                    self.stage_before_pupa_drone[old] -= 1
                    self.before_pupa_drone_counter -= 1
        if DEBUG_PRINT:
            print("After die process before pupa drone: " + ", ".join(map(str,self.stage_before_pupa_drone)))
        loop = self.pupa_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_PUPA_DIE:
                old = random.randint(0, len(self.stage_pupa) - 1)
                if self.stage_pupa[old] > 0:
                    self.stage_pupa[old] -= 1
                    self.pupa_counter -= 1
        if DEBUG_PRINT:
            print("After die process pupa: " + ", ".join(map(str,self.stage_pupa)))
        loop = self.pupa_drone_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_PUPA_DIE:
                old = random.randint(0, len(self.stage_pupa_drone) - 1)
                if self.stage_pupa_drone[old] > 0:
                    self.stage_pupa_drone[old] -= 1
                    self.pupa_drone_counter -= 1
        if DEBUG_PRINT:
            print("After die process pupa drone: " + ", ".join(map(str,self.stage_pupa_drone)))
        loop = self.imago_worker_young_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_IMAGO_YOUNG_DIE:
                old = random.randint(0, len(self.imago_worker_young) - 1)
                if self.imago_worker_young[old] > 0:
                    self.imago_worker_young[old] -= 1
                    self.imago_worker_young_counter -= 1
        if DEBUG_PRINT:
            print("After die process young imago: " + ", ".join(map(str,self.imago_worker_young)))
        loop = self.pollen_collectors
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_IMAGO_ADULT_DIE:
                old = random.randint(0, len(self.imago_worker_pollen_collectors) - 1)
                if self.imago_worker_pollen_collectors[old] > 0:
                    self.imago_worker_pollen_collectors[old] -= 1
                    self.pollen_collectors -= 1
        if DEBUG_PRINT:
            print("After die process pollen collectors: " + ", ".join(map(str,self.imago_worker_pollen_collectors)))
        loop = self.nectar_collectors
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_IMAGO_ADULT_DIE:
                old = random.randint(0, len(self.imago_worker_nectar_collectors) - 1)
                if self.imago_worker_nectar_collectors[old] > 0:
                    self.imago_worker_nectar_collectors[old] -= 1
                    self.nectar_collectors -= 1
        if DEBUG_PRINT:
            print("After die process nectar collectors: " + ", ".join(map(str,self.imago_worker_nectar_collectors)))
        loop = self.imago_drone_counter
        for i in range(1, loop):
            decide = random.randint(1, 100)
            if decide > COEFFICIENT_IMAGO_ADULT_DIE:
                old = random.randint(0, len(self.imago_drone) - 1)
                if self.imago_drone[old] > 0:
                    self.imago_drone[old] -= 1
                    self.imago_drone_counter -= 1
        if DEBUG_PRINT:
            print("After die process imago drone: " + ", ".join(map(str,self.imago_drone)))

    def simulate_day(self,new_eggs):
        self.new_fertility_of_bee_mother(new_eggs)
        self.simulate_natural_process_of_dying()