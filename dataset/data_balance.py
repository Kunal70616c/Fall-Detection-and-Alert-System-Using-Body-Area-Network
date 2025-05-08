import pandas as pd

# Load the dataset
df = pd.read_csv("fall_dataset.csv")

# Separate fall and nonfall data
fall_data = df[df["motion"] == "fall"]
nonfall_data = df[df["motion"] == "nonfall"]

# Match number of nonfall entries to fall entries
nonfall_sampled = nonfall_data.sample(n=len(fall_data), random_state=1)

# Combine both balanced data
balanced_df = pd.concat([fall_data, nonfall_sampled])

# Optional: Shuffle the combined data
balanced_df = balanced_df.sample(frac=1, random_state=1).reset_index(drop=True)

#Save to new file if needed
balanced_df.to_csv("balanced_fall_dataset.csv", index=False)

# Count of fall entries
print("Number of Fall entries:", len(fall_data))
