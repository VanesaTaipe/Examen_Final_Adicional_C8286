
1. Dijkstra-Scholten para la detección de terminación de procesos distribuidos:
   - Este algoritmo se implementa principalmente en la clase `Node`, específicamente en los métodos `start_process`, `finish_process`, y `receive_termination`.
   - La estructura de árbol se mantiene con los atributos `parent` y `children`.
   - Cuando un proceso termina (`finish_process`), envía un mensaje "TERMINATE" a su padre.
   - El método `receive_termination` maneja la propagación de los mensajes de terminación hacia arriba en el árbol.

2. Ricart-Agrawala para la exclusión mutua en el acceso a recursos compartidos:
   - Este algoritmo se implementa en la clase `RicartAgrawalaMutex`.
   - Los métodos `request_access`, `receive_request`, `receive_reply`, `check_enter_cs`, `enter_critical_section`, y `leave_critical_section` implementan el protocolo de exclusión mutua.
   - Cuando un nodo quiere entrar en la sección crítica, envía solicitudes a todos los demás nodos y espera sus respuestas.

3. Sincronización de relojes para asegurar que todos los nodos tengan una vista consistente del tiempo:
   - Esto se implementa en el método `synchronize_clocks` de la clase `Network` y el método `synchronize_clock` de la clase `Node`.
   - Se calcula un tiempo promedio entre todos los nodos y luego cada nodo ajusta su reloj a este tiempo.

4. Algoritmo de recolección de basura (Cheney) para gestionar la memoria en los nodos de computación:
   - Este algoritmo se implementa en la clase `CheneyCollector`.
   - Los métodos `allocate`, `collect`, y `copy` implementan el algoritmo de copia de Cheney para la recolección de basura.
   - Cada nodo tiene su propio recolector de basura que se utiliza en el método `collect_garbage` de la clase `Node`.

La simulación de tareas científicas se realiza en el método `simulate_scientific_task` de la clase `Network`, donde:
- Se realizan solicitudes de exclusión mutua.
- Se lleva a cabo la recolección de basura en cada nodo.
- Se sincronizan los relojes de los nodos.
- Se finalizan los procesos para detectar la terminación global.
