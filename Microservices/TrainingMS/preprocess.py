import pandas as pd 

#data preprocces
df = pd.read_csv("dataset.csv")
split_ratio = 0.8
split_point = int(len(df) * split_ratio)
train_data = df[:split_point]  
simulation_data = df[split_point:]  
simulation_data.to_csv("/var/lib/data/simulation_data.csv", index=False)
train_data.to_csv("/var/lib/data/train_data.csv", index=False)
print("Preprocessing data finshed.")