import json 
import os 
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

inventario = { 
    100000: 5, 
    50000: 4, 
    20000: 10, 
    10000: 10 
} 

ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cajero.json")
ruta_tarjetas = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarjetas.json")

class SistemaTarjetas:
    def __init__(self):
        self.tarjetas = self.cargar_tarjetas()
    
    def cargar_tarjetas(self):
        if os.path.exists(ruta_tarjetas):
            try:
                with open(ruta_tarjetas, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self.crear_tarjetas_iniciales()
        else:
            return self.crear_tarjetas_iniciales()
    
    def crear_tarjetas_iniciales(self):
        tarjetas = {
            "377768969964166": {
                "tipo": "American Express",
                "nombre": "Benjamin Salazar",
                "cvv": "3326",
                "expiry": "10/28",
                "pin": "1234",
                "saldo": 2500000,
                "intentos_fallidos": 0,
                "bloqueada": False
            },
            "4919863358399424": {
                "tipo": "Visa",
                "nombre": "Zoey Ramírez",
                "cvv": "900",
                "expiry": "10/27",
                "pin": "5678",
                "saldo": 1800000,
                "intentos_fallidos": 0,
                "bloqueada": False
            },
            "3518644647667217": {
                "tipo": "JCB",
                "nombre": "Jonathan Torres",
                "cvv": "395",
                "expiry": "10/27",
                "pin": "9012",
                "saldo": 950000,
                "intentos_fallidos": 0,
                "bloqueada": False
            },
            "3597235120349176": {
                "tipo": "JCB",
                "nombre": "Andres Morales",
                "cvv": "306",
                "expiry": "10/27",
                "pin": "3456",
                "saldo": 1200000,
                "intentos_fallidos": 0,
                "bloqueada": False
            },
            "4938720370786325": {
                "tipo": "Visa",
                "nombre": "Sofia Pérez",
                "cvv": "276",
                "expiry": "10/27",
                "pin": "7890",
                "saldo": 3200000,
                "intentos_fallidos": 0,
                "bloqueada": False
            },
            "5377359758756423": {
                "tipo": "MasterCard",
                "nombre": "Angel Arias",
                "cvv": "510",
                "expiry": "10/28",
                "pin": "1111",
                "saldo": 1500000,
                "intentos_fallidos": 0,
                "bloqueada": False
            }
        }
        self.guardar_tarjetas(tarjetas)
        return tarjetas
    
    def guardar_tarjetas(self, tarjetas=None):
        if tarjetas is None:
            tarjetas = self.tarjetas
        try:
            with open(ruta_tarjetas, "w", encoding="utf-8") as f:
                json.dump(tarjetas, f, indent=4, ensure_ascii=False)
        except:
            pass
    
    def obtener_lista_tarjetas(self):
        return [(num, info.get('nombre', 'Usuario'), info.get('tipo', 'Tarjeta'), info.get('bloqueada', False)) 
                for num, info in self.tarjetas.items()]
    
    def validar_tarjeta(self, numero_tarjeta):
        return numero_tarjeta in self.tarjetas
    
    def validar_pin(self, numero_tarjeta, pin):
        if numero_tarjeta not in self.tarjetas:
            return False, "Tarjeta no válida"
        
        tarjeta = self.tarjetas[numero_tarjeta]
        
        if tarjeta["bloqueada"]:
            return False, "Tarjeta bloqueada. Contacte a su banco"
        
        if tarjeta["pin"] == pin:
            tarjeta["intentos_fallidos"] = 0
            self.guardar_tarjetas()
            return True, "Pin correcto"
        else:
            tarjeta["intentos_fallidos"] += 1
            
            if tarjeta["intentos_fallidos"] >= 3:
                tarjeta["bloqueada"] = True
                self.guardar_tarjetas()
                return False, "Tarjeta bloqueada por 3 intentos fallidos"
            
            intentos_restantes = 3 - tarjeta["intentos_fallidos"]
            self.guardar_tarjetas()
            return False, f"Pin incorrecto. Intentos restantes: {intentos_restantes}"
    
    def obtener_saldo(self, numero_tarjeta):
        if numero_tarjeta in self.tarjetas:
            return self.tarjetas[numero_tarjeta]["saldo"]
        return 0
    
    def descontar_saldo(self, numero_tarjeta, monto):
        if numero_tarjeta in self.tarjetas:
            tarjeta = self.tarjetas[numero_tarjeta]
            if tarjeta["saldo"] >= monto:
                tarjeta["saldo"] -= monto
                self.guardar_tarjetas()
                return True, tarjeta["saldo"]
            else:
                return False, "Saldo insuficiente"
        return False, "Tarjeta no válida"
    
    def obtener_info(self, numero_tarjeta):
        if numero_tarjeta in self.tarjetas:
            return self.tarjetas[numero_tarjeta]
        return None
    
    def consignar_saldo(self, numero_tarjeta, monto):
        if numero_tarjeta in self.tarjetas:
            self.tarjetas[numero_tarjeta]["saldo"] += monto
            self.guardar_tarjetas()
            return True, self.tarjetas[numero_tarjeta]["saldo"]
        return False, "Tarjeta no válida"
    
    def buscar_tarjeta_por_nombre(self, nombre):
        nombre_lower = nombre.lower().strip()
        for num, info in self.tarjetas.items():
            if info['nombre'].lower() == nombre_lower:
                return num, info
        return None, None
    
    def transferir_saldo(self, num_origen, num_destino, monto):
        if num_origen not in self.tarjetas or num_destino not in self.tarjetas:
            return False, "Tarjeta no válida"
        
        tarjeta_origen = self.tarjetas[num_origen]
        
        if tarjeta_origen["saldo"] < monto:
            return False, "Saldo insuficiente"
        
        tarjeta_origen["saldo"] -= monto
        self.tarjetas[num_destino]["saldo"] += monto
        self.guardar_tarjetas()
        
        return True, tarjeta_origen["saldo"]
    
    def cambiar_pin(self, numero_tarjeta, pin_actual, pin_nuevo):
        if numero_tarjeta not in self.tarjetas:
            return False, "Tarjeta no válida"
        
        tarjeta = self.tarjetas[numero_tarjeta]
        
        if tarjeta["pin"] != pin_actual:
            return False, "PIN actual incorrecto"
        
        if len(pin_nuevo) < 4:
            return False, "El nuevo PIN debe tener al menos 4 dígitos"
        
        tarjeta["pin"] = pin_nuevo
        self.guardar_tarjetas()
        return True, "PIN cambiado exitosamente"

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
        return None, "no pues, no son billetes imaginarios"
 
    billetes = calcular_billetes(inv, monto) 
    if not billetes: 
        return None, "No se puede dispensar ese monto con los billetes disponibles"
 
    for den, cant in billetes.items(): 
        inv[den] -= cant 
 
    guardar_inventario(inv) 
    return billetes, None

inventario_actual = cargar_inventario()
sistema_tarjetas = SistemaTarjetas()
tarjeta_actual = None
sesion_activa = False

class VentanaLogin:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Acceso al Cajero")
        self.window.configure(bg='#EC0000')
        self.window.resizable(False, False)
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'acd662d8d6bbadc5f028dfb394db087b-Photoroom.ico')
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except Exception:
            pass
        
        width = 550
        height = 650
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.resultado = None
        self.tarjeta_seleccionada = None
        self.crear_interfaz()
    
    def formatear_numero_tarjeta(self, numero):
        return f"{numero[:4]}-{numero[4:8]}-{numero[8:12]}-{numero[12:]}"
    
    def crear_interfaz(self):
        main_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, bd=5)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="BANCO SANTANDER", 
                font=('Arial', 20, 'bold'), bg='white', fg='#EC0000').pack(pady=(20, 5))
        tk.Label(main_frame, text="Seleccione su tarjeta", 
                font=('Arial', 12), bg='white', fg='#666666').pack(pady=(0, 15))
        
        seleccion_frame = tk.LabelFrame(main_frame, text="Tarjetas Disponibles", 
                                        font=('Arial', 11, 'bold'), bg='white', 
                                        fg='#EC0000', relief=tk.GROOVE, bd=2)
        seleccion_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        canvas_frame = tk.Frame(seleccion_frame, bg='white')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(canvas_frame, bg='white', yscrollcommand=scrollbar.set, 
                          highlightthickness=0, height=300)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=canvas.yview)
        
        tarjetas_container = tk.Frame(canvas, bg='white')
        canvas_window = canvas.create_window((0, 0), window=tarjetas_container, anchor='nw')
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        tarjetas_container.bind('<Configure>', on_frame_configure)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        lista_tarjetas = sistema_tarjetas.obtener_lista_tarjetas()
        self.var_tarjeta = tk.StringVar()
        
        colores_tipo = {
            "Visa": "#1A1F71",
            "MasterCard": "#EB001B",
            "American Express": "#006FCF",
            "JCB": "#0E4C96"
        }
        
        for i, (numero, nombre, tipo, bloqueada) in enumerate(lista_tarjetas):
            frame_tarjeta = tk.Frame(tarjetas_container, bg='white', relief=tk.SOLID, bd=1)
            frame_tarjeta.pack(fill=tk.X, padx=5, pady=6)
            
            color_estado = '#e74c3c' if bloqueada else '#27ae60'
            estado_texto = 'BLOQUEADA' if bloqueada else 'ACTIVA'
            estado = 'disabled' if bloqueada else 'normal'
            
            radio = tk.Radiobutton(frame_tarjeta, 
                                  variable=self.var_tarjeta,
                                  value=numero,
                                  bg='white',
                                  state=estado,
                                  command=self.on_tarjeta_seleccionada)
            radio.pack(side=tk.LEFT, padx=8, pady=10)
            
            info_frame = tk.Frame(frame_tarjeta, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)
            
            nombre_frame = tk.Frame(info_frame, bg='white')
            nombre_frame.pack(fill=tk.X)
            
            tk.Label(nombre_frame, text=nombre, 
                    font=('Arial', 11, 'bold'), bg='white', fg='#333333',
                    anchor='w').pack(side=tk.LEFT)
            
            color_tipo = colores_tipo.get(tipo, '#666666')
            tk.Label(nombre_frame, text=f"  {tipo}", 
                    font=('Arial', 9, 'bold'), bg='white', fg=color_tipo,
                    anchor='w').pack(side=tk.LEFT)
            
            tk.Label(info_frame, text=self.formatear_numero_tarjeta(numero), 
                    font=('Arial', 9), bg='white', fg='#666666',
                    anchor='w').pack(fill=tk.X)
            
            tk.Label(frame_tarjeta, text=estado_texto, 
                    font=('Arial', 9, 'bold'), bg='white', fg=color_estado,
                    width=10).pack(side=tk.RIGHT, padx=10)
        
        pin_frame = tk.Frame(main_frame, bg='white')
        pin_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        tk.Label(pin_frame, text="PIN:", 
                font=('Arial', 11, 'bold'), bg='white', fg='#333333').pack(side=tk.LEFT, padx=5)
        
        self.entry_pin = tk.Entry(pin_frame, font=('Arial', 12), width=15,
                                  relief=tk.SOLID, bd=2, show='*', justify='center',
                                  state='disabled')
        self.entry_pin.pack(side=tk.LEFT, padx=5)
        self.entry_pin.bind('<Return>', lambda e: self.validar_acceso())
        
        info_frame = tk.Frame(main_frame, bg='#f9f9f9', relief=tk.GROOVE, bd=1)
        info_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        tk.Label(info_frame, text="💡 por si algo los pins estan en el json xd", 
                font=('Arial', 8), bg='#f9f9f9', fg='#666666').pack(pady=5)
        
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=15)
        
        self.btn_ingresar = tk.Button(btn_frame, text="INGRESAR", 
                 font=('Arial', 12, 'bold'),
                 bg='#EC0000', fg='white',
                 width=12, height=2,
                 relief=tk.RAISED, bd=3,
                 command=self.validar_acceso,
                 cursor='hand2',
                 state='disabled')
        self.btn_ingresar.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="CANCELAR", 
                 font=('Arial', 12, 'bold'),
                 bg='#666666', fg='white',
                 width=12, height=2,
                 relief=tk.RAISED, bd=3,
                 command=self.cancelar,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def on_tarjeta_seleccionada(self):
        self.tarjeta_seleccionada = self.var_tarjeta.get()
        if self.tarjeta_seleccionada:
            self.entry_pin.config(state='normal')
            self.btn_ingresar.config(state='normal')
            self.entry_pin.focus()
    
    def validar_acceso(self):
        if not self.tarjeta_seleccionada:
            messagebox.showwarning("Advertencia", "Seleccione una tarjeta")
            return
        
        pin = self.entry_pin.get().strip()
        
        if not pin:
            messagebox.showwarning("Advertencia", "Ingrese su PIN")
            return
        
        valido, mensaje = sistema_tarjetas.validar_pin(self.tarjeta_seleccionada, pin)
        
        if valido:
            self.resultado = self.tarjeta_seleccionada
            self.window.destroy()
        else:
            messagebox.showerror("Error", mensaje)
            self.entry_pin.delete(0, tk.END)
            
            info = sistema_tarjetas.obtener_info(self.tarjeta_seleccionada)
            if info and info["bloqueada"]:
                self.window.after(2000, self.window.destroy)
    
    def cancelar(self):
        self.window.destroy()
    
    def mostrar(self):
        self.window.mainloop()
        return self.resultado

