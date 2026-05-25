import pandas as pd
import matplotlib.pyplot as plt
import os

# Carga de datos usando ruta relativa para reproducibilidad en Colab
df = pd.read_csv("datos/dataset.csv")
df["fecha"] = pd.to_datetime(df["fecha"])

equipos = sorted(set(df["equipo_local"].tolist() + df["equipo_visitante"].tolist()))
stats = {eq: {"PJ":0,"PG":0,"PE":0,"PP":0,"GF":0,"GC":0} for eq in equipos}

# Procesar cada partido y calcular resultados por equipo
for _, fila in df.iterrows():
    local  = fila["equipo_local"]
    visita = fila["equipo_visitante"]
    gl = fila["goles_local"]
    gv = fila["goles_visitante"]
    stats[local]["PJ"]  += 1
    stats[visita]["PJ"] += 1
    stats[local]["GF"]  += gl
    stats[local]["GC"]  += gv
    stats[visita]["GF"] += gv
    stats[visita]["GC"] += gl
    if gl > gv:
        stats[local]["PG"]  += 1
        stats[visita]["PP"] += 1
    elif gl < gv:
        stats[visita]["PG"] += 1
        stats[local]["PP"]  += 1
    else:
        stats[local]["PE"]  += 1
        stats[visita]["PE"] += 1

# Construir tabla de posiciones con puntos y diferencia de goles
tabla = pd.DataFrame(stats).T.reset_index()
tabla.columns = ["Equipo","PJ","PG","PE","PP","GF","GC"]
tabla["Pts"] = tabla["PG"] * 3 + tabla["PE"]
tabla["DG"]  = tabla["GF"] - tabla["GC"]
tabla = tabla.sort_values(["Pts","DG","GF"], ascending=[False,False,False]).reset_index(drop=True)
tabla.index += 1

print("="*50)
print("TABLA DE POSICIONES")
print("="*50)
print(tabla[["Equipo","PJ","PG","PE","PP","GF","GC","DG","Pts"]].to_string())

total_goles = df["goles_local"].sum() + df["goles_visitante"].sum()
promedio = total_goles / len(df)
print(f"\nTotal de goles: {total_goles}")
print(f"Promedio por partido: {promedio:.2f}")
print(f"Equipo lider: {tabla.iloc[0]['Equipo']}")

os.makedirs("resultados", exist_ok=True)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Torneo Deportivo - Analisis de Rendimiento", fontsize=14, fontweight="bold")

equipos_orden = tabla["Equipo"].tolist()
x = range(len(equipos_orden))
ancho = 0.25

ax1 = axes[0]
ax1.bar(x, tabla["PG"].tolist(), ancho, label="Ganados", color="#2ecc71")
ax1.bar([i+ancho for i in x], tabla["PE"].tolist(), ancho, label="Empatados", color="#f39c12")
ax1.bar([i+ancho*2 for i in x], tabla["PP"].tolist(), ancho, label="Perdidos", color="#e74c3c")
ax1.set_title("Resultados por equipo")
ax1.set_xticks([i+ancho for i in x])
ax1.set_xticklabels(equipos_orden, rotation=15, ha="right")
ax1.set_ylabel("Partidos")
ax1.legend()
ax1.grid(axis="y", alpha=0.3)

ax2 = axes[1]
colores = ["#f1c40f" if i==0 else "#95a5a6" for i in range(len(equipos_orden))]
ax2.barh(equipos_orden[::-1], tabla["Pts"].tolist()[::-1], color=colores[::-1])
ax2.set_title("Ranking final por puntos")
ax2.set_xlabel("Puntos")
ax2.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig("resultados/analisis_deportivo.png", dpi=150, bbox_inches="tight")
print("\nGrafico guardado en resultados/analisis_deportivo.png")
