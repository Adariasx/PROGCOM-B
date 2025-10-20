import tkinter as tk
from tkinter import messagebox, font
import random
import json
import google.generativeai as genai
import threading
import time

letra_actual = ""
dificultad = "intermedio"
categorias_por_dificultad = {
    "facil": ["Nombre", "Animal", "Pais"],
    "intermedio": ["Nombre", "Animal", "Pais", "Fruta", "Objeto"],
    "crazy": ["Nombre", "Animal", "Pais", "Fruta", "Objeto", "Ciudad", "Profesion", "Marca"]
}
tiempo_espera_ia = {
    "facil": (8, 12),
    "intermedio": (5, 8),
    "crazy": (3, 5)
}
categorias = []
respuestas_jugador = {}
respuestas_gemini = {}
puntaje_jugador = 0
puntaje_gemini = 0
ronda = 0
jugador_termino = False
gemini_termino = False
tiempo_inicio = 0
tiempo_jugador = 0
tiempo_gemini = 0
campos_texto = {}
labels_gemini = {}
btn_stop = None
puntos_ronda_jugador = 0
puntos_ronda_gemini = 0

fuente_titulo = None
fuente_normal = None
fuente_categoria = None

def obtener_respuestas_gemini(letra, cats):
    try:
        genai.configure(api_key=xd)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""Estamos jugando STOP (tambien conocido como Basta).
La letra elegida es: {letra}
Las categorias son: {', '.join(cats)}

Devuelveme UNA palabra valida por cada categoria que EMPIECE con la letra "{letra}".
Las palabras deben ser en ESPANOL.

IMPORTANTE: Responde UNICAMENTE con un JSON valido en este formato:
{{
    {', '.join([f'"{cat}": "palabra"' for cat in cats])}
}}

