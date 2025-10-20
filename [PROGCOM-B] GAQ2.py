import tkinter as tk
from tkinter import messagebox, scrolledtext
import google.generativeai as genai

api_key = ""
model = None
numero_secreto = ""
intentos = []
modo_inverso = False
numero_jugador = ""
intentos_gemini = []
historial_gemini = []

def configurar_gemini():
    global model
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error al configurar Gemini: {str(e)}")
        return False

def generar_numero_con_gemini():
    global numero_secreto, intentos
    if not model:
        if not configurar_gemini():
            return False
    
    prompt = """Genera un número secreto de exactamente 4 dígitos para el juego de picas y fijas.
    IMPORTANTE: 
    - Los 4 dígitos deben ser DIFERENTES entre sí
    - Responde ÚNICAMENTE con los 4 dígitos, sin espacios, sin explicaciones
    - Ejemplo de respuesta válida: 3851
    - NO incluyas texto adicional, solo el número"""
    
    try:
        response = model.generate_content(prompt)
        numero = response.text.strip()
        
        if len(numero) == 4 and numero.isdigit() and len(set(numero)) == 4:
            numero_secreto = numero
            intentos = []
            actualizar_historial()
            texto_estado.config(text="Gemini ha generado un nuevo numero secreto")
            return True
        else:
            texto_estado.config(text="Error: Gemini no genero un numero valido. Intenta de nuevo.")
            return False
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar numero con Gemini: {str(e)}")
        return False

def evaluar_con_gemini(intento):
    prompt = f"""Eres el juez del juego Picas y Fijas.
    Número secreto: {numero_secreto}
    Intento del jugador: {intento}
    
    Evalúa el intento siguiendo estas reglas:
    - FIJA: Un dígito está en la posición correcta
    - PICA: Un dígito existe en el número pero está en posición incorrecta
    
    Responde ÚNICAMENTE en este formato exacto:
    Fijas: X
    Picas: Y
    
    Donde X es el número de fijas e Y es el número de picas.
    NO agregues texto adicional."""
    
    try:
        response = model.generate_content(prompt)
        resultado = response.text.strip()
        
        fijas = 0
        picas = 0
        
        for linea in resultado.split('\n'):
            if 'Fijas:' in linea or 'fijas:' in linea:
                fijas = int(''.join(filter(str.isdigit, linea)))
            elif 'Picas:' in linea or 'picas:' in linea:
                picas = int(''.join(filter(str.isdigit, linea)))
        
        return fijas, picas
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al evaluar con Gemini: {str(e)}")
        return None, None

def gemini_adivina():
    if not model:
        return None
    
    contexto_intentos = ""
    if historial_gemini:
        contexto_intentos = "\n\nIntentos anteriores:\n"
        for intento in historial_gemini:
            contexto_intentos += f"Número: {intento['numero']}, Fijas: {intento['fijas']}, Picas: {intento['picas']}\n"
    
    prompt = f"""Estás jugando Picas y Fijas y debes ADIVINAR un número de 4 dígitos diferentes.
    
    Reglas:
    - FIJA: dígito correcto en posición correcta
    - PICA: dígito correcto pero en posición incorrecta
    
    {contexto_intentos}
    
    Basándote en los intentos anteriores (si los hay), genera tu siguiente intento.
    IMPORTANTE:
    - Debe ser un número de 4 dígitos DIFERENTES
    - Usa lógica deductiva basada en los resultados anteriores
    - Si es tu primer intento, elige un número aleatorio
    - Responde ÚNICAMENTE con los 4 dígitos, sin explicaciones
    - Ejemplo: 5732
    """
    
    try:
        response = model.generate_content(prompt)
        intento = response.text.strip()
        
        if len(intento) == 4 and intento.isdigit() and len(set(intento)) == 4:
            return intento
        else:
            return None
            
    except:
        return None

def evaluar_intento_jugador(intento):
    fijas = 0
    picas = 0
    
    for i in range(4):
        if intento[i] == numero_jugador[i]:
            fijas += 1
        elif intento[i] in numero_jugador:
            picas += 1
    
    return fijas, picas

def mostrar_instrucciones_normales():
    for widget in instrucciones_texto.winfo_children():
        widget.destroy()
    
    instrucciones = [
        "Fija: Digito correcto en posicion correcta",
        "Pica: Digito correcto en posicion incorrecta",
        "Ingresa 4 digitos diferentes",
        "Gemini genera y  el programa evalua el numero secreto"
    ]
    
    for inst in instrucciones:
        tk.Label(
            instrucciones_texto,
            text=inst,
            font=("Arial", 9),
            bg="#4a5568",
            fg="#e2e8f0",
            anchor="w"
        ).pack(padx=15, pady=2, anchor="w")
    
    tk.Label(instrucciones_texto, text="", bg="#4a5568").pack(pady=3)

