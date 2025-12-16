# 🚀 Automated Crypto ETL Pipeline (Serverless)

Este proyecto es un sistema completo de **Ingeniería de Datos End-to-End** que extrae, transforma y carga (ETL) información financiera de criptomonedas en la nube de forma totalmente automatizada.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-4285F4?logo=google-cloud&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/DevOps-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Looker Studio](https://img.shields.io/badge/BI-Looker_Studio-EA4335?logo=google-analytics&logoColor=white)

## 📋 Arquitectura del Proyecto

El flujo de datos está diseñado para ser **100% Serverless** (sin servidores que mantener) y coste cero:

```mermaid
graph LR
  A[API CoinGecko] -->|Extracción JSON| B(Script Python ETL)
  B -->|Transformación & Limpieza| B
  B -->|Carga Histórica| C[(Google BigQuery)]
  C -->|Conexión Directa| D[Dashboard Looker Studio]
  E[GitHub Actions] -->|Ejecución Diaria Automática| B


🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.

Librerías: requests (API), google-cloud-bigquery (Cloud connection), os, json.

Cloud Computing: Google BigQuery (Data Warehouse).

CI/CD & Automatización: GitHub Actions (YAML Workflows).

Seguridad: Gestión de credenciales mediante GitHub Secrets (Service Accounts encriptadas).

Business Intelligence: Google Looker Studio.



⚙️ Configuración Local
Si deseas correr este proyecto en tu máquina local:

1. Clonar el repositorio: git clone [https://github.com/JesusSack/Proyecto_Crypto_ETL.git](https://github.com/JesusSack/Proyecto_Crypto_ETL.git)
cd Proyecto_Crypto_ETL


2. Instalar dependencias: pip install requests google-cloud-bigquery


3. Configurar Credenciales de Google: Necesitas una Service Account de Google Cloud con permisos de "BigQuery Admin".

Descarga el archivo .json de la llave.

Renómbralo a credenciales_google.json y colócalo en la raíz del proyecto.

4. Ejecutar el ETL: python extraer_crypto_api.py

🤖 Automatización (CI/CD)
El archivo .github/workflows/ejecucion_diaria.yml contiene la lógica para la ejecución automática.

Utiliza un entorno virtual Ubuntu en la nube de GitHub.

Inyecta las credenciales de Google de forma segura desde los Repository Secrets en tiempo de ejecución.

No requiere intervención humana.

📊 Visualización
Los datos se visualizan en un tablero de control que permite monitorear:

Tendencia de precios históricos.

Volumen de mercado y Capitalización.

Comparativa entre monedas.

Desarrollado como proyecto de Ingeniería de Datos aplicada a Finanzas.