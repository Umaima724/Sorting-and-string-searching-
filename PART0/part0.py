import pandas as pd
import re

df = pd.read_csv("Reviews.csv")

print("Original dataset shape:", df.shape)
print("\nOriginal columns:")
print(df.columns.tolist())


df["Text_Raw"] = df["Text"].copy()

required_columns = [
    "ProductId",
    "Score",
    "Time",
    "HelpfulnessNumerator",
    "HelpfulnessDenominator",
    "Text"
]

df = df.dropna(subset=required_columns).copy()

print("\nShape after removing missing values:", df.shape)


df["Text"] = df["Text"].apply(
    lambda text: re.sub(r"<[^>]*>", " ", str(text)).lower()
)

df["Text"] = df["Text"].apply(
    lambda text: re.sub(r"\s+", " ", text).strip()
)

df = df[df["HelpfulnessDenominator"] != 0].copy()

df["ratio"] = (
    df["HelpfulnessNumerator"] /
    df["HelpfulnessDenominator"]
)


df = df[df["ratio"] <= 1].copy()

print("\nShape after helpfulness filtering:", df.shape)

S1000 = df.head(1000).copy()


df.to_csv("Reviews_Cleaned.csv", index=False)
S1000.to_csv("S1000.csv", index=False)

print("\nFinal cleaned dataset shape:", df.shape)
print("S1000 shape:", S1000.shape)

print("\nFirst five rows of S1000:")
print(
    S1000[
        ["ProductId", "Score", "Text", "ratio"]
    ].head()
)

print("\nPart 0 completed successfully!")
