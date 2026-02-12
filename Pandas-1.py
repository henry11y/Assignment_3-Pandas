import pandas as pd

# 1) Load CSVs (change paths if yours are in a folder like data/)
petal_df = pd.read_csv("data/Petal_Data.csv")
sepal_df = pd.read_csv("data/Sepal_Data.csv")

# 2) Clean column names (lowercase + underscores)
petal_df.columns = [c.strip().lower().replace(" ", "_") for c in petal_df.columns]
sepal_df.columns = [c.strip().lower().replace(" ", "_") for c in sepal_df.columns]

# 3) Rename columns to match required names (edit these if your headers differ)
rename_map = {
    "sampleid": "sample_id",
    "id": "sample_id",
    "species_name": "species",
    "petal_length_cm": "petal_length",
    "petal_width_cm": "petal_width",
    "sepal_length_cm": "sepal_length",
    "sepal_width_cm": "sepal_width",
}
petal_df = petal_df.rename(columns=rename_map)
sepal_df = sepal_df.rename(columns=rename_map)

# 4) Merge into one DataFrame (sample id + species)
df = pd.merge(petal_df, sepal_df, on=["sample_id", "species"], how="inner")

# 5) Keep only the required columns (in the order the assignment wants)
df = df[["sample_id", "species", "petal_length", "petal_width", "sepal_length", "sepal_width"]]

print("\n--- Combined DataFrame (first 5 rows) ---")
print(df.head())

# =========================
# PART 2: Correlations (6 comparisons)
# =========================
corr = df[["petal_length", "petal_width", "sepal_length", "sepal_width"]].corr()

print("\n--- Correlations (6 comparisons) ---")
print("petal_length vs petal_width:", corr.loc["petal_length", "petal_width"])
print("petal_length vs sepal_length:", corr.loc["petal_length", "sepal_length"])
print("petal_length vs sepal_width:", corr.loc["petal_length", "sepal_width"])
print("petal_width  vs sepal_length:", corr.loc["petal_width", "sepal_length"])
print("petal_width  vs sepal_width:", corr.loc["petal_width", "sepal_width"])
print("sepal_length vs sepal_width:", corr.loc["sepal_length", "sepal_width"])

# =========================
# PART 3-5: Mean / Median / Std by species
# =========================
grouped = df.groupby("species")[["petal_length", "petal_width", "sepal_length", "sepal_width"]]

means = grouped.mean()
medians = grouped.median()
stds = grouped.std()

print("\n--- Mean by species ---")
print(means)

print("\n--- Median by species ---")
print(medians)

print("\n--- Standard deviation by species ---")
print(stds)

# =========================
# PART 6: Most similar / least similar (based on mean measurements)
# =========================
species_list = list(means.index)

distances = []
for i in range(len(species_list)):
    for j in range(i + 1, len(species_list)):
        s1 = species_list[i]
        s2 = species_list[j]

        diff = means.loc[s1] - means.loc[s2]
        dist = (diff ** 2).sum() ** 0.5
        distances.append((s1, s2, dist))

distances.sort(key=lambda x: x[2])

most_similar = distances[0]
least_similar = distances[-1]

print("\n--- Similarity (based on mean measurements) ---")
print("Most similar:", most_similar[0], "and", most_similar[1], "| distance =", most_similar[2])
print("Least similar:", least_similar[0], "and", least_similar[1], "| distance =", least_similar[2])

print("\nUse this table to reference your measurements in your answer:")
print(means) 