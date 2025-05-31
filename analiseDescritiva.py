import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. Carregamento e preparação dos dados ---
df = pd.read_csv('resultados_csv/data_final_limpo.csv', sep=',')

# Pivotar taxas de desistência (long → wide)
df_desistencia = df[['Território', 'Ano', 'Modalidade de ensino',
                     'Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade']]

pivot_desistencia = df_desistencia.pivot_table(
    index=['Território', 'Ano'],
    columns='Modalidade de ensino',
    values='Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade'
).reset_index()

pivot_desistencia.columns.name = None
pivot_desistencia = pivot_desistencia.rename(columns={
    'Cursos gerais': 'desist_cursos_gerais',
    'Cursos Tecnológicos e Profissionais': 'desist_cursos_tecn_prof',
    'Total': 'desist_total'
})

# Modalidade com mais desistência
modalidades_cols = ['desist_cursos_gerais', 'desist_cursos_tecn_prof']
pivot_desistencia['Modalidade_mais_desistencia'] = pivot_desistencia[modalidades_cols].idxmax(axis=1)
pivot_desistencia['Modalidade_mais_desistencia'] = pivot_desistencia['Modalidade_mais_desistencia'] \
    .str.replace('desist_', '').str.replace('_', ' ').str.title()

# Remover duplicados e juntar info da modalidade
df_unico = df.drop_duplicates(subset=['Território', 'Ano']).copy()
df_unico = df_unico.merge(
    pivot_desistencia[['Território', 'Ano', 'Modalidade_mais_desistencia']],
    on=['Território', 'Ano'],
    how='left'
)

# --- 2. PCA e Clustering ---
features = df_unico.drop(columns=['Território', 'Ano', 'Modalidade de ensino', 'Modalidade_mais_desistencia'])
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

pca = PCA(n_components=2)
components = pca.fit_transform(scaled_features)

kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
labels = kmeans.fit_predict(scaled_features)

# --- 3. Construção do DataFrame final para visualização ---
df_unico['Grupo'] = labels
pca_df = pd.DataFrame(components, columns=["PC1", "PC2"])
pca_df['Grupo'] = labels
pca_df['Território'] = df_unico['Território']
pca_df['Ano'] = df_unico['Ano']
pca_df['Desemprego_jovens'] = df_unico['Desemprego registado nos centros de emprego (para menores de 25 anos)']
pca_df['Desistencia_total'] = df_unico['Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade']
pca_df['Modalidade_mais_desistencia'] = df_unico['Modalidade_mais_desistencia']

# Identificar extremos
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

# --- 4. Gráfico final ---
fig, (ax_scatter, ax_legend) = plt.subplots(1, 2, figsize=(18, 10), gridspec_kw={'width_ratios': [4, 1]})

# Scatter PCA
sns.scatterplot(
    data=pca_df,
    x="PC1",
    y="PC2",
    hue="Grupo",
    palette="Set1",
    alpha=0.6,
    s=60,
    ax=ax_scatter
)

# Destacar municípios extremos
for i, (_, row) in enumerate(extremos.iterrows(), start=1):
    ax_scatter.scatter(row["PC1"], row["PC2"], color='black', s=140, marker='o')
    ax_scatter.text(row["PC1"], row["PC2"], str(i), color='white', fontsize=12, fontweight='bold',
                    ha='center', va='center')

# Títulos e eixos
ax_scatter.set_title("Análise de Municípios: Desemprego Jovem e Desistência Escolar (PCA)", fontsize=14)
ax_scatter.set_xlabel("Componente Principal 1 (PC1)")
ax_scatter.set_ylabel("Componente Principal 2 (PC2)")
ax_scatter.grid(True)

# Texto explicativo da legenda lateral
legend_texts = []
for i, (_, row) in enumerate(extremos.iterrows(), start=1):
    txt = (
        f"{i}. {row['Território']} ({int(row['Ano'])})\n"
        f"   Desemprego jovens: {row['Desemprego_jovens']:.0f} pessoas\n"
        f"   Desistência: {row['Desistencia_total']:.1f}%\n"
        f"   Modalidade + desistência: {row['Modalidade_mais_desistencia']}\n"
    )
    legend_texts.append(txt)

legend_str = "\n".join(legend_texts)

ax_legend.axis('off')
ax_legend.text(0, 1, legend_str, fontsize=10, va='top', ha='left', wrap=True)

# Nota de rodapé explicativa
plt.figtext(0.5, 0.01,
    "Nota: O número de desempregados jovens (<25 anos) representa a média mensal de inscritos nos centros de emprego durante o ano.\n"
    "Fonte: Pordata | Clusters baseados em PCA e KMeans.",
    wrap=True, ha='center', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()
