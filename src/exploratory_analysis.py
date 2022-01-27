import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from datetime import datetime

def user_status(data):
    status = []
    for i in range(13):
    # If the user has no purchase in the current month
        if data[i] == 0:
            # If the user has made purchases before
            if len(status) > 0:
                # If the user is unregistered in the previous month
                if status[i-1] == "No Registrado":
                # The the user is also unregistered this month
                    status.append("No Registrado")
                # Otherwise the user is an active user, i.e., he/she already registered
                else:
                    status.append("Inactivo")
            # Otherwise the user is not registered in the current month, i.e., he/she has never made any purchases
            else:
                status.append("No Registrado")
        else:
            # This is the first purchase of the user
            if len(status) == 0:
                status.append("Primera Compra")
            else:
                if status[i-1] == "Inactivo":
                    status.append("Regresó")
                elif status[i-1] == "No Registrado":
                    status.append("Primera Compra")
                else:
                    status.append("Activo")
    return status

def run():
    # Fijamos el directorio de trabajo
    DIRECTORY =  "/home/spperez/masiv_model/"

    # Datos
    df = pd.read_csv(DIRECTORY + "data/interim/clean_data.csv")
    df["InvoiceDate"] = df["InvoiceDate"].apply(lambda x: x.split(' ')[0])
    df["InvoiceDate"] = df["InvoiceDate"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    
    # Evolución de las ventas mes a mes
    monthly_sales = pd.read_csv(DIRECTORY + "data/interim/monetary_value_month.csv")
    monthly_sales["Prop_sales"] = (100*monthly_sales["Monetary"]/(monthly_sales["Monetary"].sum())).round(2)
    # Evolución de las Transacciones mes a mes
    monthly_transa = pd.read_csv(DIRECTORY + "data/interim/transactions_month.csv")
    monthly_transa["Prop_transa"] = (100*monthly_transa["Transactions"]/(monthly_transa["Transactions"].sum())).round(2)

    # Un solo gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_sales["Month"], monthly_sales["Prop_sales"], marker = 'o', label = "Venta")
    ax.plot(monthly_transa["Month"], monthly_transa["Prop_transa"], marker = 'o', label = "Transacciones")
    ax.set(title = "Evolución Mes a Mes",
           xlabel = "Mes",
           ylabel = "Porcentaje")
    plt.setp(ax.get_xticklabels(), rotation = 45)
    plt.legend()
    plt.savefig(DIRECTORY + "reports/figures/mes_mes.png")

    # Evolución de las ventas Semana a Semana
    weekly_sales = pd.read_csv(DIRECTORY + "data/interim/monetary_value_week.csv")
    weekly_sales["Prop_sales"] = (100*weekly_sales["Monetary"]/(weekly_sales["Monetary"].sum())).round(2)
    # Evolución de las Transacciones Semana a Semana
    weekly_transa = pd.read_csv(DIRECTORY + "data/interim/transactions_week.csv")
    weekly_transa["Prop_transa"] = (100*weekly_transa["Transactions"]/(weekly_transa["Transactions"].sum())).round(2)

    # Un solo gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(weekly_sales["YearWeek"], weekly_sales["Prop_sales"], marker = 'o', label = "Venta")
    ax.plot(weekly_transa["YearWeek"], weekly_transa["Prop_transa"], marker = 'o', label = "Transacciones")
    ax.set(title = "Evolución Semana a Semana",
           xlabel = "Semana",
           ylabel = "Porcentaje")
    plt.setp(ax.get_xticklabels(), rotation = 90)
    plt.legend()
    plt.xticks(fontsize=8)
    plt.savefig(DIRECTORY + "reports/figures/semana_semana.png")
    
    user_month_pivot = df.pivot_table(index=["CustomerID"], 
                                    columns=["Month"], 
                                    values=["InvoiceNo"], 
                                    aggfunc="count", 
                                    fill_value=0)
    
    # Replace count of invoices with 1
    user_month_pivot = user_month_pivot.applymap(lambda x: 1 if x>0 else 0)
    
    user_month_status = pd.DataFrame(user_month_pivot.apply(lambda x: pd.Series(user_status(x)), axis=1))
    user_month_status.columns = user_month_pivot.columns
    
    month_status_pivot = pd.DataFrame(user_month_status.replace("No Registrado", np.NaN).apply(lambda x: pd.value_counts(x)))

    month_status_pivot = month_status_pivot.fillna(0).T
    month_status_pivot.reset_index(inplace=True)
    month_status_pivot.set_index("Month", inplace=True)

    ax = month_status_pivot.plot.area(figsize = (12,6))
    plt.title("Number of Users by Status in each month")
    plt.savefig(DIRECTORY + "reports/figures/status.png")


if __name__ == "__main__":
    run()