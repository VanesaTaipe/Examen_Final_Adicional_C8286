import asyncio
import logging
import threading

# Configuración de logging para registrar información
logging.basicConfig(level=logging.INFO)

# Definición de prioridades para los eventos
class EventPriority:
    LOW = 3
    MEDIUM = 2
    HIGH = 1

# Clase para representar eventos
class Event:
    def __init__(self, event_type, priority, data):
        self.type = event_type
        self.priority = priority
        self.data = data

    # Método para comparar eventos basándose en su prioridad
    def __lt__(self, other):
        return self.priority < other.priority

# Simulador de Jupyter Notebook
class NotebookSimulator:
    def __init__(self):
        self.cells = []  # Lista para almacenar celdas
        self.event_queue = asyncio.PriorityQueue()  # Cola de eventos priorizada
        self.shared_resource = 0  # Recurso compartido
        self.resource_lock = threading.Lock()  # Bloqueo para acceso seguro a recursos compartidos

    # Método principal para ejecutar el simulador
    async def run(self):
        event_handler_task = asyncio.create_task(self.event_handler())
        
        # Simular algunos eventos con diferentes prioridades
        await self.add_event('add_cell', EventPriority.HIGH, 'print("Hello, World!")')
        await self.add_event('execute_cell', EventPriority.MEDIUM, 0)
        await self.add_event('modify_cell', EventPriority.LOW, (0, 'print("Modified cell")'))
        await self.add_event('execute_cell', EventPriority.MEDIUM, 0)
        
        await self.event_queue.join()  # Esperar a que se procesen todos los eventos
        event_handler_task.cancel()  # Cancelar el manejador de eventos
        try:
            await event_handler_task
        except asyncio.CancelledError:
            logging.info("Event handler task cancelled")

    # Método para añadir eventos a la cola
    async def add_event(self, event_type, priority, data):
        event = Event(event_type, priority, data)
        await self.event_queue.put(event)

    # Manejador de eventos
    async def event_handler(self):
        while True:
            try:
                event = await self.event_queue.get()
                await self.process_event(event)
                self.event_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error processing event: {e}")

    # Procesador de eventos
    async def process_event(self, event):
        try:
            if event.type == 'add_cell':
                await self.add_cell(event.data)
            elif event.type == 'execute_cell':
                await self.execute_cell(event.data)
            elif event.type == 'modify_cell':
                await self.modify_cell(*event.data)
            else:
                logging.warning(f"Unknown event type: {event.type}")
        except Exception as e:
            logging.error(f"Error processing event {event.type}: {e}")

    # Método para añadir una celda
    async def add_cell(self, content):
        self.cells.append(content)
        logging.info(f"Added cell: {content}")

    # Método para ejecutar una celda
    async def execute_cell(self, cell_index):
        if 0 <= cell_index < len(self.cells):
            cell_content = self.cells[cell_index]
            logging.info(f"Executing cell {cell_index}: {cell_content}")
            try:
                await asyncio.sleep(1)  # Simular ejecución asíncrona
                with self.resource_lock:
                    exec(cell_content)
            except Exception as e:
                logging.error(f"Error executing cell {cell_index}: {e}")
        else:
            logging.error(f"Invalid cell index: {cell_index}")

    # Método para modificar una celda
    async def modify_cell(self, cell_index, new_content):
        if 0 <= cell_index < len(self.cells):
            self.cells[cell_index] = new_content
            logging.info(f"Modified cell {cell_index}: {new_content}")
        else:
            logging.error(f"Invalid cell index: {cell_index}")

    # Método para actualizar un recurso compartido de forma segura
    def update_shared_resource(self, value):
        with self.resource_lock:
            self.shared_resource += value
            logging.info(f"Updated shared resource: {self.shared_resource}")

# Función principal asíncrona
async def main():
    notebook = NotebookSimulator()
    await notebook.run()

# Punto de entrada del programa
if __name__ == "__main__":
    asyncio.run(main())
