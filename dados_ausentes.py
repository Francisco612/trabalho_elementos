import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data_final.csv", encoding="utf-8", sep=";")

# Verifica se existem dados ausentes
# print(df[df.isnull().any(axis=1)])
print(df.isnull().sum())
# Mostrar apenas colunas com os dados ausentes
'''missing = df.isnull().sum()
print(missing[missing > 0])'''

#mapa de calor para visualizar os dados ausentes
cols_com_faltas = df.columns[df.isnull().any()]
df_faltas = df[cols_com_faltas]

#heatmap
plt.figure(figsize=(12, 6))  # aumenta o tamanho do gráfico
sns.heatmap(df_faltas.isnull(), cbar=False, cmap='viridis')
plt.title("Mapa de Dados Ausentes")
plt.show()

