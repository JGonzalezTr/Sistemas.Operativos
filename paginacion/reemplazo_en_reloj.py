class Page:
    def __init__(self, id):
        self.id = id
        self.reference_bit = 0  # Bit de referencia

    def __repr__(self):
        return f"Page({self.id}, R={self.reference_bit})"

def clock_replacement_algorithm(memory_frames, pages):
    memory = []  # Marcos en memoria
    page_faults = 0  # Contador de fallos de página
    pointer = 0  # Puntero del reloj

    for page_id in pages:
        print(f"\nAccessing page {page_id}")

        # Buscar si la página ya está en memoria
        page_in_memory = next((p for p in memory if p.id == page_id), None)

        if page_in_memory:
            # La página está en memoria: actualizar su bit de referencia
            page_in_memory.reference_bit = 1
            print(f"Page {page_id} is already in memory. Marking R=1.")
        else:
            # Fallo de página
            page_faults += 1
            print(f"Page {page_id} caused a page fault.")

            if len(memory) < memory_frames:
                # Hay espacio en memoria: añadir la nueva página
                memory.append(Page(page_id))
            else:
                # Reemplazo usando el algoritmo de reloj
                while True:
                    current_page = memory[pointer]
                    if current_page.reference_bit == 0:
                        # Reemplazar página si R=0
                        print(f"Replacing page {current_page.id} with page {page_id}.")
                        memory[pointer] = Page(page_id)
                        pointer = (pointer + 1) % memory_frames  # Avanzar el puntero
                        break
                    else:
                        # Dar una segunda oportunidad: reiniciar R y mover al siguiente
                        print(f"Page {current_page.id} gets a second chance. Resetting R=0.")
                        current_page.reference_bit = 0
                        pointer = (pointer + 1) % memory_frames

        # Mostrar el estado actual de la memoria
        print(f"Memory: {memory}")

    print(f"\nTotal page faults: {page_faults}")
    return page_faults

# Simulación
if __name__ == "__main__":
    memory_frames = 3  # Número de marcos en memoria
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]  # Secuencia de páginas
    clock_replacement_algorithm(memory_frames, pages)




