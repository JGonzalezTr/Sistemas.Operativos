def fifo_algorithm(memory_frames, pages):
    memory = []  # Marcos en memoria
    page_faults = 0  # Contador de fallos de página
    queue = []  # Cola para gestionar las páginas en memoria

    for page in pages:
        print(f"Accessing page {page}")

        if page not in memory:
            # Fallo de página
            page_faults += 1
            print(f"Page {page} caused a page fault.")

            if len(memory) < memory_frames:
                # Hay espacio en memoria: añadir la página
                memory.append(page)
                queue.append(page)
            else:
                # Reemplazo FIFO
                page_to_replace = queue.pop(0)  # Eliminar la página más antigua
                memory.remove(page_to_replace)  # Eliminar de memoria
                memory.append(page)  # Añadir la nueva página
                queue.append(page)  # Añadirla al final de la cola

        else:
            print(f"Page {page} is already in memory.")

        print(f"Memory: {memory}")

    print(f"\nTotal page faults: {page_faults}")
    return page_faults

# Simulación
if __name__ == "__main__":
    memory_frames = 3  # Número de marcos en memoria
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]  # Secuencia de páginas
    fifo_algorithm(memory_frames, pages)
