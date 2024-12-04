def round_robin(processes, quantum):
    time = 0
    queue = processes[:]
    remaining_burst_times = [p['burst'] for p in processes]
    
    waiting_times = []
    turnaround_times = []
    
    print("Planificación de Turno Circular (Round Robin) - Detalles de Ejecución")
    print("-----------------------------------------------------------")
    
    while queue:
        process = queue.pop(0)  # Extraemos el primer proceso de la cola
        burst_time = remaining_burst_times[process['id']]
        
        print(f"Tiempo: {time} - Proceso {process['id']} con tiempo restante {burst_time}")
        
        # Si el proceso tiene menos tiempo que el quantum, termina en este ciclo
        if burst_time <= quantum:
            time += burst_time
            remaining_burst_times[process['id']] = 0
            waiting_times.append(time - process['arrival'] - process['burst'])
            turnaround_times.append(time - process['arrival'])
            print(f"Proceso {process['id']} terminó en el tiempo {time}.")
        else:
            # Si el proceso no termina, se ejecuta solo por un quantum
            time += quantum
            remaining_burst_times[process['id']] -= quantum
            queue.append(process)  # Vuelve a poner el proceso al final de la cola
            print(f"Proceso {process['id']} no terminó, vuelve a la cola con tiempo restante {remaining_burst_times[process['id']]}")

        print("Estado de la cola:", [p['id'] for p in queue])
        print("-" * 50)
    
    # Cálculos de promedios
    avg_waiting = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    avg_turnaround = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
    
    return avg_waiting, avg_turnaround


# Datos de ejemplo
processes = [
    {'id': 0, 'arrival': 0, 'burst': 8},
    {'id': 1, 'arrival': 1, 'burst': 4},
    {'id': 2, 'arrival': 2, 'burst': 2},
]

quantum = 3  # Tiempo de ejecución por proceso (quantum)

avg_waiting, avg_turnaround = round_robin(processes, quantum)

print(f"Tiempo promedio de espera: {avg_waiting:.2f}")
print(f"Tiempo promedio de finalización: {avg_turnaround:.2f}")
