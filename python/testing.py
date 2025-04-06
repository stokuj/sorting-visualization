from sorting_algorithms import quick_gen

data = [5, 3, 8, 1, 2]
generator = quick_gen(data.copy(), pivot_method='random')  # np. dla pivot_method='random'

# Sprawdź, czy generator zwraca klatki
for frame in generator:
    print(frame)  # Jeśli nic nie drukuje, generator jest uszkodzony