def crear_interfaz_cajero(numero_tarjeta):
    global tarjeta_actual, sesion_activa, inventario_actual
    
    tarjeta_actual = numero_tarjeta
    sesion_activa = True
    info_tarjeta = sistema_tarjetas.obtener_info(numero_tarjeta)
    
    root = tk.Tk()
    root.title("Cajero Santander")
    root.configure(bg='#EC0000')
    root.resizable(False, False)
    
    width = 900
    height = 800
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    labels_inventario = {}
    
    def actualizar_inventario_display():
        for den, label in labels_inventario.items():
            cant = inventario_actual[den]
            color = '#27ae60' if cant > 0 else '#e74c3c'
            label.config(text=f"{cant} billetes", fg=color)
        
        if cajero_vacio(inventario_actual):
            btn_retirar.config(state=tk.DISABLED, bg='#999999')
        else:
            btn_retirar.config(state=tk.NORMAL, bg='#EC0000')
    
    def actualizar_saldo_display():
        saldo_actual = sistema_tarjetas.obtener_saldo(tarjeta_actual)
        label_saldo.config(text=f"${saldo_actual:,}")
    
    def set_monto_rapido(monto):
        entry_monto.delete(0, tk.END)
        entry_monto.insert(0, str(monto))
    
    def realizar_retiro():
        try:
            monto_str = entry_monto.get().strip()
            if not monto_str:
                messagebox.showwarning("Advertencia", "Por favor ingrese un monto")
                return
            
            monto = int(monto_str)
            
            if cajero_vacio(inventario_actual):
                messagebox.showerror("Error", "Cajero fuera de servicio")
                return
            
            saldo_actual = sistema_tarjetas.obtener_saldo(tarjeta_actual)
            if monto > saldo_actual:
                messagebox.showerror("Error", f"Saldo insuficiente.\nSaldo disponible: ${saldo_actual:,}")
                return
            
            billetes, error = retirar(inventario_actual, monto)
            
            if error:
                messagebox.showerror("Error", error)
                return
            
            exito, resultado = sistema_tarjetas.descontar_saldo(tarjeta_actual, monto)
            
            if not exito:
                messagebox.showerror("Error", resultado)
                return
            
            actualizar_inventario_display()
            actualizar_saldo_display()
            
            resultado_texto = f"RETIRO EXITOSO\n\n"
            resultado_texto += f"Titular: {info_tarjeta['nombre']}\n"
            resultado_texto += f"Tarjeta: {info_tarjeta['tipo']}\n"
            resultado_texto += f"Monto total: ${monto:,}\n"
            resultado_texto += f"Saldo restante: ${resultado:,}\n"
            resultado_texto += f"Hora: {datetime.now().strftime('%H:%M:%S')}\n\n"
            resultado_texto += "Billetes entregados:\n"
            resultado_texto += "-" * 40 + "\n"
            
            for den in sorted(billetes.keys(), reverse=True):
                resultado_texto += f"  ${den:,} x {billetes[den]} = ${den * billetes[den]:,}\n"
            
            text_historial.config(state=tk.NORMAL)
            text_historial.delete(1.0, tk.END)
            text_historial.insert(1.0, resultado_texto)
            text_historial.config(state=tk.DISABLED)
            
            entry_monto.delete(0, tk.END)
            
            messagebox.showinfo("Retiro Exitoso", 
                              f"Retiro de ${monto:,} procesado correctamente.\n\nPor favor retire su dinero.")
            
        except ValueError:
            messagebox.showerror("Error", "Monto invalido. Ingrese solo numeros.")
    
    def limpiar():
        entry_monto.delete(0, tk.END)
    
    def consultar_saldo():
        saldo = sistema_tarjetas.obtener_saldo(tarjeta_actual)
        messagebox.showinfo("Consulta de Saldo", 
                          f"Titular: {info_tarjeta['nombre']}\nTarjeta: {info_tarjeta['tipo']}\n\nSaldo disponible: ${saldo:,}")
    
    def consignar_dinero():
        ventana_consignar = tk.Toplevel(root)
        ventana_consignar.title("Consignar Dinero")
        ventana_consignar.configure(bg='white')
        ventana_consignar.resizable(False, False)
        ventana_consignar.geometry('400x250')
        
        x = root.winfo_x() + (root.winfo_width() // 2) - 200
        y = root.winfo_y() + (root.winfo_height() // 2) - 125
        ventana_consignar.geometry(f'+{x}+{y}')
        
        tk.Label(ventana_consignar, text="Consignar Dinero a su Cuenta", 
                font=('Arial', 14, 'bold'), bg='white', fg='#EC0000').pack(pady=20)
        
        frame_monto = tk.Frame(ventana_consignar, bg='white')
        frame_monto.pack(pady=15)
        
        tk.Label(frame_monto, text="Monto a consignar:", 
                font=('Arial', 11), bg='white', fg='#333333').pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_monto, text="$", 
                font=('Arial', 12, 'bold'), bg='white', fg='#EC0000').pack(side=tk.LEFT)
        
        entry_monto_consignar = tk.Entry(frame_monto, font=('Arial', 12), width=15, relief=tk.SOLID, bd=2)
        entry_monto_consignar.pack(side=tk.LEFT, padx=5)
        entry_monto_consignar.focus()
        
        def procesar_consignacion():
            try:
                monto = int(entry_monto_consignar.get().strip())
                
                if monto <= 0:
                    messagebox.showerror("Error", "Ingrese un monto válido mayor a $0")
                    return
                
                exito, nuevo_saldo = sistema_tarjetas.consignar_saldo(tarjeta_actual, monto)
                
                if exito:
                    actualizar_saldo_display()
                    messagebox.showinfo("Éxito", f"Consignación exitosa de ${monto:,}\n\nNuevo saldo: ${nuevo_saldo:,}")
                    ventana_consignar.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo procesar la consignación")
                    
            except ValueError:
                messagebox.showerror("Error", "Ingrese solo números")
        
        tk.Button(ventana_consignar, text="CONSIGNAR", 
                 font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                 width=15, height=2, relief=tk.RAISED, bd=3,
                 command=procesar_consignacion, cursor='hand2').pack(pady=10)
        
        tk.Button(ventana_consignar, text="CANCELAR", 
                 font=('Arial', 11, 'bold'), bg='#666666', fg='white',
                 width=15, height=2, relief=tk.RAISED, bd=3,
                 command=ventana_consignar.destroy, cursor='hand2').pack()
    
    def transferir_dinero():
        ventana_transferir = tk.Toplevel(root)
        ventana_transferir.title("Transferir Dinero")
        ventana_transferir.configure(bg='white')
        ventana_transferir.resizable(False, False)
        ventana_transferir.geometry('450x300')
        
        x = root.winfo_x() + (root.winfo_width() // 2) - 225
        y = root.winfo_y() + (root.winfo_height() // 2) - 150
        ventana_transferir.geometry(f'+{x}+{y}')
        
        tk.Label(ventana_transferir, text="Transferir a Otra Persona", 
                font=('Arial', 14, 'bold'), bg='white', fg='#EC0000').pack(pady=20)
        
        frame_nombre = tk.Frame(ventana_transferir, bg='white')
        frame_nombre.pack(pady=10)
        
        tk.Label(frame_nombre, text="Nombre del destinatario:", 
                font=('Arial', 11), bg='white', fg='#333333').pack(side=tk.LEFT, padx=5)
        
        entry_nombre_dest = tk.Entry(frame_nombre, font=('Arial', 11), width=20, relief=tk.SOLID, bd=2)
        entry_nombre_dest.pack(side=tk.LEFT, padx=5)
        entry_nombre_dest.focus()
        
        frame_monto = tk.Frame(ventana_transferir, bg='white')
        frame_monto.pack(pady=10)
        
        tk.Label(frame_monto, text="Monto a transferir:", 
                font=('Arial', 11), bg='white', fg='#333333').pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_monto, text="$", 
                font=('Arial', 12, 'bold'), bg='white', fg='#EC0000').pack(side=tk.LEFT)
        
        entry_monto_transfer = tk.Entry(frame_monto, font=('Arial', 12), width=15, relief=tk.SOLID, bd=2)
        entry_monto_transfer.pack(side=tk.LEFT, padx=5)
        
        def procesar_transferencia():
            try:
                nombre_dest = entry_nombre_dest.get().strip()
                monto = int(entry_monto_transfer.get().strip())
                
                if not nombre_dest:
                    messagebox.showerror("Error", "Ingrese el nombre del destinatario")
                    return
                
                if monto <= 0:
                    messagebox.showerror("Error", "Ingrese un monto válido mayor a $0")
                    return
                
                num_destino, info_destino = sistema_tarjetas.buscar_tarjeta_por_nombre(nombre_dest)
                
                if not num_destino:
                    messagebox.showerror("Error", f"No se encontró ningún usuario con el nombre:\n{nombre_dest}")
                    return
                
                if num_destino == tarjeta_actual:
                    messagebox.showerror("Error", "No puede transferirse a sí mismo")
                    return
                
                saldo_actual = sistema_tarjetas.obtener_saldo(tarjeta_actual)
                if monto > saldo_actual:
                    messagebox.showerror("Error", f"Saldo insuficiente\nSaldo disponible: ${saldo_actual:,}")
                    return
                
                exito, nuevo_saldo = sistema_tarjetas.transferir_saldo(tarjeta_actual, num_destino, monto)
                
                if exito:
                    actualizar_saldo_display()
                    messagebox.showinfo("Éxito", 
                                      f"Transferencia exitosa\n\n"
                                      f"Destinatario: {info_destino['nombre']}\n"
                                      f"Monto: ${monto:,}\n\n"
                                      f"Nuevo saldo: ${nuevo_saldo:,}")
                    ventana_transferir.destroy()
                else:
                    messagebox.showerror("Error", nuevo_saldo)
                    
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")
        
        tk.Button(ventana_transferir, text="TRANSFERIR", 
                 font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                 width=15, height=2, relief=tk.RAISED, bd=3,
                 command=procesar_transferencia, cursor='hand2').pack(pady=15)
        
        tk.Button(ventana_transferir, text="CANCELAR", 
                 font=('Arial', 11, 'bold'), bg='#666666', fg='white',
                 width=15, height=2, relief=tk.RAISED, bd=3,
                 command=ventana_transferir.destroy, cursor='hand2').pack()
    
    def cambiar_contrasena():
        ventana_cambio = tk.Toplevel(root)
        ventana_cambio.title("Cambiar Contraseña")
        ventana_cambio.configure(bg='white')
        ventana_cambio.resizable(False, False)
        ventana_cambio.geometry('400x300')
        
        x = root.winfo_x() + (root.winfo_width() // 2) - 200
        y = root.winfo_y() + (root.winfo_height() // 2) - 150
        ventana_cambio.geometry(f'+{x}+{y}')
        
        tk.Label(ventana_cambio, text="Cambiar PIN", 
                font=('Arial', 14, 'bold'), bg='white', fg='#EC0000').pack(pady=20)
        
        frame_actual = tk.Frame(ventana_cambio, bg='white')
        frame_actual.pack(pady=10)
        
        tk.Label(frame_actual, text="PIN actual:", 
                font=('Arial', 11), bg='white', fg='#333333', width=15, anchor='e').pack(side=tk.LEFT, padx=5)
        
        entry_pin_actual = tk.Entry(frame_actual, font=('Arial', 12), width=15, 
                                    relief=tk.SOLID, bd=2, show='*', justify='center')
        entry_pin_actual.pack(side=tk.LEFT, padx=5)
        entry_pin_actual.focus()
        
        frame_nuevo = tk.Frame(ventana_cambio, bg='white')
        frame_nuevo.pack(pady=10)
        
        tk.Label(frame_nuevo, text="PIN nuevo:", 
                font=('Arial', 11), bg='white', fg='#333333', width=15, anchor='e').pack(side=tk.LEFT, padx=5)
        
        entry_pin_nuevo = tk.Entry(frame_nuevo, font=('Arial', 12), width=15, 
                                   relief=tk.SOLID, bd=2, show='*', justify='center')
        entry_pin_nuevo.pack(side=tk.LEFT, padx=5)
        
        frame_confirmar = tk.Frame(ventana_cambio, bg='white')
        frame_confirmar.pack(pady=10)
        
        tk.Label(frame_confirmar, text="Confirmar PIN:", 
                font=('Arial', 11), bg='white', fg='#333333', width=15, anchor='e').pack(side=tk.LEFT, padx=5)
        
        entry_pin_confirmar = tk.Entry(frame_confirmar, font=('Arial', 12), width=15, 
                                       relief=tk.SOLID, bd=2, show='*', justify='center')
        entry_pin_confirmar.pack(side=tk.LEFT, padx=5)
        
        def procesar_cambio():
            pin_actual = entry_pin_actual.get().strip()
            pin_nuevo = entry_pin_nuevo.get().strip()
            pin_confirmar = entry_pin_confirmar.get().strip()
            
            if not pin_actual or not pin_nuevo or not pin_confirmar:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            if pin_nuevo != pin_confirmar:
                messagebox.showerror("Error", "Los nuevos PINs no coinciden")
                return
            
            if len(pin_nuevo) < 4:
                messagebox.showerror("Error", "El nuevo PIN debe tener al menos 4 dígitos")
                return
            
            exito, mensaje = sistema_tarjetas.cambiar_pin(tarjeta_actual, pin_actual, pin_nuevo)
            
            if exito:
                messagebox.showinfo("Éxito", "PIN cambiado correctamente")
                ventana_cambio.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        
        tk.Button(ventana_cambio, text="CAMBIAR PIN", 
                 font=('Arial', 11, 'bold'), bg='#f39c12', fg='white',
                 width=15, height=2, relief=tk.RAISED, bd=3,
                 command=procesar_cambio, cursor='hand2').pack(pady=15)
        
        tk.Button(ventana_cambio, text="CANCELAR", 
                 font=('Arial', 11, 'bold'), bg='#666666', fg='white',
                 width=15, height=2, relief=tk.RAISED, bd=3,
                 command=ventana_cambio.destroy, cursor='hand2').pack()
    
    def salir():
        respuesta = messagebox.askyesno("Salir", "¿Desea finalizar la sesión?")
        if respuesta:
            global sesion_activa
            sesion_activa = False
            root.destroy()
    
    main_frame = tk.Frame(root, bg='#EC0000')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    header_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=3)
    header_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(header_frame, text="BANCO SANTANDER", 
            font=('Arial', 26, 'bold'), bg='white', fg='#EC0000').pack(pady=10)
    
    user_info_frame = tk.Frame(header_frame, bg='white')
    user_info_frame.pack(pady=(0, 10))
    
    tk.Label(user_info_frame, text=f"Bienvenido/a: {info_tarjeta['nombre']}", 
            font=('Arial', 12, 'bold'), bg='white', fg='#333333').pack()
    tk.Label(user_info_frame, text=f"{info_tarjeta['tipo']}", 
            font=('Arial', 10), bg='white', fg='#666666').pack()
    
    content_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=3)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    left_column = tk.Frame(content_frame, bg='white')
    left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 7), pady=15)
    
    right_column = tk.Frame(content_frame, bg='white')
    right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(7, 15), pady=15)
    
    saldo_frame = tk.Frame(left_column, bg='#f0f0f0', relief=tk.GROOVE, bd=2)
    saldo_frame.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(saldo_frame, text="Saldo Disponible:", 
            font=('Arial', 11, 'bold'), bg='#f0f0f0', fg='#333333').pack(side=tk.LEFT, padx=15, pady=10)
    
    label_saldo = tk.Label(saldo_frame, text="", 
                          font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#27ae60')
    label_saldo.pack(side=tk.LEFT, padx=10)
    
    tk.Button(saldo_frame, text="Actualizar", 
             font=('Arial', 9),
             bg='#EC0000', fg='white',
             relief=tk.RAISED, bd=2,
             command=consultar_saldo,
             cursor='hand2').pack(side=tk.RIGHT, padx=15)
    
    inv_frame = tk.LabelFrame(left_column, text="Inventario de Billetes", 
                              font=('Arial', 10, 'bold'), bg='white', fg='#EC0000',
                              relief=tk.GROOVE, bd=2)
    inv_frame.pack(fill=tk.X, pady=(0, 10))
    
    inv_grid = tk.Frame(inv_frame, bg='white')
    inv_grid.pack(padx=10, pady=8)
    
    for i, den in enumerate(sorted(inventario_actual.keys(), reverse=True)):
        tk.Label(inv_grid, text=f"${den:,}", 
                font=('Arial', 9, 'bold'), bg='white', fg='#333333',
                width=10).grid(row=i//2, column=(i%2)*2, padx=5, pady=2, sticky='w')
        
        label_cant = tk.Label(inv_grid, text="", 
                             font=('Arial', 8), bg='white', fg='#666666')
        label_cant.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=2, sticky='w')
        labels_inventario[den] = label_cant
    
    retiro_frame = tk.LabelFrame(left_column, text="Realizar Retiro", 
                                font=('Arial', 10, 'bold'), bg='white', fg='#EC0000',
                                relief=tk.GROOVE, bd=2)
    retiro_frame.pack(fill=tk.BOTH, expand=True)
    
    input_frame = tk.Frame(retiro_frame, bg='white')
    input_frame.pack(pady=10)
    
    tk.Label(input_frame, text="Monto:", 
            font=('Arial', 10, 'bold'), bg='white', fg='#333333').pack(side=tk.LEFT, padx=5)
    
    tk.Label(input_frame, text="$", 
            font=('Arial', 12, 'bold'), bg='white', fg='#EC0000').pack(side=tk.LEFT)
    
    entry_monto = tk.Entry(input_frame, font=('Arial', 12), width=13,
                           relief=tk.SOLID, bd=2)
    entry_monto.pack(side=tk.LEFT, padx=5)
    entry_monto.bind('<Return>', lambda e: realizar_retiro())
    
    tk.Label(retiro_frame, text="Montos rapidos:", 
            font=('Arial', 8, 'bold'), bg='white', fg='#666666').pack(pady=(0, 5))
    
    botones_frame = tk.Frame(retiro_frame, bg='white')
    botones_frame.pack(pady=5)
    
    montos_rapidos = [10000, 20000, 50000, 100000, 200000, 500000]
    for i, monto in enumerate(montos_rapidos):
        btn = tk.Button(botones_frame, text=f"${monto//1000}k", 
                      font=('Arial', 8, 'bold'),
                      bg='#f0f0f0', fg='#333333',
                      width=7, height=1,
                      relief=tk.RAISED, bd=2,
                      command=lambda m=monto: set_monto_rapido(m))
        btn.grid(row=i//3, column=i%3, padx=3, pady=3)
    
    btn_frame = tk.Frame(retiro_frame, bg='white')
    btn_frame.pack(pady=10)
    
    btn_retirar = tk.Button(btn_frame, text="RETIRAR", 
                            font=('Arial', 10, 'bold'),
                            bg='#EC0000', fg='white',
                            width=12, height=2,
                            relief=tk.RAISED, bd=3,
                            command=realizar_retiro,
                            cursor='hand2')
    btn_retirar.pack(side=tk.LEFT, padx=3)
    
    tk.Button(btn_frame, text="LIMPIAR", 
             font=('Arial', 10, 'bold'),
             bg='#666666', fg='white',
             width=12, height=2,
             relief=tk.RAISED, bd=3,
             command=limpiar,
             cursor='hand2').pack(side=tk.LEFT, padx=3)
    
    servicios_frame = tk.LabelFrame(right_column, text="Servicios Adicionales", 
                                   font=('Arial', 10, 'bold'), bg='white', fg='#EC0000',
                                   relief=tk.GROOVE, bd=2)
    servicios_frame.pack(fill=tk.X, pady=(0, 10))
    
    tk.Button(servicios_frame, text="💰 Consignar Dinero", 
             font=('Arial', 10, 'bold'),
             bg='#27ae60', fg='white',
             width=25, height=2,
             relief=tk.RAISED, bd=3,
             command=consignar_dinero,
             cursor='hand2').pack(padx=10, pady=8)
    
    tk.Button(servicios_frame, text="💸 Transferir a Otra Persona", 
             font=('Arial', 10, 'bold'),
             bg='#3498db', fg='white',
             width=25, height=2,
             relief=tk.RAISED, bd=3,
             command=transferir_dinero,
             cursor='hand2').pack(padx=10, pady=8)
    
    tk.Button(servicios_frame, text="🔐 Cambiar PIN", 
             font=('Arial', 10, 'bold'),
             bg='#f39c12', fg='white',
             width=25, height=2,
             relief=tk.RAISED, bd=3,
             command=cambiar_contrasena,
             cursor='hand2').pack(padx=10, pady=8)
    
    historial_frame = tk.LabelFrame(right_column, text="Ultimo Retiro", 
                                   font=('Arial', 10, 'bold'), bg='white', fg='#EC0000',
                                   relief=tk.GROOVE, bd=2)
    historial_frame.pack(fill=tk.BOTH, expand=True)
    
    text_historial = tk.Text(historial_frame, height=8, width=40,
                             font=('Courier', 8), bg='#f9f9f9',
                             relief=tk.SUNKEN, bd=2, state=tk.DISABLED)
    text_historial.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
    
    footer_frame = tk.Frame(main_frame, bg='#EC0000')
    footer_frame.pack(fill=tk.X, pady=(10, 0))
    
    tk.Button(footer_frame, text="Consultar Saldo", 
             font=('Arial', 10, 'bold'),
             bg='white', fg='#EC0000',
             relief=tk.RAISED, bd=2,
             command=consultar_saldo,
             cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    tk.Button(footer_frame, text="Finalizar Sesion", 
             font=('Arial', 10, 'bold'),
             bg='#333333', fg='white',
             relief=tk.RAISED, bd=2,
             command=salir,
             cursor='hand2').pack(side=tk.RIGHT, padx=5)
    
    actualizar_inventario_display()
    actualizar_saldo_display()
    
    root.mainloop()

## PROGRAMA PRINCIPAL
ventana_login = VentanaLogin()
tarjeta_validada = ventana_login.mostrar()

if tarjeta_validada:
    crear_interfaz_cajero(tarjeta_validada)