def mostrar_instrucciones_inversas():
    for widget in instrucciones_texto.winfo_children():
        widget.destroy()
    
    instrucciones = [
        "Tu piensas un numero de 4 digitos diferentes",
        "Gemini intentara adivinarlo usando logica",
        "Ingresa tu numero secreto y confirmalo",
        "El programa evaluara automaticamente",
        "Gemini empezara a adivinar el numero hasta ganar"
    ]
    
    for inst in instrucciones:
        tk.Label(
            instrucciones_texto,
            text=inst,
            font=("Arial", 9),
            bg="#4a5568",
            fg="#e2e8f0",
            anchor="w"
        ).pack(padx=15, pady=2, anchor="w")
    
    tk.Label(instrucciones_texto, text="", bg="#4a5568").pack(pady=3)

def configurar_api():
    global api_key
    api_key = entrada_api.get().strip()
    
    if not api_key:
        messagebox.showwarning("Advertencia", "Por favor ingresa tu API Key de Gemini")
        return
    
    if configurar_gemini():
        texto_estado.config(
            text="API configurada. Elige un modo de juego",
            fg="#48bb78"
        )
        boton_modo_normal.config(state="normal")
        boton_modo_inverso.config(state="normal")
        messagebox.showinfo("Exito", "API de Gemini configurada correctamente")

def modo_normal():
    global modo_inverso
    modo_inverso = False
    inverso_frame.pack_forget()
    entrada_frame.pack(pady=15)
    mostrar_instrucciones_normales()
    historial_label.config(text="Historial de Intentos:")
    
    if generar_numero_con_gemini():
        entrada.config(state="normal")
        boton_intentar.config(state="normal")
        entrada.delete(0, tk.END)
        entrada.focus()

def modo_gemini_adivina():
    global modo_inverso, numero_jugador, historial_gemini, intentos_gemini
    modo_inverso = True
    entrada_frame.pack_forget()
    inverso_frame.pack(pady=15)
    mostrar_instrucciones_inversas()
    historial_label.config(text="Intentos de Gemini:")
    
    numero_jugador = ""
    historial_gemini = []
    intentos_gemini = []
    entrada_numero_secreto.config(state="normal")
    entrada_numero_secreto.delete(0, tk.END)
    boton_confirmar_numero.config(state="normal")
    boton_gemini_intenta.config(state="disabled")
    
    texto_estado.config(
        text="Ingresa tu numero secreto de 4 digitos diferentes \n (ADVERTENCIA: Si no tienes una buena PC puedes sufrir de bajones de rendimiento)",
        fg="#fbd38d" 
    )
    
    actualizar_historial()
    entrada_numero_secreto.focus()

def confirmar_numero_secreto():
    global numero_jugador, historial_gemini
    numero = entrada_numero_secreto.get().strip()
    
    if len(numero) != 4:
        messagebox.showwarning("Error", "Debes ingresar exactamente 4 digitos")
        return
    
    if not numero.isdigit():
        messagebox.showwarning("Error", "Solo se permiten numeros")
        return
    
    if len(set(numero)) != 4:
        messagebox.showwarning("Error", "Los 4 digitos deben ser diferentes")
        return
    
    numero_jugador = numero
    historial_gemini = []
    entrada_numero_secreto.config(state="disabled")
    boton_confirmar_numero.config(state="disabled")
    boton_gemini_intenta.config(state="disabled")
    
    texto_estado.config(
        text="Numero valido, que empieze el juego!",
        fg="#48bb78"
    )
    
    root.after(1000, proceso_automatico_gemini)

def gemini_hacer_intento():
    texto_estado.config(text="Gemini esta adivinando...")
    root.update()
    
    intento = gemini_adivina()
    
    if not intento:
        messagebox.showerror("Error", "Ocurrio un error en la API")
        return False
    
    fijas, picas = evaluar_intento_jugador(intento)
    
    historial_gemini.append({
        'numero': intento,
        'fijas': fijas,
        'picas': picas
    })
    
    actualizar_historial()
    
    if fijas == 4:
        texto_estado.config(
            text=f"Gemini adivino tu numero en {len(historial_gemini)} intentos",
            fg="#ed8936"
        )
        messagebox.showinfo(
            "Gemini Gano",
            f"Gemini adivino tu numero {numero_jugador} en {len(historial_gemini)} intentos\n\nLa IA es impresionante jeje"
        )
        return True
    else:
        texto_estado.config(
            text=f"Intento #{len(historial_gemini)} - Gemini continua adivinando...",
            fg="#fbd38d"
        )
        return False

