import google.generativeai as genai
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
import threading

xd                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      "AIzaSyDgqykUgip0hmTH_MMuFjHi24m8z_yLufc"
password = ""
reglas = []
nivel = 0
max_nivel = 15
juego_activo = False
model = None
gemini_disponible = False

ventana = None
txt_password = None
txt_reglas = None
lbl_nivel = None
lbl_estado = None
btn_validar = None
btn_siguiente = None
btn_iniciar = None

def configurar_gemini():
    global model, gemini_disponible
    try:
        genai.configure(api_key=xd)
        model = genai.GenerativeModel('gemini-2.5-flash')
        gemini_disponible = True
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo configurar Gemini: {e}")
        return False

def generar_regla_con_gemini():
    if not gemini_disponible:
        return generar_regla_fallback()
    
    reglas_previas = "\n".join([f"{i+1}. {r['regla']}" for i, r in enumerate(reglas)])
    
    prompt = f"""Eres el creador de un juego de contraseñas progresivamente difícil llamado "The Password Game".

El jugador ya tiene estas reglas activas:
{reglas_previas if reglas_previas else "Ninguna (esta es la primera regla)"}

Tu tarea: Crear la regla #{nivel + 1} que sea:
- Más desafiante que las anteriores
- Creativa y original
- Validable programáticamente

Niveles de dificultad según el número:
- Reglas 1-3: Básicas (longitud, números, mayúsculas, símbolos)
- Reglas 4-7: Intermedias (sumas, palabras específicas, patrones)
- Reglas 8-12: Avanzadas (operaciones matemáticas, secuencias, prohibiciones)
- Reglas 13-15: LOCAS (condiciones múltiples, conflictos con reglas anteriores)

Responde SOLO con un JSON válido en este formato:
{{
    "regla": "Descripción de la regla en español",
    "tipo": "uno de: longitud, contenido, matematica, patron, prohibicion"
}}

Ejemplos de reglas según nivel (LO PUEDES USAR COMO EJEMPLO, recomiendo que hagas nuevas reglas para que no sean predecibles):
Nivel 1: "Tu contraseña debe tener al menos 8 caracteres"
Nivel 3: "Debe incluir al menos un número"
Nivel 5: "Los números en tu contraseña deben sumar 20"
Nivel 8: "Debe contener el nombre de un país"
Nivel 10: "No puede contener dos letras iguales consecutivas"
Nivel 13: "Debe incluir un número primo mayor a 10"

Genera ahora la regla #{nivel + 1}:"""

    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        
        if texto.startswith('```'):
            texto = texto[7:]
        if texto.startswith('```'):
            texto = texto[3:]
        if texto.endswith('```'):
            texto = texto[:-3]
        
        texto = texto.strip()
        regla_data = json.loads(texto)
        
        if "regla" not in regla_data:
            return generar_regla_fallback()
        
        return regla_data
        
    except Exception as e:
        return generar_regla_fallback()

def generar_regla_fallback():
    reglas_fallback = [
        {"regla": "Tu contraseña debe tener al menos 5 caracteres", "tipo": "longitud"},
        {"regla": "Debe incluir al menos un número", "tipo": "contenido"},
        {"regla": "Debe incluir al menos una letra mayúscula", "tipo": "contenido"},
        {"regla": "Debe incluir al menos un símbolo (!@#$%^&*)", "tipo": "contenido"},
        {"regla": "Los números deben sumar 15", "tipo": "matematica"},
        {"regla": "Debe contener la palabra 'dragon'", "tipo": "contenido"},
        {"regla": "Debe tener exactamente 3 vocales", "tipo": "patron"},
        {"regla": "No puede contener la letra 'e'", "tipo": "prohibicion"},
        {"regla": "Debe incluir el año actual (2025)", "tipo": "contenido"},
        {"regla": "Debe empezar con una letra mayúscula", "tipo": "patron"},
        {"regla": "Los números deben estar juntos (consecutivos)", "tipo": "patron"},
        {"regla": "Debe incluir un número primo", "tipo": "matematica"},
        {"regla": "No puede tener dos letras iguales seguidas", "tipo": "prohibicion"},
        {"regla": "Debe contener exactamente 2 símbolos", "tipo": "contenido"},
        {"regla": "La suma de los valores ASCII de las letras debe ser par", "tipo": "matematica"}
    ]
    
    if nivel < len(reglas_fallback):
        return reglas_fallback[nivel]
    else:
        return {"regla": "Debe contener al menos 20 caracteres", "tipo": "longitud"}

