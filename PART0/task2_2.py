import csv
import time

def counting_sort_digit(records, base, digit_position):
   
    n = len(records)
    count = [0] * base
    output = [None] * n

    for record in records:
        timestamp = int(record["Time"])
        digit = (timestamp // digit_position) % base
        count[digit] += 1

    for i in range(1, base):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        timestamp = int(records[i]["Time"])
        digit = (timestamp // digit_position) % base

        position = count[digit] - 1
        output[position] = records[i]
        count[digit] -= 1

    return output


def radix_sort_base10(records):

    if not records:
        return []

    result = records[:]
    max_time = max(int(record["Time"]) for record in result)

    digit_position = 1

    while max_time // digit_position > 0:
        result = counting_sort_digit(
            result, 10, digit_position
        )
        digit_position *= 10

    return result


def radix_sort_base256(records):

    if not records:
        return []

    result = records[:]
    max_time = max(int(record["Time"]) for record in result)

    digit_position = 1

    while max_time // digit_position > 0:
        result = counting_sort_digit(
            result, 256, digit_position
        )
        digit_position *= 256

    return result

def load_reviews(filename):
    with open(filename, "r", encoding="utf-8-sig",
              newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def main():
    filename = "Reviews_Cleaned.csv"
    reviews = load_reviews(filename)

    print("Total reviews:", len(reviews))

    start = time.perf_counter()
    sorted_base10 = radix_sort_base10(reviews)
    time_base10 = time.perf_counter() - start

    start = time.perf_counter()
    sorted_base256 = radix_sort_base256(reviews)
    time_base256 = time.perf_counter() - start

    correct_base10 = all(
        int(sorted_base10[i]["Time"])
        <= int(sorted_base10[i + 1]["Time"])
        for i in range(len(sorted_base10) - 1)
    )

    correct_base256 = all(
        int(sorted_base256[i]["Time"])
        <= int(sorted_base256[i + 1]["Time"])
        for i in range(len(sorted_base256) - 1)
    )

    same_order = (
        [int(r["Time"]) for r in sorted_base10]
        == [int(r["Time"]) for r in sorted_base256]
    )

    print("\nBase-10 execution time:", round(time_base10, 4), "seconds")
    print("Base-256 execution time:", round(time_base256, 4), "seconds")

    print("\nBase-10 sorted correctly:", correct_base10)
    print("Base-256 sorted correctly:", correct_base256)
    print("Both results agree:", same_order)

    print("\nFirst 10 timestamps:")
    print([int(r["Time"]) for r in sorted_base256[:10]])

    with open("Reviews_Sorted_By_Time.csv", "w",
              encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=sorted_base256[0].keys()
        )

        writer.writeheader()
        writer.writerows(sorted_base256)

    print("\nSorted dataset saved to Reviews_Sorted_By_Time.csv")


if __name__ == "__main__":
    main()