def proceso_automatico_gemini():
    gano = gemini_hacer_intento()
    if not gano:
        root.after(1500, proceso_automatico_gemini)

def realizar_intento():
    intento = entrada.get().strip()
    
    if len(intento) != 4:
        messagebox.showwarning("Error", "Debes ingresar exactamente 4 digitos")
        return
    
    if not intento.isdigit():
        messagebox.showwarning("Error", "Solo se permiten numeros")
        return
    
    if len(set(intento)) != 4:
        messagebox.showwarning("Error", "Los 4 digitos deben ser diferentes")
        return
    
    texto_estado.config(text="Gemini esta evaluando tu adivinacion...")
    root.update()
    
    fijas, picas = evaluar_con_gemini(intento)
    
    if fijas is None or picas is None:
        return
    
    intentos.append({
        'numero': intento,
        'fijas': fijas,
        'picas': picas
    })
    
    actualizar_historial()
    
    if fijas == 4:
        texto_estado.config(
            text=f"GANASTE en {len(intentos)} intentos",
            fg="#48bb78"
        )
        messagebox.showinfo(
            "Felicitaciones",
            f"Adivinaste el numero {numero_secreto} en {len(intentos)} intentos\n\nFelicidades!"
        )
        entrada.config(state="disabled")
        boton_intentar.config(state="disabled")
    else:
        texto_estado.config(
            text=f"Intento #{len(intentos)} - Continua intentando",
            fg="#fbd38d"
        )
    
    entrada.delete(0, tk.END)
    entrada.focus()

def actualizar_historial():
    historial_texto.config(state="normal")
    historial_texto.delete(1.0, tk.END)
    
    if modo_inverso:
        if not historial_gemini:
            historial_texto.insert(tk.END, "Gemini aun no ha intentado adivinar.\n")
        else:
            historial_texto.insert(tk.END, "=" * 55 + "\n")
            for i, intento in enumerate(historial_gemini, 1):
                linea = f"#{i:2d} | Gemini intento: {intento['numero']} | "
                linea += f"Fijas: {intento['fijas']} | Picas: {intento['picas']}\n"
                historial_texto.insert(tk.END, linea)
            historial_texto.insert(tk.END, "=" * 55 + "\n")
    else:
        if not intentos:
            historial_texto.insert(tk.END, "Aun no hay intentos. Comienza a jugar\n")
        else:
            historial_texto.insert(tk.END, "=" * 55 + "\n")
            for i, intento in enumerate(intentos, 1):
                linea = f"#{i:2d} | Tu intento: {intento['numero']} | "
                linea += f"Fijas: {intento['fijas']} | Picas: {intento['picas']}\n"
                historial_texto.insert(tk.END, linea)
            historial_texto.insert(tk.END, "=" * 55 + "\n")
    
    historial_texto.config(state="disabled")
    historial_texto.see(tk.END)

### interfaz grafica ###

root = tk.Tk()
root.title("Picas y Fijas con API de gemini")
root.geometry("650x750")
root.configure(bg="#2d3748")
root.resizable(False, True)

titulo_frame = tk.Frame(root, bg="#2d3748")
titulo_frame.pack(pady=15)

titulo = tk.Label(
    titulo_frame,
    text="PICAS Y FIJAS",
    font=("Arial", 26, "bold"),
    bg="#2d3748",
    fg="white"
)
titulo.pack()

subtitulo = tk.Label(
    titulo_frame,
    text="Usando la API de Gemini.",
    font=("Arial", 11),
    bg="#2d3748",
    fg="#48bb78"
)
subtitulo.pack()

api_frame = tk.Frame(root, bg="#4a5568", relief="solid", bd=1)
api_frame.pack(pady=10, padx=20, fill=tk.X)

tk.Label(
    api_frame,
    text="Ponga la api key AQUI:",
    font=("Arial", 10, "bold"),
    bg="#4a5568",
    fg="white"
).pack(side=tk.LEFT, padx=10, pady=10)

entrada_api = tk.Entry(
    api_frame,
    font=("Arial", 10),
    width=30,
    show="*",
    bg="white"
)
entrada_api.pack(side=tk.LEFT, padx=5, pady=10)

boton_config = tk.Button(
    api_frame,
    text="Configurar",
    font=("Arial", 9, "bold"),
    bg="#48bb78",
    fg="white",
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2",
    command=configurar_api
)
boton_config.pack(side=tk.LEFT, padx=5, pady=10)

