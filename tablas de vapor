import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import streamlit as st

st.set_page_config(page_title="Tablas de vapor", layout="centered")

# Estilos personalizados (dark + naranja)
st.markdown("""
<style>
    body, .stApp { background-color: #0e1117; color: white; }
    .stButton>button {
        background-color: #ff4b00;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
    }
    .stButton>button:hover { opacity: 0.85; }
    div[data-baseweb="radio"] label span { color: #ff8c00; }
</style>
""", unsafe_allow_html=True)

# --- Datos base ---
T = np.array([0, 95, 170, 245, 320, 374])  # °C
P = np.array([0.611, 84.5, 791, 4010, 22064, 101325])  # kPa
H_liq = np.array([0, 398, 725, 1050, 1410, 2090])  # kJ/kg
H_vap = np.array([2500, 2706, 2810, 2865, 2800, 2090])  # kJ/kg

# Ordenar por presión
idx = np.argsort(P)
P = P[idx]
T = T[idx]
H_liq = H_liq[idx]
H_vap = H_vap[idx]

# --- Crear splines ---
cs_T_from_P = CubicSpline(P, T, extrapolate=False)
cs_P_from_T = CubicSpline(T, P, extrapolate=False)
cs_Hl_from_T = CubicSpline(T, H_liq, extrapolate=False)
cs_Hv_from_T = CubicSpline(T, H_vap, extrapolate=False)

# --- UI ---
st.title("🔥 Propiedades de saturación del agua")
modo = st.radio("Selecciona qué deseas calcular:",
                ["Calcular presión (dado T)", "Calcular temperatura (dado P)"])

if modo == "Calcular presión (dado T)":
    temp = st.number_input("Temperatura (°C)", value=150.0)
    if st.button("Calcular"):
        P_sat = cs_P_from_T(temp)
        if np.isnan(P_sat):
            st.error("Temperatura fuera de rango")
        else:
            H_l = cs_Hl_from_T(temp)
            H_v = cs_Hv_from_T(temp)
            Q = H_v - H_l
            st.success(f"Presión de saturación: {P_sat:.2f} kPa")
            st.write(f"Entalpía líquido sat.: {H_l:.2f} kJ/kg")
            st.write(f"Entalpía vapor sat.: {H_v:.2f} kJ/kg")
            st.write(f"Calor latente: {Q:.2f} kJ/kg")

            fig, ax = plt.subplots()
            ax.plot(P, T, linewidth=2)
            ax.scatter(P_sat, temp, s=50)
            ax.set_xlabel("Presión (kPa)")
            ax.set_ylabel("Temperatura (°C)")
            ax.set_title("Curva de saturación del agua")
            ax.grid(True)
            ax.legend(["Curva de saturación", "Punto interpolado"])
            st.pyplot(fig)

else:
    pres = st.number_input("Presión (kPa)", value=2000.0)
    if st.button("Calcular"):
        T_sat = cs_T_from_P(pres)
        if np.isnan(T_sat):
            st.error("Presión fuera de rango")
        else:
            H_l = cs_Hl_from_T(T_sat)
            H_v = cs_Hv_from_T(T_sat)
            Q = H_v - H_l
            st.success(f"Temperatura de saturación: {T_sat:.2f} °C")
            st.write(f"Entalpía líquido sat.: {H_l:.2f} kJ/kg")
            st.write(f"Entalpía vapor sat.: {H_v:.2f} kJ/kg")
            st.write(f"Calor latente: {Q:.2f} kJ/kg")

            fig, ax = plt.subplots()
            ax.plot(P, T, linewidth=2)
            ax.scatter(pres, T_sat, s=50)
            ax.set_xlabel("Presión (kPa)")
            ax.set_ylabel("Temperatura (°C)")
            ax.set_title("Curva de saturación del agua")
            ax.grid(True)
            ax.legend(["Curva de saturación", "Temperatura de saturación"])
            st.pyplot(fig)


    btn.click(calc, [modo, temp, pres], [out_text, out_plot])

app.launch()
