import time 
import random 

class Message:
    def __init__(self, sender, content, timestamp):
        self.sender = sender      # Almacena el ID del nodo que envía el mensaje
        self.content = content    # Almacena el contenido del mensaje
        self.timestamp = timestamp  # Almacena la marca de tiempo del mensaje

class Node:
    def __init__(self, node_id, total_nodes, network):
        self.node_id = node_id        # ID único del nodo
        self.total_nodes = total_nodes  # Número total de nodos en la red
        self.network = network        # Referencia a la red a la que pertenece el nodo
        self.clock = 0                # Reloj lógico del nodo
        self.parent = None            # Padre en el árbol de detección de terminación
        self.children = set()         # Conjunto de hijos en el árbol de detección de terminación
        self.active = True            # Indica si el nodo está activo
        self.request_queue = []       # Cola de solicitudes para exclusión mutua
        self.replies_received = 0     # Número de respuestas recibidas para exclusión mutua
        self.memory = []              # Simula la memoria del nodo para recolección de basura

    def send_message(self, recipient_id, content):
        message = Message(self.node_id, content, self.clock)  # Crea un nuevo mensaje
        self.network.deliver_message(recipient_id, message)  # Envía el mensaje a través de la red

    def receive_message(self, message):
        self.clock = max(self.clock, message.timestamp) + 1  # Actualiza el reloj lógico
        if message.content == "REQUEST":
            self.handle_mutex_request(message)  # Maneja solicitud de exclusión mutua
        elif message.content == "REPLY":
            self.handle_mutex_reply(message)  # Maneja respuesta de exclusión mutua
        elif message.content == "TERMINATE":
            self.handle_termination(message)  # Maneja mensaje de terminación

    def handle_mutex_request(self, message):
        self.request_queue.append((message.timestamp, message.sender))  # Añade solicitud a la cola
        self.request_queue.sort()  # Ordena la cola de solicitudes
        self.send_message(message.sender, "REPLY")  # Envía respuesta al solicitante

    def handle_mutex_reply(self, message):
        self.replies_received += 1  # Incrementa el contador de respuestas recibidas
        if self.replies_received == self.total_nodes - 1:  # Si se recibieron todas las respuestas
            self.enter_critical_section()  # Entra en la sección crítica

    def enter_critical_section(self):
        print(f"Nodo {self.node_id} ingresando a la sección crítica")  # Notifica entrada a sección crítica
        time.sleep(0.1)  # Simula trabajo en la sección crítica
        self.leave_critical_section()  # Sale de la sección crítica

    def leave_critical_section(self):
        self.replies_received = 0  # Reinicia el contador de respuestas
        self.request_queue = [(t, n) for t, n in self.request_queue if n != self.node_id]  # Limpia la cola
        for _, node_id in self.request_queue:
            self.send_message(node_id, "REPLY")  # Envía respuestas a las solicitudes pendientes
        print(f"Nodo {self.node_id} dejando la sección crítica")  # Notifica salida de sección crítica

    def request_mutex(self):
        self.clock += 1  # Incrementa el reloj lógico
        self.request_queue.append((self.clock, self.node_id))  # Añade su propia solicitud a la cola
        for node_id in range(self.total_nodes):
            if node_id != self.node_id:
                self.send_message(node_id, "REQUEST")  # Envía solicitud a todos los demás nodos

    def handle_termination(self, message):
        if self.parent is None and message.sender != self.node_id:
            self.parent = message.sender  # Establece el padre en el árbol de terminación
            self.children.add(message.sender)  # Añade el remitente como hijo
        elif message.sender in self.children:
            self.children.remove(message.sender)  # Elimina el hijo que ha terminado
        self.check_termination()  # Verifica si el nodo ha terminado

    def check_termination(self):
        if not self.active and not self.children:  # Si el nodo no está activo y no tiene hijos
            if self.parent is not None:
                self.send_message(self.parent, "TERMINATE")  # Notifica terminación al padre
    def synchronize_clock(self, average_time):
        self.clock = average_time  # Ajusta el reloj al tiempo promedio

    def collect_garbage(self):
        new_memory = []
        for obj in self.memory:
            if obj is not None:
                new_memory.append(obj)  # Copia objetos no nulos a la nueva memoria
        self.memory = new_memory  # Actualiza la memoria con solo objetos no nulos
        print(f"Nodo {self.node_id}: Recolección de basura completa")  # Notifica recolección completada

class Network:
    def __init__(self, num_nodes):
        self.nodes = [Node(i, num_nodes, self) for i in range(num_nodes)]  # Crea los nodos de la red

    def deliver_message(self, recipient_id, message):
        self.nodes[recipient_id].receive_message(message)  # Entrega el mensaje al nodo destinatario

    def start(self):
        print("Iniciando la red")  # Notifica inicio de la simulación
        self.synchronize_clocks()  # Sincroniza los relojes de los nodos
        self.simulate_mutex_requests()  # Simula solicitudes de exclusión mutua
        self.simulate_garbage_collection()  # Simula recolección de basura
        self.stop()  # Detiene la simulación

    def stop(self):
        print("Deteniendo la red")  # Notifica detención de la simulación
        for node in self.nodes:
            node.active = False  # Marca todos los nodos como inactivos
        self.nodes[0].check_termination()  # Inicia la detección de terminación desde el nodo 0

    def synchronize_clocks(self):
        average_time = sum(node.clock for node in self.nodes) / len(self.nodes)  # Calcula tiempo promedio
        for node in self.nodes:
            node.synchronize_clock(average_time)  # Sincroniza cada nodo al tiempo promedio
        print("Relojes sincronizados")  # Notifica sincronización completada

    def simulate_mutex_requests(self):
        for node in self.nodes[:3]:  # Para los primeros 3 nodos
            node.request_mutex()  # Simula una solicitud de exclusión mutua
            time.sleep(0.5)  # Espera entre solicitudes

    def simulate_garbage_collection(self):
        for node in self.nodes:
            for _ in range(5):
                node.memory.append(f"obj{_}")  # Añade objetos a la memoria del nodo
            node.collect_garbage()  # Realiza recolección de basura en el nodo
def main():
    network = Network(5)  # Crea una red con 5 nodos
    network.start()  # Inicia la simulación de la red

if __name__ == "__main__":
    main()  
