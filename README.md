# 📊 Dashboard Financeiro Avançado - Multi-Empresas

[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29+-orange)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)](https://www.sqlite.org/)

---

## 🔹 Descrição do Projeto

Este projeto consiste em um **dashboard financeiro interativo** desenvolvido em **Python** utilizando **Streamlit**, com foco em **engenharia de dados aplicada**.  
Ele permite a visualização e análise de indicadores financeiros de múltiplas empresas, como faturamento, lucro bruto, lucro líquido e margem de lucro, em um ambiente web acessível via link.

O projeto implementa **ETL completo**:

- **Ingestão de dados (Data Ingestion):** coleta automática de dados financeiros das empresas usando a biblioteca `yfinance`.
- **Limpeza e transformação (Data Cleaning & Transformation):** tratamento de valores ausentes e cálculo de métricas derivadas.
- **Persistência (Data Persistence):** armazenamento em **SQLite** garantindo histórico e consistência.
- **Visualização (Data Visualization):** gráficos interativos com `Plotly`.
- **Exportação de dados:** download em CSV para análises externas.
- **Logs de atualização:** rastreabilidade da última atualização de cada empresa.

---

## 🔹 Funcionalidades Principais

- Comparação de múltiplas empresas lado a lado  
- ETL automático: download, limpeza, transformação e armazenamento  
- Visualizações interativas:
  - Faturamento acumulado
  - Lucro Bruto x Lucro Líquido
  - Margem de Lucro
- Exportação de dados em CSV  
- Logs de atualização das informações  

---

## 🔹 Tecnologias Utilizadas

- **Python 3.11+**  
- **Streamlit** – dashboards web interativos  
- **Pandas** – manipulação e transformação de dados  
- **yfinance** – extração de dados financeiros históricos  
- **Plotly** – visualizações avançadas  
- **SQLite** – banco de dados relacional para persistência  

---

## 🔹 Estrutura do Projeto

## 🔹 Conceitos de Engenharia de Dados Aplicados

| Conceito | Implementação |
|----------|---------------|
| **Data Ingestion** | Coleta automática de dados financeiros via API `yfinance`. |
| **Data Cleaning** | Preenchimento de valores ausentes e consistência de dados. |
| **Data Transformation** | Cálculo de métricas derivadas: margem de lucro e faturamento acumulado. |
| **Data Persistence** | Salvamento em SQLite com histórico (`Last_Update`). |
| **Data Visualization** | Gráficos interativos com Plotly e Streamlit. |
| **Data Aggregation** | Estatísticas agregadas por empresa e visualização multi-empresa. |
| **Data Quality & Logs** | Garantia de schema consistente e logs de atualização. |

---

## 🔹 Como Executar

1. Instale as dependências:

pip install streamlit pandas yfinance plotly

2. Execute o dashboard:

streamlit run app.py

3. Acesse o dashboard no navegador no link gerado pelo Streamlit.

https://guilhermebertidashboard.streamlit.app/

5. Utilize o botão de download CSV para exportar os dados.

