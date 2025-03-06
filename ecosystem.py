import random
import sys

sys.setrecursionlimit(2000)

class Organism:
    def __init__(self, symbol):
        self.symbol = symbol

class Predator(Organism):
    def __init__(self, energy=5):
        super().__init__("🦊")
        self.energy = energy

class Prey(Organism):
    def __init__(self, energy=3):
        super().__init__("🐔")
        self.energy = energy

class Plant(Organism):
    def __init__(self):
        super().__init__("🌿")

def create_empty_matrix(size, row=0, matrix=None):
    if matrix is None:
        matrix = []
    if row == size:
        return matrix
    return create_empty_matrix(size, row + 1, matrix + [["⚫" for _ in range(size)]])

def place_organisms(matrix, predators, preys, plants):
    if predators == 0 and preys == 0 and plants == 0:
        return matrix
    r, c = random.randint(0, len(matrix) - 1), random.randint(0, len(matrix) - 1)
    if matrix[r][c] == "⚫":
        if predators > 0:
            matrix[r][c] = Predator()
            return place_organisms(matrix, predators - 1, preys, plants)
        elif preys > 0:
            matrix[r][c] = Prey()
            return place_organisms(matrix, predators, preys - 1, plants)
        elif plants > 0:
            matrix[r][c] = Plant()
            return place_organisms(matrix, predators, preys, plants - 1)
    return place_organisms(matrix, predators, preys, plants)

def find_adjacent_prey(matrix, r, c, size, directions=None, index=0):
    if directions is None:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    if index >= len(directions): 
        return None, None

    dr, dc = directions[index]  
    new_r, new_c = r + dr, c + dc

    if 0 <= new_r < size and 0 <= new_c < size and isinstance(matrix[new_r][new_c], Prey):
        return new_r, new_c 

    return find_adjacent_prey(matrix, r, c, size, directions, index + 1)

def move_predators(matrix, size, r=0, c=0):
    """Moves predators one cell toward the nearest prey and reduces their energy."""
    if r >= size:
        return matrix
    if c >= size:
        return move_predators(matrix, size, r + 1, 0)
    if isinstance(matrix[r][c], Predator):
        predator = matrix[r][c]
        predator.energy -= 1
        if predator.energy <= 0:
            matrix[r][c] = "⚫" 
        else:
            prey_r, prey_c = find_adjacent_prey(matrix, r, c, size)
            if prey_r is not None:
                predator.energy += 2
                matrix[prey_r][prey_c] = predator
                matrix[r][c] = "⚫"
                if predator.energy >= 10:
                    matrix[r][c] = Predator()
    return move_predators(matrix, size, r, c + 1)

def move_preys(matrix, size, r=0, c=0):
    """Moves preys to an adjacent cell and consumes plants if available using full recursion."""
    if r >= size:
        return matrix
    if c >= size:
        return move_preys(matrix, size, r + 1, 0)
    
    if isinstance(matrix[r][c], Prey):
        prey = matrix[r][c]
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(directions)

        def try_move(index=0):
            if index >= len(directions):
                return  

            dr, dc = directions[index]
            new_r, new_c = r + dr, c + dc

            if 0 <= new_r < size and 0 <= new_c < size:
                if isinstance(matrix[new_r][new_c], Plant):  
                    prey.energy += 1
                    matrix[new_r][new_c] = prey
                    matrix[r][c] = "⚫"
                    return
                elif matrix[new_r][new_c] == "⚫":  
                    matrix[new_r][new_c] = prey
                    matrix[r][c] = "⚫"
                    return

            return try_move(index + 1) 

        try_move() 
        if prey.energy >= 5: 
            matrix[r][c] = Prey()
            
    return move_preys(matrix, size, r, c + 1) 

def grow_plants(matrix, count, size, attempts=0):
    if count == 0 or attempts >= 10:
        return matrix
    r, c = random.randint(0, size - 1), random.randint(0, size - 1)
    if matrix[r][c] == "⚫":
        matrix[r][c] = Plant()
        return grow_plants(matrix, count - 1, size, 0)
    return grow_plants(matrix, count, size, attempts + 1)

def run_simulation(matrix, size, cycles, current_cycle=1):
    if current_cycle > cycles:
        return matrix
    print(f"\nCycle {current_cycle}:")
    print_matrix(matrix)
    matrix = move_predators(matrix, size)
    matrix = move_preys(matrix, size)
    if current_cycle % 4 == 0:
        matrix = grow_plants(matrix, 2, size)
    return run_simulation(matrix, size, cycles, current_cycle + 1)

def print_matrix(matrix, row=0):
    if row >= len(matrix):
        return
    print(" ".join([cell.symbol if isinstance(cell, Organism) else cell for cell in matrix[row]]))
    print_matrix(matrix, row + 1)

"""CONFIGURACION"""
size = 5
num_predators = 2
num_prey = 8
num_plants = 5
cycles = 10 

ecosystem = create_empty_matrix(size)
ecosystem = place_organisms(ecosystem, num_predators, num_prey, num_plants)

ecosystem = run_simulation(ecosystem, size, cycles)
