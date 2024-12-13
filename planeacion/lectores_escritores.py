import threading
import time

# Variables globales
mutex = threading.Semaphore(1)  # Mutex para proteger la variable read_count
write_mutex = threading.Semaphore(1)  # Mutex para escritores
read_count = 0  # Número de lectores actuales

def reader(i):
    global read_count
    while True:
        time.sleep(1)  # Simula tiempo de espera
        # Leer
        mutex.acquire()  # Entrar en la región crítica
        read_count += 1  # Incrementar el contador de lectores
        if read_count == 1:
            write_mutex.acquire()  # Si es el primer lector, bloquear a los escritores
        mutex.release()  # Salir de la región crítica

        # Realizar la lectura aquí
        print(f"Lector {i} leyendo recurso compartido...")

        mutex.acquire()  # Entrar en la región crítica
        read_count -= 1  # Decrementar el contador de lectores
        if read_count == 0:
            write_mutex.release()  # Si es el último lector, liberar a los escritores
        mutex.release()  # Salir de la región crítica

def writer(i):
    while True:
        time.sleep(2)  # Simula tiempo de espera
        # Escribir
        write_mutex.acquire()  # Entrar en la región crítica (exclusiva para el escritor)

        # Realizar la escritura aquí
        print(f"Escritor {i} escribiendo en el recurso compartido...")

        write_mutex.release()  # Liberar el semáforo de los escritores

# Crear hilos para lectores y escritores
num_lectores = 3
num_escritores = 2

lectores = []
escritores = []

for i in range(num_lectores):
    t = threading.Thread(target=reader, args=(i,))
    lectores.append(t)
    t.start()

for i in range(num_escritores):
    t = threading.Thread(target=writer, args=(i,))
    escritores.append(t)
    t.start()

# Para evitar que el programa termine inmediatamente
for t in lectores + escritores:
    t.join()
