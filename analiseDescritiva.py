import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Carregar dados
df = pd.read_csv('resultados_csv/data_final_limpo.csv', sep=',')

# Separar apenas colunas numéricas
features = df.drop(columns=['Território', 'Ano', 'Modalidade de ensino'])

# Normalizar
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# PCA
pca = PCA(n_components=2)
components = pca.fit_transform(scaled_features)

# KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(scaled_features)

# DataFrame com resultados
df['Grupo'] = labels
pca_df = pd.DataFrame(components, columns=["PC1", "PC2"])
pca_df['Grupo'] = labels
pca_df['Território'] = df['Território']
pca_df['Ano'] = df['Ano']
pca_df['Taxa_desemprego_menores_25'] = df['Desemprego registado nos centros de emprego (para menores de 25 anos)']
pca_df['Taxa_desistencia_secundario'] = df['Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade']

# Identificar Top 3 extremos
top3_mais_desemprego = pca_df.nlargest(3, 'Taxa_desemprego_menores_25')
top3_menos_desemprego = pca_df.nsmallest(3, 'Taxa_desemprego_menores_25')
top3_mais_desistencia = pca_df.nlargest(3, 'Taxa_desistencia_secundario')
top3_menos_desistencia = pca_df.nsmallest(3, 'Taxa_desistencia_secundario')

# Concatenar e remover duplicados
extremos = pd.concat([
    top3_mais_desemprego,
    top3_menos_desemprego,
    top3_mais_desistencia,
    top3_menos_desistencia
]).drop_duplicates(subset=['Território', 'Ano']).reset_index(drop=True)

# Gráfico
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=pca_df,
    x="PC1",
    y="PC2",
    hue="Grupo",
    palette="Set1",
    alpha=0.6,
    s=60
)

# Destacar extremos com deslocamentos variados
for i, (_, row) in enumerate(extremos.iterrows()):
    dx, dy = offsets[i % len(offsets)]
    plt.scatter(row["PC1"], row["PC2"], color='black', s=120, marker='X')
    label = (
        f"{row['Território']} ({int(row['Ano'])})\n"
        f"Desemp.: {row['Taxa_desemprego_menores_25']:.1f}%\n"
        f"Desist.: {row['Taxa_desistencia_secundario']:.1f}%"
    )
    plt.text(row["PC1"] + dx, row["PC2"] + dy, label, fontsize=8, fontweight='bold')

plt.title("Distribuição PCA dos Municípios")
plt.xlabel("Componente Principal 1 (PC1)")
plt.ylabel("Componente Principal 2 (PC2)")
plt.legend(title="Grupos (KMeans)")
plt.grid(True)
plt.tight_layout()
plt.show()
