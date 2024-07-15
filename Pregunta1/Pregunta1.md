
1. Sistema basado en eventos que simula Jupyter Notebooks:

   - La clase `NotebookSimulator` simula un Jupyter Notebook.
   - El método `run()` en esta clase crea un bucle de eventos asíncrono.
   - Los diferentes tipos de eventos (añadir celda, ejecutar celda, modificar celda) se manejan en el método `process_event()`.

2. Uso de asyncio para ejecución asíncrona:

   - Se utiliza `asyncio.run(main())` para iniciar el bucle de eventos principal.
   - Los métodos `run()`, `event_handler()`, `process_event()`, `add_cell()`, `execute_cell()`, y `modify_cell()` son corrutinas asíncronas (definidas con `async def`).
   - Se usa `asyncio.create_task()` para crear tareas asíncronas.
   - `asyncio.PriorityQueue()` se utiliza para manejar eventos de forma asíncrona y priorizada.

3. Manejo de errores y registro de logs:

   - Se utiliza `logging` para registrar información, advertencias y errores.
   - Hay bloques try-except en varias partes del código, especialmente en `event_handler()` y `process_event()`, para capturar y registrar errores.

4. Operaciones seguras en hilos:

   - Se utiliza `threading.Lock()` (self.resource_lock) para proteger el acceso a recursos compartidos.
   - El método `update_shared_resource()` demuestra el uso de este lock para operaciones thread-safe.

5. Sistema para filtrar y priorizar eventos:

   - La clase `EventPriority` define diferentes niveles de prioridad (HIGH, MEDIUM, LOW).
   - La clase `Event` incluye un método `__lt__()` que permite comparar eventos basándose en su prioridad.
   - Se utiliza `asyncio.PriorityQueue()` para manejar los eventos según su prioridad.

6. Simulación de interacciones de usuario:

   - En el método `run()`, se simulan interacciones de usuario añadiendo eventos a la cola con diferentes prioridades:
     ```python
     await self.add_event('add_cell', EventPriority.HIGH, 'print("Hello, World!")')
     await self.add_event('execute_cell', EventPriority.MEDIUM, 0)
     await self.add_event('modify_cell', EventPriority.LOW, (0, 'print("Modified cell")'))
     await self.add_event('execute_cell', EventPriority.MEDIUM, 0)
     ```
Resultados:

INFO:root:Added cell: print("Hello, World!")
INFO:root:Executing cell 0: print("Hello, World!")
Hello, World!
INFO:root:Executing cell 0: print("Hello, World!")
Hello, World!
INFO:root:Modified cell 0: print("Modified cell")

---------------------------------------------

1. `INFO:root:Added cell: print("Hello, World!")`
   - Se añade correctamente la primera celda con el contenido "print("Hello, World!")".

2. `INFO:root:Executing cell 0: print("Hello, World!")`
   `Hello, World!`
   - Se ejecuta la celda 0, que imprime "Hello, World!".

3. `INFO:root:Executing cell 0: print("Hello, World!")`
   `Hello, World!`
   - Se ejecuta nuevamente la celda 0, aún con el contenido original.

4. `INFO:root:Modified cell 0: print("Modified cell")`
   - Se modifica el contenido de la celda 0 a "print("Modified cell")".





