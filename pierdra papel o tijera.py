import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class PiedraPapeloTijera:
    def __init__(self, root):
        self.root = root
        self.opciones_clasico = [
            ("Piedra", "🪨"),
            ("Papel", "📄"),
            ("Tijera", "✂️")
        ]
        self.opciones_extendido = [
            ("Piedra", "🪨"),
            ("Papel", "📄"),
            ("Tijera", "✂️"),
            ("Lagarto", "🦎"),
            ("Spock", "🖖"),
            ("Pistola", "🔫"),
            ("Ninja", "🥷"),
            ("Pirata", "🏴‍☠️"),
            ("Meteorito", "☄️"),
            ("Carro", "🚗")
        ]
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0
        self.seleccionar_modo()

    def seleccionar_modo(self):
        self.modo_ventana = tk.Toplevel(self.root)
        self.modo_ventana.title("Selecciona el modo de juego")
        tk.Label(self.modo_ventana, text="Elige el modo de juego:", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.modo_ventana, text="Clásico", width=15, font=("Arial", 12), command=lambda: self.iniciar_juego('clasico')).pack(pady=5)
        tk.Button(self.modo_ventana, text="Extendido", width=15, font=("Arial", 12), command=lambda: self.iniciar_juego('extendido')).pack(pady=5)

    def iniciar_juego(self, modo):
        self.modo_ventana.destroy()
        if modo == 'clasico':
            self.choices = self.opciones_clasico
        else:
            self.choices = self.opciones_extendido
        self.ventana_juego(self.root)

    def ventana_juego(self, root):

        # Colores de fondo
        bg_color = "#e0e7ff"  # Azul claro
        frame_color = "#c7d2fe"  # Azul más intenso
        self.root.configure(bg=bg_color)

        self.resultado = tk.Label(root, text="", font=("Arial", 18, "bold"), bg=bg_color)
        self.resultado.pack(pady=(10, 10))
        self.label = tk.Label(root, text="Elige tu opción:", font=("Arial", 14), bg=bg_color)
        self.label.pack(pady=10)
        self.botones = tk.Frame(root, bg=frame_color)
        self.botones.pack()
        self.botones_lista = []
        for nombre, emoji in self.choices:
            img = self.cargar_imagen(nombre)
            if img:
                btn = tk.Button(self.botones, text=f"{emoji} {nombre}", image=img, compound="top", width=90, height=90, command=lambda n=nombre: self.jugar(n), bg=frame_color)
                btn.image = img
            else:
                btn = tk.Button(self.botones, text=f"{emoji} {nombre}", width=12, command=lambda n=nombre: self.jugar(n), bg=frame_color)
            btn.pack(side=tk.LEFT, padx=5, pady=10)
            self.botones_lista.append(btn)
        self.marcador = tk.Label(root, text="Victorias: 0 | Derrotas: 0 | Empates: 0", font=("Arial", 12), bg=bg_color)
        self.marcador.pack(pady=10)

    def cargar_imagen(self, nombre):
        ruta = os.path.join("img", f"{nombre}.png")
        if os.path.exists(ruta):
            img = Image.open(ruta).resize((60, 60))
            return ImageTk.PhotoImage(img)
        return None

    def jugar(self, eleccion_del_usuario):
        self.eleccion_del_usuario = eleccion_del_usuario
        bot_nombre, bot_emoji = random.choice(self.choices)
        self.bot = bot_nombre
        user_emoji = next(e for n, e in self.choices if n == eleccion_del_usuario)
        result = self.quien_gana()

        if result == "Ganaste":
            self.resultado.config(fg="green")
            self.ganados += 1
        elif result == "Perdiste":
            self.resultado.config(fg="red")
            self.perdidos += 1
        else:
            self.resultado.config(fg="gray")
            self.empates += 1

        self.resultado.config(
            text=f"{result}\n\nElegiste: {user_emoji} {self.eleccion_del_usuario}\nBot eligió: {bot_emoji} {self.bot}"
        )
        self.marcador.config(text=f"Victorias: {self.ganados} | Derrotas: {self.perdidos} | Empates: {self.empates}")
        messagebox.showinfo("Resultado", result)

    def quien_gana(self):
        # Diccionario de reglas: cada opción vence a la lista asociada
        reglas = {
            "Piedra":     ["Tijera", "Lagarto", "Pistola", "Meteorito", "Carro"],
            "Papel":      ["Piedra", "Spock", "Pistola", "Meteorito", "Carro"],
            "Tijera":     ["Papel", "Lagarto", "Pistola", "Ninja", "Carro"],
            "Lagarto":    ["Spock", "Papel", "Pistola", "Pirata", "Carro"],
            "Spock":      ["Tijera", "Piedra", "Pistola", "Ninja", "Carro"],
            "Pistola":    ["Spock", "Lagarto", "Tijera", "Pirata", "Carro"],
            "Ninja":      ["Pirata", "Papel", "Lagarto", "Pistola", "Carro"],
            "Pirata":     ["Papel", "Spock", "Meteorito", "Ninja", "Carro"],
            "Meteorito":  ["Piedra", "Tijera", "Lagarto", "Spock", "Carro"],
            "Carro":      ["Piedra", "Papel", "Tijera", "Lagarto", "Spock", "Pistola", "Ninja", "Pirata", "Meteorito"],
        }
        if self.eleccion_del_usuario == self.bot:
            return "Empate"
        elif self.bot in reglas[self.eleccion_del_usuario]:
            return "Ganaste"
        else:
            return "Perdiste"

if __name__ == "__main__":  # Corregido: __name__ en lugar de _name_
    root = tk.Tk()
    app = PiedraPapeloTijera(root)
    root.mainloop()
