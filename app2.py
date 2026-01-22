import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Formulário de Saldo", layout="centered")

# ===============================
# Carregar base Excel
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BASE = os.path.join(BASE_DIR, "Terminais.xlsx")

df = pd.read_excel(CAMINHO_BASE)

# ===============================
# Título
# ===============================
st.title("Formulário de Saldo por Estação")

# ===============================
# Pergunta 1 - Estação (lista suspensa)
# ===============================
estacoes = (
    df["Estação"]
    .dropna()
    .sort_values()
    .unique()
)

estacao_selecionada = st.selectbox(
    "Selecione sua estação",
    estacoes
)

# ===============================
# Pergunta 2 - Pontos da estação
# ===============================
st.subheader("Informe o saldo dos pontos abaixo")

df_pontos = df[df["Estação"] == estacao_selecionada]

saldos = []

for _, row in df_pontos.iterrows():
    saldo = st.number_input(
        label=row["Ponto"],
        min_value=0.0,
        step=1.0
    )

    saldos.append({
        "Estação": estacao_selecionada,
        "Ponto": row["Ponto"],
        "Saldo": saldo
    })

# ===============================
# Botão Enviar
# ===============================
if st.button("Enviar"):
    resultado = pd.DataFrame(saldos)

    st.success("Dados enviados com sucesso!")
    st.dataframe(resultado)


