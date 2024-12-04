def fifo(processes):
    processes.sort(key=lambda x: x['arrival'])  # Ordenar por tiempo de llegada
    time = 0
    waiting_times = []
    turnaround_times = []
    
    for process in processes:
        if time < process['arrival']:
            time = process['arrival']  # Esperar si el proceso aún no llega
        waiting_time = time - process['arrival']
        waiting_times.append(waiting_time)
        time += process['burst']
        turnaround_times.append(time - process['arrival'])
    
    avg_waiting = sum(waiting_times) / len(waiting_times)
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    
    return avg_waiting, avg_turnaround


def srtf(processes):
    processes.sort(key=lambda x: x['arrival'])  # Ordenar por tiempo de llegada
    time = 0
    completed = 0
    n = len(processes)
    burst_remaining = [p['burst'] for p in processes]
    waiting_times = [0] * n
    turnaround_times = [0] * n
    
    while completed < n:
        # Buscar el proceso con el menor tiempo restante que ya haya llegado
        shortest = None
        for i in range(n):
            if processes[i]['arrival'] <= time and burst_remaining[i] > 0:
                if shortest is None or burst_remaining[i] < burst_remaining[shortest]:
                    shortest = i
        
        if shortest is not None:
            burst_remaining[shortest] -= 1
            if burst_remaining[shortest] == 0:  # Proceso completado
                completed += 1
                finish_time = time + 1
                turnaround_times[shortest] = finish_time - processes[shortest]['arrival']
                waiting_times[shortest] = turnaround_times[shortest] - processes[shortest]['burst']
        
        time += 1
    
    avg_waiting = sum(waiting_times) / len(waiting_times)
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    
    return avg_waiting, avg_turnaround


# Datos de prueba
processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 8},
    {'id': 'P2', 'arrival': 1, 'burst': 4},
    {'id': 'P3', 'arrival': 2, 'burst': 2},
]

fifo_avg_waiting, fifo_avg_turnaround = fifo(processes)
srtf_avg_waiting, srtf_avg_turnaround = srtf(processes)

print("FIFO:")
print(f"Tiempo promedio de espera: {fifo_avg_waiting:.2f}")
print(f"Tiempo promedio de finalización: {fifo_avg_turnaround:.2f}")

print("\nSRTF:")
print(f"Tiempo promedio de espera: {srtf_avg_waiting:.2f}")
print(f"Tiempo promedio de finalización: {srtf_avg_turnaround:.2f}")

# Análisis de resultados
if fifo_avg_waiting > srtf_avg_waiting:
    print("\nSRTF genera menores tiempos de espera promedio que FIFO.")
elif fifo_avg_waiting < srtf_avg_waiting:
    print("\nFIFO genera menores tiempos de espera promedio que SRTF.")
else:
    print("\nAmbos algoritmos generan el mismo tiempo de espera promedio.")

