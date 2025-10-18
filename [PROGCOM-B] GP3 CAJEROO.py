import json 
import os 
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

## inventario 
inventario = { 
    100000: 5, 
    50000: 4, 
    20000: 10, 
    10000: 10 
} 

ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cajero.json") 

## funcionamiento del cajero 
def cargar_inventario(): 
    if os.path.exists(ruta_archivo): 
        try: 
            with open(ruta_archivo, "r", encoding="utf-8") as f: 
                datos = json.load(f) 
                return {int(k): v for k, v in datos.items()} 
        except: 
            guardar_inventario(inventario) 
            return inventario.copy() 
    else: 
        guardar_inventario(inventario) 
        return inventario.copy() 

def guardar_inventario(inv): 
    try: 
        with open(ruta_archivo, "w", encoding="utf-8") as f: 
            json.dump(inv, f, indent=4, ensure_ascii=False) 
    except: 
        pass

def cajero_vacio(inv): 
    return all(cant == 0 for cant in inv.values()) 

def calcular_billetes(inv, monto): 
    temp = inv.copy() 
    entregar = {} 
    restante = monto 
 
    for den in sorted(temp.keys(), reverse=True): 
        if restante >= den and temp[den] > 0: 
            necesarios = restante // den 
            usar = min(necesarios, temp[den]) 
            if usar > 0: 
                entregar[den] = usar 
                restante -= usar * den 
 
    if restante == 0: 
        return entregar 
    else: 
        return None 

def retirar(inv, monto): 
    if monto <= 0: 
        return None, "Monto invalido. Debe ser mayor a $0"
 
    billetes = calcular_billetes(inv, monto) 
    if not billetes: 
        return None, "No se puede dispensar ese monto con los billetes disponibles"
 
    for den, cant in billetes.items(): 
        inv[den] -= cant 
 
    guardar_inventario(inv) 
    return billetes, None

## Variables globales para la interfaz
inventario_actual = cargar_inventario()
labels_inventario = {}

## Funciones de la interfaz
def actualizar_inventario_display():
    global inventario_actual, labels_inventario, btn_retirar
    
    for den, label in labels_inventario.items():
        cant = inventario_actual[den]
        color = '#27ae60' if cant > 0 else '#e74c3c'
        label.config(text=f"{cant} billetes disponibles", fg=color)
    
    if cajero_vacio(inventario_actual):
        btn_retirar.config(state=tk.DISABLED, bg='#999999')
        messagebox.showwarning("Cajero Vacio", 
                             "El cajero esta fuera de servicio.\n\nNo hay billetes disponibles.")
    else:
        btn_retirar.config(state=tk.NORMAL, bg='#EC0000')

def set_monto_rapido(monto):
    entry_monto.delete(0, tk.END)
    entry_monto.insert(0, str(monto))

def realizar_retiro():
    global inventario_actual
    
    try:
        monto_str = entry_monto.get().strip()
        if not monto_str:
            messagebox.showwarning("Advertencia", "Por favor ingrese un monto")
            return
        
        monto = int(monto_str)
        
        if cajero_vacio(inventario_actual):
            messagebox.showerror("Error", "Cajero fuera de servicio")
            return
        
        billetes, error = retirar(inventario_actual, monto)
        
        if error:
            messagebox.showerror("Error", error)
            return
        
        actualizar_inventario_display()
        
        resultado = f"RETIRO EXITOSO\n\n"
        resultado += f"Monto total: ${monto:,}\n"
        resultado += f"Hora: {datetime.now().strftime('%H:%M:%S')}\n\n"
        resultado += "Billetes entregados:\n"
        resultado += "-" * 40 + "\n"
        
        for den in sorted(billetes.keys(), reverse=True):
            resultado += f"  ${den:,} x {billetes[den]} = ${den * billetes[den]:,}\n"
        
        text_historial.config(state=tk.NORMAL)
        text_historial.delete(1.0, tk.END)
        text_historial.insert(1.0, resultado)
        text_historial.config(state=tk.DISABLED)
        
        entry_monto.delete(0, tk.END)
        
        messagebox.showinfo("Retiro Exitoso", 
                          f"Retiro de ${monto:,} procesado correctamente.\n\nPor favor retire su dinero.")
        
    except ValueError:
        messagebox.showerror("Error", "Monto invalido. Ingrese solo numeros.")

def limpiar():
    entry_monto.delete(0, tk.END)

def recargar_cajero():
    global inventario_actual, inventario
    
    respuesta = messagebox.askyesno("Recargar Cajero", 
                                    "Desea recargar el cajero al inventario inicial?\n\nEsto restaurara todas las denominaciones.")
    if respuesta:
        inventario_actual = inventario.copy()
        guardar_inventario(inventario_actual)
        actualizar_inventario_display()
        
        text_historial.config(state=tk.NORMAL)
        text_historial.delete(1.0, tk.END)
        text_historial.insert(1.0, "Cajero recargado exitosamente")
        text_historial.config(state=tk.DISABLED)
        
        messagebox.showinfo("Exito", "Cajero recargado correctamente")

def salir():
    respuesta = messagebox.askyesno("Salir", "Esta seguro que desea salir?")
    if respuesta:
        root.destroy()

## INTERFAZ GRAFICA
root = tk.Tk()
root.title("Cajero Automatico Santander")
root.configure(bg='#EC0000')
root.resizable(False, False)

