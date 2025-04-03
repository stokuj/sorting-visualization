import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from itertools import zip_longest

# Generowanie losowych danych
data = [random.randint(0, 100) for _ in range(20)]
data_copy = data.copy()

# Przygotowanie wykresu
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Porównanie algorytmów sortowania')

# Konfiguracja Bubble Sort
ax1.set_title('Bubble Sort')
bars_bubble = ax1.bar(range(len(data)), data, align='edge', color='skyblue')
ax1.set_xlim(0, len(data))
ax1.set_ylim(0, 110)

# Konfiguracja Quick Sort
ax2.set_title('Quick Sort')
bars_quick = ax2.bar(range(len(data_copy)), data_copy, align='edge', color='lightgreen')
ax2.set_xlim(0, len(data_copy))
ax2.set_ylim(0, 110)

def bubble_generator(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
            yield arr.copy(), j, j+1
        if not swapped:
            break

def quick_sort_generator(arr):
    arr = arr.copy()
    stack = [(0, len(arr)-1)]
    
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        
        pivot = arr[high]
        i = low - 1
        yield arr.copy(), low, high, pivot, []
        
        for j in range(low, high):
            yield arr.copy(), low, high, pivot, [j, i]
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr.copy(), low, high, pivot, [j, i]
        
        arr[i+1], arr[high] = arr[high], arr[i+1]
        yield arr.copy(), low, high, pivot, [i+1, high]
        
        stack.append((low, i))
        stack.append((i+2, high))

def init():
    for bar in bars_bubble:
        bar.set_color('skyblue')
    for bar in bars_quick:
        bar.set_color('lightgreen')
    return [*bars_bubble, *bars_quick]

def update(frame):
    bubble_state, quick_state = frame
    
    # Aktualizacja Bubble Sort
    if bubble_state is not None:
        arr_bub, j, k = bubble_state
        for i, bar in enumerate(bars_bubble):
            bar.set_height(arr_bub[i])
            bar.set_color('salmon' if i in {j, j+1} else 'skyblue')
    
    # Aktualizacja Quick Sort
    if quick_state is not None:
        arr_quick, low, high, pivot, pointers = quick_state
        for i, bar in enumerate(bars_quick):
            color = 'lightgreen'
            if i == pivot:
                color = 'gold'
            elif low <= i <= high:
                color = 'mediumseagreen'
            if i in pointers:
                color = 'salmon'
            bar.set_height(arr_quick[i])
            bar.set_color(color)
    
    return [*bars_bubble, *bars_quick]

# Utworzenie generatorów
bubble_gen = bubble_generator(data)
quick_gen = quick_sort_generator(data_copy)

# Połącz generatory i wypełnij brakujące wartości
frames = zip_longest(bubble_gen, quick_gen, fillvalue=None)

# Utworzenie animacji
ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    init_func=init,
    blit=True,
    interval=500,
    repeat=False
)

plt.show()