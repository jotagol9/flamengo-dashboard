import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# =========================
#  ESTILO
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e0e0e;
        color: white;
    }
    h1, h2, h3 {
        color: #ff1a1a;
    }
    .metric {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
#  DADOS
# =========================
df = pd.read_csv("flamengo.csv")
df.columns = df.columns.str.lower().str.strip()

def pontos(r):
    return 3 if r == "V" else 1 if r == "E" else 0

df["pontos"] = df["resultado"].apply(pontos)
df["pontos_acumulados"] = df["pontos"].cumsum()

# =========================
#  HEADER COM LOGO
# =========================
col_logo, col_title = st.columns([1,8])

with col_logo:
    st.image("logo.png", width=120)

with col_title:
    st.markdown(
        """
        <div style='display:flex; align-items:center; height:100%;'>
            <h1 style='margin:0;'>Flamengo — Brasileirão</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
#  FILTRO
# =========================
local_opcao = st.selectbox("Local", ["Todos", "Casa", "Fora"])

if local_opcao != "Todos":
    df = df[df["local"] == local_opcao]

# =========================
#  MÉTRICAS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Jogos", len(df))
col2.metric("Pontos", df["pontos"].sum())
col3.metric("Gols", df["gols_fla"].sum())
col4.metric("Aproveitamento (%)", f"{(df['pontos'].sum()/(len(df)*3)*100):.1f}")

# =========================
#  GRÁFICOS 
# =========================
col5, col6 = st.columns(2)

with col5:
    st.subheader("Finalizações por Resultado")
    fig, ax = plt.subplots()
    df.groupby("resultado")["finalizacoes"].mean().plot(
        kind="bar", ax=ax, color="#ff1a1a"
    )
    st.pyplot(fig)

with col6:
    st.subheader("Posse por Resultado")
    fig2, ax2 = plt.subplots()
    df.groupby("resultado")["posse"].mean().plot(
        kind="bar", ax=ax2, color="black"
    )
    st.pyplot(fig2)

# =========================
#  GRÁFICOS 
# =========================
col7, col8 = st.columns(2)

with col7:
    st.subheader("Pontos acumulados")
    fig3, ax3 = plt.subplots()
    ax3.plot(df["rodada"], df["pontos_acumulados"], marker="o", color="#ff1a1a")
    st.pyplot(fig3)

with col8:
    st.subheader("Gols marcados x sofridos")
    fig4, ax4 = plt.subplots()
    ax4.plot(df["rodada"], df["gols_fla"], label="Marcados", color="#ff1a1a")
    ax4.plot(df["rodada"], df["gols_adv"], label="Sofridos", color="white")
    ax4.legend()
    st.pyplot(fig4)

# =========================
#  RESUMO
# =========================
st.subheader("Resumo")

st.write(f"""
- Total de pontos: {df['pontos'].sum()}
- Média de gols: {df['gols_fla'].mean():.2f}
- Média de finalizações: {df['finalizacoes'].mean():.1f}
""")

# =========================
#  TABELA
# =========================
st.subheader("Tabela de jogos")
st.dataframe(df)