def validar_regla_con_gemini(pwd, regla_data):

    if not gemini_disponible:
        return True
    
    regla = regla_data["regla"]
    
    prompt = f"""Eres un validador estricto de contraseñas.

REGLA: {regla}
CONTRASEÑA: {pwd}

Valida si la contraseña cumple EXACTAMENTE con la regla especificada.

Responde ÚNICAMENTE con un JSON en este formato:
{{
    "cumple": true,
    "razon": "Explicación breve"
}}

O:

{{
    "cumple": false,
    "razon": "Explicación de por qué no cumple"
}}

NO agregues texto adicional, solo el JSON."""

    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        
 
        if texto.startswith('```json'):
            texto = texto[7:]
        if texto.startswith('```'):
            texto = texto[3:]
        if texto.endswith('```'):
            texto = texto[:-3]
        
        texto = texto.strip()
        resultado = json.loads(texto)
        
        return resultado.get("cumple", False)
        
    except Exception as e:
        print(f"Error al validar con Gemini: {e}")
        return False

def validar_password(pwd):
    errores = []
    
    for i, regla_data in enumerate(reglas):
        regla = regla_data["regla"]
        
        if not validar_regla_con_gemini(pwd, regla_data):
            mensaje_error = f"Regla {i+1} no cumplida: {regla}"
            errores.append((i+1, mensaje_error))
    
    return len(errores) == 0, errores

def actualizar_display():

    txt_reglas.config(state='normal')
    txt_reglas.delete(1.0, tk.END)
    
    lbl_nivel.config(text=f"Nivel: {nivel}/{max_nivel}")
    
# REGLAS ON LIVEEE
    for i, regla_data in enumerate(reglas):
        txt_reglas.insert(tk.END, f"○ {i+1}. {regla_data['regla']}\n")
    
    txt_reglas.config(state='disabled')

def validar_click():
    global password
    password = txt_password.get()
    
    if not password:
        lbl_estado.config(text="Ingresa una contraseña", foreground="orange")
        return
    
    # Deshabilitar botón mientras valida
    btn_validar.config(state='disabled', text="Validando....")
    lbl_estado.config(text="Validando contraseña...", foreground="blue")
    ventana.update()
    
    # Validar en un hilo separado
    thread = threading.Thread(target=validar_thread)
    thread.daemon = True
    thread.start()

def validar_thread():
    password = txt_password.get()
    
    #Displays THE PASSWOOOOOORD
    txt_reglas.config(state='normal')
    txt_reglas.delete(1.0, tk.END)
    
    todas_cumplen = True
    
    for i, regla_data in enumerate(reglas):
        cumple = validar_regla_con_gemini(password, regla_data)
        
        if not cumple:
            todas_cumplen = False
        
        simbolo = "✓" if cumple else "✗"
        color = "green" if cumple else "red"
        
        txt_reglas.insert(tk.END, f"{simbolo} {i+1}. {regla_data['regla']}\n", color)
    
    txt_reglas.tag_config("green", foreground="green")
    txt_reglas.tag_config("red", foreground="red")
    txt_reglas.config(state='disabled')
    
    # Valifacion de la contraseñaaaaaaa
    if todas_cumplen:
        lbl_estado.config(text="¡Contraseña válida! Haz clic en 'Siguiente Nivel'", foreground="green")
        btn_siguiente.config(state='normal')
        btn_validar.config(state='disabled', text="Validar Contraseña")
    else:
        lbl_estado.config(text="La contraseña no cumple todas las reglas", foreground="red")
        btn_validar.config(state='normal', text="Validar Contraseña")

def siguiente_nivel_thread():
    global nivel, juego_activo
    
    if nivel >= max_nivel:
        messagebox.showinfo("¡Felicidades! 🎉", 
                          f"¡HAS COMPLETADO EL JUEGO!\n\nTu contraseña final: {password}\nReglas completadas: {nivel}/{max_nivel}")
        reiniciar_juego()
        return
    
    lbl_estado.config(text="Generando nueva regla", foreground="blue")
    ventana.update()
    
    nueva_regla = generar_regla_con_gemini()
    reglas.append(nueva_regla)
    nivel += 1
    
    actualizar_display()
    
    lbl_estado.config(text=f"Nueva regla #{nivel} agregada. Modifica tu contraseña", foreground="blue")
    btn_siguiente.config(state='disabled')
    btn_validar.config(state='normal')

def siguiente_nivel():
    thread = threading.Thread(target=siguiente_nivel_thread)
    thread.daemon = True
    thread.start()

