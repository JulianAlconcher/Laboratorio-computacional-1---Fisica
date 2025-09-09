
from logging import root
from tkinter import Frame, Tk, Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar, Canvas
from tkinter.ttk import Separator
from logic import calcular_campo_total, parsear_coordenadas, formatear_resultado, graficar_campo_electrico
from PIL import Image, ImageTk
import os

# Variable global para mantener referencia de imágenes
photo_references = []

def mostrar_ventana_resultados(cargas, x_punto, y_punto, Ex, Ey, magnitud, angulo, imagen_path):
    """
    Crea una nueva ventana para mostrar los resultados con el diseño especificado.
    """
    ventana_resultado = Toplevel()
    ventana_resultado.title("Resultados - Campo Eléctrico")
    ventana_resultado.geometry("1000x700")
    ventana_resultado.configure(bg='white')
    
    # Frame principal
    main_frame = Frame(ventana_resultado, bg='white')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Sección izquierda: Configuración de cargas
    left_frame = Frame(main_frame, bg='white', relief='solid', bd=1)
    left_frame.pack(side='left', fill='y', padx=(0, 10))
    
    Label(left_frame, text="Configuración de cargas", font=('Arial', 12, 'bold'), 
          bg='white').pack(pady=10)
    
    for i, (carga, x, y) in enumerate(cargas, 1):
        Label(left_frame, text=f"q{i}: {carga:.2e} C", font=('Arial', 10), 
              bg='white').pack(anchor='w', padx=10)
        Label(left_frame, text=f"Posición: ({x}, {y})", font=('Arial', 9), 
              bg='white', fg='gray').pack(anchor='w', padx=10)
    
    Label(left_frame, text=f"\nPunto de cálculo:", font=('Arial', 10, 'bold'), 
          bg='white').pack(anchor='w', padx=10)
    Label(left_frame, text=f"({x_punto}, {y_punto})", font=('Arial', 10), 
          bg='white').pack(anchor='w', padx=10)
    
    # Sección de resultado
    Label(left_frame, text="\nResultado", font=('Arial', 12, 'bold'), 
          bg='white').pack(pady=(20, 5))
    
    resultado_frame = Frame(left_frame, bg='black', relief='solid', bd=1)
    resultado_frame.pack(fill='x', padx=10, pady=5)
    
    resultado_text = f"Ex = {Ex:.2e} N/C\nEy = {Ey:.2e} N/C\nMagnitud = {magnitud:.2e} N/C\nÁngulo = {angulo:.1f}°"
    
    Label(resultado_frame, text=resultado_text, font=('Arial', 10), 
          bg='black', fg='blue', justify='left').pack(pady=10, padx=10)
    
    # Sección derecha: Gráfico
    right_frame = Frame(main_frame, bg='white', relief='solid', bd=1)
    right_frame.pack(side='right', fill='both', expand=True)
    
    Label(right_frame, text="GRAFICO", font=('Arial', 16, 'bold'), 
          bg='white').pack(pady=10)
    
    # Cargar y mostrar la imagen del gráfico
    try:
        # Cargar imagen
        img = Image.open(imagen_path)
        img = img.resize((700, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        # Canvas para la imagen
        canvas = Canvas(right_frame, bg='white', width=700, height=500)
        canvas.pack(pady=10)
        canvas.create_image(350, 250, image=photo)
        
        # Guardar referencia para evitar garbage collection
        photo_references.append(photo)
        
    except Exception as e:
        Label(right_frame, text=f"Error cargando gráfico: {str(e)}", 
              font=('Arial', 12), bg='white', fg='red').pack(pady=50)
    
    # Botón cerrar
    Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy,
           font=('Arial', 12), bg='lightgray').pack(side='bottom', pady=10)

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
        
        # Generar el gráfico E(x) vs x
        print("Generando gráfico...")
        imagen_path = graficar_campo_electrico(cargas, x_punto, y_punto)
        
        # Mostrar la nueva ventana de resultados
        mostrar_ventana_resultados(cargas, x_punto, y_punto, Ex_total, Ey_total, 
                                 magnitud, angulo, imagen_path)
        
        print(f"Cargas: {cargas}")
        print(f"Punto: ({x_punto}, {y_punto})")
        print(f"Campo eléctrico: Ex={Ex_total:.2e}, Ey={Ey_total:.2e}")
        print(f"Magnitud: {magnitud:.2e} N/C, Ángulo: {angulo:.1f}°")
        print(f"Gráfico guardado en: {imagen_path}")
        
    except Exception as e:
        messagebox.showerror("Error de cálculo", f"Error al calcular el campo eléctrico: {str(e)}")
        print(f"Error: {e}")

def crear_interfaz():
    global carga1, carga2, carga3, carga1_xy, carga2_xy, carga3_xy, entry_punto, label_resultado, frame_cargas

    root = Tk()
    root.title("Laboratorio Computacional 1 - Física")
    root.geometry("800x300")
    
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
    # Crear un frame para centrar el botón
    frame_cargas = Frame(root)
    frame_cargas.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
    Button(root, text="Calcular y Graficar", command=calcular_graficar).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    label_resultado = Label(root, text="",font=('Arial', 12), fg='#FFFFFF', justify='left') # resultado del campo eléctrico
    label_resultado.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    crear_interfaz()