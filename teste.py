# Arquivo: gut_priorizacao.py
# Para rodar: streamlit run gut_priorizacao.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# Dados originais da matriz GUT
# ===============================
dados = [
    [1, "Oferecer planos de financiamento e parcelamento facilitado", 5, 5, 4],
    [2, "Desenvolver pacotes integrados (embriões + consultoria técnica especializada)", 5, 4, 5],
    [3, "Parcerias estratégicas com laboratórios veterinários locais + central de suporte remoto", 5, 4, 5],
    [4, "Oferta de embriões congelados de alta qualidade com garantia de viabilidade", 5, 4, 4],
    [5, "Promover treinamentos e workshops focados em manejo reprodutivo", 4, 4, 5],
    [6, "Desenvolver plataformas digitais para acompanhar ciclo reprodutivo e enviar alertas", 4, 5, 5],
    [7, "Investir em técnicas avançadas de congelamento/descongelamento", 5, 4, 4],
    [8, "Oferecer descontos progressivos, programas de fidelidade e benefícios por indicação", 4, 4, 4],
    [9, "Comercializar embriões de alta qualidade genética (maior potencial de concepção)", 5, 4, 5],
    [10, "Desenvolver embriões adaptados às condições locais + linhas customizadas para diferentes perfis de produtores", 4, 3, 4],
    [11, "Análise criteriosa das receptoras para seleção das melhores candidatas", 4, 4, 5],
    [12, "Divulgar estudos de caso e resultados reais", 3, 3, 4]
]

df = pd.DataFrame(dados, columns=["Nº", "Ação Proposta", "G", "U", "T"])

# ===============================
# Configuração do Streamlit
# ===============================
st.set_page_config(page_title="Matriz GUT Interativa", layout="wide")
st.title("📊 Priorização de Ações - Matriz GUT")
st.markdown("Ajuste os valores de *Gravidade, **Urgência* e *Tendência* para simular novos cenários.")

# ===============================
# Entrada interativa com sliders
# ===============================
for i in df.index:
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
    col1.write(f"*{df.loc[i, 'Ação Proposta']}*")
    df.loc[i, "G"] = col2.slider("G", 1, 5, df.loc[i, "G"], key=f"G{i}")
    df.loc[i, "U"] = col3.slider("U", 1, 5, df.loc[i, "U"], key=f"U{i}")
    df.loc[i, "T"] = col4.slider("T", 1, 5, df.loc[i, "T"], key=f"T{i}")

# ===============================
# Cálculo de prioridade
# ===============================
df["Prioridade"] = df["G"] * df["U"] * df["T"]
df = df.sort_values(by="Prioridade", ascending=False)

# Classificação de prioridade para cores
def classificar_prioridade(valor):
    if valor >= 80:
        return "Alta"
    elif valor >= 50:
        return "Média"
    else:
        return "Baixa"

df["Nível"] = df["Prioridade"].apply(classificar_prioridade)

# ===============================
# Exibir tabela
# ===============================
st.subheader("📋 Ranking de Ações")
st.dataframe(df, use_container_width=True)

# ===============================
# Gráfico de barras
# ===============================
cores = {"Alta": "red", "Média": "orange", "Baixa": "green"}
fig = px.bar(
    df,
    x="Prioridade",
    y="Ação Proposta",
    orientation="h",
    color="Nível",
    color_discrete_map=cores,
    title="Ranking de Prioridades (GUT)"
)
st.plotly_chart(fig, use_container_width=True)

# ===============================
# Exportação para Excel
# ===============================
def to_excel(df):
    return df.to_excel(index=False)

st.download_button(
    label="📥 Baixar Excel",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="matriz_gut_prioridades.csv",
    mime="text/csv"
)