# Centrar ventana
root.update_idletasks()
width = 800
height = 700
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Frame principal
main_frame = tk.Frame(root, bg='#EC0000')
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Header
header_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=3)
header_frame.pack(fill=tk.X, pady=(0, 15))

tk.Label(header_frame, text="CAJERO AUTOMATICO", 
        font=('Arial', 26, 'bold'), bg='white', fg='#EC0000').pack(pady=10)
tk.Label(header_frame, text="BANCO SANTANDER", 
        font=('Arial', 14), bg='white', fg='#333333').pack(pady=(0, 10))

# Frame de contenido
content_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=3)
content_frame.pack(fill=tk.BOTH, expand=True)

# SECCION INVENTARIO
inv_frame = tk.LabelFrame(content_frame, text="Inventario de Billetes", 
                          font=('Arial', 12, 'bold'), bg='white', fg='#EC0000',
                          relief=tk.GROOVE, bd=2)
inv_frame.pack(fill=tk.BOTH, padx=15, pady=10)

for i, den in enumerate(sorted(inventario_actual.keys(), reverse=True)):
    frame_bill = tk.Frame(inv_frame, bg='white')
    frame_bill.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(frame_bill, text=f"${den:,}", 
            font=('Arial', 11, 'bold'), bg='white', fg='#333333',
            width=15, anchor='w').pack(side=tk.LEFT)
    
    label_cant = tk.Label(frame_bill, text="", 
                         font=('Arial', 11), bg='white', fg='#666666')
    label_cant.pack(side=tk.LEFT)
    labels_inventario[den] = label_cant

# SECCION RETIRO
retiro_frame = tk.LabelFrame(content_frame, text="Realizar Retiro", 
                            font=('Arial', 12, 'bold'), bg='white', fg='#EC0000',
                            relief=tk.GROOVE, bd=2)
retiro_frame.pack(fill=tk.X, padx=15, pady=10)

# Input de monto
input_frame = tk.Frame(retiro_frame, bg='white')
input_frame.pack(pady=15)

tk.Label(input_frame, text="Monto a retirar:", 
        font=('Arial', 11, 'bold'), bg='white', fg='#333333').pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="$", 
        font=('Arial', 14, 'bold'), bg='white', fg='#EC0000').pack(side=tk.LEFT)

entry_monto = tk.Entry(input_frame, font=('Arial', 14), width=15,
                       relief=tk.SOLID, bd=2)
entry_monto.pack(side=tk.LEFT, padx=5)
entry_monto.bind('<Return>', lambda e: realizar_retiro())

# Botones rapidos
tk.Label(retiro_frame, text="Montos rapidos:", 
        font=('Arial', 10, 'bold'), bg='white', fg='#666666').pack(pady=(5, 10))

botones_frame = tk.Frame(retiro_frame, bg='white')
botones_frame.pack(pady=5)

montos_rapidos = [10000, 20000, 50000, 100000, 200000, 500000]
for i, monto in enumerate(montos_rapidos):
    btn = tk.Button(botones_frame, text=f"${monto//1000}k", 
                  font=('Arial', 10, 'bold'),
                  bg='#f0f0f0', fg='#333333',
                  width=8, height=1,
                  relief=tk.RAISED, bd=2,
                  command=lambda m=monto: set_monto_rapido(m))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)

# Botones principales
btn_frame = tk.Frame(retiro_frame, bg='white')
btn_frame.pack(pady=15)

btn_retirar = tk.Button(btn_frame, text="RETIRAR", 
                        font=('Arial', 12, 'bold'),
                        bg='#EC0000', fg='white',
                        width=15, height=2,
                        relief=tk.RAISED, bd=3,
                        command=realizar_retiro,
                        cursor='hand2')
btn_retirar.pack(side=tk.LEFT, padx=5)

tk.Button(btn_frame, text="LIMPIAR", 
         font=('Arial', 12, 'bold'),
         bg='#666666', fg='white',
         width=15, height=2,
         relief=tk.RAISED, bd=3,
         command=limpiar,
         cursor='hand2').pack(side=tk.LEFT, padx=5)

# SECCION HISTORIAL
historial_frame = tk.LabelFrame(content_frame, text="Ultimo Retiro", 
                               font=('Arial', 12, 'bold'), bg='white', fg='#EC0000',
                               relief=tk.GROOVE, bd=2)
historial_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

text_historial = tk.Text(historial_frame, height=6, width=70,
                         font=('Courier', 10), bg='#f9f9f9',
                         relief=tk.SUNKEN, bd=2, state=tk.DISABLED)
text_historial.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Footer
footer_frame = tk.Frame(main_frame, bg='#EC0000')
footer_frame.pack(fill=tk.X, pady=(10, 0))

tk.Button(footer_frame, text="Recargar Cajero", 
         font=('Arial', 10, 'bold'),
         bg='white', fg='#EC0000',
         relief=tk.RAISED, bd=2,
         command=recargar_cajero,
         cursor='hand2').pack(side=tk.LEFT, padx=5)

tk.Button(footer_frame, text="Salir", 
         font=('Arial', 10, 'bold'),
         bg='#333333', fg='white',
         relief=tk.RAISED, bd=2,
         command=salir,
         cursor='hand2').pack(side=tk.RIGHT, padx=5)


actualizar_inventario_display()


root.mainloop()
