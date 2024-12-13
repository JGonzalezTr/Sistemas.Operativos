import threading
import time
import random

# Definiciones
N = 5  # Número de filósofos
PENSANDO = 0
HAMBRIENTO = 1
COMIENDO = 2

# Estado de los filósofos
estado = [PENSANDO] * N  # Inicialmente todos los filósofos están pensando
mutex = threading.Lock()  # Exclusión mutua para la región crítica
semaforos = [threading.Semaphore(0) for _ in range(N)]  # Semáforos para cada filósofo

# Funciones de simulación
def pensar(i):
    print(f"Filósofo {i} está pensando.")
    time.sleep(random.uniform(1, 3))  # Pensando durante 1 a 3 segundos

def comer(i):
    print(f"Filósofo {i} está comiendo.")
    time.sleep(random.uniform(1, 3))  # Comiendo durante 1 a 3 segundos

def tomar_tenedores(i):
    with mutex:
        estado[i] = HAMBRIENTO  # El filósofo está intentando tomar los tenedores
        probar(i)

def poner_tenedores(i):
    with mutex:
        estado[i] = PENSANDO  # El filósofo termina de comer y vuelve a pensar
        probar((i + N - 1) % N)  # Verifica si el vecino izquierdo puede comer
        probar((i + 1) % N)  # Verifica si el vecino derecho puede comer

def probar(i):
    # El filósofo solo puede comer si sus dos vecinos no están comiendo
    if estado[i] == HAMBRIENTO and estado[(i + N - 1) % N] != COMIENDO and estado[(i + 1) % N] != COMIENDO:
        estado[i] = COMIENDO
        semaforos[i].release()  # Desbloquea al filósofo para que coma

def filosofo(i):
    while True:
        pensar(i)
        tomar_tenedores(i)
        semaforos[i].acquire()  # Espera a que se le liberen los tenedores
        comer(i)
        poner_tenedores(i)

# Crear y lanzar los hilos de los filósofos
hilos = []
for i in range(N):
    hilo = threading.Thread(target=filosofo, args=(i,))
    hilos.append(hilo)
    hilo.start()

# Unir los hilos para que el programa siga corriendo
for hilo in hilos:
    hilo.join()
