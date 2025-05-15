import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os

# Crear archivo si no existe
archivo = "inventarioExamenFranz.xlsx"
if not os.path.exists(archivo):
    df = pd.DataFrame(columns=["Producto", "Cantidad", "Tipo", "Fecha", "Hora", "PrincipioActivo", "AccionTerapeutica", "FechaVencimiento", "FechaIngreso"])
    df.to_excel(archivo, index=False)

# Función para registrar movimientos
def registrar_movimiento():
    producto = entrada_producto.get().strip()
    cantidad = entrada_cantidad.get().strip()
    # Para los medicamentos
    principio_activo = entrada_principio_activo.get()
    accion_terapeutica = entrada_accion_terapeutica.get()
    tipo = combo_tipo.get()

    if not producto or not cantidad or not tipo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
        return

    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    fecha_vencimiento = datetime.now().strftime("%Y-%m-%d")
    fecha_ingreso = datetime.now().strftime("%Y-%m-%d")

    df = pd.read_excel(archivo)

    # "Producto", "Cantidad", "Tipo", "Fecha", "Hora", "PrincipioActivo", "AccionTerapeutica", "FechaVencimiento", "FechaIngreso"
    nuevo = pd.DataFrame([[producto, cantidad, tipo, fecha, hora, principio_activo, accion_terapeutica, fecha_vencimiento, fecha_ingreso]], columns=df.columns)
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_excel(archivo, index=False)

    actualizar_tablas()
    messagebox.showinfo("Movimiento registrado", f"{tipo} de {cantidad} unidades de '{producto}'.")

# Actualiza historial y stock
def actualizar_tablas():
    df = pd.read_excel(archivo)
    
    # Tabla de historial
    for fila in tabla_historial.get_children():
        tabla_historial.delete(fila)
    for _, fila in df.iterrows():
        tabla_historial.insert("", "end", values=list(fila))

    # Tabla de stock actual
    resumen = df.groupby(["Producto", "Tipo"])["Cantidad"].sum().unstack().fillna(0)
    resumen["Stock Actual"] = resumen.get("Entrada", 0) + resumen.get("Devolución", 0) - resumen.get("Salida", 0)

    for fila in tabla_stock.get_children():
        tabla_stock.delete(fila)

    for producto, fila in resumen.iterrows():
        tabla_stock.insert("", "end", values=(producto, fila.get("Entrada", 0), fila.get("Salida", 0),
                                              fila.get("Devolución", 0), fila["Stock Actual"]))
        
# Funcion para la Salida de productos
df = pd.read_excel(archivo)

# Gráfico de stock
def graficar_stock():
    df = pd.read_excel(archivo)
    resumen = df.groupby(["Producto", "Tipo"])["Cantidad"].sum().unstack().fillna(0)
    resumen["Stock Actual"] = resumen.get("Entrada", 0) + resumen.get("Devolución", 0) - resumen.get("Salida", 0)
    resumen["Stock Actual"].plot(kind="bar", title="Stock Actual por Producto")
    plt.ylabel("Unidades")
    plt.tight_layout()
    plt.show()

# Gráfico de historial
def graficar_historial():
    df = pd.read_excel(archivo)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    historial = df.groupby(["Fecha", "Tipo"])["Cantidad"].sum().unstack().fillna(0)
    historial.plot(marker='o', title="Historial de Entradas, Salidas y Devoluciones")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.show()

# Interfaz
root = Tk()
root.title("Sistema Profesional de Inventario-Franz Joel Quispe Mamani")
root.geometry("1000x700")
root.configure(bg="#f0f0f0")

frame = Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

Label(frame, text="Producto:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
entrada_producto = Entry(frame, font=("Arial", 12))
entrada_producto.grid(row=0, column=1, padx=10, pady=5)

Label(frame, text="Cantidad:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
entrada_cantidad = Entry(frame, font=("Arial", 12))
entrada_cantidad.grid(row=1, column=1, padx=10, pady=5)

# Nuevos Labels
Label(frame, text="Principio Activo:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
entrada_principio_activo =  ttk.Combobox(frame, values=["Paracetamol", "Metformina", "Loratadina", "Amoxicilina", "Ibuprofeno"], font=("Arial", 12), state="readonly")
entrada_principio_activo.grid(row=2, column=1, padx=10, pady=5)

Label(frame, text="Accion Terapeutica:", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
entrada_accion_terapeutica = ttk.Combobox(frame, values=["Antidiabético", "Antibiótico", "Antiinflamatorio", "Analgésico"], font=("Arial", 12), state="readonly")
entrada_accion_terapeutica.grid(row=3, column=1, padx=10, pady=5)

Label(frame, text="Tipo de Movimiento:", bg="#f0f0f0", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
combo_tipo = ttk.Combobox(frame, values=["Entrada", "Salida", "Devolución"], font=("Arial", 12), state="readonly")
combo_tipo.grid(row=4, column=1, padx=10, pady=5)

Button(frame, text="Registrar Movimiento", command=registrar_movimiento, bg="#28a745", fg="white", font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=10)

# Tabla de historial
Label(root, text="Historial de Movimientos", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
# "Producto", "Cantidad", "Tipo", "Fecha", "Hora", "PrincipioActivo", "AccionTerapeutica", "FechaVencimiento", "FechaIngreso"
tabla_historial = ttk.Treeview(root, columns=["Producto", "Cantidad", "Tipo", "Fecha", "Hora", "PrincipioActivo", "AccionTerapeutica", "FechaVencimiento", "FechaIngreso"], show="headings", height=8)
for col in ["Producto", "Cantidad", "Tipo", "Fecha", "Hora", "PrincipioActivo", "AccionTerapeutica", "FechaVencimiento", "FechaIngreso"]:
    tabla_historial.heading(col, text=col)
    tabla_historial.column(col, anchor="center", width=120)
tabla_historial.pack(padx=10, pady=10)

# Tabla de stock
Label(root, text="Stock Actual por Producto", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
tabla_stock = ttk.Treeview(root, columns=["Producto", "Entradas", "Salidas", "Devoluciones", "Stock Actual"], show="headings", height=6)
for col in ["Producto", "Entradas", "Salidas", "Devoluciones", "Stock Actual"]:
    tabla_stock.heading(col, text=col)
    tabla_stock.column(col, anchor="center", width=130)
tabla_stock.pack(padx=10, pady=10)

# Botones de gráficos
frame_graficos = Frame(root, bg="#f0f0f0")
frame_graficos.pack(pady=10)
Button(frame_graficos, text="📊 Ver Gráfico de Stock", command=graficar_stock, bg="#007bff", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=20)
Button(frame_graficos, text="📈 Ver Historial", command=graficar_historial, bg="#17a2b8", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=20)

actualizar_tablas()
root.mainloop()
