import pandas as pd
import itertools
import os

# read in the main data set
df = pd.read_csv("DOC_20221229010716.csv")

# get all the column names, excluding the "class" column
column_names = [col for col in df.columns if col != "class"]

# get all combinations of sets with a minimum combination of 2
combinations = list(itertools.combinations(column_names, 2))

# create a folder to resemble the csv title
folder_name = "DOC_20221229010716"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# iterate through each combination and save down a new csv in the folder
for i, combination in enumerate(combinations):
    # select the columns for this combination
    subset = df[list(combination) + ["class"]]
    # save the subset to a new csv in the folder
    subset.to_csv(f"{folder_name}/DOC_20221229010716_{i+1}.csv", index=False)
