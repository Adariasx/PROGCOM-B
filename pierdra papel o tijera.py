import tkinter as tk
import random

# Opciones del juego con emojis
opciones = {
    "Piedra": "🪨",
    "Papel": "📄",
    "Tijera": "✂️",
    "Lagarto": "🦎",
    "Spock": "🖖",
    "Ninja": "🥷",
    "Pirata": "🏴‍☠️",
    "Dinosaurio": "🦖",
    "Alien": "👽",
    "Mago": "🧙"
}

# Reglas extendidas
reglas = {
    "Piedra": ["Tijera", "Lagarto", "Pirata"],
    "Papel": ["Piedra", "Spock", "Alien"],
    "Tijera": ["Papel", "Lagarto", "Ninja"],
    "Lagarto": ["Spock", "Papel", "Mago"],
    "Spock": ["Tijera", "Piedra", "Alien"],
    "Ninja": ["Pirata", "Mago", "Papel"],
    "Pirata": ["Alien", "Ninja", "Lagarto"],
    "Dinosaurio": ["Piedra", "Tijera", "Pirata"],
    "Alien": ["Dinosaurio", "Ninja", "Spock"],
    "Mago": ["Alien", "Dinosaurio", "Piedra"]
}

# Colores para los botones
colores = {
    "Piedra": "#a6a6a6",
    "Papel": "#ffffff",
    "Tijera": "#ff6666",
    "Lagarto": "#77dd77",
    "Spock": "#87cefa",
    "Ninja": "#2c2c2c",
    "Pirata": "#8b4513",
    "Dinosaurio": "#006400",
    "Alien": "#7fffd4",
    "Mago": "#9370db"
}

class JuegoPPTLS:
    def __init__(self, master):
        self.master = master
        master.title("Mega Piedra Papel Tijera EXTREMO ⚔️")

        # Variables para el marcador
        self.puntos_usuario = 0
        self.puntos_ia = 0

        self.label = tk.Label(master, text="Elige tu jugada:", font=("Arial", 14))
        self.label.pack(pady=10)

        # Frame de botones (en dos filas porque ahora son muchos)
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack()

        fila = 0
        col = 0
        for opcion, emoji in opciones.items():
            btn = tk.Button(
                self.frame_botones,
                text=f"{emoji} {opcion}",
                width=14,
                height=2,
                bg=colores[opcion],
                command=lambda op=opcion: self.jugar(op)
            )
            btn.grid(row=fila, column=col, padx=5, pady=5)
            col += 1
            if col == 5:  # para pasar a segunda fila
                fila += 1
                col = 0

        # Marcador
        self.marcador = tk.Label(master, text="👤 0 - 0 🤖", font=("Arial", 14, "bold"), fg="darkblue")
        self.marcador.pack(pady=10)

        # Resultado de la partida
        self.resultado = tk.Label(master, text="", font=("Arial", 12), fg="blue", justify="center")
        self.resultado.pack(pady=10)

        # Emoji grande del resultado
        self.resultado_emoji = tk.Label(master, text="", font=("Arial", 40))
        self.resultado_emoji.pack(pady=5)

        # Botón de reinicio
        self.btn_reiniciar = tk.Button(master, text="🔄 Reiniciar", font=("Arial", 12), command=self.reiniciar)
        self.btn_reiniciar.pack(pady=10)

    def jugar(self, eleccion_usuario):
        eleccion_ia = random.choice(list(opciones.keys()))
        resultado = self.comprobar_ganador(eleccion_usuario, eleccion_ia)

        # Mostrar jugadas
        texto = (
            f"👤 Tú: {opciones[eleccion_usuario]} {eleccion_usuario}\n"
            f"🤖 IA: {opciones[eleccion_ia]} {eleccion_ia}\n\n"
            f"{resultado}"
        )
        self.resultado.config(text=texto)

        # Actualizar marcador y emoji
        if "Ganaste" in resultado:
            self.puntos_usuario += 1
            self.resultado_emoji.config(text="🎉", fg="green")
        elif "Perdiste" in resultado:
            self.puntos_ia += 1
            self.resultado_emoji.config(text="💀", fg="red")
        else:
            self.resultado_emoji.config(text="😐", fg="gray")

        self.marcador.config(text=f"👤 {self.puntos_usuario} - {self.puntos_ia} 🤖")

    def comprobar_ganador(self, usuario, ia):
        if usuario == ia:
            return "😐 ¡Empate!"
        elif ia in reglas[usuario]:
            return "🎉 ¡Ganaste!"
        else:
            return "💀 ¡Perdiste!"

    def reiniciar(self):
        self.puntos_usuario = 0
        self.puntos_ia = 0
        self.marcador.config(text="👤 0 - 0 🤖")
        self.resultado.config(text="")
        self.resultado_emoji.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoPPTLS(root)
    root.mainloop()
