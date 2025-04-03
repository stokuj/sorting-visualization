# main.py

from sort_animation import run_animations, run_single_algorithm_animation

run_animations('data.json', 'animations/animation_1.gif', interval=50)
print(f'Animacja została zapisana w: animations/animation_1.gif')

run_animations('data.json', 'animations/animation_2.gif', interval=200)
print(f'Animacja została zapisana w: animations/animation_2.gif')

algorithms = [
    'bubble', 
    'quick', 
    'selection', 
    'insertion', 
    'merge', 
    'heap', 
    'shell', 
    'cocktail', 
    'radix'
]
for algo in algorithms:
    run_single_algorithm_animation(
        data_path='data.json',
        save_path=f'animations/{algo}_animation.gif',
        algorithm_name=algo
    )
    print(f'Animacja {algo} zapisana!')