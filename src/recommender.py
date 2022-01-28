import warnings
import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix

from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


def PurchaseMatrix(datos):
    """
    Crea la matriz de incidencia,
    donde 1 indica si el cliente ha comprado el producto j,
    0 en otro caso

    Parametros
    --------
    datos: Data frame
           Data frame tiene las columnas CustomerID, ProductID y Quantity
    Retorna
    ------
    Mincidencia : ndarray
                 Matriz de incidencia.
    list_ProductID : ndarray
                 Lista con los ProductID
    """
    
    CustomerID = datos[["CustomerID"]].drop_duplicates()
    CustomerID.sort_values(inplace=True, by="CustomerID")
    CustomerID.reset_index(inplace=True)
    CustomerID['index_j'] = np.arange(CustomerID.shape[0])


    ProductID = datos[["ProductID"]].drop_duplicates()
    ProductID.sort_values(inplace=True, by="ProductID")
    ProductID.reset_index(inplace=True)
    ProductID['index_i'] = np.arange(ProductID.shape[0])

    datos = datos[["CustomerID", "ProductID"]].merge(CustomerID, on="CustomerID")
    datos = datos.merge(ProductID, on="ProductID")
    Mincidencia = lil_matrix((ProductID.shape[0], CustomerID.shape[0]))

    Mincidencia[datos['index_i'], datos['index_j']] = 1
    Mincidencia_csr = Mincidencia.tocsr()
    sumCol = np.array(Mincidencia_csr.sum(axis=0) >= 2).ravel()
    Mincidencia = Mincidencia[:, sumCol]


    list_ProductID = ProductID["ProductID"].to_numpy()

    return Mincidencia, list_ProductID


def favorito(datos):
    """
    Halla el Producto favorito segun la cantidad de unidades compradas

    Parametros
    ----------
    datos: Data frame
           Data frame tiene las columnas CustomerID, ProductID y Quantity
    Returns
    ------
    preferido: Data frame
               Retorna un data frame con el producto preferido
               segun las unidades

    """
    # Filtra Und diferentes de cero
    datos = datos[datos["Quantity"] != 0].reset_index(drop=True)
    # Por PartyID saca la posicion del maximo numero
    indexdatos = datos.groupby(["CustomerID"]).idxmax()
    preferido = datos.iloc[indexdatos["Quantity"]]
    preferido.drop(columns=["Quantity"], inplace=True)
    
    return preferido



def run():
    # Fijamos el directorio de trabajo
    DIRECTORY =  "/home/spperez/masiv_model/"

    # Datos
    df = pd.read_csv(DIRECTORY + "data/interim/clean_data.csv")
    
    # Se selecionan solo lo necesario
    data = df[["CustomerID", "StockCode", "Quantity"]].drop_duplicates().reset_index(drop=True)

    # Creando un id unico para el producto
    df_plu = pd.DataFrame({"StockCode": data["StockCode"].unique(), "ProductID": range(1, 3666)})
    
    # unimos las dos bd
    data = pd.merge(data, df_plu, how="left", on="StockCode")

    # base de datos con los nombres 
    data_name = df[["StockCode", "Description"]].drop_duplicates().reset_index(drop=True)

    # Calcula la matriz de incidencia
    M_incidencia, ProductID = PurchaseMatrix(data)

    # Calculo similaridad
    similarities = cosine_similarity(M_incidencia)*-1
    
    # se hace la recomendación 5, para esta caso
    cols = ["ProductID"] + [f"Recomendación_{i}" for i in range(1, 5 + 1)]
    ProductID = np.array(ProductID)
    top = np.argsort(similarities)[:, :5 + 1]
    recomendacion = ProductID[top].squeeze()
    recomendacion = pd.DataFrame(data=recomendacion, columns=cols)

    # Se fijan los elementas de la diagonal
    recomendacion["ProductID"] = ProductID
    
    # Se encuentra el producto favorita de cada cliente
    df_favo = favorito(data)

    # Se le pega a cada cliente las recomendaciones segun el prod. favo
    recomendacion_cliente = pd.merge(df_favo[["CustomerID","ProductID"]], recomendacion, on="ProductID", how='left')

    # Diccionario de nombres de productos 
    df_dic = pd.merge(data_name, df_plu, on="StockCode", how="inner").drop_duplicates()

    # Se retiran los nombres duplicados
    for i in range(1, df_dic.shape[0]):
        con_1 = df_dic["StockCode"][i] == df_dic["StockCode"][i-1]
        con_2 = df_dic["ProductID"][i] == df_dic["ProductID"][i-1]
        if con_1 & con_2:
            df_dic["Description"][i] = df_dic["Description"][i-1]
    
        i += 1

    df_dic.drop_duplicates(inplace=True)

    # Se guardan los nombres del los productos
    df_dic.to_csv(DIRECTORY + "data/interim/product_names.csv", index=False)
    
    # se guarda la recomendación
    recomendacion_cliente.to_csv(DIRECTORY + "data/processed/recomendation.csv", index=False)


if __name__ == "__main__":
    run()
