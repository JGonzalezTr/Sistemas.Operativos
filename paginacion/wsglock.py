import time

class Page:
    def __init__(self, page_id):
        self.page_id = page_id         # Identificador único de la página
        self.referenced = False        # Bit de referencia
        self.modified = False          # Bit de modificado
        self.load_time = time.time()   # Tiempo de carga en memoria
        self.last_used_time = time.time()  # Última vez que se utilizó

    def __repr__(self):
        return f"Page({self.page_id}, Ref={self.referenced}, Mod={self.modified})"


class WSClock:
    def __init__(self, size, tau):
        self.size = size              # Tamaño del buffer de páginas
        self.tau = tau                # Umbral del intervalo del Working Set
        self.pages = []               # Lista de páginas
        self.clock_pointer = 0        # Puntero al estilo reloj

    def add_page(self, page_id):
        # Verificar si la página ya está cargada
        for page in self.pages:
            if page.page_id == page_id:
                page.referenced = True
                page.last_used_time = time.time()
                return f"Page {page_id} is already in memory."

        # Si no está cargada, intentar cargarla
        if len(self.pages) < self.size:
            # Hay espacio disponible, cargar la página
            self.pages.append(Page(page_id))
            return f"Page {page_id} loaded into memory."
        else:
            # No hay espacio disponible, aplicar WSClock para el reemplazo
            return self.replace_page(page_id)

    def replace_page(self, page_id):
        while True:
            page = self.pages[self.clock_pointer]

            # Condición 1: Si la página no está referenciada y está fuera del Working Set
            current_time = time.time()
            if not page.referenced and (current_time - page.last_used_time > self.tau):
                # Si está modificada, simula escritura al disco
                if page.modified:
                    print(f"Writing Page {page.page_id} to disk before replacement.")
                # Reemplazar la página
                print(f"Replacing Page {page.page_id} with Page {page_id}.")
                self.pages[self.clock_pointer] = Page(page_id)
                return f"Page {page_id} replaced Page {page.page_id}."

            # Condición 2: Si la página está referenciada, apagar el bit y mover el puntero
            if page.referenced:
                page.referenced = False

            # Avanzar el puntero del reloj
            self.clock_pointer = (self.clock_pointer + 1) % self.size

# Ejemplo de uso
wsclock = WSClock(size=3, tau=5)  # Tamaño del buffer = 3, tau = 5 segundos

print(wsclock.add_page(1))  # Cargar página 1
print(wsclock.add_page(2))  # Cargar página 2
print(wsclock.add_page(3))  # Cargar página 3
time.sleep(2)               # Simular paso de tiempo
print(wsclock.add_page(4))  # Cargar página 4, reemplazar según WSClock
time.sleep(6)               # Simular más tiempo
print(wsclock.add_page(5))  # Cargar página 5, evaluar reemplazo
