# sort_animation.py

import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import zip_longest
from sorting_algorithms import (
    bubble_gen, quick_gen, selection_gen, insertion_gen,
    merge_gen, heap_gen, shell_gen, cocktail_gen, radix_gen
)

# Wspólna konfiguracja algorytmów
ALGORITHM_CONFIG = {
    'bubble': {
        'title': 'Bubble Sort',
        'color': 'skyblue',
        'active_color': 'salmon',
        'generator': bubble_gen
    },
    'quick': {
        'title': 'Quick Sort',
        'color': 'lightgreen',
        'active_color': 'gold',
        'generator': quick_gen
    },
    'selection': {
        'title': 'Selection Sort',
        'color': 'lavender',
        'active_color': 'mediumorchid',
        'generator': selection_gen
    },
    'insertion': {
        'title': 'Insertion Sort',
        'color': 'peachpuff',
        'active_color': 'darkorange',
        'generator': insertion_gen
    },
    'merge': {
        'title': 'Merge Sort',
        'color': 'lightcoral',
        'active_color': 'aqua',
        'generator': merge_gen
    },
    'heap': {
        'title': 'Heap Sort',
        'color': 'lightblue',
        'active_color': 'navy',
        'generator': heap_gen
    },
    'shell': {
        'title': 'Shell Sort',
        'color': 'thistle',
        'active_color': 'purple',
        'generator': shell_gen
    },
    'cocktail': {
        'title': 'Cocktail Sort',
        'color': 'wheat',
        'active_color': 'peru',
        'generator': cocktail_gen
    },
    'radix': {
        'title': 'Radix Sort',
        'color': 'lightcyan',
        'active_color': 'teal',
        'generator': radix_gen
    }
}

def init_bars(bars, color):
    for bar in bars:
        bar.set_color(color)
    return bars

def load_data(data_path):
    with open(data_path, 'r') as f:
        return json.load(f)

def create_plot_grid():
    fig, axs = plt.subplots(3, 3, figsize=(14, 14))
    fig.suptitle('Porównanie algorytmów sortowania', fontsize=16)
    return fig, axs

def setup_algorithm_axes(ax, title, color, data_length):
    ax.set_title(title)
    ax.set_xlim(0, data_length)
    ax.set_ylim(0, 110)
    ax.set_xticks([])
    ax.set_yticks([])

def create_animation(fig, update_func, init_func, frames, interval):
    return animation.FuncAnimation(
        fig,
        update_func,
        frames=frames,
        init_func=init_func,
        blit=False,
        interval=interval,
        repeat=False,
        cache_frame_data=False
    )

# Wspólna funkcja dla aktualizacji stanu
def handle_algorithm_state(algorithm, state, bars):
    if not state:
        return

    arr = state[0]
    for idx, bar in enumerate(bars):
        bar.set_height(arr[idx])
        
    # Bubble Sort
    if algorithm == 'bubble':
        _, j, k = state
        for i, bar in enumerate(bars):
            bar.set_color(ALGORITHM_CONFIG['bubble']['active_color'] if i in {j, k} else ALGORITHM_CONFIG['bubble']['color'])

    # Quick Sort
    elif algorithm == 'quick':
        _, low, high, pivot, ptrs = state
        for i, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['quick']['color']
            if i == pivot:
                color = 'gold'
            elif low <= i <= high:
                color = 'mediumseagreen'
            if i in ptrs:
                color = ALGORITHM_CONFIG['quick']['active_color']
            bar.set_color(color)
    elif algorithm == 'selection':
        _, i, min_idx, *rest = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['selection']['color']
            if idx == i:
                color = ALGORITHM_CONFIG['selection']['active_color']
            elif idx == min_idx:
                color = 'salmon'
            elif idx in rest:
                color = 'plum'
            bar.set_color(color)

    elif algorithm == 'insertion':
        _, i, j = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['insertion']['color']
            if idx == i:
                color = 'salmon'
            elif idx == j:
                color = ALGORITHM_CONFIG['insertion']['active_color']
            bar.set_color(color)

    elif algorithm == 'merge':
        _, i, j = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['merge']['color']
            if idx == i or idx == j:
                color = ALGORITHM_CONFIG['merge']['active_color']
            bar.set_color(color)

    elif algorithm == 'heap':
        _, i, j = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['heap']['color']
            if idx == i or idx == j:
                color = ALGORITHM_CONFIG['heap']['active_color']
            bar.set_color(color)

    elif algorithm == 'shell':
        _, current, prev = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['shell']['color']
            if idx == current or idx == prev:
                color = ALGORITHM_CONFIG['shell']['active_color']
            bar.set_color(color)

    elif algorithm == 'cocktail':
        _, i, j = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['cocktail']['color']
            if idx == i or idx == j:
                color = ALGORITHM_CONFIG['cocktail']['active_color']
            bar.set_color(color)

    elif algorithm == 'radix':
        _, pos, bucket = state
        for idx, bar in enumerate(bars):
            color = ALGORITHM_CONFIG['radix']['color']
            if idx == pos:
                color = ALGORITHM_CONFIG['radix']['active_color']
            bar.set_color(color)


def run_animations(data_path, save_path, interval=50):
    data = load_data(data_path)
    datasets = [data.copy() for _ in range(9)]
    fig, axs = create_plot_grid()
    
    algorithms = [
        {'name': 'bubble', 'ax': axs[0,0]},
        {'name': 'quick', 'ax': axs[0,1]},
        {'name': 'selection', 'ax': axs[0,2]},
        {'name': 'insertion', 'ax': axs[1,0]},
        {'name': 'merge', 'ax': axs[1,1]},
        {'name': 'heap', 'ax': axs[1,2]},
        {'name': 'shell', 'ax': axs[2,0]},
        {'name': 'cocktail', 'ax': axs[2,1]},
        {'name': 'radix', 'ax': axs[2,2]}
    ]

    bars = []
    for algo in algorithms:
        config = ALGORITHM_CONFIG[algo['name']]
        setup_algorithm_axes(algo['ax'], config['title'], config['color'], len(data))
        bars.append(algo['ax'].bar(range(len(data)), data, align='edge', color=config['color']))

    def update(frame):
        for idx, (algo, dataset) in enumerate(zip(algorithms, datasets)):
            handle_algorithm_state(algo['name'], frame[idx], bars[idx])
        return [bar for sublist in bars for bar in sublist]

    frames = zip_longest(*[ALGORITHM_CONFIG[algo['name']]['generator'](dataset) for algo, dataset in zip(algorithms, datasets)])
    
    ani = create_animation(fig, update, lambda: init_bars([bar for sublist in bars for bar in sublist], None), frames, interval)
    ani.save(save_path, writer='pillow', fps=60)
    plt.close(fig)

def run_single_algorithm_animation(data_path, save_path, algorithm_name, interval=50):
    if algorithm_name not in ALGORITHM_CONFIG:
        raise ValueError(f"Nieznany algorytm: {algorithm_name}")

    config = ALGORITHM_CONFIG[algorithm_name]
    data = load_data(data_path)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    setup_algorithm_axes(ax, config['title'], config['color'], len(data))
    bars = ax.bar(range(len(data)), data, align='edge', color=config['color'])
    
    generator = config['generator'](data.copy())

    def update(frame):
        state = next(generator, None)
        if state:
            handle_algorithm_state(algorithm_name, state, bars)
        return bars

    ani = create_animation(fig, update, lambda: init_bars(bars, config['color']), generator, interval)
    ani.save(save_path, writer='pillow', fps=60)
    plt.close(fig)