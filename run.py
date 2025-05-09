import json

def check_capacity(int: max_capacity, dict: guests) -> bool:
    # список событий (кортежи из дат + count)
    events = []
    for guest in guests:
        events.append((guest["check-in"], 1))   # въезд
        events.append((guest["check-out"], -1)) # выезд

    # сортируем события по дате
    events.sort(key=lambda x: (x[0], x[1]))
    # (по усл. можно заехать и выехать в тот же день в одну комнату)

    current = 0
    max_guests = 0
    for date, change in events:
        current += change
        if current > max_guests:
            max_guests = current

    return max_guests <= max_capacity

if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())
    
    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)
    
    result = check_capacity(max_capacity, guests)
    print(result)
