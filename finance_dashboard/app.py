import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from db_utils import create_table, save_data, load_data
from datetime import datetime

st.title("📊 Dashboard Financeiro Avançado - Multi-Empresas")

# ====================================================
# 1️⃣ Seleção de múltiplas empresas
# ====================================================
tickers = st.multiselect(
    "Selecione as empresas para comparação:",
    ["AAPL", "MSFT", "GOOGL", "AMZN"],
    default=["AAPL", "MSFT"]
)

# ====================================================
# 2️⃣ ETL automático para cada empresa
# ====================================================
all_data = {}
for ticker in tickers:
    st.subheader(f"📂 Processando {ticker}")

    # 2.1 Carregar dados do banco
    data_db = load_data(ticker)
    if not data_db.empty:
        st.success(f"✅ Dados de {ticker} carregados do banco")
        # Garantir que todos os dados tenham Last_Update
        if "Last_Update" not in data_db.columns:
            data_db["Last_Update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(ticker, data_db)
    else:
        st.info(f"🔄 Nenhum dado no banco de {ticker}, baixando da web")

    # 2.2 Baixar dados da web (ETL)
    company = yf.Ticker(ticker)
    income_stmt = company.financials.T
    income_stmt = income_stmt[["Total Revenue", "Gross Profit", "Net Income"]]
    income_stmt = income_stmt.reset_index()
    income_stmt.rename(columns={
        "index": "Data",
        "Total Revenue": "Faturamento",
        "Gross Profit": "Lucro_Bruto",
        "Net Income": "Lucro_Liquido"
    }, inplace=True)

    # 2.3 Limpeza de dados
    income_stmt["Faturamento"] = income_stmt["Faturamento"].fillna(0)
    income_stmt["Lucro_Bruto"] = income_stmt["Lucro_Bruto"].fillna(0)
    income_stmt["Lucro_Liquido"] = income_stmt["Lucro_Liquido"].fillna(0)

    # 2.4 Transformações e métricas derivadas
    income_stmt["Margem_Lucro"] = income_stmt["Lucro_Liquido"] / income_stmt["Faturamento"]
    income_stmt["Faturamento_Acumulado"] = income_stmt["Faturamento"].cumsum()
    income_stmt["Last_Update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2.5 Salvar no banco
    create_table(ticker)
    save_data(ticker, income_stmt)

    all_data[ticker] = income_stmt

# ====================================================
# 3️⃣ Combinar dados para visualização multi-empresa
# ====================================================
combined = pd.DataFrame()
for ticker, df in all_data.items():
    temp = df.copy()
    temp["Empresa"] = ticker
    combined = pd.concat([combined, temp])

# ====================================================
# 4️⃣ Exportação de dados
# ====================================================
csv = combined.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download CSV de todos os dados",
    data=csv,
    file_name="financial_data.csv",
    mime="text/csv"
)

# ====================================================
# 5️⃣ Visualizações
# ====================================================
st.subheader("📈 Faturamento Acumulado - Multi-Empresa")
fig1 = go.Figure()
for ticker in tickers:
    df = all_data[ticker]
    fig1.add_trace(go.Scatter(
        x=df["Data"],
        y=df["Faturamento_Acumulado"],
        mode='lines+markers',
        name=ticker
    ))
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📈 Lucro Bruto x Lucro Líquido - Multi-Empresa")
fig2 = go.Figure()
for ticker in tickers:
    df = all_data[ticker]
    fig2.add_trace(go.Bar(x=df["Data"], y=df["Lucro_Bruto"], name=f"{ticker} Lucro Bruto"))
    fig2.add_trace(go.Bar(x=df["Data"], y=df["Lucro_Liquido"], name=f"{ticker} Lucro Líquido"))
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📈 Margem de Lucro - Multi-Empresa")
fig3 = go.Figure()
for ticker in tickers:
    df = all_data[ticker]
    fig3.add_trace(go.Scatter(x=df["Data"], y=df["Margem_Lucro"], mode='lines+markers', name=ticker))
st.plotly_chart(fig3, use_container_width=True)

# ====================================================
# 6️⃣ Logs de atualização
# ====================================================
st.subheader("📄 Logs de Atualização")
logs = []
for ticker, df in all_data.items():
    if "Last_Update" in df.columns and not df.empty:
        last_update = df["Last_Update"].iloc[0]
        logs.append(f"{ticker}: Última atualização em {last_update}")
    else:
        logs.append(f"{ticker}: Sem registro de atualização")
st.write("\n".join(logs))
