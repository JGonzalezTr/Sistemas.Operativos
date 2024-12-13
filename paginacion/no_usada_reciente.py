import random

class Page:
    def __init__(self, id):
        self.id = id
        self.reference_bit = 0  # Bit R: Indica si la página fue accedida
        self.modified_bit = 0   # Bit M: Indica si la página fue modificada

    def __repr__(self):
        return f"Page({self.id}, R={self.reference_bit}, M={self.modified_bit})"

def nru_algorithm(memory_frames, pages, reset_interval=5):
    memory = []  # Marcos en memoria
    page_faults = 0

    # Simular acceso a las páginas
    for i, page_id in enumerate(pages):
        print(f"\nAccessing page {page_id}")
        
        # Buscar si la página ya está en memoria
        page_in_memory = next((p for p in memory if p.id == page_id), None)

        if page_in_memory:
            # Actualizar el bit de referencia si ya está en memoria
            page_in_memory.reference_bit = 1
            print(f"Page {page_id} is already in memory.")
        else:
            # Fallo de página: reemplazar o añadir
            page_faults += 1
            print(f"Page {page_id} caused a page fault.")

            if len(memory) < memory_frames:
                # Hay espacio disponible en memoria
                new_page = Page(page_id)
                memory.append(new_page)
            else:
                # Reemplazar página según NRU
                page_to_replace = select_page_to_replace(memory)
                print(f"Replacing page {page_to_replace.id} with page {page_id}.")
                memory.remove(page_to_replace)
                memory.append(Page(page_id))
        
        # Mostrar el estado de la memoria
        print(f"Memory: {memory}")

        # Reiniciar los bits de referencia cada cierto intervalo
        if (i + 1) % reset_interval == 0:
            reset_reference_bits(memory)
            print("Reference bits have been reset.")

    print(f"\nTotal page faults: {page_faults}")
    return page_faults

def select_page_to_replace(memory):
    # Clasificar las páginas según los bits R y M
    categories = {
        0: [],  # Clase 0: R=0, M=0
        1: [],  # Clase 1: R=0, M=1
        2: [],  # Clase 2: R=1, M=0
        3: []   # Clase 3: R=1, M=1
    }

    for page in memory:
        category = 2 * page.reference_bit + page.modified_bit
        categories[category].append(page)

    # Seleccionar una página de la categoría más baja disponible
    for category in range(4):
        if categories[category]:
            return random.choice(categories[category])  # Selección aleatoria dentro de la clase

def reset_reference_bits(memory):
    for page in memory:
        page.reference_bit = 0

# Simulación
if __name__ == "__main__":
    memory_frames = 3  # Número de marcos en memoria
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]  # Secuencia de páginas
    nru_algorithm(memory_frames, pages)
