import asyncio
import logging
import threading

# Configuración de logging
logging.basicConfig(level=logging.INFO)

class EventPriority:
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class Event:
    def __init__(self, event_type, priority, data):
        self.type = event_type
        self.priority = priority
        self.data = data

    def __lt__(self, other):
        return self.priority < other.priority

class NotebookSimulator:
    def __init__(self):
        self.cells = []
        self.event_queue = asyncio.PriorityQueue()
        self.shared_resource = 0
        self.resource_lock = threading.Lock()

    async def run(self):
        event_handler_task = asyncio.create_task(self.event_handler())
        
        # Simular algunos eventos con diferentes prioridades
        await self.add_event('add_cell', EventPriority.HIGH, 'print("Hello, World!")')
        await self.add_event('execute_cell', EventPriority.MEDIUM, 0)
        await self.add_event('modify_cell', EventPriority.LOW, (0, 'print("Modified cell")'))
        await self.add_event('execute_cell', EventPriority.MEDIUM, 0)
        
        await self.event_queue.join()
        event_handler_task.cancel()
        try:
            await event_handler_task
        except asyncio.CancelledError:
            logging.info("Event handler task cancelled")

    async def add_event(self, event_type, priority, data):
        event = Event(event_type, priority, data)
        await self.event_queue.put(event)

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

    async def add_cell(self, content):
        self.cells.append(content)
        logging.info(f"Added cell: {content}")

    async def execute_cell(self, cell_index):
        if 0 <= cell_index < len(self.cells):
            cell_content = self.cells[cell_index]
            logging.info(f"Executing cell {cell_index}: {cell_content}")
            try:
                # Simular ejecución asíncrona
                await asyncio.sleep(1)
                with self.resource_lock:
                    exec(cell_content)
            except Exception as e:
                logging.error(f"Error executing cell {cell_index}: {e}")
        else:
            logging.error(f"Invalid cell index: {cell_index}")

    async def modify_cell(self, cell_index, new_content):
        if 0 <= cell_index < len(self.cells):
            self.cells[cell_index] = new_content
            logging.info(f"Modified cell {cell_index}: {new_content}")
        else:
            logging.error(f"Invalid cell index: {cell_index}")

    def update_shared_resource(self, value):
        with self.resource_lock:
            self.shared_resource += value
            logging.info(f"Updated shared resource: {self.shared_resource}")

async def main():
    notebook = NotebookSimulator()
    await notebook.run()

if __name__ == "__main__":
    asyncio.run(main())
