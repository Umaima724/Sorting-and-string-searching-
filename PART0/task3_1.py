import csv

PATTERN = "highly recommend"
DATASET_FILE = "Reviews_Cleaned.csv"
LIMIT = 10000


def naive_search(text, pattern):
    
    n = len(text)
    m = len(pattern)

    comparisons = 0
    matches = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            matches += 1

    return matches, comparisons


def build_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = build_lps(pattern)

    comparisons = 0
    matches = 0

    i = 0  
    j = 0  

    while i < n:

        while j > 0:
            comparisons += 1

            if text[i] == pattern[j]:
                break

            j = lps[j - 1]

        if j == 0:
            comparisons += 1

            if text[i] == pattern[0]:
                j = 1
        else:
            j += 1

        i += 1


        if j == m:
            matches += 1
            j = lps[j - 1]

    return matches, comparisons


def load_reviews(filename, limit):
    reviews = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if len(reviews) >= limit:
                break

            text = row.get("Text", "")

            if text:
                reviews.append(text.lower())

    return reviews


def main():
    reviews = load_reviews(DATASET_FILE, LIMIT)

    print("Reviews loaded:", len(reviews))
    print("Search phrase:", repr(PATTERN))

    naive_matches = 0
    naive_comparisons = 0

    kmp_matches = 0
    kmp_comparisons = 0

    for review in reviews:
        matches, comparisons = naive_search(review, PATTERN)
        naive_matches += matches
        naive_comparisons += comparisons

        matches, comparisons = kmp_search(review, PATTERN)
        kmp_matches += matches
        kmp_comparisons += comparisons

    print("\nResults")
    print("Naive matches:", naive_matches)
    print("Naive character comparisons:", naive_comparisons)

    print("\nKMP matches:", kmp_matches)
    print("KMP character comparisons:", kmp_comparisons)

    print("\nComparison")
    if naive_comparisons > 0:
        reduction = (
            (naive_comparisons - kmp_comparisons)
            / naive_comparisons
        ) * 100

        print(f"Comparison reduction with KMP: {reduction:.2f}%")

    if naive_matches == kmp_matches:
        print("Verification: Both algorithms found the same matches.")
    else:
        print("WARNING: The match counts differ!")


if __name__ == "__main__":
    main()
