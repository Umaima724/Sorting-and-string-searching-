import csv

def counting_sort_reviews(reviews):

    n = len(reviews)

    count = [0] * 6

    for review in reviews:
        score = int(review["Score"])
        count[score] += 1

    frequencies = count[:]

    for i in range(1, 6):
        count[i] += count[i - 1]

    output = [None] * n

    for i in range(n - 1, -1, -1):
        score = int(reviews[i]["Score"])

        position = count[score] - 1
        output[position] = reviews[i]

        count[score] -= 1

    return output, frequencies

def load_reviews(filename):
    with open(filename, "r", encoding="utf-8-sig",
              newline="") as file:
        reader = csv.DictReader(file)
        reviews = list(reader)

    return reviews

def main():
    filename = "Reviews_Cleaned.csv"

    reviews = load_reviews(filename)

    print("Total reviews loaded:", len(reviews))

    sorted_reviews, frequencies = counting_sort_reviews(reviews)

    print("\nCounts of each score:")

    for score in range(1, 6):
        print(f"Score {score}: {frequencies[score]}")

    is_sorted = all(
        int(sorted_reviews[i]["Score"])
        <= int(sorted_reviews[i + 1]["Score"])
        for i in range(len(sorted_reviews) - 1)
    )

    print("\nSorted correctly:", is_sorted)

    with open("Reviews_Sorted_By_Score.csv", "w",
              encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=sorted_reviews[0].keys()
        )

        writer.writeheader()
        writer.writerows(sorted_reviews)

    print("Sorted dataset saved to Reviews_Sorted_By_Score.csv")


if __name__ == "__main__":
    main()
