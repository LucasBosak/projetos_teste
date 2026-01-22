import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Saldo de Guias", layout="centered")

# =================================
# Caminhos
# =================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BASE = os.path.join(BASE_DIR, "Terminais.xlsx")
CAMINHO_SAIDA = os.path.join(BASE_DIR, "respostas.xlsx")

# =================================
# Carregar base
# =================================
df = pd.read_excel(CAMINHO_BASE)

# =================================
# Seleção da estação
# =================================
estacoes = df["Estação"].dropna().sort_values().unique()

estacao_selecionada = st.selectbox(
    "Selecione sua estação",
    estacoes
)

# =================================
# Título
# =================================
st.title("Informe o saldo de guias de arrecadação dos pontos abaixo:")

# Lista que armazenará os dados do envio
dados = []

# =================================
# Pontos da estação (dinâmicos)
# =================================
df_pontos = df[df["Estação"] == estacao_selecionada]

st.subheader("Pontos da estação")

for _, row in df_pontos.iterrows():
    saldo = st.number_input(
        label=row["Ponto"],
        min_value=0,
        step=1
    )

    dados.append({
        "Data": datetime.now(),
        "Estação": estacao_selecionada,
        "Item": row["Ponto"],
        "Saldo": saldo
    })

# =================================
# Itens fixos (iguais para todas as estações)
# =================================
st.subheader("Itens fixos")

itens_fixos = [
    "Malote PP",
    "Malote P",
    "Malote M",
    "Malote G",
    "Malote GG",
    "Saco bananinha",
    "Saco ráfia",
    "RRM",
    "Álcool",
    "Siga viagem",
    "BDV - Sala de segurança",
    "BDV - Bilheteria"
]

for item in itens_fixos:
    saldo = st.number_input(
        label=item,
        min_value=0,
        step=1
    )

    dados.append({
        "Data": datetime.now(),
        "Estação": estacao_selecionada,
        "Item": item,
        "Saldo": saldo
    })

# =================================
# Envio (sem exibir histórico)
# =================================
if st.button("Enviar"):
    resultado = pd.DataFrame(dados)

    if os.path.exists(CAMINHO_SAIDA):
        base_existente = pd.read_excel(CAMINHO_SAIDA)
        resultado = pd.concat([base_existente, resultado], ignore_index=True)

    resultado.to_excel(CAMINHO_SAIDA, index=False)

    st.success("Envio realizado com sucesso!")

