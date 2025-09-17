import tkinter as tk
from tkinter import messagebox
import random

class PiedraPapeloTijera:
    def __init__(self, root):
        self.ventana_juego(root)

    def ventana_juego(self, root):
        self.root = root
        self.root.title("Piedra, Papel o Tijera")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.choices = ["Piedra", "Papel", "Tijera"]
        self.elección_del_usuario = None
        self.bot = None

        ## Contador
        self.ganados = 0
        self.perdidos = 0
        self.empates = 0

        ## q hacer
        self.label = tk.Label(root, text="Elige tu opción:", font=("Arial", 14))
        self.label.pack(pady=20)

        ## btones
        self.botones = tk.Frame(root)
        self.botones.pack()

        self.rock_button = tk.Button(self.botones, text="Piedra", width=10, command=lambda: self.jugar("Piedra"))
        self.rock_button.pack(side=tk.LEFT, padx=10)

        self.boton_papel = tk.Button(self.botones, text="Papel", width=10, command=lambda: self.jugar("Papel"))
        self.boton_papel.pack(side=tk.LEFT, padx=10)

        self.tijeras_boton = tk.Button(self.botones, text="Tijera", width=10, command=lambda: self.jugar("Tijera"))
        self.tijeras_boton.pack(side=tk.LEFT, padx=10)

        # resutlado
        self.resultado = tk.Label(root, text="", font=("Arial", 12))
        self.resultado.pack(pady=20)

        # marcador
        self.marcador = tk.Label(root, text="Victorias: 0 | Derrotas: 0 | Empates: 0", font=("Arial", 12))
        self.marcador.pack(pady=10)

    def jugar(self, elección_del_usuario):
        self.elección_del_usuario = elección_del_usuario
        self.bot = random.choice(self.choices)

        result = self.quien_gana()

        # quien perdio o gano
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
            text=f"elegiste: {self.elección_del_usuario}\n"
                 f"bot eligió: {self.bot}\n"
                 f"{result}"
        )

        # marcador
        self.marcador.config(text=f"Victorias: {self.ganados} | Derrotas: {self.perdidos} | Empates: {self.empates}")

        # ventana para q sepa 
        messagebox.showinfo("Resultado", result)

    def quien_gana(self):
        if self.elección_del_usuario == self.bot:
            return "Empate"
        elif (self.elección_del_usuario == "Piedra" and self.bot == "Tijera") or \
             (self.elección_del_usuario == "Papel" and self.bot == "Piedra") or \
             (self.elección_del_usuario == "Tijera" and self.bot == "Papel"):
            return "Ganaste"
        else:
            return "Perdiste"

if __name__ == "__main__":
    root = tk.Tk()
    app = PiedraPapeloTijera(root)
    root.mainloop()
