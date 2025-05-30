import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("../resultados_csv/data_final.csv", encoding="utf-8", sep=";")

print(df.columns)

df.columns = [
    "Ano",
    "Território",
    "Modalidade de ensino",
    "Taxa_desistencia_secundario",
    "Desemprego_menores_25"
]

df["Taxa_desistencia_secundario"] = pd.to_numeric(df["Taxa_desistencia_secundario"], errors="coerce")
df["Desemprego_menores_25"] = pd.to_numeric(df["Desemprego_menores_25"], errors="coerce")

df = df.dropna(subset=["Taxa_desistencia_secundario", "Desemprego_menores_25"])

#Calcular correlações entre as variáveis numéricas
numericas = df[["Ano", "Taxa_desistencia_secundario", "Desemprego_menores_25"]]
correlacoes = numericas.corr()

print(correlacoes)


# Criar um heatmap para visualizar a matriz de correlação
# Tamanho da figura
plt.figure(figsize=(8, 6))

# Heatmap com valores anotados
sns.heatmap(correlacoes, annot=True, cmap="coolwarm", fmt=".2f")

plt.title("Matriz de Correlação")
plt.show()