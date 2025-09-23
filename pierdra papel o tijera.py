import tkinter as tk
from tkinter import messagebox
import random

# Opciones del juego
opciones = ["Piedra", "Papel", "Tijera", "Lagarto", "Spock"]

# Reglas: qué gana a qué
# Cada clave gana a los valores en la lista
reglas = {
    "Piedra": ["Tijera", "Lagarto"],
    "Papel": ["Piedra", "Spock"],
    "Tijera": ["Papel", "Lagarto"],
    "Lagarto": ["Spock", "Papel"],
    "Spock": ["Tijera", "Piedra"]
}

class JuegoPPTLS:
    def __init__(self, master):
        self.master = master
        master.title("Piedra Papel Tijera Lagarto Spock")

        self.label = tk.Label(master, text="Elige tu jugada:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack()

        # Crear botones para cada opción
        for opcion in opciones:
            btn = tk.Button(self.frame_botones, text=opcion, width=12, height=2,
                            command=lambda op=opcion: self.jugar(op))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.resultado = tk.Label(master, text="", font=("Arial", 12), fg="blue")
        self.resultado.pack(pady=20)

    def jugar(self, eleccion_usuario):
        eleccion_ia = random.choice(opciones)
        resultado = self.comprobar_ganador(eleccion_usuario, eleccion_ia)

        texto = f"Tú elegiste: {eleccion_usuario}\nIA eligió: {eleccion_ia}\n\n{resultado}"
        self.resultado.config(text=texto)

    def comprobar_ganador(self, usuario, ia):
        if usuario == ia:
            return "¡Empate!"
        elif ia in reglas[usuario]:
            return "¡Ganaste!"
        else:
            return "¡Perdiste!"

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoPPTLS(root)
    root.mainloop()
