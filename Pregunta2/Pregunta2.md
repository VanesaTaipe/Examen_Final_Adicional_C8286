1. Algoritmo de Chandy-Lamport para instantáneas globales:
   - Implementado en la clase `Process`, específicamente en los métodos `initiate_snapshot()` y `receive_message()`.
   - El método `tomar_instantanea()` en `SistemaCoordinacion` inicia el proceso de instantánea global.
   - Se utilizan mensajes de tipo 'MARKER' para coordinar la toma de instantáneas entre los robots.

2. Algoritmo de Raymond para exclusión mutua:
   - Implementado en la clase `RaymondMutex`.
   - Los métodos `request_access()` y `leave_critical_section()` gestionan el acceso a la sección crítica.
   - Se utiliza en `ejecutar_tarea()` de `SistemaCoordinacion` para garantizar acceso exclusivo a recursos compartidos.

3. Relojes vectoriales para ordenamiento parcial:
   - Implementado en la clase `VectorClock`.
   - Cada `Process` tiene su propio `VectorClock`.
   - Los relojes se actualizan en `update_state()` y `receive_message()` de `Process`.
   - Se utilizan para ordenar eventos y detectar potenciales violaciones de causalidad.

4. Recolector de basura generacional:
   - Implementado en la clase `GenerationalCollector`.
   - El método `allocate()` crea nuevos objetos en la generación joven.
   - `collect_young()` realiza la recolección de basura, moviendo objetos sobrevivientes a la generación vieja.
   - Se utiliza en `ejecutar_tarea()` de `SistemaCoordinacion` para alocar objetos y en `recolectar_basura()` para realizar la recolección.

El sistema de coordinación se implementa principalmente en la clase `SistemaCoordinacion`, que integra todos estos componentes:
- Crea y gestiona los robots (`Process`), mutexes (`RaymondMutex`), y el recolector de basura.
- Ejecuta tareas en robots aleatorios, utilizando exclusión mutua y actualizando relojes vectoriales.
- Toma instantáneas periódicas del estado global del sistema.
- Realiza recolección de basura y muestra el estado final del sistema.

  Resultados:


```
--- Tarea 1 ---
Robot 0 iniciando tarea
Reloj Robot 0: [0, 0]
Robot 0 nuevo estado: Estado después de tarea 3
Objeto alocado para robot 0: RobotObject(robot=0, task=496)
Robot 0 envió mensaje a Robot 1

--- Tarea 2 ---
Robot 1 iniciando tarea
Reloj Robot 1: [1, 1]
Robot 1 nuevo estado: Estado después de tarea 1
Objeto alocado para robot 1: RobotObject(robot=1, task=915)
Robot 1 envió mensaje a Robot 0

--- Iniciando instantánea global ---
Instantánea global completada

--- Recolección de basura ---
Objetos en generación joven: 1
Objetos en generación vieja: 0

--- Mostrando instantáneas ---
Robot 0:
  Estado local: State after message from 1
  Reloj vectorial: [2, 2]

Robot 1:
  Estado local: Estado después de tarea 1
  Reloj vectorial: [1, 2]
```


Tarea 1:

El Robot 0 inicia la tarea.
Su reloj vectorial inicial es [0, 0].
Realiza la tarea y actualiza su estado.
Aloca un objeto (RobotObject(robot=0, task=496)).
Envía un mensaje al Robot 1.


Tarea 2:

El Robot 1 inicia la tarea.
Su reloj vectorial es [1, 1] (incrementó debido al mensaje recibido del Robot 0).
Realiza la tarea y actualiza su estado.
Aloca un objeto (RobotObject(robot=1, task=915)).
Envía un mensaje al Robot 0.


Instantánea global:

Se inicia y completa la instantánea global utilizando el algoritmo de Chandy-Lamport.


Recolección de basura:

Se realiza la recolección de basura generacional.
Queda 1 objeto en la generación joven y 0 en la vieja.


Instantáneas finales:

Robot 0:

Estado local: "State after message from 1" (refleja que recibió un mensaje del Robot 1).
Reloj vectorial: [2, 2] (actualizado después de recibir el mensaje del Robot 1).


Robot 1:

Estado local: "Estado después de tarea 1" (su estado después de realizar la tarea).
Reloj vectorial: [1, 2] (refleja que conoce el evento del Robot 0 y su propio evento).
  
