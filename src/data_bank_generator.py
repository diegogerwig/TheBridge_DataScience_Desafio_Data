import random
import datetime
import numpy as np
import csv
import os
from pathlib import Path
from config import (
    perfiles_ingreso,
    categorias_trx
)
from faker import Faker

from fastapi import FastAPI, HTTPException

app = FastAPI()
fake = Faker(['es_ES'])

@app.get("/")
def read_root():
    """
    Punto de entrada de la API

    Returns:
        str: bienvenida
    """
    return "Bienvenido a la API de generación de transacciones bancarias!"

@app.get("/transacciones")
def gen_transactions(perfil:str, desde:datetime.datetime, hasta:datetime.datetime = None):
    """
    Genera transacciones basado en el perfil indicado

    Parámetros

        perfil (str): Uno de los perfiles disponibles
        desde (datetime.datetime): Fecha origen en formato %YYYY-%MM-%DD
        hasta (datetime.datetime): Fecha fin en formato %YYYY-%MM-%DD. Defecto: None
    """

    # Generamos el dato tipo
    customer_name = fake.name()
    account_name = fake.iban()
    transaction_city = fake.city()

    if perfil not in perfiles_ingreso:
        raise HTTPException(status_code=400, detail="Perfil desconocido")

    datos_perfil = perfiles_ingreso[perfil]

    # Generamos datos que serán estables durante el periodo
    trans_nomina = random.uniform(datos_perfil["nomina"][0], datos_perfil["nomina"][1])
    balance = random.uniform(
        datos_perfil['initial_balance_range'][0],
        datos_perfil['initial_balance_range'][1]
    )

    if not hasta:
        hasta = datetime.datetime.now()

    idx = 1
    transactions = []
    current_date = desde
    cambio_mes = True
    while current_date <= hasta:

        if random.random() < (datos_perfil['transaction_frequency'] / 7):
            if current_date.day < 10 and cambio_mes:
                # Nomina
                balance += trans_nomina
                transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                transaction = {
                    'cliente': customer_name,
                    'cuenta': account_name,
                    'perfil': perfil,
                    'tipo_de_transacción': "transferencia",
                    'cantidad_eur': trans_nomina,
                    'timestamp': current_date,
                    'ciudad': transaction_city,
                    'categoría_transacción': "Nómina",
                    'balance' : balance,
                    'ref_id_transacción': transaction_ref_id
                }
                transactions.append(transaction)
                idx += 1

                # Gastos típicos
                # TODO

                cambio_mes = False

            # Otros
            transaction_type = random.choice(categorias_trx)
            transaction_time = current_date
            transaction_amount = random.uniform(
                datos_perfil['transaction_range'][0],
                datos_perfil['transaction_range'][1]
            )

            if transaction_amount < balance:
                transaction_category = np.random.choice(categorias_trx)
                transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                balance -= transaction_amount
                transaction = {
                    'cliente': customer_name,
                    'cuenta': account_name,
                    'perfil': perfil,
                    'tipo_de_transacción': transaction_type,
                    'cantidad_eur': transaction_amount,
                    'timestamp': transaction_time,
                    'ciudad': transaction_city,
                    'balance' : balance,
                    'categoría_transacción': transaction_category,
                    'ref_id_transacción': transaction_ref_id
                }

                transactions.append(transaction)
                idx += 1

        # Identificamos cuando cambia el mes
        new_date = current_date + datetime.timedelta(days=1)
        if new_date.month != current_date.month:
            cambio_mes = True
        current_date = new_date

    # Guardar en CSV
    save_to_csv(transactions)

    return transactions

def save_to_csv(transactions):
    """
    Guarda las transacciones en un archivo CSV en la carpeta /data
    """
    # Crear la carpeta /data si no existe
    data_folder = Path(__file__).parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    # Generar el nombre del archivo
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M")
    filename = f"data_bank_trx_{timestamp}.csv"
    filepath = data_folder / filename

    # Escribir las transacciones en el archivo CSV
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)

    print(f"Transacciones guardadas en: {filepath}")

if __name__ == "__main__":
    transactions = gen_transactions("Altos ingresos", datetime.datetime(2024, 4, 1))
    print(transactions)