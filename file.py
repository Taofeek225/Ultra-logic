from sklearn.datasets import load_iris
import pandas as pd

df = pd.DataFrame(load_iris().data, columns=load_iris().feature_names)
df['target'] = load_iris().target

print(df.head())
print(df.describe())

import seaborn as sns
import matplotlib.pyplot as plt

sns.pairplot(df, hue='target')
plt.show()
