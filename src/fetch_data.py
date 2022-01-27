import pandas as pd
import numpy as np
import openpyxl 
import os

from datetime import datetime, timedelta

def run():
    # Fijamos el directorio de trabajo
    DIRECTORY =  "/home/spperez/masiv_model/"

    # Se fija el formato de InvoiceDate para no tener problemas
    df = pd.read_excel(io = DIRECTORY + "data/raw/online_retail.xlsx", 
        sheet_name="Online Retail", converters={'InvoiceDate':str})

    # La variable InvoiceDate se pasa de string a fecha
    df["InvoiceDate"] = df["InvoiceDate"].apply(lambda x: x.split(' ')[0])
    df["InvoiceDate"] = df["InvoiceDate"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # Se borran los faltantes
    df = df[pd.notnull(df["CustomerID"])]

    # Se retiran los valores negativos o iguales a cero
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df.reset_index(inplace=True, drop=True)

    df.to_csv(DIRECTORY + 'data/interim/clean_data.csv', index=False)

    # Se cargan datos externos de las semanas y los meses
    df_dates = pd.read_csv(DIRECTORY + 'data/external/dates.csv', sep=";")
    df_dates["DAYDT"] = df_dates["DAYDT"].apply(lambda x: x.split(' ')[0])
    df_dates["DAYDT"] = df_dates["DAYDT"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    
    # Datos monetarios semanales
    df_week = df.merge(df_dates, how="left", left_on="InvoiceDate", right_on="DAYDT")
    df_week.sort_values(by=["InvoiceDate"], ascending=True, inplace=True)
    df_week = df_week.groupby(["YEARID", "WEEKOFYEARID"])["OrderValue"].sum().reset_index()
    df_week["YearWeek"] = df_week["YEARID"].astype(str) + "-" + df_week["WEEKOFYEARID"].astype(str)
    df_week.rename(columns={"OrderValue": "Monetary"}, inplace=True)

    # Datos transacciones semanales
    df_week_transa = df.merge(df_dates, how="left", left_on="InvoiceDate", right_on="DAYDT")
    df_week_transa.sort_values(by=["InvoiceDate"], ascending=True, inplace=True)
    df_week_transa = df_week_transa.groupby(["YEARID", "WEEKOFYEARID"])[["InvoiceNo"]].nunique().reset_index()
    df_week_transa["YearWeek"] = df_week_transa["YEARID"].astype(str) + "-" + df_week_transa["WEEKOFYEARID"].astype(str)
    df_week_transa.rename(columns={"InvoiceNo": "Transactions"}, inplace=True)
    
    # Se guardan los datos en la carperta interim
    df_week.to_csv(DIRECTORY + 'data/interim/monetary_value_week.csv', index=False)
    df_week_transa.to_csv(DIRECTORY + 'data/interim/transactions_week.csv', index=False)

    # Datos monetarios semanales
    df_month = df.groupby("Month")["OrderValue"].sum().reset_index()
    df_month.rename(columns={"OrderValue": "Monetary"}, inplace=True)

    df_month_transa = df.groupby("Month")[["InvoiceNo"]].nunique().reset_index()
    df_month_transa.rename(columns={"InvoiceNo": "Transactions"}, inplace=True)

    # Se guardan los datos en la carperta interim
    df_month.to_csv(DIRECTORY + 'data/interim/monetary_value_month.csv', index=False)
    df_month_transa.to_csv(DIRECTORY + 'data/interim/transactions_month.csv', index=False)


if __name__ == "__main__":
    run()