class AgingAlgorithm:
    def __init__(self, num_frames):
        self.num_frames = num_frames          # Número de marcos de página
        self.frames = []                      # Páginas en memoria
        self.counters = {}                    # Contadores asociados a cada página
        self.reference_bits = {}              # Bits de referencia de las páginas

    def access_page(self, page):
        # Si la página ya está en memoria, marcarla como referenciada
        if page in self.frames:
            self.reference_bits[page] = 1
            print(f"Página {page} ya está en memoria.")
        else:
            # Si hay espacio disponible, agregar la página
            if len(self.frames) < self.num_frames:
                self.frames.append(page)
                self.counters[page] = 0
                self.reference_bits[page] = 1
                print(f"Página {page} cargada en memoria (espacio disponible).")
            else:
                # Reemplazo: encontrar la página con el contador más bajo
                page_to_replace = min(self.frames, key=lambda p: self.counters[p])
                print(f"Reemplazando página {page_to_replace} con página {page}.")
                self.frames.remove(page_to_replace)
                del self.counters[page_to_replace]
                del self.reference_bits[page_to_replace]

                self.frames.append(page)
                self.counters[page] = 0
                self.reference_bits[page] = 1

    def update_counters(self):
        print("Actualizando contadores...")
        for page in self.frames:
            self.counters[page] >>= 1  # Desplazar a la derecha
            if self.reference_bits[page] == 1:
                self.counters[page] |= 0b10000000  # Establecer el bit más significativo
            self.reference_bits[page] = 0  # Restablecer el bit de referencia
        self.print_state()

    def print_state(self):
        print("Estado actual:")
        print(f"Frames: {self.frames}")
        print(f"Contadores: {self.counters}")
        print(f"Bits de referencia: {self.reference_bits}")
        print("-" * 30)


# Simulación del algoritmo
num_frames = 3
aging = AgingAlgorithm(num_frames)

# Secuencia de accesos a páginas
page_sequence = [1, 2, 3, 2, 4, 1, 5, 3, 2, 4]

for i, page in enumerate(page_sequence):
    print(f"\nAcceso a la página {page}:")
    aging.access_page(page)
    aging.update_counters()
    
    

