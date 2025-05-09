
import sys

import collections


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


# ближайише доступные неисследованные клетки
def get_neighbors(data, pos, collected_keys=set()):

    rows = len(data)
    if rows == 0:
        return []
    cols = len(data[0])
    
    x, y = pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        
        # проверка на index out of range
        if 0 <= nx < rows and 0 <= ny < cols:
            cell = data[nx][ny]
            
            # проверка на проходимость
            if (cell == '.' or cell == '@' or
                cell.islower() or
                (cell.isupper() and cell.lower() in collected_keys)):  # на двери
                neighbors.append((nx, ny))
    
    return neighbors


# ищет ключ, ближайший к текущей позиции и считает число шагов до него
def pathway(data, pos, collected_keys=None):
    if collected_keys is None:
        collected_keys = set()
    
    checked = [pos]  # проверенные клетки
    ways = [pos]
    steps = 0 # счетчик
    
    while ways:
        next_ways = []
        
        for current_pos in ways:
            x, y = current_pos
            cell = data[x][y]
            
            # проверяем нашли ли ключ
            if cell.islower() and cell not in collected_keys:
                return (steps, current_pos, cell)
            
            # получаем соседей для текущей позиции
            for neighbor in get_neighbors(data, current_pos, collected_keys):
                if neighbor not in checked:
                    checked.append(neighbor)
                    next_ways.append(neighbor)
        
        ways = next_ways
        steps += 1
    
    return None  # если ключ не найден


# определяет положения всех роботов на сетке
def robot_finder(data):
    robot_positions = []
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            if row[j] == '@':
                robot_positions.append((i, j))
    return robot_positions

def solve(data):
    collected_keys = set()
    count = 0
    
    while True:
        # все роботы
        robots = [(i, j) for i, row in enumerate(data) 
                 for j, cell in enumerate(row) if cell == '@']
        
        # ищем ближайший ключ для каждого робота
        candidates = []
        for pos in robots:
            result = pathway(data, pos, collected_keys)
            if result:  # если ключ найден
                candidates.append((pos, result))  # (стартовая позиция, (шаги, позиция_ключа, ключ))
        
        # если ключей больше нет то конец цикла
        if not candidates:
            break
        
        # выбираем робота с минимальным количеством шагов до его ближайшего ключа
        candidates.sort(key=lambda x: x[1][0])
        best_robot_pos, (steps, key_pos, key) = candidates[0]
        
        # обновляем данные
        count += steps
        print(steps, key_pos)
        collected_keys.add(key)
        
        # обновляем позицию робота (в сетке)
        x, y = best_robot_pos
        data[x][y] = '.'  # очистка
        x, y = key_pos
        data[x][y] = '@'  # постановка
        
    return count, collected_keys

def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()
