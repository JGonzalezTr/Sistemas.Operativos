def round_robin_with_priority(processes, quantum):
    time = 0
    # Ordenar los procesos por prioridad (menor número = mayor prioridad)
    processes.sort(key=lambda p: p['priority'])
    
    # Crear una lista para manejar las colas por prioridad
    queue = processes[:]
    remaining_burst_times = {p['id']: p['burst'] for p in processes}
    
    waiting_times = {p['id']: 0 for p in processes}
    turnaround_times = {p['id']: 0 for p in processes}
    
    print("Planificación Round Robin con Prioridades - Detalles de Ejecución")
    print("-----------------------------------------------------------")
    
    while any(remaining_burst_times[p['id']] > 0 for p in processes):
        # Iterar sobre los procesos de la cola ordenados por prioridad
        for process in queue[:]:
            pid = process['id']
            burst_time = remaining_burst_times[pid]
            
            if burst_time > 0:
                print(f"Tiempo: {time} - Proceso {pid} (Prioridad {process['priority']}) con tiempo restante {burst_time}")
                
                # Si el proceso puede terminar dentro del quantum
                if burst_time <= quantum:
                    time += burst_time
                    remaining_burst_times[pid] = 0
                    waiting_times[pid] = time - process['arrival'] - process['burst']
                    turnaround_times[pid] = time - process['arrival']
                    print(f"Proceso {pid} terminó en el tiempo {time}.")
                else:
                    # Si el proceso no termina, se ejecuta solo por un quantum
                    time += quantum
                    remaining_burst_times[pid] -= quantum
                    print(f"Proceso {pid} no terminó, vuelve a la cola con tiempo restante {remaining_burst_times[pid]}")

                print("Estado actual:")
                for p in queue:
                    rid = p['id']
                    print(f"  Proceso {rid}: Tiempo restante {remaining_burst_times[rid]} | Prioridad {p['priority']}")
                print("-" * 50)

    # Cálculo de promedios
    avg_waiting = sum(waiting_times.values()) / len(waiting_times)
    avg_turnaround = sum(turnaround_times.values()) / len(turnaround_times)
    
    return avg_waiting, avg_turnaround


# Datos de ejemplo
processes = [
    {'id': 0, 'arrival': 0, 'burst': 8, 'priority': 2},
    {'id': 1, 'arrival': 1, 'burst': 4, 'priority': 1},
    {'id': 2, 'arrival': 2, 'burst': 2, 'priority': 3},
]

quantum = 3  # Tiempo de ejecución por proceso (quantum)

avg_waiting, avg_turnaround = round_robin_with_priority(processes, quantum)

print(f"\nTiempo promedio de espera: {avg_waiting:.2f}")
print(f"Tiempo promedio de finalización: {avg_turnaround:.2f}")
