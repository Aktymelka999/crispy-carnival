import pandas as pd

df = pd.read_csv("transactions.csv", sep=";")

# Сохраняем в Excel
df.to_excel("transactions_excel.xlsx", index=False)

print("✅ transactions_excel.xlsx создан из локального CSV!")
