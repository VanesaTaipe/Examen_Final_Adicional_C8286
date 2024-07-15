
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
  
Resultados:

```
Starting the network
[(0, 19.333333333333332), (1, 19.333333333333332), (2, 19.333333333333332)]
Nodo 2 ingresando a la seccion critica
Nodo 2 dejando la seccion critica
Nodo 2 ingresando a la seccion critica
Nodo 2 dejando la seccion critica
Nodo 0 ingresando a la seccion critica
Nodo 0 dejando la seccion critica
Nodo 1 ingresando a la seccion critica
Nodo 1 dejando la seccion critica
Nodo 2 ingresando a la seccion critica
Nodo 2 dejando la seccion critica
Nodo 2 ingresando a la seccion critica
Nodo 2 dejando la seccion critica
Nodo 0 ingresando a la seccion critica
Nodo 0 dejando la seccion critica
Nodo 0 ingresando a la seccion critica
Nodo 0 dejando la seccion critica
Asignado obj0 en: 0
Recoleccion de basura completa en Nodo 0
Asignado obj1 en: 0
Recoleccion de basura completa en Nodo 1
Asignado obj2 en: 0
Recoleccion de basura completa en Nodo 2
[(0, 41.666666666666664), (1, 41.666666666666664), (2, 41.666666666666664)]
Node 0 finished process
Node 0 detected global termination
Node 0 detected global termination
```



1. "Starting the network": Indica que la red de nodos ha comenzado a inicializarse.

2. "[(0, 19.333333333333332), (1, 19.333333333333332), (2, 19.333333333333332)]": 
   Este es el resultado de la primera sincronización de relojes. Cada tupla representa (id_nodo, tiempo_sincronizado). Todos los nodos han sincronizado sus relojes a 19.333333333333332.

3. Las líneas "Nodo X ingresando a la seccion critica" seguidas por "Nodo X dejando la seccion critica":
   Estas líneas muestran la ejecución del algoritmo de exclusión mutua de Ricart-Agrawala. Cada nodo solicita acceso a la sección crítica, entra en ella, y luego la abandona. Esto ocurre varias veces para diferentes nodos, simulando múltiples accesos a recursos compartidos.

4. "Asignado objX en: 0" seguido por "Recoleccion de basura completa en Nodo X":
   Estas líneas muestran la ejecución del algoritmo de recolección de basura de Cheney en cada nodo. Cada nodo asigna un objeto y luego realiza una recolección de basura.

5. "[(0, 41.666666666666664), (1, 41.666666666666664), (2, 41.666666666666664)]":
   Este es el resultado de la segunda sincronización de relojes. Observa que el tiempo ha avanzado desde la primera sincronización, reflejando el paso del tiempo durante la ejecución de las tareas.

6. "Node 0 finished process":
   Indica que el Nodo 0 ha terminado su proceso.

7. "Node 0 detected global termination" (repetido):
   Estas líneas indican que el Nodo 0 ha detectado la terminación global del sistema. Esto es parte del algoritmo de Dijkstra-Scholten para la detección de terminación. 


