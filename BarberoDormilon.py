import random
import time
from datetime import timedelta

class BarberShop:
    def __init__(self, total_clients, num_chairs):
        # Inicialización de variables
        self.barber_sleeping = True  # El barbero comienza durmiendo
        self.customers_attended = 0  # Número de clientes atendidos
        self.total_customers = 0  # Número total de clientes
        self.customers_left = 0  # Número de clientes que se fueron sin ser atendidos
        self.customer_waiting_time = {}  # Tiempo de espera de cada cliente
        self.barber_work_time = timedelta(minutes=0)  # Tiempo total de trabajo del barbero
        self.total_clients = total_clients  # Número total de clientes a simular
        self.customer_number = 1  # Inicializar número de cliente
        self.chairs = num_chairs  # Número de sillas en la barbería
        self.customer_queue = []  # Lista para mantener el orden de los clientes en sillas

    def barber_work(self):
        if self.barber_sleeping:
            # El barbero está durmiendo al principio
            print("> El barbero está durmiendo")
            time.sleep(random.uniform(5, 15) / 60)  # Tiempo de siesta del barbero
            self.barber_sleeping = False  # El barbero se despierta cuando llega un cliente

        if self.customer_queue:
            # Si hay clientes en las sillas, el barbero atiende al siguiente
            customer_number, wait_time = self.customer_queue.pop(0)

            if wait_time > 30:  # Si el cliente ha esperado más de 30 minutos, se va
                print(f"> El cliente {customer_number} se fue debido a la espera prolongada [Espero {wait_time:.2f} min].")
                self.customers_left += 1
                del self.customer_waiting_time[customer_number]
            else:
                work_duration = timedelta(minutes=random.uniform(20, 35))  # Tiempo de trabajo del barbero (20 a 35 minutos)
                print(f"> El barbero está despierto y está afeitando al cliente {customer_number}")
                print(f"> El barbero atendió al cliente {customer_number} [tardó {work_duration.seconds // 60} min {work_duration.seconds % 60} seg].")
                self.customers_attended += 1
                self.barber_work_time += work_duration
                time.sleep(random.uniform(5, 15) / 60)
        else:
            # Si no hay clientes en las sillas, el barbero espera
            print("> El barbero está esperando a un cliente.")
            self.barber_sleeping = True

        self.total_customers += 1

    def customer_visit(self):
        if self.total_customers < self.total_clients:
            # Simulación de la llegada de un cliente
            wait_time = random.uniform(5, 15)
            print(f"> Un cliente {self.customer_number} llega a la barbería")
            customer_number = self.customer_number
            self.customer_number += 1
            if len(self.customer_queue) < self.chairs:
                self.customer_waiting_time[customer_number] = wait_time
                self.customer_queue.append((customer_number, wait_time))
            else:
                print(f"> El cliente {customer_number} se fue debido a que no había sillas disponibles.")
                self.customers_left += 1

    def calculate_customers_remaining(self, customers_to_remove=0):
        remaining_customers = len(self.customer_queue) - customers_to_remove
        return remaining_customers

    def run_simulation(self):
        total_simulation_time = 0

        while self.customers_attended < self.total_clients:
            # Simulación de la atención de clientes y el barbero
            action = random.choice(["customer", "barber"])
            if action == "customer":
                self.customer_visit()
                time.sleep(random.uniform(1, 5) / 60)
            else:
                if self.customer_queue:
                    self.barber_work()
                else:
                    # Si no hay clientes, el barbero espera
                    print("> El barbero está durmiendo.")
                    time.sleep(1)

            total_simulation_time += 1

        # Verifica si se generaron más clientes de los especificados y los hace irse
        if self.customers_attended > self.total_clients:
            extra_customers = self.customers_attended - self.total_clients
            print(f"\nSe generaron {extra_customers} clientes extras que se van.")
            self.customers_left += extra_customers

        self.end_time = time.time()
        print("\nLa simulación ha terminado.")

        # Calcula el total de clientes como la suma de atendidos y los que se fueron
        total_clients = self.customers_attended + self.customers_left
        print("\nResultados de la simulación:")
        print(f"Clientes atendidos: {self.customers_attended}")
        print(f"Total de clientes: {total_clients}")
        print(f"Clientes que se fueron debido a que el barbero estaba durmiendo, estaban esperando demasiado o no había sillas disponibles: {self.customers_left}")
        hours, rem = divmod(self.barber_work_time.seconds, 3600)
        minutes, _ = divmod(rem, 60)
        print(f"Tiempo de trabajo del barbero: {hours} horas {minutes} minutos")

total_clients = int(input("Ingrese el número de clientes: "))
num_chairs = int(input("Ingrese el número de sillas en la barbería: "))
barber_shop = BarberShop(total_clients, num_chairs)
barber_shop.run_simulation()

