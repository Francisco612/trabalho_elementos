import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar dados
df = pd.read_csv('resultados_csv/data_final_limpo.csv')

# 2. Filtrar e calcular modalidade com mais desistência
df_desistencia = df[
    ['Território', 'Ano', 'Modalidade de ensino',
     'Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade']
]

# Agrupar por Território e Ano → manter só a modalidade com maior taxa de desistência
idx_max = df_desistencia.groupby(['Território', 'Ano'])[
    'Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade'
].idxmax()

df_mais_desistencia = df_desistencia.loc[idx_max].copy()
df_mais_desistencia['Modalidade_mais_desistencia'] = df_mais_desistencia['Modalidade de ensino']
df_mais_desistencia = df_mais_desistencia[['Território', 'Ano', 'Modalidade_mais_desistencia']]

# 3. Juntar essa informação com dados únicos
df_unico = df.drop_duplicates(subset=['Território', 'Ano']).copy()
df_unico = df_unico.merge(df_mais_desistencia, on=['Território', 'Ano'], how='left')

# 4. PCA e Clustering
features = df_unico.drop(columns=['Território', 'Ano', 'Modalidade de ensino', 'Modalidade_mais_desistencia'])
scaled = StandardScaler().fit_transform(features)
components = PCA(n_components=2).fit_transform(scaled)
labels = KMeans(n_clusters=3, random_state=42, n_init='auto').fit_predict(scaled)

# 5. Construir dataframe final
df_unico['Grupo'] = labels
pca_df = pd.DataFrame(components, columns=['PC1', 'PC2'])
pca_df['Grupo'] = labels
pca_df['Território'] = df_unico['Território']
pca_df['Ano'] = df_unico['Ano']
pca_df['Desemprego_jovens'] = df_unico['Desemprego registado nos centros de emprego (para menores de 25 anos)']
pca_df['Desistencia_total'] = df_unico['Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade']
pca_df['Modalidade_mais_desistencia'] = df_unico['Modalidade_mais_desistencia']

# 6. Identificar extremos
top3_mais_desemprego = pca_df.nlargest(3, 'Desemprego_jovens')
top3_menos_desemprego = pca_df.nsmallest(3, 'Desemprego_jovens')
top3_mais_desistencia = pca_df.nlargest(3, 'Desistencia_total')
top3_menos_desistencia = pca_df.nsmallest(3, 'Desistencia_total')

extremos = pd.concat([
    top3_mais_desemprego,
    top3_menos_desemprego,
    top3_mais_desistencia,
    top3_menos_desistencia
]).drop_duplicates(subset=['Território', 'Ano']).reset_index(drop=True)

# 7. Gráfico
fig, (ax_scatter, ax_legend) = plt.subplots(1, 2, figsize=(18, 10), gridspec_kw={'width_ratios': [4, 1]})
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Grupo', palette='Set1', alpha=0.6, s=60, ax=ax_scatter)

for i, (_, row) in enumerate(extremos.iterrows(), start=1):
    ax_scatter.scatter(row['PC1'], row['PC2'], color='black', s=140)
    ax_scatter.text(row['PC1'], row['PC2'], str(i), color='white', fontsize=12, fontweight='bold', ha='center', va='center')

ax_scatter.set_title("Análise de Municípios: Desemprego Jovem e Desistência Escolar (PCA)")
ax_scatter.set_xlabel("Componente Principal 1 (PC1)")
ax_scatter.set_ylabel("Componente Principal 2 (PC2)")
ax_scatter.grid(True)

# Legenda lateral
ax_legend.axis('off')
legendas = []
for i, (_, row) in enumerate(extremos.iterrows(), start=1):
    texto = (
        f"{i}. {row['Território']} ({int(row['Ano'])})\n"
        f"   Desemprego jovens: {row['Desemprego_jovens']:.0f} pessoas\n"
        f"   Desistência: {row['Desistencia_total']:.1f}%\n"
        f"   Modalidade + desistência: {row['Modalidade_mais_desistencia']}\n"
    )
    legendas.append(texto)

ax_legend.text(0, 1, "\n".join(legendas), va='top', fontsize=10)

plt.figtext(0.5, 0.01,
    "Nota: O número de desempregados jovens (<25 anos) representa a média mensal de inscritos nos centros de emprego durante o ano.\n"
    "Fonte: Pordata | Clusters baseados em PCA e KMeans.",
    ha='center', fontsize=9)
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()
