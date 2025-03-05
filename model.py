import random

class Organismo:
    """Clase base para los organismos en el ecosistema."""
    def __init__(self, simbolo):
        self.simbolo = simbolo

class Depredador(Organismo):
    """Representa un depredador en el ecosistema."""
    def __init__(self, energia=10):
        super().__init__("🦊")
        self.energia = energia

class Presa(Organismo):
    """Representa una presa en el ecosistema."""
    def __init__(self, energia=3):
        super().__init__("🐔")
        self.energia = energia

class Planta(Organismo):
    """Representa una planta en el ecosistema."""
    def __init__(self):
        super().__init__("🌱")

def create_empty_matrix(size, row=0, matrix=None):
    """Función recursiva para crear una matriz vacía."""
    if matrix is None:
        matrix = []
    if row == size:
        return matrix
    return create_empty_matrix(size, row + 1, matrix + [["⚫" for _ in range(size)]])

def place_organisms(matrix, predators, preys, plants):
    """Coloca los organismos en la matriz de forma recursiva."""
    if predators == 0 and preys == 0 and plants == 0:
        return matrix
    r, c = random.randint(0, len(matrix) - 1), random.randint(0, len(matrix) - 1)
    if matrix[r][c] == "⚫":
        if predators > 0:
            matrix[r][c] = Depredador()
            return place_organisms(matrix, predators - 1, preys, plants)
        elif preys > 0:
            matrix[r][c] = Presa()
            return place_organisms(matrix, predators, preys - 1, plants)
        elif plants > 0:
            matrix[r][c] = Planta()
            return place_organisms(matrix, predators, preys, plants - 1)
    return place_organisms(matrix, predators, preys, plants)

def move_predators(matrix, size, r=0, c=0):
    """Mueve depredadores una celda hacia la presa más cercana y reduce su energía."""
    if r >= size:
        return matrix
    if c >= size:
        return move_predators(matrix, size, r + 1, 0)
    if isinstance(matrix[r][c], Depredador):
        matrix[r][c].energia -= 1
        if matrix[r][c].energia <= 0:
            matrix[r][c] = "⚫"  # Depredador muere
        else:
            prey_r, prey_c = find_adjacent_prey(matrix, r, c, size)
            if prey_r is not None and prey_c is not None:
                matrix[r][c].energia += 2
                matrix[prey_r][prey_c] = matrix[r][c]
                matrix[r][c] = "⚫"
            else:
                new_r, new_c = move_adjacent(r, c, size)
                if matrix[new_r][new_c] == "⚫":
                    matrix[new_r][new_c] = matrix[r][c]
                    matrix[r][c] = "⚫"
    return move_predators(matrix, size, r, c + 1)

def find_adjacent_prey(matrix, r, c, size, directions=None):
    """Busca una presa adyacente."""
    if directions is None:
        directions = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1),
                      (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]
    if not directions:
        return None, None
    new_r, new_c = directions[0]
    if 0 <= new_r < size and 0 <= new_c < size and isinstance(matrix[new_r][new_c], Presa):
        return new_r, new_c
    return find_adjacent_prey(matrix, r, c, size, directions[1:])

def move_adjacent(r, c, size):
    """Mueve un organismo a una celda adyacente válida."""
    directions = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    random.shuffle(directions)
    for new_r, new_c in directions:
        if 0 <= new_r < size and 0 <= new_c < size:
            return new_r, new_c
    return r, c

def run_simulation(matrix, size, cycles, current_cycle=1):
    """Ejecuta la simulación de manera recursiva e imprime cada ciclo."""
    if current_cycle > cycles:
        return matrix
    print(f"\nCiclo {current_cycle}:")
    print_matrix(matrix)
    matrix = move_predators(matrix, size)
    matrix = move_preys(matrix, size)
    if current_cycle % 3 == 0:
        matrix = grow_plants(matrix, 2, size)
    return run_simulation(matrix, size, cycles, current_cycle + 1)

def print_matrix(matrix, row=0):
    """Función recursiva para imprimir la matriz."""
    if row >= len(matrix):
        return
    print(" ".join([cell.simbolo if isinstance(cell, Organismo) else cell for cell in matrix[row]]))
    print_matrix(matrix, row + 1)

# Configuración inicial
size = 9
num_predators = 3
num_prey = 6
num_plants = 5
cycles = 10

# Creación del ecosistema
ecosystem = create_empty_matrix(size)
ecosystem = place_organisms(ecosystem, num_predators, num_prey, num_plants)

# Ejecutar simulación e imprimir ciclos
print("Estado inicial del ecosistema:")
print_matrix(ecosystem)
ecosystem = run_simulation(ecosystem, size, cycles)

# Imprimir estado final
print("\nEstado final del ecosistema:")
print_matrix(ecosystem)
