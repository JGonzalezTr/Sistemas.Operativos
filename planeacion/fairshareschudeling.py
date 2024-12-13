def fair_share_scheduling(groups, quantum):
    """
    Planificación por partes equitativas (Fair Share Scheduling) con un bucle 'for'.

    :param groups: Lista de grupos, cada uno con 'id', 'quota', y 'processes'.
                   Cada proceso tiene 'id', 'burst', y 'remaining'.
    :param quantum: Cantidad de tiempo que un proceso puede ejecutar por turno.
    """
    time = 0
    waiting_times = {}
    turnaround_times = {}

    # Contamos el tiempo total restante de todos los procesos
    total_remaining_time = sum(process['remaining'] for group in groups for process in group['processes'])

    # Estimamos el número de iteraciones basándonos en el tiempo total restante
    # Asegurándonos de no hacer iteraciones infinitas, por ejemplo, con la fórmula:
    total_rounds = (total_remaining_time + quantum - 1) // quantum

    print("Planificación por Partes Equitativas - Detalles de Ejecución")
    print("-----------------------------------------------------------")

    # Iteramos por un número estimado de rondas
    for _ in range(total_rounds):
        for group in groups:
            # Procesos activos en este grupo
            active_processes = [p for p in group['processes'] if p['remaining'] > 0]

            if not active_processes:
                continue

            # Tiempo disponible para este grupo en esta ronda
            group_time = int(group['quota'] * quantum)

            print(f"Tiempo {time}: Grupo {group['id']} tiene {group_time} unidades de tiempo.")

            for process in active_processes:
                if group_time <= 0:
                    break  # Si el tiempo del grupo se consumió, pasar al siguiente grupo

                # Determinar cuánto tiempo puede ejecutarse el proceso
                exec_time = min(group_time, process['remaining'], quantum)
                process['remaining'] -= exec_time
                group_time -= exec_time
                time += exec_time

                # Registrar tiempos si el proceso termina
                if process['remaining'] == 0 and process['id'] not in turnaround_times:
                    turnaround_times[process['id']] = time
                    waiting_times[process['id']] = time - process['burst']
                    print(f"Proceso {process['id']} del grupo {group['id']} terminó en el tiempo {time}.")

                print(f"Proceso {process['id']} ejecutado por {exec_time} unidades. Resta {process['remaining']} unidades.")

            print("-" * 50)

    # Cálculos de promedios
    avg_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    avg_turnaround_time = sum(turnaround_times.values()) / len(turnaround_times)

    return avg_waiting_time, avg_turnaround_time


# Datos de ejemplo
groups = [
    {
        'id': 1,
        'quota': 0.5,  # 50% del tiempo de CPU para este grupo
        'processes': [
            {'id': 'A', 'burst': 8, 'remaining': 8},
            {'id': 'B', 'burst': 6, 'remaining': 6},
        ]
    },
    {
        'id': 2,
        'quota': 0.3,  # 30% del tiempo de CPU para este grupo
        'processes': [
            {'id': 'C', 'burst': 4, 'remaining': 4},
        ]
    },
    {
        'id': 3,
        'quota': 0.2,  # 20% del tiempo de CPU para este grupo
        'processes': [
            {'id': 'D', 'burst': 10, 'remaining': 10},
        ]
    },
]

quantum = 4  # Tiempo máximo de ejecución por proceso por turno

avg_waiting, avg_turnaround = fair_share_scheduling(groups, quantum)

print(f"\nTiempo promedio de espera: {avg_waiting:.2f}")
print(f"Tiempo promedio de finalización: {avg_turnaround:.2f}")
