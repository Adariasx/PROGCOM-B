import tkinter as tk 
from tkinter import messagebox, ttk
import math 

#### main code de esta mkada 
tablero = [' ' for _ in range(9)] 
jugador = '😎'
botsito = '🤖'
jugador_actual = jugador 
bottone = [] 
dificultad = 'dificil'
puntuacion_jugador = 0
puntuacion_bot = 0

# Opciones de símbolos disponibles
SIMBOLOS_JUGADOR = ['X', 'O', '😎', '🔥', '⭐', '💎', '🎮', '👑', '⚡', '🌟']
SIMBOLOS_BOT = ['O', 'X', '🤖', '👾', '💀', '🎯', '🔮', '💣', '🌙', '☠️']

COLORES_JUGADOR = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
COLORES_BOT = ['#e74c3c', '#3498db', '#c0392b', '#d35400', '#8e44ad', '#16a085', '#7f8c8d', '#2c3e50']

def cambiar_simbolo_jugador():
    global jugador
    ventana_simbolos = tk.Toplevel(root)
    ventana_simbolos.title("Elige tu símbolo")
    ventana_simbolos.configure(bg='#2c3e50')
    ventana_simbolos.resizable(False, False)
    
    tk.Label(ventana_simbolos, text="Selecciona tu símbolo:", 
             font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
    
    frame_simbolos = tk.Frame(ventana_simbolos, bg='#2c3e50')
    frame_simbolos.pack(padx=20, pady=10)
    
    for i, simbolo in enumerate(SIMBOLOS_JUGADOR):
        btn = tk.Button(frame_simbolos, text=simbolo, font=('Arial', 24, 'bold'),
                       width=3, height=1, bg='#34495e', fg='#ecf0f1',
                       command=lambda s=simbolo: seleccionar_simbolo_jugador(s, ventana_simbolos))
        btn.grid(row=i//5, column=i%5, padx=5, pady=5)
    
    ventana_simbolos.transient(root)
    ventana_simbolos.grab_set()

def cambiar_simbolo_bot():
    global botsito
    ventana_simbolos = tk.Toplevel(root)
    ventana_simbolos.title("Elige símbolo del bot")
    ventana_simbolos.configure(bg='#2c3e50')
    ventana_simbolos.resizable(False, False)
    
    tk.Label(ventana_simbolos, text="Selecciona símbolo del bot:", 
             font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(pady=10)
    
    frame_simbolos = tk.Frame(ventana_simbolos, bg='#2c3e50')
    frame_simbolos.pack(padx=20, pady=10)
    
    for i, simbolo in enumerate(SIMBOLOS_BOT):
        btn = tk.Button(frame_simbolos, text=simbolo, font=('Arial', 24, 'bold'),
                       width=3, height=1, bg='#34495e', fg='#ecf0f1',
                       command=lambda s=simbolo: seleccionar_simbolo_bot(s, ventana_simbolos))
        btn.grid(row=i//5, column=i%5, padx=5, pady=5)
    
    ventana_simbolos.transient(root)
    ventana_simbolos.grab_set()

def seleccionar_simbolo_jugador(simbolo, ventana):
    global jugador
    jugador = simbolo
    actualizar_etiquetas()
    ventana.destroy()
    reseteo()

def seleccionar_simbolo_bot(simbolo, ventana):
    global botsito
    botsito = simbolo
    actualizar_etiquetas()
    ventana.destroy()
    reseteo()

def cambiar_dificultad():
    global dificultad
    ventana_dif = tk.Toplevel(root)
    ventana_dif.title("Dificultad")
    ventana_dif.configure(bg='#2c3e50')
    ventana_dif.resizable(False, False)
    
    tk.Label(ventana_dif, text="Selecciona la dificultad:", 
             font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(pady=15)
    
    dificultades = [
        ('Fácil (Aleatorio)', 'facil'),
        ('Medio (50% inteligente)', 'medio'),
        ('Difícil (Invencible)', 'dificil')
    ]
    
    for texto, nivel in dificultades:
        btn = tk.Button(ventana_dif, text=texto, font=('Arial', 12, 'bold'),
                       width=25, bg='#34495e', fg='#ecf0f1',
                       command=lambda n=nivel: seleccionar_dificultad(n, ventana_dif))
        btn.pack(padx=20, pady=5)
    
    ventana_dif.transient(root)
    ventana_dif.grab_set()

def seleccionar_dificultad(nivel, ventana):
    global dificultad
    dificultad = nivel
    actualizar_etiquetas()
    ventana.destroy()
    reseteo()

def actualizar_etiquetas():
    sub.config(text=f"Jugador: {jugador} | Bot: {botsito} | Dificultad: {dificultad.upper()}")
    puntos_label.config(text=f"Jugador: {puntuacion_jugador} | Bot: {puntuacion_bot}")

def movimiento_de_jugador(pos): 
    global jugador_actual 
    if tablero[pos] == ' ' and jugador_actual == jugador: 
        tablero[pos] = jugador 
        bottone[pos].config(text=jugador, fg=COLORES_JUGADOR[0]) 
 
        if orale_ganaste(jugador): 
            global puntuacion_jugador
            puntuacion_jugador += 1
            actualizar_etiquetas()
            messagebox.showinfo("🎉 ¡Victoria!", f"¡Ganaste! {jugador} es el campeón") 
            reseteo() 
            return 
 
        if ' ' not in tablero: 
            messagebox.showinfo("😐 Empate", "Empate técnico - ambos son buenos") 
            reseteo() 
            return 
 
        jugador_actual = botsito 
        root.after(500, botsito_mueve) 

def botsito_mueve(): 
    global jugador_actual, puntuacion_bot
    
    if dificultad == 'facil':
        # Movimiento aleatorio
        import random
        movimientos_disponibles = [i for i in range(9) if tablero[i] == ' ']
        if movimientos_disponibles:
            mejor_movimiento = random.choice(movimientos_disponibles)
    elif dificultad == 'medio':
        # 50% probabilidad de jugar perfecto, 50% aleatorio
        import random
        if random.random() < 0.5:
            mejor_movimiento = movimiento_inteligente()
        else:
            movimientos_disponibles = [i for i in range(9) if tablero[i] == ' ']
            mejor_movimiento = random.choice(movimientos_disponibles) if movimientos_disponibles else None
    else:  # dificil
        mejor_movimiento = movimiento_inteligente()
 
    if mejor_movimiento is not None: 
        tablero[mejor_movimiento] = botsito 
        bottone[mejor_movimiento].config(text=botsito, fg=COLORES_BOT[0]) 
 
        if orale_ganaste(botsito): 
            puntuacion_bot += 1
            actualizar_etiquetas()
            messagebox.showinfo("🤖 Bot gana", f"{botsito} gana - Mejor suerte la próxima") 
            reseteo() 
            return 
 
        if ' ' not in tablero: 
            messagebox.showinfo("😐 Empate", "Empate - ¡Bien jugado!") 
            reseteo() 
            return 
 
        jugador_actual = jugador

def movimiento_inteligente():
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
    
    return mejor_movimiento

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

def resetear_puntuacion():
    global puntuacion_jugador, puntuacion_bot
    puntuacion_jugador = 0
    puntuacion_bot = 0
    actualizar_etiquetas()
    reseteo()

# interfazszzzzzzzzzzzzzzzzzzzzzzzzzzzzz 
root = tk.Tk() 
root.title("TIC TAC TOE PRO") 
root.configure(bg='#2c3e50') 

frame = tk.Frame(root, bg='#2c3e50') 
frame.pack(padx=20, pady=20) 
root.resizable(False, False) 

titulo = tk.Label(frame, text="TIC TAC TOE PRO", 
                  font=('Arial', 24, 'bold'), 
                  bg='#2c3e50', fg='#ecf0f1') 
titulo.grid(row=0, column=0, columnspan=3, pady=10) 

sub = tk.Label(frame, text=f"Jugador: {jugador} | Bot: {botsito} | Dificultad: {dificultad.upper()}", 
               font=('Arial', 11), 
               bg='#2c3e50', fg='#95a5a6') 
sub.grid(row=1, column=0, columnspan=3, pady=5)

puntos_label = tk.Label(frame, text=f"Jugador: {puntuacion_jugador} | Bot: {puntuacion_bot}", 
                        font=('Arial', 13, 'bold'), 
                        bg='#2c3e50', fg='#f39c12') 
puntos_label.grid(row=2, column=0, columnspan=3, pady=5)

for i in range(9): 
    b = tk.Button(frame, text=' ', font=('Arial', 32, 'bold'), 
                  width=5, height=2, 
                  bg='#34495e', fg='#ecf0f1', 
                  activebackground='#475a6b', 
                  command=lambda x=i: movimiento_de_jugador(x)) 
    b.grid(row=i // 3 + 3, column=i % 3, padx=5, pady=5) 
    bottone.append(b) 

# Frame para botones de control
control_frame = tk.Frame(frame, bg='#2c3e50')
control_frame.grid(row=6, column=0, columnspan=3, pady=10)

reseteo_bottone = tk.Button(control_frame, text="🔄 Reiniciar", 
                      font=('Arial', 12, 'bold'), 
                      bg='#27ae60', fg='white', 
                      activebackground='#2ecc71', 
                      command=reseteo)
reseteo_bottone.grid(row=0, column=0, padx=5)

simbolo_jugador_btn = tk.Button(control_frame, text="🎭 Tu símbolo", 
                      font=('Arial', 12, 'bold'), 
                      bg='#3498db', fg='white', 
                      activebackground='#5dade2', 
                      command=cambiar_simbolo_jugador)
simbolo_jugador_btn.grid(row=0, column=1, padx=5)

simbolo_bot_btn = tk.Button(control_frame, text="🤖 Bot símbolo", 
                      font=('Arial', 12, 'bold'), 
                      bg='#e74c3c', fg='white', 
                      activebackground='#ec7063', 
                      command=cambiar_simbolo_bot)
simbolo_bot_btn.grid(row=0, column=2, padx=5)

dificultad_btn = tk.Button(control_frame, text="⚙️ Dificultad", 
                      font=('Arial', 12, 'bold'), 
                      bg='#f39c12', fg='white', 
                      activebackground='#f8c471', 
                      command=cambiar_dificultad)
dificultad_btn.grid(row=1, column=0, padx=5, pady=5)

resetear_puntos_btn = tk.Button(control_frame, text="🏆 Resetear puntos", 
                      font=('Arial', 12, 'bold'), 
                      bg='#9b59b6', fg='white', 
                      activebackground='#bb8fce', 
                      command=resetear_puntuacion)
resetear_puntos_btn.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

root.mainloop()
