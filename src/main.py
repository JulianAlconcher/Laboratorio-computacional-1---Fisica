
from tkinter import Frame, Tk, Label, Entry, Button, messagebox
from logic import calcular_campo_total, parsear_coordenadas, formatear_resultado

def validar_cargas(carga1_val, carga2_val, carga3_val):
    """
    Valida que las cargas cumplan con las condiciones:
    1. Dos cargas positivas y una negativa O dos cargas negativas y una positiva
    2. Las 3 magnitudes deben ser distintas
    3. Los números deben ser decimales (float)
    
    Retorna: (bool, str) - (es_valido, mensaje_error)
    """
    try:
        # Convertir a float para validar que son números decimales
        cargas = [float(carga1_val), float(carga2_val), float(carga3_val)]
    except ValueError:
        return False, "Error: Todas las cargas deben ser números decimales válidos"
    
    # Verificar que ninguna carga sea cero
    if any(carga == 0 for carga in cargas):
        return False, "Error: Las cargas no pueden ser cero"
    
    # Verificar que las magnitudes sean distintas
    magnitudes = [abs(carga) for carga in cargas]
    if len(set(magnitudes)) != 3:
        return False, "Error: Las 3 magnitudes deben ser distintas entre ellas"
    
    # Contar cargas positivas y negativas
    positivas = sum(1 for carga in cargas if carga > 0)
    negativas = sum(1 for carga in cargas if carga < 0)
    
    # Validar configuración de signos
    if positivas == 2 and negativas == 1:
        return True, "Configuración válida: 2 cargas positivas y 1 negativa"
    elif positivas == 1 and negativas == 2:
        return True, "Configuración válida: 1 carga positiva y 2 negativas"
    else:
        return False, "Error: Debe haber 2 cargas de un signo y 1 del signo opuesto"

def calcular_graficar():
    """
    Valida las cargas ingresadas y calcula el campo eléctrico en el punto especificado.
    Implementa el inciso b) del ejercicio.
    """
    print("Función calcular_graficar llamada")

    # Obtener valores de las cargas
    carga1_val = carga1.get().strip()
    carga2_val = carga2.get().strip()
    carga3_val = carga3.get().strip()
    
    # Verificar que todos los campos de cargas estén llenos
    if not all([carga1_val, carga2_val, carga3_val]):
        messagebox.showerror("Error", "Por favor ingrese valores para todas las cargas")
        return
    
    # Validar las cargas
    es_valido, mensaje = validar_cargas(carga1_val, carga2_val, carga3_val)
    
    if not es_valido:
        messagebox.showerror("Error de validación", mensaje)
        return
    
    # Obtener coordenadas de las cargas
    try:
        coord1_str = carga1_xy.get().strip()
        coord2_str = carga2_xy.get().strip()
        coord3_str = carga3_xy.get().strip()
        
        if not all([coord1_str, coord2_str, coord3_str]):
            messagebox.showerror("Error", "Por favor ingrese las coordenadas de todas las cargas")
            return
            
        x1, y1 = parsear_coordenadas(coord1_str)
        x2, y2 = parsear_coordenadas(coord2_str)
        x3, y3 = parsear_coordenadas(coord3_str)
        
    except ValueError as e:
        messagebox.showerror("Error de coordenadas", f"Error en coordenadas de cargas: {str(e)}")
        return
    
    # Obtener punto donde calcular el campo
    try:
        punto_str = entry_punto.get().strip()
        if not punto_str:
            messagebox.showerror("Error", "Por favor ingrese el punto donde calcular el campo")
            return
            
        x_punto, y_punto = parsear_coordenadas(punto_str)
        
    except ValueError as e:
        messagebox.showerror("Error de punto", f"Error en punto de entrada: {str(e)}")
        return
    
    # Convertir cargas a float
    try:
        q1 = float(carga1_val)
        q2 = float(carga2_val)
        q3 = float(carga3_val)
    except ValueError:
        messagebox.showerror("Error", "Error al convertir cargas a números")
        return
    
    # Crear lista de cargas para el cálculo
    cargas = [
        (q1, x1, y1),
        (q2, x2, y2),
        (q3, x3, y3)
    ]
    
    # Calcular el campo eléctrico total en el punto especificado
    try:
        Ex_total, Ey_total, magnitud, angulo = calcular_campo_total(cargas, x_punto, y_punto)
        
        # Formatear y mostrar el resultado
        resultado_texto = formatear_resultado(Ex_total, Ey_total, magnitud, angulo)
        label_resultado.config(text=resultado_texto)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Cálculo exitoso", 
                          f"Campo eléctrico calculado en el punto ({x_punto}, {y_punto})")
        
        print(f"Cargas: {cargas}")
        print(f"Punto: ({x_punto}, {y_punto})")
        print(f"Campo eléctrico: Ex={Ex_total:.2e}, Ey={Ey_total:.2e}")
        print(f"Magnitud: {magnitud:.2e} N/C, Ángulo: {angulo:.1f}°")
        
    except Exception as e:
        messagebox.showerror("Error de cálculo", f"Error al calcular el campo eléctrico: {str(e)}")
        print(f"Error: {e}")

def crear_interfaz():
    global carga1, carga2, carga3, carga1_xy, carga2_xy, carga3_xy, entry_punto, label_resultado, frame_cargas

    root = Tk()
    root.title("Laboratorio Computacional 1 - Física")
    
    Label(root, text="Carga 1: ").grid(row=0, column=0, padx=10, pady=10)
    carga1 = Entry(root)
    carga1.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Coordenada (x,y) Carga 1: ").grid(row=0, column=2, padx=10, pady=10)
    carga1_xy = Entry(root)
    carga1_xy.grid(row=0, column=3, padx=10, pady=10)

    Label(root, text="Carga 2: ").grid(row=1, column=0, padx=10, pady=10)
    carga2 = Entry(root)
    carga2.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Coordenada (x,y) Carga 2: ").grid(row=1, column=2, padx=10, pady=10)
    carga2_xy = Entry(root)
    carga2_xy.grid(row=1, column=3, padx=10, pady=10)

    Label(root, text="Carga 3: ").grid(row=2, column=0, padx=10, pady=10)
    carga3 = Entry(root)
    carga3.grid(row=2, column=1, padx=10, pady=10)

    Label(root, text="Coordenada (x,y) Carga 3: ").grid(row=2, column=2, padx=10, pady=10)
    carga3_xy = Entry(root)
    carga3_xy.grid(row=2, column=3, padx=10, pady=10)

    Label(root, text="Punto de entrada (x,y):").grid(row=3, column=0, padx=10, pady=10)
    entry_punto = Entry(root)
    entry_punto.grid(row=3, column=1, padx=10, pady=10)

    frame_cargas = Frame(root)
    frame_cargas.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
    Button(root, text="Calcular y Graficar", command=calcular_graficar).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    label_resultado = Label(root, text="",font=('Arial', 12), fg='#FFFFFF', justify='left') # resultado del campo eléctrico
    label_resultado.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    crear_interfaz()