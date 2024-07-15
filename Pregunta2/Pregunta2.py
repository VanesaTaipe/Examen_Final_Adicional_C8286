import random
from collections import defaultdict

# Implementación de relojes vectoriales para ordenamiento parcial de eventos
class VectorClock:
    def __init__(self, num_processes, process_id):
        self.clock = [0] * num_processes
        self.process_id = process_id

    def tick(self):
        # Incrementa el tiempo local del proceso
        self.clock[self.process_id] += 1

    def update(self, other_clock):
        # Actualiza el reloj con información de otro proceso
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], other_clock[i])
        self.tick()

    def __str__(self):
        return f"{self.clock}"

# Implementación del algoritmo de Raymond para exclusión mutua
class RaymondMutex:
    def __init__(self, process_id):
        self.process_id = process_id
        self.holder = process_id
        self.request_queue = []

    def request_access(self):
        # Solicita acceso a la sección crítica
        if self.holder != self.process_id:
            self.request_queue.append(self.process_id)
            while self.holder != self.process_id:
                pass  # Espera activa (no óptimo en un sistema real)

    def leave_critical_section(self):
        # Libera la sección crítica
        if self.request_queue:
            self.holder = self.request_queue.pop(0)
        else:
            self.holder = self.process_id

# Clase para representar objetos creados por los robots
class RobotObject:
    def __init__(self, robot_id, task_id):
        self.robot_id = robot_id
        self.task_id = task_id

    def __str__(self):
        return f"RobotObject(robot={self.robot_id}, task={self.task_id})"

# Implementación del recolector de basura generacional
class GenerationalCollector:
    def __init__(self, young_threshold):
        self.young_generation = []
        self.old_generation = []
        self.young_threshold = young_threshold

    def allocate(self, robot_id, task_id):
        # Crea un nuevo objeto en la generación joven
        obj = RobotObject(robot_id, task_id)
        self.young_generation.append(obj)
        return obj

    def collect_young(self):
        # Realiza la recolección de basura en la generación joven
        survivors = [obj for obj in self.young_generation if random.random() > 0.3]
        self.old_generation.extend(survivors[self.young_threshold:])
        self.young_generation = survivors[:self.young_threshold]
        return len(self.young_generation), len(self.old_generation)

# Implementación del algoritmo de Chandy-Lamport para instantáneas globales
class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.state = f"Initial State {process_id}"
        self.channels = defaultdict(list)
        self.neighbors = []
        self.marker_received = {}
        self.local_snapshot = None
        self.vector_clock = None

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for neighbor in neighbors:
            self.marker_received[neighbor.process_id] = False

    def initiate_snapshot(self):
        # Inicia el proceso de toma de instantánea
        self.local_snapshot = self.state
        self.marker_received = {neighbor: False for neighbor in self.marker_received}
        for neighbor in self.neighbors:
            neighbor.receive_message(('MARKER', self.process_id, self.vector_clock.clock))

    def receive_message(self, message):
        # Procesa mensajes recibidos, incluyendo marcadores para instantáneas
        message_type, sender_id, content = message
        if message_type == 'MARKER':
            if self.local_snapshot is None:
                self.local_snapshot = self.state
                self.marker_received[sender_id] = True
                for neighbor in self.neighbors:
                    if neighbor.process_id != sender_id:
                        neighbor.receive_message(('MARKER', self.process_id, self.vector_clock.clock))
            else:
                self.marker_received[sender_id] = True
        else:
            if self.local_snapshot is not None and not all(self.marker_received.values()):
                self.channels[sender_id].append(content)
            self.vector_clock.update(content)
            self.state = f"State after message from {sender_id}"

    def update_state(self, new_state):
        self.state = new_state
        self.vector_clock.tick()

# Sistema principal de coordinación de tareas
class SistemaCoordinacion:
    def __init__(self, num_robots, num_tareas):
        self.num_robots = num_robots
        self.num_tareas = num_tareas
        self.robots = [Process(i) for i in range(num_robots)]
        self.mutexes = [RaymondMutex(i) for i in range(num_robots)]
        for i, robot in enumerate(self.robots):
            robot.vector_clock = VectorClock(num_robots, i)
            neighbors = self.robots[:i] + self.robots[i+1:]
            robot.set_neighbors(neighbors)
        self.collector = GenerationalCollector(100)

    def ejecutar_tareas(self):
        for task in range(self.num_tareas):
            print(f"\n--- Tarea {task + 1} ---")
            robot_id = random.randint(0, self.num_robots - 1)
            self.ejecutar_tarea(robot_id)
            if task % 2 == 1:  # Tomar instantánea cada 2 tareas
                self.tomar_instantanea()

    def ejecutar_tarea(self, robot_id):
        # Ejecuta una tarea en un robot específico
        robot = self.robots[robot_id]
        mutex = self.mutexes[robot_id]
        
        print(f"Robot {robot_id} iniciando tarea")
        print(f"Reloj Robot {robot_id}: {robot.vector_clock}")

        mutex.request_access()  # Solicita acceso exclusivo (Raymond)
        
        nuevo_estado = f"Estado después de tarea {random.randint(1, 10)}"
        robot.update_state(nuevo_estado)
        print(f"Robot {robot_id} nuevo estado: {nuevo_estado}")

        obj = self.collector.allocate(robot_id, random.randint(1, 1000))
        print(f"Objeto alocado para robot {robot_id}: {obj}")

        mutex.leave_critical_section()  # Libera acceso exclusivo

        self.enviar_mensaje(robot_id)

    def enviar_mensaje(self, robot_id):
        # Envía un mensaje a un robot vecino aleatorio
        if self.robots[robot_id].neighbors:
            destino = random.choice(self.robots[robot_id].neighbors)
            mensaje = self.robots[robot_id].vector_clock.clock
            destino.receive_message(('NORMAL', robot_id, mensaje))
            print(f"Robot {robot_id} envió mensaje a Robot {destino.process_id}")

    def tomar_instantanea(self):
        # Inicia el proceso de toma de instantánea global (Chandy-Lamport)
        print("\n--- Iniciando instantánea global ---")
        self.robots[0].initiate_snapshot()
        while not all(robot.local_snapshot is not None for robot in self.robots):
            pass
        print("Instantánea global completada")

    def recolectar_basura(self):
        # Realiza la recolección de basura generacional
        print("\n--- Recolección de basura ---")
        young, old = self.collector.collect_young()
        print(f"Objetos en generación joven: {young}")
        print(f"Objetos en generación vieja: {old}")

    def mostrar_instantaneas(self):
        # Muestra las instantáneas tomadas de todos los robots
        print("\n--- Mostrando instantáneas ---")
        for robot in self.robots:
            print(f"Robot {robot.process_id}:")
            print(f"  Estado local: {robot.local_snapshot}")
            print(f"  Reloj vectorial: {robot.vector_clock}")
            for neighbor_id, channel in robot.channels.items():
                print(f"  Canal desde Robot {neighbor_id}: {channel}")
            print()

def main():
    num_robots = 2
    num_tareas = 2
    sistema = SistemaCoordinacion(num_robots, num_tareas)
    
    sistema.ejecutar_tareas()
    sistema.recolectar_basura()
    sistema.mostrar_instantaneas()

if __name__ == "__main__":
    main()
