from pandas import read_csv
import matplotlib.pyplot as plt

df = read_csv('out/logs.csv', parse_dates=[0], index_col=0, squeeze=True, delimiter="\t")
df.plot()
plt.xticks(rotation=15)
plt.show()
