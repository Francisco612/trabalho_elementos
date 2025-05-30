import pandas as pd
import numpy as np

# Função para remover outliers
def remover_outliers(df, metodo='iqr', threshold=3):
    df_numeric = df.select_dtypes(include=[np.number])

    if metodo == 'zscore':
        z_scores = np.abs((df_numeric - df_numeric.mean()) / df_numeric.std())
        mask = (z_scores < threshold).all(axis=1)
    elif metodo == 'iqr':
        Q1 = df_numeric.quantile(0.25)
        Q3 = df_numeric.quantile(0.75)
        IQR = Q3 - Q1
        mask = ~((df_numeric < (Q1 - 1.5 * IQR)) | (df_numeric > (Q3 + 1.5 * IQR))).any(axis=1)
    else:
        raise ValueError("Método deve ser 'zscore' ou 'iqr'.")

    return df[mask]



# 1. Carregar o arquivo CSV
df_original = pd.read_csv('resultados_csv/data_final_sem_va.csv', sep=';')

# 2. Mostrar informações básicas antes da remoção
print("Shape original:", df_original.shape)
print("\nResumo estatístico:\n", df_original.describe())

# 3. Remover outliers
df_sem_outliers = remover_outliers(df_original, metodo='iqr')

# 4. Mostrar resultado após a limpeza
print("\nShape após remoção de outliers:", df_sem_outliers.shape)
print("\nResumo após remoção:\n", df_sem_outliers.describe())

# 5. (Opcional) Salvar o novo DataFrame em um CSV
df_sem_outliers.to_csv('resultados_csv/data_final_limpo.csv', index=False)