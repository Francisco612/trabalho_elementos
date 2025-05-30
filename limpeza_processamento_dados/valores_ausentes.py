import pandas as pd

def limpar_valores_ausentes():

    df = pd.read_csv('resultados_csv/data_final.csv', sep=';')
    print("Shape original:", df.shape)
    df_sem_na = df.dropna()
    print("Shape após remoção de valores ausentes:", df_sem_na.shape)
    df_sem_na.to_csv('resultados_csv/data_final_sem_va.csv', index=False)
    return df_sem_na
