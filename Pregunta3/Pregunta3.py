import time
import random

class Message:
    def __init__(self, sender, content, timestamp):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp

class Node:
    def __init__(self, node_id, total_nodes, network):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.network = network
        self.clock = random.randint(0, 30)  # Inicializa el reloj con un tiempo aleatorio
        self.mutex = RicartAgrawalaMutex(self)  # Crea el objeto para manejar la exclusión mutua
        self.collector = CheneyCollector(10)  # Crea el recolector de basura
        self.parent = None  # Para el algoritmo Dijkstra-Scholten
        self.children = set()  # Para el algoritmo Dijkstra-Scholten
        self.active = True  # Indica si el nodo está activo

    def send_message(self, recipient_id, content):
        # Envía un mensaje a otro nodo
        if recipient_id is not None and 0 <= recipient_id < self.total_nodes:
            message = Message(self.node_id, content, self.clock)
            self.network.deliver_message(recipient_id, message)
        else:
            print(f"Invalid recipient_id: {recipient_id}")

    def receive_message(self, message):
        # Procesa los mensajes recibidos
        if message is None:
            print(f"Node {self.node_id} received None message")
            return
        self.clock = max(self.clock, message.timestamp) + 1  # Actualiza el reloj lógico
        if message.content == "TERMINATE":
            self.receive_termination(message.sender)
        elif message.content == "REQUEST":
            self.mutex.receive_request(message.sender)
        elif message.content == "REPLY":
            self.mutex.receive_reply()

    def request_mutex(self):
        # Solicita acceso a la sección crítica
        self.mutex.request_access()

    def release_mutex(self):
        # Libera la sección crítica
        self.mutex.leave_critical_section()

    def receive_termination(self, child_id):
        # Maneja la recepción de un mensaje de terminación (Dijkstra-Scholten)
        if child_id in self.children:
            self.children.remove(child_id)
        if not self.active and not self.children:
            if self.parent is not None:
                self.send_message(self.parent, "TERMINATE")
            else:
                print(f"Node {self.node_id} detected global termination")

    def synchronize_clock(self, master_time):
        # Sincroniza el reloj del nodo con el tiempo maestro
        self.clock = master_time

    def collect_garbage(self):
        # Realiza la recolección de basura
        addr = self.collector.allocate(f"obj{self.node_id}")
        print(f"Asignado obj{self.node_id} en: {addr}")
        self.collector.collect()
        print(f"Recoleccion de basura completa en Nodo {self.node_id}")

    def start_process(self):
        # Inicia el proceso del nodo
        self.active = True
        if self.parent is None and self.node_id != 0:
            self.parent = 0
            self.send_message(0, "ACTIVATE")

    def finish_process(self):
        # Finaliza el proceso del nodo
        self.active = False
        if not self.children:
            if self.parent is not None:
                self.send_message(self.parent, "TERMINATE")
            else:
                print(f"Node {self.node_id} finished process")

class RicartAgrawalaMutex:
    def __init__(self, node):
        self.node = node
        self.requesting = False
        self.replies_received = 0

    def request_access(self):
        # Solicita acceso a la sección crítica
        self.requesting = True
        self.replies_received = 0
        for i in range(self.node.total_nodes):
            if i != self.node.node_id:
                self.node.send_message(i, "REQUEST")
        self.check_enter_cs()

    def receive_request(self, sender_id):
        # Maneja la recepción de una solicitud de acceso
        if not self.requesting or sender_id < self.node.node_id:
            self.node.send_message(sender_id, "REPLY")
        # else: defer the reply

    def receive_reply(self):
        # Maneja la recepción de una respuesta
        self.replies_received += 1
        self.check_enter_cs()

    def check_enter_cs(self):
        # Verifica si se puede entrar a la sección crítica
        if self.replies_received == self.node.total_nodes - 1:
            self.enter_critical_section()

    def enter_critical_section(self):
        # Entra a la sección crítica
        print(f"Nodo {self.node.node_id} ingresando a la seccion critica")
        time.sleep(1)
        self.leave_critical_section()

    def leave_critical_section(self):
        # Sale de la sección crítica
        self.requesting = False
        print(f"Nodo {self.node.node_id} dejando la seccion critica")
        for i in range(self.node.total_nodes):
            if i != self.node.node_id:
                self.node.send_message(i, "REPLY")

class CheneyCollector:
    def __init__(self, size):
        self.size = size
        self.from_space = [None] * size
        self.to_space = [None] * size
        self.free_ptr = 0

    def allocate(self, obj):
        # Asigna un objeto en la memoria
        if self.free_ptr >= self.size:
            self.collect()
        addr = self.free_ptr
        self.from_space[addr] = obj
        self.free_ptr += 1
        return addr

    def collect(self):
        # Realiza la recolección de basura
        self.to_space = [None] * self.size
        self.free_ptr = 0
        for obj in self.from_space:
            if obj is not None:
                self.copy(obj)
        self.from_space, self.to_space = self.to_space, self.from_space

    def copy(self, obj):
        # Copia un objeto durante la recolección de basura
        addr = self.free_ptr
        self.to_space[addr] = obj
        self.free_ptr += 1
        return addr

class Network:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.nodes = [Node(i, num_nodes, self) for i in range(num_nodes)]

    def deliver_message(self, recipient_id, message):
        # Entrega un mensaje a un nodo específico
        if recipient_id is not None and 0 <= recipient_id < self.num_nodes:
            self.nodes[recipient_id].receive_message(message)
        else:
            print(f"Invalid recipient_id: {recipient_id}")

    def start(self):
        # Inicia la red
        print("Starting the network")
        self.synchronize_clocks()
        for node in self.nodes:
            node.start_process()

    def synchronize_clocks(self):
        # Sincroniza los relojes de todos los nodos
        master_time = sum(node.clock for node in self.nodes) / len(self.nodes)
        for node in self.nodes:
            node.synchronize_clock(master_time)
        print([(node.node_id, node.clock) for node in self.nodes])

    def simulate_scientific_task(self):
        # Simula la ejecución de tareas científicas
        # Realizar solicitudes de exclusión mutua
        for _ in range(3):
            node = random.choice(self.nodes)
            node.request_mutex()
        
        # Realizar la recolección de basura en los nodos
        for node in self.nodes:
            node.collect_garbage()

        # Sincronizar los relojes de los nodos
        self.synchronize_clocks()

        # Finalizar procesos para detectar terminación
        for node in self.nodes:
            node.finish_process()

        # Esperar a que se detecte la terminación global
        time.sleep(2)

if __name__ == "__main__":
    network = Network(3)  # Crea una red con 3 nodos
    network.start()  # Inicia la red
    network.simulate_scientific_task()  # Simula la ejecución de tareas científicas
