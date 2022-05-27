from sklearn.cluster import KMeans
import pandas as pd

df = pd.read_csv("test_score.csv", index_col=0)

vec = KMeans(n_clusters=3)

vec.fit(df)
print(vec.labels_)
