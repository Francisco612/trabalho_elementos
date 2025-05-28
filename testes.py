# Criar um gráfico de dispersão para visualizar a relação entre as variáveis numéricas
# implementar em analise_dados.py após a análise de dados ausentes e outliers

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="Taxa_desistencia_secundario",
    y="Desemprego_menores_25",
    hue="Ano",
    palette="viridis",
    alpha=0.7
)
plt.title("Relação entre Taxa de Desistência e Desemprego (Jovens < 25 anos)")
plt.xlabel("Taxa de Retenção e Desistência (%)")
plt.ylabel("Desemprego Registado (Jovens < 25 anos)")
plt.legend(title="Ano", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


