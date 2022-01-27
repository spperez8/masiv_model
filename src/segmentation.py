import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import umap

from scipy import stats
from sklearn.cluster import KMeans
from yellowbrick.cluster import SilhouetteVisualizer


def kmeans(normalised_df_rfm, clusters_number, origin_data):
    
    kmeans = KMeans(n_clusters = clusters_number, random_state = 123)
    kmeans.fit(normalised_df_rfm)

    # Saca los clústeres
    cluster_labels = kmeans.labels_
        
    # Create a cluster label column in original dataset
    df_new = origin_data.assign(Cluster = cluster_labels)
    
    # UMAP
    reducer = umap.UMAP(random_state=1234)
    embedding = reducer.fit_transform(normalised_df_rfm)
    
    # Plot
    plt.title("Gráfico de {} Clústeres".format(clusters_number))
    sns.set_theme(style=None)
    sns.scatterplot(x=embedding[:, 0], y=embedding[:, 1], hue=cluster_labels, style=cluster_labels, palette="Set1")
    
    return df_new


def run():
    # Fijamos el directorio de trabajo
    DIRECTORY =  "/home/spperez/masiv_model/"

    # Datos
    df = pd.read_csv(DIRECTORY + "data/processed/rfm_standardized.csv", index_col="CustomerID")

    df_rmf_std = pd.DataFrame(df, columns=["FrequencyStd", "RecencyStd", "MonetaryValueStd"])

    # Número de Grupos
    inertias = [] 
    K = range(1,10) 
  
    for k in K: 
        kmeanModel = KMeans(n_clusters=k, random_state = 123).fit(df_rmf_std) 
        kmeanModel.fit(df_rmf_std)     
        inertias.append(kmeanModel.inertia_)

    # Grafico
    plt.plot(K, inertias, marker = 'o') 
    plt.xlabel('Número de Clústeres') 
    plt.ylabel('Suma de Distancias al Cuadrado') 
    plt.title('Método del Codo')  
    plt.savefig(DIRECTORY + "reports/figures/grupos.png")

    df_rfm_k4 = kmeans(df_rmf_std, 4, df[["Frequency", "Recency", "MonetaryValue"]])
    plt.savefig(DIRECTORY + "reports/figures/umap_4c.png")

    # Índice Silhouette
    model = KMeans(4, random_state=123)
    visualizer = SilhouetteVisualizer(model, colors='yellowbrick', show=False)
    visualizer.fit(df_rmf_std)
    plt.savefig(DIRECTORY + "reports/figures/silueta_4c.png")
    visualizer.show()  

    # Índice Silhouette
    model = KMeans(5, random_state=123)
    visualizer = SilhouetteVisualizer(model, colors='yellowbrick')
    visualizer.fit(df_rmf_std)  
    plt.savefig(DIRECTORY + "reports/figures/silueta_5c.png")      
    visualizer.show() 

    df_rfm_k4.to_csv(DIRECTORY + "data/processed/customer_segment.csv", index=False)

if __name__ == "__main__":
    run()