def iniciar_juego():
    global nivel, reglas, password, juego_activo
    
    if not configurar_gemini():
        return
    
    nivel = 0
    reglas = []
    password = ""
    juego_activo = True
    
    txt_password.delete(0, tk.END)
    txt_password.config(state='normal')
    
    btn_iniciar.config(state='disabled')
    btn_validar.config(state='normal')
    
    siguiente_nivel()

def reiniciar_juego():
    global nivel, reglas, password, juego_activo
    
    nivel = 0
    reglas = []
    password = ""
    juego_activo = False
    
    txt_password.delete(0, tk.END)
    txt_password.config(state='disabled')
    txt_reglas.config(state='normal')
    txt_reglas.delete(1.0, tk.END)
    txt_reglas.config(state='disabled')
    
    lbl_nivel.config(text=f"Nivel: 0/{max_nivel}")
    lbl_estado.config(text="Presiona 'Iniciar Juego' para comenzar", foreground="black")
    
    btn_iniciar.config(state='normal')
    btn_validar.config(state='disabled')
    btn_siguiente.config(state='disabled')

def Interfaz_del_juegooo():
    global ventana, txt_password, txt_reglas, lbl_nivel, lbl_estado, btn_validar, btn_siguiente, btn_iniciar
    
    ventana = tk.Tk()
    ventana.title("THE PASSWORD GAME - Powered by some AI from google lul")
    ventana.geometry("800x600")
    ventana.configure(bg="#1e1e1e")
    
    frame_titulo = tk.Frame(ventana, bg="#2d2d2d", pady=10)
    frame_titulo.pack(fill='x')
    
    tk.Label(frame_titulo, text="THE PASSWORD GAME", 
             font=("Arial", 20, "bold"), bg="#2d2d2d", fg="#00d4ff").pack()
    tk.Label(frame_titulo, text="Verifica y valida!!", 
             font=("Arial", 10), bg="#2d2d2d", fg="#888").pack()
    
    frame_nivel = tk.Frame(ventana, bg="#1e1e1e", pady=10)
    frame_nivel.pack(fill='x')
    
    lbl_nivel = tk.Label(frame_nivel, text=f"Nivel: 0/{max_nivel}", 
                        font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#ffcc00")
    lbl_nivel.pack()
    
    frame_reglas = tk.Frame(ventana, bg="#1e1e1e", padx=20, pady=10)
    frame_reglas.pack(fill='both', expand=True)
    
    tk.Label(frame_reglas, text="REGLAS ACTIVAS:", 
             font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white", anchor='w').pack(fill='x')
    
    txt_reglas = scrolledtext.ScrolledText(frame_reglas, height=12, 
                                           font=("Courier", 10), 
                                           bg="#2d2d2d", fg="white",
                                           state='disabled', wrap='word')
    txt_reglas.pack(fill='both', expand=True)
    
    frame_password = tk.Frame(ventana, bg="#1e1e1e", padx=20, pady=10)
    frame_password.pack(fill='x')
    
    tk.Label(frame_password, text="Tu contraseña:", 
             font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white").pack(anchor='w')
    
    txt_password = tk.Entry(frame_password, font=("Arial", 12), 
                           bg="#2d2d2d", fg="white", insertbackground="white",
                           state='disabled')
    txt_password.pack(fill='x', pady=5)
    
    frame_estado = tk.Frame(ventana, bg="#1e1e1e", padx=20)
    frame_estado.pack(fill='x')
    
    lbl_estado = tk.Label(frame_estado, text="Presiona 'Iniciar Juego' para comenzar", 
                         font=("Arial", 10), bg="#1e1e1e", fg="yellow")
    lbl_estado.pack(pady=5)
    
    frame_botones = tk.Frame(ventana, bg="#1e1e1e", pady=15)
    frame_botones.pack()
    
    btn_iniciar = tk.Button(frame_botones, text="Iniciar Juego", 
                           font=("Arial", 12, "bold"),
                           bg="#00aa00", fg="white", 
                           padx=20, pady=10,
                           command=iniciar_juego)
    btn_iniciar.pack(side='left', padx=5)
    
    btn_validar = tk.Button(frame_botones, text="Validar Contraseña", 
                           font=("Arial", 12, "bold"),
                           bg="#0066cc", fg="white", 
                           padx=20, pady=10,
                           state='disabled',
                           command=validar_click)
    btn_validar.pack(side='left', padx=5)
    
    btn_siguiente = tk.Button(frame_botones, text="Siguiente Nivel", 
                             font=("Arial", 12, "bold"),
                             bg="#ff8800", fg="white", 
                             padx=20, pady=10,
                             state='disabled',
                             command=siguiente_nivel)
    btn_siguiente.pack(side='left', padx=5)
    
    ventana.mainloop()

Interfaz_del_juegooo()
