import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import umap

from datetime import datetime
from scipy import stats
from sklearn.preprocessing import StandardScaler
from feature_engine.outliers import Winsorizer

def run():
    # Fijamos el directorio de trabajo
    DIRECTORY =  "/home/spperez/masiv_model/"
    
    # Datos
    df = pd.read_csv(DIRECTORY + "data/interim/clean_data.csv")
    df["InvoiceDate"] = df["InvoiceDate"].apply(lambda x: x.split(' ')[0])
    df["InvoiceDate"] = df["InvoiceDate"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    
    # Se crea la variable recency
    df_r = df.groupby(['CustomerID'], as_index=False)['InvoiceDate'].max()
    df_r.rename(columns={"InvoiceDate": "LastInvoiceDate"}, inplace=True)
    current_date = df_r["LastInvoiceDate"].max()
    df_r["Recency"] = (current_date - df_r["LastInvoiceDate"])/np.timedelta64(1, 'D')
    df_r.drop(columns=["LastInvoiceDate"], inplace=True)

    # Se crean las variables Frecuencia y Monto
    df_fm = df.groupby('CustomerID').agg({
        'InvoiceNo'   : lambda x:x.nunique(),
         'OrderValue'  : lambda x:x.sum(),
        })

    df_fm.rename(columns = {
        'InvoiceNo' :'Frequency',
        'OrderValue':'MonetaryValue'
        }, inplace= True) 

    # Datos RMF
    df_rfm = df_r.merge(df_fm, left_on="CustomerID", right_on="CustomerID")

    # Se estandarizan las varaibles
    df_rfm_std  = df_rfm.copy()
    df_rfm_std[["FrequencyStd", "RecencyStd", "MonetaryValueStd"]]  = StandardScaler().fit_transform(df_rfm_std[["Frequency", "Recency", "MonetaryValue"]])

    # Datos atípicos
    capper = Winsorizer(capping_method="quantiles", tail="both", fold=0.05, variables=["FrequencyStd", "RecencyStd", "MonetaryValueStd"])
    capper.fit(df_rfm_std)

    # Se aplica a los datos
    df_rfm_std_wo = capper.transform(df_rfm_std)

    sns.set_theme(style=None)
    sns.pairplot(df_rfm_std_wo[["FrequencyStd", "RecencyStd", "MonetaryValueStd"]])
    plt.savefig(DIRECTORY + "reports/figures/distribucion.png")

    # Proyección de UMAP
    reducer = umap.UMAP(random_state=1234)
    embedding = reducer.fit_transform(df_rfm_std_wo[["FrequencyStd", "RecencyStd", "MonetaryValueStd"]])
    plt.title('Proyección de UMAP de los datos', fontsize=15)
    sns.set_theme(style=None)
    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1])
    plt.savefig(DIRECTORY + "reports/figures/UMAP.png")

    # Se guardan los datos RFM ya procesados.
    df_rfm_std_wo.to_csv(DIRECTORY + "data/processed/rfm_standardized.csv", index=False)



if __name__ == "__main":
    run()