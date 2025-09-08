
from tkinter import Frame, Tk, Label, Entry, Button, messagebox

def obtener_datos():
   print("Función obtener_datos llamada")

def crear_campos():
   print("Función crear_campos llamada")

def crear_interfaz():
    """
    Interfaz gráfica para solicitar datos al usuario.
    """
    global entry_num_cargas, entries_cargas, entries_posiciones, entry_punto, label_resultado, frame_cargas
    
    root = Tk()
    root.title("Datos para Cálculo del Campo Eléctrico y Potencial")
    
    Label(root, text="Número de Cargas:").grid(row=0, column=0, padx=10, pady=10)
    entry_num_cargas = Entry(root)
    entry_num_cargas.grid(row=0, column=1, padx=10, pady=10)
    
    Button(root, text="Cargar Valores", command=crear_campos).grid(row=0, column=2, padx=10, pady=10)
    
    Label(root, text="Cargas (en Coulombs):").grid(row=1, column=0, padx=10, pady=10)
    
    
    frame_cargas = Frame(root)
    frame_cargas.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
    Label(root, text="Punto (x y):").grid(row=3, column=0, padx=10, pady=10)
    entry_punto = Entry(root)
    entry_punto.grid(row=3, column=1, padx=10, pady=10)
    
    Button(root, text="Calcular y Graficar", command=obtener_datos).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    
    label_resultado = Label(root, text="",font=('Arial', 20), fg= '#0000FF') # resultado del campo eléctrico
    label_resultado.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()


crear_interfaz()