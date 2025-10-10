import tkinter as tk
from tkinter import messagebox
import math

#### main code de esta mkada
tablero = [' ' for _ in range(9)]
jugador = 'X'
botsito = 'O'
jugador_actual = jugador
bottone = []


def movimiento_de_jugador(pos):
    global jugador_actual
    if tablero[pos] == ' ' and jugador_actual == jugador:
        tablero[pos] = jugador
        bottone[pos].config(text=jugador, fg='#3498db')

        if orale_ganaste(jugador):
            messagebox.showinfo("Ganaste", "Ganaste wooojooo")
            reseteo()
            return

        if ' ' not in tablero:
            messagebox.showinfo("Empate", "Dos bobos")
            reseteo()
            return

        jugador_actual = botsito
        root.after(500, botsito_mueve)


def botsito_mueve():
    global jugador_actual
    mejor_puntuacion = -math.inf
    mejor_movimiento = None

    for i in range(9):
        if tablero[i] == ' ':
            tablero[i] = botsito
            puntos = codigo_minmax(tablero, 0, False)
            tablero[i] = ' '
            if puntos > mejor_puntuacion:
                mejor_puntuacion = puntos
                mejor_movimiento = i

    if mejor_movimiento is not None:
        tablero[mejor_movimiento] = botsito
        bottone[mejor_movimiento].config(text=botsito, fg='#e74c3c')

        if orale_ganaste(botsito):
            messagebox.showinfo("bot gana", "tu noob")
            reseteo()
            return

        if ' ' not in tablero:
            messagebox.showinfo("empate", "Buena esa bro")
            reseteo()
            return

        jugador_actual = jugador


def codigo_minmax(tablero, depth, is_maximizing):
    if orale_ganaste(botsito):
        return 10 - depth
    if orale_ganaste(jugador):
        return depth - 10
    if ' ' not in tablero:
        return 0

    if is_maximizing:
        mejor_ruta = -math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = botsito
                score = codigo_minmax(tablero, depth + 1, False)
                tablero[i] = ' '
                mejor_ruta = max(score, mejor_ruta)
        return mejor_ruta
    else:
        mejor_ruta = math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = jugador
                score = codigo_minmax(tablero, depth + 1, True)
                tablero[i] = ' '
                mejor_ruta = min(score, mejor_ruta)
        return mejor_ruta


def orale_ganaste(player):
    combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(tablero[i] == player for i in combo) for combo in combos)


def reseteo():
    global tablero, jugador_actual
    tablero = [' ' for _ in range(9)]
    jugador_actual = jugador
    for btn in bottone:
        btn.config(text=' ', fg='#ecf0f1')


# interfazszzzzzzzzzzzzzzzzzzzzzzzzzzzzz
root = tk.Tk()
root.title("TIC TAC TOE")
root.configure(bg='#2c3e50')

frame = tk.Frame(root, bg='#2c3e50')
frame.pack(padx=20, pady=20)
root.resizable(False, False)

titulo = tk.Label(frame, text="TIC TAC TOE",
                  font=('Arial', 24, 'bold'),
                  bg='#2c3e50', fg='#ecf0f1')
titulo.grid(row=0, column=0, columnspan=3, pady=10)

sub = tk.Label(frame, text="Jugador: X | botsito: O",
               font=('Arial', 12),
               bg='#2c3e50', fg='#95a5a6')
sub.grid(row=1, column=0, columnspan=3, pady=5)

for i in range(9):
    b = tk.Button(frame, text=' ', font=('Arial', 32, 'bold'),
                  width=5, height=2,
                  bg='#34495e', fg='#ecf0f1',
                  activebackground='#475a6b',
                  command=lambda x=i: movimiento_de_jugador(x))
    b.grid(row=i // 3 + 2, column=i % 3, padx=5, pady=5)
    bottone.append(b)

reseteo_bottone = tk.Button(frame, text="Reiniciar",
                      font=('Arial', 14, 'bold'),
                      bg='#27ae60', fg='white',
                      activebackground='#2ecc71',
                      command=reseteo)
reseteo_bottone.grid(row=5, column=0, columnspan=3, pady=15)

root.mainloop()  