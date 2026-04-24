import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("ggplot")

df = pd.read_csv("flamengo.csv")
df.columns = df.columns.str.lower().str.strip()

def pontos(r):
    return 3 if r == "V" else 1 if r == "E" else 0

df["pontos"] = df["resultado"].apply(pontos)
df["pontos_acumulados"] = df["pontos"].cumsum()

plt.figure(figsize=(10,5))
df.groupby("resultado")["finalizacoes"].mean().plot(kind="bar")
plt.title("Finalizações por Resultado")
plt.xlabel("Resultado")
plt.ylabel("Finalizações")
plt.grid(axis="y")
plt.show()

casa = df[df["local"] == "Casa"]
fora = df[df["local"] == "Fora"]

plt.figure(figsize=(8,5))
plt.bar(["Casa", "Fora"], [casa["gols_fla"].mean(), fora["gols_fla"].mean()])
plt.title("Gols: Casa vs Fora")
plt.ylabel("Gols")
plt.show()

plt.figure(figsize=(10,5))
plt.plot(df["rodada"], df["pontos_acumulados"], marker="o")
plt.title("Pontos Acumulados")
plt.xlabel("Rodada")
plt.ylabel("Pontos")
plt.grid()
plt.show()

plt.figure(figsize=(8,5))
df.groupby("resultado")["posse"].mean().plot(kind="bar")
plt.title("Posse por Resultado")
plt.ylabel("Posse (%)")
plt.show()