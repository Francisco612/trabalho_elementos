import pandas as pd
import numpy as np


def remover_outliers(df, metodo='iqr', threshold=3):
    """
    Remove outliers de um DataFrame usando Z-score ou IQR.

    Parâmetros:
        df (pd.DataFrame): DataFrame de entrada.
        metodo (str): 'zscore' ou 'iqr'.
        threshold (float): Limite de corte para o Z-score (default = 3).

    Retorna:
        pd.DataFrame: DataFrame sem os outliers.
    """
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
