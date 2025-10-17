import json
import os

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
        except Exception as e:
            print("Error al leer el archivo:", e)
            print("Se usará el inventario por defecto.")
            guardar_inventario(inventario)
            return inventario.copy()
    else:
        guardar_inventario(inventario)
        print("Se creó el archivo de inventario en:", ruta_archivo)
        return inventario.copy()


def guardar_inventario(inventario):
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Error al guardar el inventario:", e)


def mostrar_inventario(inventario):
    print("\n selecciona el valor a retirar")
    for den in sorted(inventario.keys(), reverse=True):
        print(f"  ${den:,}: {inventario[den]} billetes")
    print()


def cajero_vacio(inventario):
    return all(cant == 0 for cant in inventario.values())

#### Funcion retiro del dinero

def calcular_billetes(inventario, monto):
    temp = inventario.copy()
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


def retirar(inventario, monto):
    if monto <= 0:
        print("Monto invalido")
        return inventario

    billetes = calcular_billetes(inventario, monto)
    if not billetes:
        print("Monto invalido")
        return inventario

    for den, cant in billetes.items():
        inventario[den] -= cant

    print("\n Retiro exitoso!")
    print("Retire su dinero")
    for den in sorted(billetes.keys(), reverse=True):
        print(f"  ${den:,}: {billetes[den]} billetes")

    guardar_inventario(inventario)
    return inventario

## Interfaz cajero basico

print("=" * 60)
print("Bienvenido al cajero santander")
print("=" * 60)

inventario = cargar_inventario()
mostrar_inventario(inventario)

while True:
    if cajero_vacio(inventario):
        print("\n cajero fuera de servicio")
        break

    entrada = input("Ingrese monto a retirar $")
    if entrada.lower() in ["salir", "exit"]:
        print("\n Gracias por usar este servicio")
        break

    try:
        monto = int(entrada)
    except ValueError:
        print("Monto invalido")
        continue

    inventario = retirar(inventario, monto)
    mostrar_inventario(inventario)

print("=" * 60)
