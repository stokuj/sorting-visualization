import json
import random

# Generowanie danych
data = [random.randint(0, 100) for _ in range(20)]

# Zapis danych do pliku JSON
with open('data.json', 'w') as f:
    json.dump(data, f)

print("Dane zostały zapisane do pliku data.json")
