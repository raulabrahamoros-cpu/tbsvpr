import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import streamlit as st

# Dark + acento naranja
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background-color: #0e1117;}
[data-testid="stHeader"] {background-color: #0e1117;}
.css-1d391kg {color: #ff4b00;}
.stButton>button {background-color:#ff4b00; color:white; border-radius:6px;}
.stRadio>label {color:white;}
.stNumberInput>label {color:white;}
</style>
""", unsafe_allow_html=True)

# --- Datos base ---
T = np.array([0, 95, 170, 245, 320, 374])
P = np.array([0.611, 84.5, 791, 4010, 22064, 101325])
H_liq = np.array([0, 398, 725, 1050, 1410, 2090])
H_vap = np.array([2500, 2706, 2810, 2865, 2802, 2084])

# Ordenar por presión
idx = np.argsort(P)
T = T[idx]
P = P[idx]
H_liq = H_liq[idx]
H_vap = H_vap[idx]

# Crear splines
cs_P = CubicSpline(T, P, extrapolate=False)
cs_T = CubicSpline(P, T, extrapolate=False)
cs_Hl_T = CubicSpline(T, H_liq, extrapolate=False)
cs_Hv_T = CubicSpline(T, H_vap, extrapolate=False)
cs_Hl_P = CubicSpline(P, H_liq, extrapolate=False)
cs_Hv_P = CubicSpline(P, H_vap, extrapolate=False)

st.title("Propiedades de saturación del agua")

modo = st.radio("¿Qué deseas calcular?", ["Presión (dado T)", "Temperatura (dado P)"])

if modo == "Presión (dado T)":
    temp = st.number_input("Ingresa la temperatura (°C)", value=25.0)
    P_sat = cs_P(temp)

    if np.isnan(P_sat):
        st.error("Temperatura fuera de rango")
    else:
        H_l = cs_Hl_T(temp)
        H_v = cs_Hv_T(temp)
        Q = H_v - H_l

        st.success(f"""
        Resultados para T = {temp} °C:
        - Presión de saturación = {P_sat:.2f} kPa
        - Entalpía líquido sat. = {H_l:.2f} kJ/kg
        - Entalpía vapor sat. = {H_v:.2f} kJ/kg
        - Calor latente = {Q:.2f} kJ/kg
        """)

        fig, ax = plt.subplots()
        ax.plot(P, T, linewidth=2, label="Curva de saturación")
        ax.scatter(P_sat, temp, s=60, label="Punto interpolado")

        ax.set_xlabel("Presión (kPa)")
        ax.set_ylabel("Temperatura (°C)")
        ax.set_title("Temperatura vs Presión de saturación")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

else:
    pres = st.number_input("Ingresa la presión (kPa)", value=101.35)
    T_sat = cs_T(pres)

    if np.isnan(T_sat):
        st.error("Presión fuera de rango")
    else:
        H_l = cs_Hl_P(pres)
        H_v = cs_Hv_P(pres)
        Q = H_v - H_l

        st.success(f"""
        Resultados para P = {pres} kPa:
        - Temperatura de saturación = {T_sat:.2f} °C
        - Entalpía líquido sat. = {H_l:.2f} kJ/kg
        - Entalpía vapor sat. = {H_v:.2f} kJ/kg
        - Calor latente = {Q:.2f} kJ/kg
        """)

        fig, ax = plt.subplots()
        ax.plot(P, T, linewidth=2, label="Curva de saturación")
        ax.scatter(pres, T_sat, s=60, label="Punto interpolado")

        ax.set_xlabel("Presión (kPa)")
        ax.set_ylabel("Temperatura (°C)")
        ax.set_title("Curva de saturación del agua")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)


    btn.click(calc, [modo, temp, pres], [out_text, out_plot])

app.launch()
