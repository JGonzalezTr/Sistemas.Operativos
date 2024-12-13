import random

def lottery_scheduling(processes, total_time):
    """
    Implementación de planificación por sorteo (Lottery Scheduling).
    
    :param processes: Lista de procesos, cada uno con 'id', 'burst', y 'tickets'.
    :param total_time: Tiempo total de ejecución del simulador.
    """
    # Inicialización
    time = 0
    waiting_times = {p['id']: 0 for p in processes}
    turnaround_times = {p['id']: 0 for p in processes}
    remaining_burst_times = {p['id']: p['burst'] for p in processes}
    active_processes = processes[:]  # Copia para operar sin alterar la lista original

    print("Planificación por sorteo - Detalles de Ejecución")
    print("-----------------------------------------------------------")
    
    while time < total_time and any(remaining_burst_times[p['id']] > 0 for p in processes):
        # Crear la lista de boletos de lotería (uno por cada proceso activo)
        lottery_pool = []
        for process in active_processes:
            if remaining_burst_times[process['id']] > 0:
                lottery_pool.extend([process['id']] * process['tickets'])
        
        if not lottery_pool:  # Si no hay procesos activos, detener la simulación
            break

        # Sorteo: elegir al azar un proceso basado en los boletos
        winner_id = random.choice(lottery_pool)
        winning_process = next(p for p in processes if p['id'] == winner_id)
        
        print(f"Tiempo {time}: Proceso {winner_id} seleccionado (boletos = {winning_process['tickets']})")

        # Ejecutar el proceso por 1 unidad de tiempo
        remaining_burst_times[winner_id] -= 1
        time += 1
        
        # Actualizar tiempos de espera para otros procesos activos
        for process in active_processes:
            pid = process['id']
            if pid != winner_id and remaining_burst_times[pid] > 0:
                waiting_times[pid] += 1
        
        # Si el proceso termina, registrar turnaround
        if remaining_burst_times[winner_id] == 0:
            turnaround_times[winner_id] = time
            print(f"Proceso {winner_id} terminó en el tiempo {time}.")
        
        print(f"Estado restante de procesos: {remaining_burst_times}")
        print("-" * 50)
    
    # Cálculo de tiempos promedio
    avg_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times.values()) / len(turnaround_times)
    
    return avg_waiting_time, avg_turnaround_time


# Datos de ejemplo
processes = [
    {'id': 0, 'burst': 8, 'tickets': 10},
    {'id': 1, 'burst': 4, 'tickets': 5},
    {'id': 2, 'burst': 2, 'tickets': 1},
]

total_time = 20  # Tiempo máximo de simulación

avg_waiting, avg_turnaround = lottery_scheduling(processes, total_time)

print(f"\nTiempo promedio de espera: {avg_waiting:.2f}")
print(f"Tiempo promedio de finalización: {avg_turnaround:.2f}")