No agregues explicaciones, solo el JSON."""

        response = model.generate_content(prompt)
        texto_respuesta = response.text.strip()
        
        if texto_respuesta.startswith('```json'):
            texto_respuesta = texto_respuesta[7:]
        if texto_respuesta.startswith('```'):
            texto_respuesta = texto_respuesta[3:]
        if texto_respuesta.endswith('```'):
            texto_respuesta = texto_respuesta[:-3]
        
        texto_respuesta = texto_respuesta.strip()
        respuestas = json.loads(texto_respuesta)
        
        for cat in cats:
            if cat not in respuestas:
                respuestas[cat] = ""
        
        return respuestas
        
    except:
        return {cat: "" for cat in cats}

def validar_respuesta(palabra, letra):
    if not palabra or palabra.strip() == "":
        return False
    return palabra.strip().upper().startswith(letra.upper())

def calcular_puntaje():
    global puntaje_jugador, puntaje_gemini, puntos_ronda_jugador, puntos_ronda_gemini
    
    puntos_ronda_jugador = 0
    puntos_ronda_gemini = 0
    bonus_velocidad = 5
    
    for categoria in categorias:
        resp_jugador = respuestas_jugador.get(categoria, "").strip()
        resp_gemini = respuestas_gemini.get(categoria, "").strip()
        
        jugador_valida = validar_respuesta(resp_jugador, letra_actual)
        gemini_valida = validar_respuesta(resp_gemini, letra_actual)
        
        if jugador_valida and gemini_valida:
            if resp_jugador.lower() == resp_gemini.lower():
                puntos_ronda_jugador += 5
                puntos_ronda_gemini += 5
            else:
                puntos_ronda_jugador += 10
                puntos_ronda_gemini += 10
        elif jugador_valida and not gemini_valida:
            puntos_ronda_jugador += 10
        elif not jugador_valida and gemini_valida:
            puntos_ronda_gemini += 10
    
    if tiempo_jugador < tiempo_gemini:
        puntos_ronda_jugador += bonus_velocidad
    elif tiempo_gemini < tiempo_jugador:
        puntos_ronda_gemini += bonus_velocidad
    
    puntaje_jugador += puntos_ronda_jugador
    puntaje_gemini += puntos_ronda_gemini

def gemini_jugar():
    global respuestas_gemini, tiempo_gemini, gemini_termino
    
    min_tiempo, max_tiempo = tiempo_espera_ia[dificultad]
    tiempo_espera = random.uniform(min_tiempo, max_tiempo)
    tiempo_por_categoria = tiempo_espera / len(categorias)
    
    for i, categoria in enumerate(categorias):
        if jugador_termino:
            tiempo_por_categoria = 0.5
        
        time.sleep(tiempo_por_categoria)
        root.after(0, lambda c=categoria: 
                  labels_gemini[c].config(text="escribiendo...", fg='#f39c12'))
    
    respuestas_gemini = obtener_respuestas_gemini(letra_actual, categorias)
    tiempo_gemini = time.time() - tiempo_inicio
    gemini_termino = True
    
    for categoria, respuesta in respuestas_gemini.items():
        root.after(0, lambda c=categoria, r=respuesta: 
                  labels_gemini[c].config(text=r, fg='#27ae60', font=('Arial', 11, 'bold')))
    
    if not jugador_termino:
        root.after(0, gemini_presiona_stop)

def jugador_presiona_stop():
    global jugador_termino, tiempo_jugador
    
    if jugador_termino:
        return
    
    jugador_termino = True
    tiempo_jugador = time.time() - tiempo_inicio
    
    for categoria, entry in campos_texto.items():
        respuestas_jugador[categoria] = entry.get().strip()
        entry.config(state='disabled')
    
    btn_stop.config(state='disabled', bg='#95a5a6')
    
    if not gemini_termino:
        messagebox.showinfo("Terminaste primero", 
                          "Has presionado STOP primero\nEsperando a que Gemini termine...")
        root.after(100, verificar_si_ambos_terminaron)
    else:
        mostrar_resultados()

def gemini_presiona_stop():
    global jugador_termino, tiempo_jugador
    
    if jugador_termino:
        return
    
    for entry in campos_texto.values():
        entry.config(state='disabled')
    
    btn_stop.config(state='disabled', bg='#95a5a6')
    
    messagebox.showwarning("Gemini ganó", 
                         f"Gemini presiono STOP primero en {tiempo_gemini:.2f} segundos\n\n"
                         "Tus respuestas actuales seran evaluadas.")
    
    for categoria, entry in campos_texto.items():
        respuestas_jugador[categoria] = entry.get().strip()
    
    jugador_termino = True
    tiempo_jugador = time.time() - tiempo_inicio
    
    mostrar_resultados()

def jugador_se_rinde():
    global jugador_termino, gemini_termino, respuestas_gemini, tiempo_jugador, tiempo_gemini
    
    respuesta = messagebox.askyesno("Rendirse", 
                                   "Seguro que quieres rendirte?\n"
                                   "Gemini ganara automaticamente esta ronda.")
    if respuesta:
        jugador_termino = True
        gemini_termino = True
        
        for categoria, entry in campos_texto.items():
            respuestas_jugador[categoria] = entry.get().strip()
        
        if not respuestas_gemini:
            respuestas_gemini = obtener_respuestas_gemini(letra_actual, categorias)
        
        tiempo_jugador = 999
        tiempo_gemini = time.time() - tiempo_inicio
        
        mostrar_resultados()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def verificar_si_ambos_terminaron():
    if jugador_termino and gemini_termino:
        mostrar_resultados()
    else:
        root.after(100, verificar_si_ambos_terminaron)

def mostrar_resultados():
    calcular_puntaje()
    
    if puntos_ronda_jugador > puntos_ronda_gemini:
        ganador_ronda = "TU GANASTE"
        color_ganador = "#27ae60"
    elif puntos_ronda_gemini > puntos_ronda_jugador:
        ganador_ronda = "GEMINI GANA"
        color_ganador = "#e74c3c"
    else:
        ganador_ronda = "EMPATE"
        color_ganador = "#f39c12"
    
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title(f"Resultados - Ronda {ronda}")
    ventana_resultados.geometry("800x700")
    ventana_resultados.configure(bg='#ecf0f1')
    ventana_resultados.transient(root)
    ventana_resultados.grab_set()
    
    frame_principal = tk.Frame(ventana_resultados, bg='#ecf0f1')
    frame_principal.pack(expand=True, fill='both', padx=20, pady=20)
    
    tk.Label(frame_principal, text=ganador_ronda, 
            font=('Arial', 28, 'bold'), bg=color_ganador, fg='white',
            relief='raised', bd=5).pack(pady=15, fill='x')
    
    frame_tiempos = tk.Frame(frame_principal, bg='white', relief='ridge', bd=2)
    frame_tiempos.pack(pady=10, fill='x')
    
    tk.Label(frame_tiempos, text="TIEMPOS", 
            font=fuente_categoria, bg='white', fg='#2c3e50').pack(pady=5)
    tk.Label(frame_tiempos, 
            text=f"Tu: {tiempo_jugador:.2f}s | Gemini: {tiempo_gemini:.2f}s",
            font=fuente_normal, bg='white', fg='#7f8c8d').pack(pady=5)
    
    frame_comp = tk.Frame(frame_principal, bg='white', relief='ridge', bd=2)
    frame_comp.pack(pady=10, fill='both', expand=True)
    
    tk.Label(frame_comp, text="Categoria", 
            font=('Arial', 10, 'bold'), bg='#34495e', fg='white',
            width=15).grid(row=0, column=0, sticky='ew', padx=1, pady=1)
    tk.Label(frame_comp, text="Tu respuesta", 
            font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
            width=20).grid(row=0, column=1, sticky='ew', padx=1, pady=1)
    tk.Label(frame_comp, text="Respuesta Gemini", 
            font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
            width=20).grid(row=0, column=2, sticky='ew', padx=1, pady=1)
    
    for i, categoria in enumerate(categorias, start=1):
        resp_jugador = respuestas_jugador.get(categoria, "")
        resp_gemini = respuestas_gemini.get(categoria, "")
        
        jugador_valida = validar_respuesta(resp_jugador, letra_actual)
        gemini_valida = validar_respuesta(resp_gemini, letra_actual)
        
        color_jugador = '#2ecc71' if jugador_valida else '#e74c3c'
        color_gemini = '#2ecc71' if gemini_valida else '#e74c3c'
        
        tk.Label(frame_comp, text=categoria, 
                font=('Arial', 10), bg='#ecf0f1',
                width=15).grid(row=i, column=0, sticky='ew', padx=1, pady=1)
        
        tk.Label(frame_comp, 
                text=resp_jugador if resp_jugador else "(vacio)", 
                font=('Arial', 10), bg=color_jugador, fg='white',
                width=20).grid(row=i, column=1, sticky='ew', padx=1, pady=1)
        
        tk.Label(frame_comp, 
                text=resp_gemini if resp_gemini else "(vacio)", 
                font=('Arial', 10), bg=color_gemini, fg='white',
                width=20).grid(row=i, column=2, sticky='ew', padx=1, pady=1)
    
    frame_puntos = tk.Frame(frame_principal, bg='#34495e', relief='raised', bd=3)
    frame_puntos.pack(pady=15, fill='x')
    
    tk.Label(frame_puntos, text=f"Puntos esta ronda:", 
            font=fuente_categoria, bg='#34495e', fg='white').pack(pady=5)
    tk.Label(frame_puntos, 
            text=f"Tu: +{puntos_ronda_jugador} pts | Gemini: +{puntos_ronda_gemini} pts", 
            font=fuente_normal, bg='#34495e', fg='#f39c12').pack(pady=5)
    
    tk.Label(frame_principal, 
            text=f"Puntaje Total: Tu {puntaje_jugador} - Gemini {puntaje_gemini}", 
            font=fuente_categoria, bg='#ecf0f1', fg='#16a085').pack(pady=10)
    
    if puntaje_gemini > puntaje_jugador and ronda >= 3:
        mostrar_ventana_gemini_gano(ventana_resultados)
        return
    
    frame_botones = tk.Frame(frame_principal, bg='#ecf0f1')
    frame_botones.pack(pady=15)
    
    btn_continuar = tk.Button(frame_botones, text="Siguiente Ronda",
                             font=fuente_normal, bg='#27ae60', fg='white',
                             activebackground='#2ecc71', cursor='hand2',
                             padx=20, pady=10, 
                             command=lambda: [ventana_resultados.destroy(), iniciar_partida()])
    btn_continuar.pack(side='left', padx=10)
    
    btn_dificultad = tk.Button(frame_botones, text="Cambiar Dificultad",
                               font=fuente_normal, bg='#f39c12', fg='white',
                               activebackground='#e67e22', cursor='hand2',
                               padx=20, pady=10,
                               command=lambda: [ventana_resultados.destroy(), 
                                               reiniciar_juego()])
    btn_dificultad.pack(side='left', padx=10)
    
    btn_salir = tk.Button(frame_botones, text="Salir",
                        font=fuente_normal, bg='#95a5a6', fg='white',
                        activebackground='#7f8c8d', cursor='hand2',
                        padx=20, pady=10,
                        command=root.quit)
    btn_salir.pack(side='left', padx=10)
xd="kLqF22Dlfxlsd08pL2/ZD6l5FLUmGp5PQRPqqXEF8TE"  
def mostrar_ventana_gemini_gano(ventana_anterior):
    ventana_anterior.destroy()
    
    ventana_gemini_gana = tk.Toplevel(root)
    ventana_gemini_gana.title("Gemini Gana")
    ventana_gemini_gana.geometry("600x500")
    ventana_gemini_gana.configure(bg='#e74c3c')
    ventana_gemini_gana.transient(root)
    ventana_gemini_gana.grab_set()
    
    frame_principal = tk.Frame(ventana_gemini_gana, bg='#e74c3c')
    frame_principal.pack(expand=True, fill='both', padx=30, pady=30)
    
    tk.Label(frame_principal, text="GEMINI GANA LA PARTIDA", 
            font=('Arial', 24, 'bold'), bg='#e74c3c', fg='white').pack(pady=15)
    
    tk.Label(frame_principal, 
            text=f"Marcador Final:\nGemini: {puntaje_gemini} pts\nTu: {puntaje_jugador} pts",
            font=('Arial', 18), bg='#e74c3c', fg='white', justify='center').pack(pady=20)
    
    tk.Label(frame_principal, 
            text="Quieres intentarlo de nuevo?",
            font=('Arial', 14), bg='#e74c3c', fg='white').pack(pady=15)
    
    frame_botones = tk.Frame(frame_principal, bg='#e74c3c')
    frame_botones.pack(pady=20)
    
    btn_reintentar = tk.Button(frame_botones, text="Reintentar Misma Dificultad",
                               font=fuente_categoria, bg='#27ae60', fg='white',
                               activebackground='#2ecc71', cursor='hand2',
                               padx=25, pady=15,
                               command=lambda: [ventana_gemini_gana.destroy(), 
                                               reiniciar_marcador(),
                                               iniciar_partida()])
    btn_reintentar.pack(pady=10)
    
    btn_cambiar = tk.Button(frame_botones, text="Cambiar Dificultad",
                           font=fuente_categoria, bg='#f39c12', fg='white',
                           activebackground='#e67e22', cursor='hand2',
                           padx=25, pady=15,
                           command=lambda: [ventana_gemini_gana.destroy(), 
                                           reiniciar_juego()])
    btn_cambiar.pack(pady=10)
    
    btn_salir = tk.Button(frame_botones, text="Salir del Juego",
                        font=fuente_normal, bg='#95a5a6', fg='white',
                        activebackground='#7f8c8d', cursor='hand2',
                        padx=25, pady=12,
                        command=root.quit)
    btn_salir.pack(pady=10)

def reiniciar_marcador():
    global puntaje_jugador, puntaje_gemini, ronda
    puntaje_jugador = 0
    puntaje_gemini = 0
    ronda = 0

def reiniciar_juego():
    global puntaje_jugador, puntaje_gemini, ronda
    puntaje_jugador = 0
    puntaje_gemini = 0
    ronda = 0
    mostrar_menu_dificultad()

def iniciar_juego(dif):
    global dificultad, categorias
    dificultad = dif
    categorias = categorias_por_dificultad[dificultad]
    iniciar_partida()

def iniciar_partida():
    global ronda, letra_actual, respuestas_jugador, respuestas_gemini
    global jugador_termino, gemini_termino, tiempo_inicio, tiempo_jugador, tiempo_gemini
    
    ronda += 1
    letra_actual = random.choice('ABCDEFGHILMNOPRSTUVWY')
    respuestas_jugador = {cat: "" for cat in categorias}
    respuestas_gemini = {}
    jugador_termino = False
    gemini_termino = False
    tiempo_inicio = time.time()
    tiempo_jugador = 0
    tiempo_gemini = 0
    
    construir_interfaz_competicion()
    threading.Thread(target=gemini_jugar, daemon=True).start()

def construir_interfaz_competicion():
    global campos_texto, labels_gemini, btn_stop
    
    for widget in root.winfo_children():
        widget.destroy()
    
    frame_principal = tk.Frame(root, bg='#f0f4f8')
    frame_principal.pack(expand=True, fill='both', padx=20, pady=20)
    
    frame_header = tk.Frame(frame_principal, bg='#e74c3c', relief='raised', bd=3)
    frame_header.pack(fill='x', pady=(0, 15))
    
    dif_texto = {
        "facil": "FACIL",
        "intermedio": "INTERMEDIO", 
        "crazy": "ARE YOU CRAZY?"
    }
    dif_color = {
        "facil": "#27ae60",
        "intermedio": "#f39c12",
        "crazy": "#e74c3c"
    }
    
    frame_header.configure(bg=dif_color[dificultad])
    
    tk.Label(frame_header, text=f"Ronda {ronda} - {dif_texto[dificultad]}", 
            font=fuente_categoria, bg=dif_color[dificultad], fg='white').pack(pady=5)
    tk.Label(frame_header, text=f"Letra: {letra_actual}", 
            font=('Arial', 32, 'bold'), bg=dif_color[dificultad], fg='white').pack(pady=10)
    tk.Label(frame_header, text=f"Marcador: Tu {puntaje_jugador} | Gemini {puntaje_gemini}",
            font=fuente_normal, bg=dif_color[dificultad], fg='white').pack(pady=5)
    
    tk.Label(frame_principal, 
            text="Gemini esta jugando en este momento - Apurate",
            font=fuente_categoria, bg='#f0f4f8', fg='#e74c3c').pack(pady=10)
    
    frame_columnas = tk.Frame(frame_principal, bg='#f0f4f8')
    frame_columnas.pack(fill='both', expand=True, pady=10)
    
    frame_jugador = tk.Frame(frame_columnas, bg='#3498db', relief='ridge', bd=3)
    frame_jugador.pack(side='left', fill='both', expand=True, padx=(0, 5))
    
    tk.Label(frame_jugador, text="TU", 
            font=fuente_categoria, bg='#3498db', fg='white').pack(pady=5)
    
    campos_texto = {}
    
    frame_campos = tk.Frame(frame_jugador, bg='#3498db')
    frame_campos.pack(fill='both', expand=True, padx=10, pady=10)
    
    for categoria in categorias:
        frame_cat = tk.Frame(frame_campos, bg='white', relief='groove', bd=2)
        frame_cat.pack(fill='x', pady=5)
        
        tk.Label(frame_cat, text=f"{categoria}:", 
                font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50',
                width=12, anchor='w').pack(side='left', padx=5, pady=8)
        
        entry = tk.Entry(frame_cat, font=fuente_normal, width=15,
                       relief='solid', bd=1)
        entry.pack(side='left', padx=5, pady=8, fill='x', expand=True)
        campos_texto[categoria] = entry
    
    frame_gemini_col = tk.Frame(frame_columnas, bg='#e74c3c', relief='ridge', bd=3)
    frame_gemini_col.pack(side='right', fill='both', expand=True, padx=(5, 0))
    
    tk.Label(frame_gemini_col, text="GEMINI", 
            font=fuente_categoria, bg='#e74c3c', fg='white').pack(pady=5)
    
    labels_gemini = {}
    
    frame_gemini_campos = tk.Frame(frame_gemini_col, bg='#e74c3c')
    frame_gemini_campos.pack(fill='both', expand=True, padx=10, pady=10)
    
    for categoria in categorias:
        frame_cat = tk.Frame(frame_gemini_campos, bg='white', relief='groove', bd=2)
        frame_cat.pack(fill='x', pady=5)
        
        tk.Label(frame_cat, text=f"{categoria}:", 
                font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50',
                width=12, anchor='w').pack(side='left', padx=5, pady=8)
        
        label = tk.Label(frame_cat, text="pensando...", 
                       font=fuente_normal, bg='#ecf0f1', fg='#95a5a6',
                       width=15, anchor='w')
        label.pack(side='left', padx=5, pady=8, fill='x', expand=True)
        labels_gemini[categoria] = label
    
    frame_botones = tk.Frame(frame_principal, bg='#f0f4f8')
    frame_botones.pack(pady=20)
    
    btn_stop = tk.Button(frame_botones, text="STOP",
                              font=('Arial', 18, 'bold'), bg='#e74c3c', fg='white',
                              activebackground='#c0392b', cursor='hand2',
                              padx=60, pady=20, command=jugador_presiona_stop)
    btn_stop.pack(side='left', padx=10)
    
    btn_rendirse = tk.Button(frame_botones, text="Rendirse",
                            font=fuente_normal, bg='#95a5a6', fg='white',
                            activebackground='#7f8c8d', cursor='hand2',
                            padx=20, pady=10, command=jugador_se_rinde)
    btn_rendirse.pack(side='left', padx=10)
    
    list(campos_texto.values())[0].focus()

def mostrar_menu_dificultad():
    for widget in root.winfo_children():
        widget.destroy()
    
    canvas = tk.Canvas(root, bg='#f0f4f8', highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    
    frame_principal = tk.Frame(canvas, bg='#f0f4f8')
    
    frame_principal.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=frame_principal, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    
    frame_contenido = tk.Frame(frame_principal, bg='#f0f4f8')
    frame_contenido.pack(padx=20, pady=20)
    
    titulo = tk.Label(frame_contenido, text="JUEGO STOP", 
                     font=fuente_titulo, bg='#f0f4f8', fg='#2c3e50')
    titulo.pack(pady=30)
    
    subtitulo = tk.Label(frame_contenido, 
                        text="MODO COMPETICION vs Gemini IA",
                        font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#e74c3c')
    subtitulo.pack(pady=10)
    
    desc = tk.Label(frame_contenido,
                   text="Compite contra Gemini en tiempo real\n"
                        "Ambos deben completar las categorias lo mas rapido posible\n"
                        "El primero en terminar presiona STOP",
                   font=fuente_normal, bg='#f0f4f8', fg='#7f8c8d')
    desc.pack(pady=15)
    
    tk.Label(frame_contenido, text="Selecciona tu dificultad:", 
            font=('Arial', 16, 'bold'), bg='#f0f4f8', fg='#2c3e50').pack(pady=20)
    
    frame_dificultades = tk.Frame(frame_contenido, bg='#f0f4f8')
    frame_dificultades.pack(pady=10)
    
    frame_facil = tk.Frame(frame_dificultades, bg='#27ae60', relief='raised', bd=3)
    frame_facil.pack(pady=10, padx=20, fill='x')
    
    tk.Label(frame_facil, text="FACIL", 
            font=('Arial', 16, 'bold'), bg='#27ae60', fg='white').pack(pady=5)
    tk.Label(frame_facil, text="3 categorias | IA lenta (8-12 seg)",
            font=fuente_normal, bg='#27ae60', fg='white').pack(pady=2)
    tk.Label(frame_facil, text="Categorias: Nombre, Animal, Pais",
            font=('Arial', 9), bg='#27ae60', fg='#ecf0f1').pack(pady=2)
    
    btn_facil = tk.Button(frame_facil, text="Jugar Facil",
                         font=fuente_categoria, bg='#2ecc71', fg='white',
                         activebackground='#27ae60', cursor='hand2',
                         padx=40, pady=10, 
                         command=lambda: iniciar_juego("facil"))
    btn_facil.pack(pady=10)
    
    frame_inter = tk.Frame(frame_dificultades, bg='#f39c12', relief='raised', bd=3)
    frame_inter.pack(pady=10, padx=20, fill='x')
    
    tk.Label(frame_inter, text="INTERMEDIO", 
            font=('Arial', 16, 'bold'), bg='#f39c12', fg='white').pack(pady=5)
    tk.Label(frame_inter, text="5 categorias | IA normal (5-8 seg)",
            font=fuente_normal, bg='#f39c12', fg='white').pack(pady=2)
    tk.Label(frame_inter, text="Categorias: Nombre, Animal, Pais, Fruta, Objeto",
            font=('Arial', 9), bg='#f39c12', fg='white').pack(pady=2)
    
    btn_inter = tk.Button(frame_inter, text="Jugar Intermedio",
                         font=fuente_categoria, bg='#e67e22', fg='white',
                         activebackground='#d68910', cursor='hand2',
                         padx=40, pady=10,
                         command=lambda: iniciar_juego("intermedio"))
    btn_inter.pack(pady=10)
    
    frame_crazy = tk.Frame(frame_dificultades, bg='#e74c3c', relief='raised', bd=3)
    frame_crazy.pack(pady=10, padx=20, fill='x')
    
    tk.Label(frame_crazy, text="TRYHARD", 
            font=('Arial', 16, 'bold'), bg='#e74c3c', fg='white').pack(pady=5)
    tk.Label(frame_crazy, text="8 categorias | IA RAPIDA (3-5 seg)",
            font=fuente_normal, bg='#e74c3c', fg='white').pack(pady=2)
    tk.Label(frame_crazy, text="Categorias: Nombre, Animal, Pais, Fruta, Objeto, Ciudad, Profesion, Marca",
            font=('Arial', 9), bg='#e74c3c', fg='white').pack(pady=2)
    
    btn_crazy = tk.Button(frame_crazy, text="MODO DIABLO",
                         font=fuente_categoria, bg='#c0392b', fg='white',
                         activebackground='#a93226', cursor='hand2',
                         padx=40, pady=10,
                         command=lambda: iniciar_juego("crazy"))
    btn_crazy.pack(pady=10)
    
    if ronda > 0:
        frame_marcador = tk.Frame(frame_principal, bg='#ecf0f1', relief='ridge', bd=2)
        frame_marcador.pack(pady=20, fill='x')
        
        tk.Label(frame_marcador, text=f"Marcador Global", 
                font=fuente_categoria, bg='#ecf0f1', fg='#2c3e50').pack(pady=5)
        tk.Label(frame_marcador, 
                text=f"Tu: {puntaje_jugador} pts | Gemini: {puntaje_gemini} pts | Rondas: {ronda}",
                font=fuente_normal, bg='#ecf0f1', fg='#16a085').pack(pady=5)

root = tk.Tk()
root.title("Juego STOP - vs la API de gemini")
root.geometry("500x750")
root.configure(bg='#f0f4f8')
root.resizable(True, False)

fuente_titulo = font.Font(family="Arial", size=24, weight="bold")
fuente_normal = font.Font(family="Arial", size=12)
fuente_categoria = font.Font(family="Arial", size=11, weight="bold")

mostrar_menu_dificultad()

root.mainloop()