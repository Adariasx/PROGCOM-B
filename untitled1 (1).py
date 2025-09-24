import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --------------------------
# Función de simulación RLC
# --------------------------
def simular_RLC(R, L, C, V0):
    # Fuente escalón
    def V_in(t):
        return V0 if t >= 0 else 0

    # Sistema de ecuaciones
    def circuito(t, y):
        i, di = y
        d2i = ((0 - R*di - (1/C)*i)) / L
        return [di, d2i]

    # Condiciones iniciales
    y0 = [0.0, 0.0]

    # Cálculo de parámetros de amortiguamiento
    alpha = R / (2*L)
    omega0 = 1 / np.sqrt(L*C)
    
    if alpha < omega0:  # Subamortiguado
        tipo = "Subamortiguado (oscilatorio)"
        omega_d = np.sqrt(omega0**2 - alpha**2)
        T = 2*np.pi/omega_d  # periodo oscilación
        t_final = 10*T  # simular 10 periodos
    elif np.isclose(alpha, omega0):
        tipo = "Críticamente amortiguado"
        t_final = 5/alpha
    else:
        tipo = "Sobreamortiguado"
        t_final = 5/alpha

    t_eval = np.linspace(0, t_final, 2000)
    sol = solve_ivp(circuito, [0, t_final], y0, t_eval=t_eval)
    
    return sol.t, sol.y, tipo

# --------------------------
# Programa interactivo
# --------------------------
if __name__ == "__main__":
    print("📡 Simulación de circuito RLC en serie 📡")
    R = float(input("Ingrese R [Ohm]: "))
    L = float(input("Ingrese L [H]: "))
    C = float(input("Ingrese C [F]: "))
    V0 = float(input("Ingrese voltaje de entrada (escalón) [V]: "))

    t, y, tipo = simular_RLC(R, L, C, V0)
    print(f"\n⚡ Tipo de respuesta: {tipo}")

    # Graficar
    plt.figure(figsize=(10,5))
    plt.plot(t, y[0], label="Corriente i(t) [A]", color="b")
    plt.plot(t, y[1], label="di/dt [A/s]", color="r", linestyle="--")
    plt.title(f"Respuesta del circuito RLC ({tipo})")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Magnitud")
    plt.grid(True)
    plt.legend()
    plt.show()