modo_frame = tk.Frame(root, bg="#2d3748")
modo_frame.pack(pady=10)

boton_modo_normal = tk.Button(
    modo_frame,
    text="Yo Adivino",
    font=("Arial", 11, "bold"),
    bg="#9f7aea",
    fg="white",
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2",
    command=modo_normal,
    state="disabled"
)
boton_modo_normal.pack(side=tk.LEFT, padx=5)

boton_modo_inverso = tk.Button(
    modo_frame,
    text="Gemini Adivina",
    font=("Arial", 11, "bold"),
    bg="#ed8936",
    fg="white",
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2",
    command=modo_gemini_adivina,
    state="disabled"
)
boton_modo_inverso.pack(side=tk.LEFT, padx=5)

texto_estado = tk.Label(
    root,
    text="La API la puedes conseguir PAGANDO tokens en Google AI studio",
    font=("Arial", 10),
    bg="#2d3748",
    fg="#fbd38d"
)
texto_estado.pack(pady=5)

entrada_frame = tk.Frame(root, bg="#2d3748")
entrada_frame.pack(pady=15)

entrada = tk.Entry(
    entrada_frame,
    font=("Arial", 24, "bold"),
    width=8,
    justify="center",
    bg="white",
    fg="#2d3748",
    relief="solid",
    bd=2,
    state="disabled"
)
entrada.pack(side=tk.LEFT, padx=5)
entrada.bind('<Return>', lambda e: realizar_intento())

boton_intentar = tk.Button(
    entrada_frame,
    text="Intentar",
    font=("Arial", 12, "bold"),
    bg="#4299e1",
    fg="white",
    padx=20,
    pady=10,
    relief="flat",
    cursor="hand2",
    command=realizar_intento,
    state="disabled"
)
boton_intentar.pack(side=tk.LEFT, padx=5)

inverso_frame = tk.Frame(root, bg="#2d3748")

tk.Label(
    inverso_frame,
    text="Ingresa tu numero secreto (4 digitos diferentes):",
    font=("Arial", 11),
    bg="#2d3748",
    fg="white"
).pack(pady=5)

entrada_inverso_frame = tk.Frame(inverso_frame, bg="#2d3748")
entrada_inverso_frame.pack(pady=5)

entrada_numero_secreto = tk.Entry(
    entrada_inverso_frame,
    font=("Arial", 20, "bold"),
    width=8,
    justify="center",
    bg="white",
    fg="#2d3748",
    relief="solid",
    bd=2
)
entrada_numero_secreto.pack(side=tk.LEFT, padx=5)

boton_confirmar_numero = tk.Button(
    entrada_inverso_frame,
    text="Confirmar",
    font=("Arial", 11, "bold"),
    bg="#48bb78",
    fg="white",
    padx=15,
    pady=8,
    relief="flat",
    cursor="hand2",
    command=confirmar_numero_secreto
)
boton_confirmar_numero.pack(side=tk.LEFT, padx=5)

boton_gemini_intenta = tk.Button(
    inverso_frame,
    text="Gemini comenzara automaticamente",
    font=("Arial", 11, "bold"),
    bg="#999999",
    fg="white",
    padx=20,
    pady=10,
    relief="flat",
    state="disabled"
)
boton_gemini_intenta.pack(pady=10)

instrucciones_frame = tk.Frame(root, bg="#4a5568", relief="solid", bd=1)
instrucciones_frame.pack(pady=10, padx=20, fill=tk.X)

tk.Label(
    instrucciones_frame,
    text="⚠️ Instrucciones:",
    font=("Arial", 10, "bold"),
    bg="#4a5568",
    fg="white",
    anchor="w"
).pack(pady=(8, 3), padx=10, anchor="w")

instrucciones_texto = tk.Frame(instrucciones_frame, bg="#4a5568")
instrucciones_texto.pack(fill=tk.X)

mostrar_instrucciones_normales()

historial_frame = tk.Frame(root, bg="#2d3748")
historial_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

historial_label = tk.Label(
    historial_frame,
    text="Historial de Intentos:",
    font=("Arial", 11, "bold"),
    bg="#2d3748",
    fg="white",
    anchor="w"
)
historial_label.pack(pady=(0, 5), anchor="w")

historial_texto = scrolledtext.ScrolledText(
    historial_frame,
    font=("Courier", 11),
    height=8,
    bg="#1a202c",
    fg="white",
    relief="solid",
    bd=1,
    state="disabled"
)
historial_texto.pack(fill=tk.BOTH, expand=True)

root.mainloop()