
import csv
import time


# ==========================================
# Insertion Sort within each bucket
# ==========================================

def insertion_sort(bucket):
    """Sort one bucket in ascending ratio order."""

    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1

        # Shift larger ratios one position to the right.
        while j >= 0 and float(bucket[j]["ratio"]) > float(key["ratio"]):
            bucket[j + 1] = bucket[j]
            j -= 1

        # Insert the current review in its correct position.
        bucket[j + 1] = key


# ==========================================
# Bucket Sort using 10 equal-sized buckets
# ==========================================

def bucket_sort_reviews(reviews):
    """Sort reviews by ratio using 10 buckets."""

    number_of_buckets = 10

    # Create 10 empty buckets.
    buckets = [[] for _ in range(number_of_buckets)]

    # Distribute reviews into buckets.
    for review in reviews:
        ratio = float(review["ratio"])

        # Map ratios from [0, 1] to bucket indices 0 through 9.
        index = int(ratio * number_of_buckets)

        # Ratio 1.0 would produce index 10, so use bucket 9.
        if index >= number_of_buckets:
            index = number_of_buckets - 1

        buckets[index].append(review)

    # Print the size of every bucket.
    print("\nBucket sizes:")
    for i in range(number_of_buckets):
        lower = i / number_of_buckets
        upper = (i + 1) / number_of_buckets

        print(
            f"Bucket {i} [{lower:.1f}, {upper:.1f}"
            f"{']' if i == 9 else ')'}: {len(buckets[i])} reviews"
        )

    # Sort each bucket independently.
    for bucket in buckets:
        insertion_sort(bucket)

    # Combine buckets in ascending order.
    sorted_reviews = []

    for bucket in buckets:
        for review in bucket:
            sorted_reviews.append(review)

    return sorted_reviews


# ==========================================
# Load the cleaned dataset
# ==========================================

def load_reviews(filename):
    with open(filename, "r", encoding="utf-8-sig",
              newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# ==========================================
# Main program
# ==========================================

def main():
    filename = "Reviews_Cleaned.csv"
    reviews = load_reviews(filename)

    print("Total reviews loaded:", len(reviews))

    start = time.perf_counter()
    sorted_reviews = bucket_sort_reviews(reviews)
    elapsed = time.perf_counter() - start

    # Verify ascending ratio order.
    is_sorted = all(
        float(sorted_reviews[i]["ratio"])
        <= float(sorted_reviews[i + 1]["ratio"])
        for i in range(len(sorted_reviews) - 1)
    )

    print("\nExecution time:", round(elapsed, 4), "seconds")
    print("Sorted correctly:", is_sorted)

    print("\nFirst 10 sorted ratios:")
    print([float(r["ratio"]) for r in sorted_reviews[:10]])

    # Save the complete sorted dataset.
    if sorted_reviews:
        with open("Reviews_Sorted_By_Ratio.csv", "w",
                  encoding="utf-8", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=sorted_reviews[0].keys()
            )

            writer.writeheader()
            writer.writerows(sorted_reviews)

    print("\nSorted dataset saved to Reviews_Sorted_By_Ratio.csv")


if __name__ == "__main__":
    main()
