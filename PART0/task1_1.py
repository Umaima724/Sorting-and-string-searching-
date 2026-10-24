import csv

def max_heapify(arr, n, i):
    
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)


def build_max_heap(arr):
    
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)

def min_heapify(arr, n, i):
    
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] < arr[smallest]:
        smallest = left

    if right < n and arr[right] < arr[smallest]:
        smallest = right

    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        min_heapify(arr, n, smallest)


def build_min_heap(arr):
    """Convert an array into a min-heap."""
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        min_heapify(arr, n, i)


def heap_sort_descending(arr):
    
    n = len(arr)

    build_min_heap(arr)

    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        min_heapify(arr, end, 0)

    return arr

def load_denominators(filename):
    
    values = []

    with open(filename, "r", encoding="utf-8-sig",
              newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            value = row.get("HelpfulnessDenominator")

            if value is not None and value.strip():
                values.append(int(float(value)))

    return values


def main():
    filename = "Reviews_Cleaned.csv"

    values = load_denominators(filename)

    print("Number of values loaded:", len(values))

    
    max_heap_test = values[:]
    build_max_heap(max_heap_test)

    
    valid_max_heap = all(
        max_heap_test[(i - 1) // 2] >= max_heap_test[i]
        for i in range(1, len(max_heap_test))
    )

    print("Max-Heap property verified:", valid_max_heap)

    
    sorted_values = heap_sort_descending(values)

    print("\nTop 10 largest HelpfulnessDenominator values:")
    print(sorted_values[:10])

    print("\nDescending order verified:",
          all(sorted_values[i] >= sorted_values[i + 1]
              for i in range(len(sorted_values) - 1)))

    
    with open("HelpfulnessDenominator_Sorted.csv", "w",
              newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["HelpfulnessDenominator"])
        writer.writerows([[value] for value in sorted_values])

    print("\nSorted values saved successfully.")


if __name__ == "__main__":
    main()
