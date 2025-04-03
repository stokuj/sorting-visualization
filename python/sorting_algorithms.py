# sorting_algorithms.py

def bubble_gen(arr):
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

def quick_gen(arr):
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
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr.copy(), low, high, pivot, [j, i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        yield arr.copy(), low, high, pivot, [i+1, high]
        stack.extend([(low, i), (i+2, high)])

def selection_gen(arr):
    arr = arr.copy()
    for i in range(len(arr)):
        min_idx = i
        yield arr.copy(), i, min_idx
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr.copy(), i, min_idx, j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr.copy(), i, min_idx

def insertion_gen(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        yield arr.copy(), i, j
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
            yield arr.copy(), i, j
        arr[j+1] = key
        yield arr.copy(), i, j

def merge_gen(arr):
    arr = arr.copy()
    current_size = 1
    n = len(arr)
    while current_size < n:
        for start in range(0, n, 2 * current_size):
            mid = min(start + current_size, n)
            end = min(start + 2 * current_size, n)
            left = arr[start:mid]
            right = arr[mid:end]
            i = j = 0
            k = start
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                yield arr.copy(), start + i, mid + j
                k += 1
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
                yield arr.copy(), start + i, mid + j
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
                yield arr.copy(), start + i, mid + j
        current_size *= 2
    yield arr.copy(), -1, -1

def heap_gen(arr):
    arr = arr.copy()
    n = len(arr)
    
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr.copy(), i, largest
            yield from heapify(arr, n, largest)
        else:
            yield arr.copy(), i, largest
    
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        yield arr.copy(), 0, i
        yield from heapify(arr, i, 0)

def shell_gen(arr):
    arr = arr.copy()
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                yield arr.copy(), j, j - gap
            arr[j] = temp
            yield arr.copy(), i, j
        gap //= 2
    yield arr.copy(), -1, -1

def cocktail_gen(arr):
    arr = arr.copy()
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                yield arr.copy(), i, i + 1
        if not swapped:
            break
        end -= 1
        swapped = False
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
                yield arr.copy(), i, i + 1
        start += 1
    yield arr.copy(), -1, -1

def radix_gen(arr):
    arr = arr.copy()
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in arr:
            digit = (num // exp) % 10
            buckets[digit].append(num)
            yield arr.copy(), num, digit
        k = 0
        for i in range(10):
            for num in buckets[i]:
                arr[k] = num
                k += 1
                yield arr.copy(), k-1, i
        exp *= 10
    yield arr.copy(), -1, -1