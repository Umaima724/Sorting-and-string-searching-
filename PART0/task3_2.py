import csv

PATTERN = "gluten free"
DATASET_FILE = "Reviews_Cleaned.csv"
CHARACTER_LIMIT = 100000

BASE = 256


def load_reviews(filename):
    reviews = []

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            text = row.get("Text", "")

            if text and text.strip():
                reviews.append(text.lower())

    return reviews


def rabin_karp(text, pattern, q):
    
    n = len(text)
    m = len(pattern)

    hash_hits = 0
    verified_matches = 0

    if m == 0 or n < m:
        return hash_hits, verified_matches, 0

    highest_power = pow(BASE, m - 1, q)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (
            BASE * pattern_hash + ord(pattern[i])
        ) % q

        window_hash = (
            BASE * window_hash + ord(text[i])
        ) % q

    for i in range(n - m + 1):

        if window_hash == pattern_hash:
            hash_hits += 1

            if text[i:i + m] == pattern:
                verified_matches += 1

        if i < n - m:
            window_hash = (
                BASE * (
                    window_hash - ord(text[i]) * highest_power
                )
                + ord(text[i + m])
            ) % q

    spurious_hits = hash_hits - verified_matches

    return hash_hits, verified_matches, spurious_hits


def main():
    reviews = load_reviews(DATASET_FILE)

    print("Reviews loaded:", len(reviews))
    print("Search phrase:", repr(PATTERN))

    text = " ".join(reviews)[:CHARACTER_LIMIT]

    print("Characters searched:", len(text))

    moduli = [101, 1_000_000_007]

    print("\nRabin-Karp Results")

    for q in moduli:
        hash_hits, matches, spurious = rabin_karp(
            text, PATTERN, q
        )

        print(f"\nModulus (q): {q}")
        print("Hash Hits:", hash_hits)
        print("Verified Matches:", matches)
        print("Spurious Hits:", spurious)

        print(
            "Verification:",
            "Passed" if hash_hits == matches + spurious
            else "Failed"
        )


if __name__ == "__main__":
    main()
