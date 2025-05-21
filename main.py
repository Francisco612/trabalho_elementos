import pandas as pd

#ab corresponde à taxa de retenção e desistência no ensino secundário
#ds corresponde aos desemprego registado nos centros de emprego (para menores de 25 anos)

ab = pd.read_csv("386.csv", encoding="utf-8", sep=",")
ds = pd.read_csv("439.csv", encoding="utf-8", sep=",")

#Merge das Regioôes com os municípios
ab["Território"] = ab["02. Nome Região (Portugal)"].astype(str) + "_" + ab["03. Âmbito Geográfico"].astype(str)
ds["Território"] = ds["02. Nome Região (Portugal)"].astype(str) + "_" + ds["03. Âmbito Geográfico"].astype(str)

# Elimina as duas colunas antigas
ab = ab.drop(columns=["02. Nome Região (Portugal)", "03. Âmbito Geográfico"])
ds = ds.drop(columns=["02. Nome Região (Portugal)", "03. Âmbito Geográfico"])


df_merged = pd.merge(ab, ds, on=["01. Ano", "Território"], how="inner")

#alterar o nome da coluna modalidade de ensino e taxa de abandono
df_merged = df_merged.rename(columns={"04. Filtro 1_x": "Modalidade de ensino"})
df_merged = df_merged.rename(columns={"09. Valor_x": "Taxa de retenção e desistência no ensino secundário, em todos os anos de escolaridade"})

#intrevalo do ano em estudo desde 2009 até 2023
df_merged["Ano"] = pd.to_numeric(df_merged.pop("01. Ano"), errors="coerce")
df_merged = df_merged[(df_merged["Ano"] >= 2009)]

df_merged = df_merged[df_merged["04. Filtro 1_y"] == "Menos de 25 anos"].drop(columns=["04. Filtro 1_y"])

# considerar todos os anos escolaridade aquando do abandono e elminar a coluna
df_merged = df_merged[df_merged["05. Filtro 2_x"] == "Total"].drop(columns=["05. Filtro 2_x"])

# eliminar colunas não necessarias/ nulas
df_merged = df_merged.drop(columns=["06. Filtro 3_x", "07. Escala_x","08. Símbolo_y","07. Escala_y","06. Filtro 3_y","05. Filtro 2_y", "08. Símbolo_x"])

#remonear a coluna do desemprego para menores de 25 anos
df_merged = df_merged.rename(columns={"09. Valor_y": "Desemprego registado nos centros de emprego (para menores de 25 anos)"})

#ordenar as colunas
df_merged = df_merged[["Ano", "Território", "Modalidade de ensino", "Taxa de retenção e desistência no ensino secunário, em todos os anos de escolaridade", "Desemprego registado nos centros de emprego(para menores de 25 anos)"]]

# Mostra resultado
#print(df_merged.head())


print(df_merged.columns)

# Guarda o resultado se quiseres
df_merged.to_csv("data_final.csv", index=False, sep=";", encoding='utf-8-sig')
