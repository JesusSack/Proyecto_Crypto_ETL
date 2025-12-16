import requests
import time
from datetime import datetime
from google.cloud import bigquery
import os

# --- CONFIGURACIÓN ---
PROJECT_ID = "proyectocrypto-481400"  
DATASET_ID = 'dw_crypto'    
TABLE_ID = "historial_precios"           

# Ruta a tus credenciales (igual que en el otro script)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciales_google.json"

# Mapeo de Monedas (ID de CoinGecko : Símbolo para tu tabla)
monedas = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'solana': 'SOL',
    'tether': 'USDT',
    'binancecoin': 'BNB'
}

def obtener_historial():
    client = bigquery.Client()
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID)
    
    filas_totales = []

    print("⏳ Iniciando descarga de datos históricos...")

    for coin_id, symbol in monedas.items():
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': '90',        
            'interval': 'daily'
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if 'prices' not in data:
                print(f"❌ Error con {coin_id}: No se encontraron datos.")
                continue

            prices = data['prices']
            market_caps = data['market_caps']
            total_volumes = data['total_volumes']

            print(f"✅ Procesando {len(prices)} días para {symbol}...")

            for i in range(len(prices)):
                timestamp = prices[i][0]
                fecha = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                
                precio = prices[i][1]
                
                cap = market_caps[i][1] if i < len(market_caps) else 0
                vol = total_volumes[i][1] if i < len(total_volumes) else 0

                fila = {
                    "fecha_carga": fecha,
                    "nombre": coin_id,
                    "symbol": symbol,
                    "precio_usd": float(precio),
                    "market_cap": float(cap),
                    "volumen": float(vol)
                }
                filas_totales.append(fila)
            
            time.sleep(2)

        except Exception as e:
            print(f"⚠️ Error procesando {coin_id}: {e}")

    if filas_totales:
        errors = client.insert_rows_json(table_ref, filas_totales)
        if errors:
            print(f"❌ Errores al insertar en BigQuery: {errors}")
        else:
            print(f"🚀 ¡ÉXITO! Se cargaron {len(filas_totales)} registros históricos en BigQuery.")
    else:
        print("No se generaron datos para subir.")

if __name__ == "__main__":
    obtener_historial()