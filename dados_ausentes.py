import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data_final.csv", encoding="utf-8", sep=";")

# Verifica se existem dados ausentes
# print(df[df.isnull().any(axis=1)])
#print(df.isnull().sum())
# Mostrar apenas colunas com os dados ausentes
'''missing = df.isnull().sum()
print(missing[missing > 0])'''


# Mostrar contagem e percentagem de valores ausentes por coluna
missing_data = df.isnull().sum().to_frame(name='Valores Ausentes')
missing_data['% do Total'] = (missing_data['Valores Ausentes'] / len(df)) * 100
missing_data = missing_data[missing_data['Valores Ausentes'] > 0]
print(missing_data)

# Criar um mapa de calor para visualizar os dados ausentes
plt.figure(figsize=(14, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
plt.title('Mapa de Valores Ausentes no Dataset')
plt.show()


# Criar gráficos para visualizar os outliers nas variáveis numéricas
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

# Boxplot da taxa de retenção e desistência
sns.boxplot(
    data=df,
    x='Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade',
    ax=axes[0],
    color='skyblue'
)
axes[0].set_title('Boxplot - Taxa de retenção e desistência')

# Boxplot do desemprego registado
sns.boxplot(
    data=df,
    x='Desemprego registado nos centros de emprego(para menores de 25 anos)',
    ax=axes[1],
    color='lightcoral'
)
axes[1].set_title('Boxplot - Desemprego registado (jovens < 25 anos)')

plt.tight_layout()
plt.show()
