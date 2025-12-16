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