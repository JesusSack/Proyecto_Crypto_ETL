import requests
import json
import os
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

NOMBRE_ARCHIVO_KEY = 'credenciales_google.json' 
DATASET_ID = 'dw_crypto'       
TABLA_ID = 'historial_precios' 

URL_API = "https://api.coingecko.com/api/v3/coins/markets"
PARAMETROS = {
    'vs_currency': 'usd',
    'ids': 'bitcoin,ethereum,solana,tether,binancecoin',
    'order': 'market_cap_desc',
    'sparkline': 'false'
}

def main():
    print(f"[{datetime.now()}] 1. 🌍 Conectando a API CoinGecko...")
    
    try:
        respuesta = requests.get(URL_API, params=PARAMETROS)
        
        if respuesta.status_code == 200:
            datos_api = respuesta.json()
            print(f"   > Datos recibidos: {len(datos_api)} monedas.")
            
            print(f"[{datetime.now()}] 2. ☁️  Conectando a Google BigQuery...")
            
            if not os.path.exists(NOMBRE_ARCHIVO_KEY):
                print(f"❌ ERROR CRÍTICO: No encuentro el archivo '{NOMBRE_ARCHIVO_KEY}'.")
                print("                                            .")
                return

            credentials = service_account.Credentials.from_service_account_file(NOMBRE_ARCHIVO_KEY)
            client = bigquery.Client(credentials=credentials, project=credentials.project_id)
            
            table_ref = f"{client.project}.{DATASET_ID}.{TABLA_ID}"
            
            rows_to_insert = []
            fecha_actual = datetime.now().isoformat()
            
            for moneda in datos_api:
                fila = {
                    "fecha_carga": fecha_actual,
                    "symbol": moneda['symbol'],
                    "nombre": moneda['name'],
                    "precio_usd": float(moneda['current_price'] or 0),
                    "volumen": float(moneda['total_volume'] or 0),
                    "market_cap": float(moneda['market_cap'] or 0)
                }
                rows_to_insert.append(fila)

            job_config = bigquery.LoadJobConfig(
                schema=[
                    bigquery.SchemaField("fecha_carga", "TIMESTAMP"),
                    bigquery.SchemaField("symbol", "STRING"),
                    bigquery.SchemaField("nombre", "STRING"),
                    bigquery.SchemaField("precio_usd", "FLOAT"),
                    bigquery.SchemaField("volumen", "FLOAT"),
                    bigquery.SchemaField("market_cap", "FLOAT"),
                ],
                write_disposition="WRITE_APPEND", 
            )

            print(f"[{datetime.now()}] 3. 🚀 Subiendo datos a la nube...")
            
            job = client.load_table_from_json(rows_to_insert, table_ref, job_config=job_config)
            
            job.result() 
            
            print(f"[{datetime.now()}] ✅ ¡ÉXITO TOTAL! Se cargaron {len(rows_to_insert)} filas en Google BigQuery.")
            print(f"   > Proyecto: {client.project}")
            print(f"   > Tabla: {DATASET_ID}.{TABLA_ID}")

        else:
            print(f"❌ Error en la API: {respuesta.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()