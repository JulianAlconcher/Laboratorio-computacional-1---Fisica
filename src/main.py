
from logging import root
from tkinter import Frame, Tk, Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar, Canvas
from tkinter.ttk import Separator
from logic import calcular_campo_total, parsear_coordenadas, formatear_resultado, graficar_campo_electrico
from PIL import Image, ImageTk
import os
import json

# Variable global para mantener referencia de imágenes
photo_references = []

def mostrar_ventana_resultados(cargas, x_punto, y_punto, Ex, Ey, magnitud, angulo, imagen_path):
    ventana = Toplevel()
    ventana.title("Resultados - Campo Eléctrico")
    ventana.geometry("1100x750")
    ventana.configure(bg="#fdfdfd")

    # Frame principal
    main_frame = Frame(ventana, bg="#fdfdfd")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ===== IZQUIERDA (Texto) =====
    left_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
    left_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=15, ipady=15)

    Label(left_frame, text="⚡ Configuración de cargas", 
          font=("Arial", 16, "bold"), bg="white").pack(pady=15)

    for i, (carga, x, y) in enumerate(cargas, 1):
        Label(left_frame, text=f"q{i}: {carga:.2e} C", 
              font=("Arial", 13), bg="white").pack(anchor="w", padx=15)
        Label(left_frame, text=f"Posición: ({x}, {y})", 
              font=("Arial", 12), fg="gray40", bg="white").pack(anchor="w", padx=15, pady=(0,5))

    Label(left_frame, text="\nPunto de cálculo:", 
          font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=15, pady=(10,0))
    Label(left_frame, text=f"({x_punto}, {y_punto})", 
          font=("Arial", 13), bg="white").pack(anchor="w", padx=15)

    # ===== RESULTADOS COMO TEXTO NORMAL =====
    Label(left_frame, text="\nResultado:", 
          font=("Arial", 14, "bold"), bg="white").pack(anchor="w", padx=15, pady=(20,0))

    Label(left_frame, text=f"Ex = {Ex:.2e} N/C", 
          font=("Arial", 13), bg="white").pack(anchor="w", padx=25)
    Label(left_frame, text=f"Ey = {Ey:.2e} N/C", 
          font=("Arial", 13), bg="white").pack(anchor="w", padx=25)
    Label(left_frame, text=f"Magnitud = {magnitud:.2e} N/C", 
          font=("Arial", 13), bg="white").pack(anchor="w", padx=25)
    Label(left_frame, text=f"Ángulo = {angulo:.1f}°", 
          font=("Arial", 13), bg="white").pack(anchor="w", padx=25)

    # ===== DERECHA (Gráfico) =====
    right_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
    right_frame.pack(side="right", fill="both", expand=True)

    Label(right_frame, text="📊 Visualización del campo", 
          font=("Arial", 18, "bold"), bg="white").pack(pady=15)

    try:
        img = Image.open(imagen_path)
        img.thumbnail((850, 600))  # mantiene proporción
        photo = ImageTk.PhotoImage(img)

        canvas = Canvas(right_frame, bg="white", 
                        width=img.width, height=img.height, 
                        highlightthickness=0)
        canvas.pack(pady=15)
        canvas.create_image(img.width//2, img.height//2, image=photo)

        photo_references.append(photo)

    except Exception as e:
        Label(right_frame, text=f"Error cargando gráfico: {str(e)}", 
              font=("Arial", 14), bg="white", fg="red").pack(pady=60)

    # ===== BOTÓN CERRAR =====
    Button(ventana, text="Cerrar", command=ventana.destroy,
           font=("Arial", 14, "bold"), bg="#f0f0f0", 
           activebackground="#cfcfcf", width=15).pack(side="bottom", pady=15)

def cargar_configuracion_predeterminada():
    """
    Carga la configuración predeterminada desde un archivo JSON y la aplica a los campos.
    """
    try:
        # Ruta al archivo JSON (en el directorio padre de src)
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_predeterminada.json')
        
        # Leer el archivo JSON
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        # Obtener la configuración
        config_data = config['configuracion_predeterminada']
        cargas_config = config_data['cargas']
        punto_config = config_data['punto_entrada']
        
        # Cargar valores en los campos de entrada
        carga1.delete(0, 'end')
        carga1.insert(0, str(cargas_config[0]['valor']))
        
        carga2.delete(0, 'end')
        carga2.insert(0, str(cargas_config[1]['valor']))
        
        carga3.delete(0, 'end')
        carga3.insert(0, str(cargas_config[2]['valor']))
        
        # Cargar coordenadas
        carga1_xy.delete(0, 'end')
        carga1_xy.insert(0, f"{cargas_config[0]['x']}, {cargas_config[0]['y']}")
        
        carga2_xy.delete(0, 'end')
        carga2_xy.insert(0, f"{cargas_config[1]['x']}, {cargas_config[1]['y']}")
        
        carga3_xy.delete(0, 'end')
        carga3_xy.insert(0, f"{cargas_config[2]['x']}, {cargas_config[2]['y']}")
        
        # Cargar punto de entrada
        entry_punto.delete(0, 'end')
        entry_punto.insert(0, f"{punto_config['x']}, {punto_config['y']}")
        
        messagebox.showinfo("Configuración cargada", 
                          "Se ha cargado la configuración predeterminada exitosamente.")
        
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de configuración predeterminada.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error al leer el archivo de configuración JSON.")
    except KeyError as e:
        messagebox.showerror("Error", f"Error en la estructura del archivo JSON: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado al cargar configuración: {str(e)}")

def calcular_y_graficar_predeterminado():
    """
    Carga la configuración predeterminada y ejecuta el cálculo automáticamente.
    """
    cargar_configuracion_predeterminada()
    # Ejecutar el cálculo directamente
    calcular_graficar()

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
    root.geometry("1000x400")
    
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
    
    # Frame para los botones
    buttons_frame = Frame(root)
    buttons_frame.grid(row=4, column=0, columnspan=4, pady=20)
    
    # Botón para cargar configuración predeterminada
    Button(buttons_frame, text="Cargar Configuración Predeterminada", 
           command=cargar_configuracion_predeterminada,
           font=('Arial', 10), bg='lightgreen', pady=5).pack(side='left', padx=5)
    
    # Botón para calcular con configuración predeterminada
    Button(buttons_frame, text="Calcular y Graficar Configuración Predeterminada", 
           command=calcular_y_graficar_predeterminado,
           font=('Arial', 10), bg='lightcoral', pady=5).pack(side='left', padx=5)
    
    # Botón normal de calcular
    Button(buttons_frame, text="Calcular y Graficar", 
           command=calcular_graficar,
           font=('Arial', 10), bg='lightblue', pady=5).pack(side='left', padx=5)
    
    # Crear un frame para centrar el botón (ya no se usa)
    frame_cargas = Frame(root)
    frame_cargas.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    # Instrucciones para el usuario
    instrucciones_frame = Frame(root)
    instrucciones_frame.grid(row=5, column=0, columnspan=4, pady=10)
    
    instrucciones_text = ("Instrucciones:\n"
                         "• Use 'Cargar Configuración Predeterminada' para cargar valores de ejemplo\n"
                         "• Use 'Calcular y Graficar Configuración Predeterminada' para ejecutar directamente con valores por defecto\n"
                         "• Use 'Calcular y Graficar' para ejecutar con los valores ingresados manualmente\n"
                         "• Formato de cargas: notación científica (ej: 3e-6 para 3×10⁻⁶ C)\n"
                         "• Formato de coordenadas: x, y (ej: 0.1, 0.2)")
    
    Label(instrucciones_frame, text=instrucciones_text, font=('Arial', 9), 
          fg='gray', justify='left').pack()

    label_resultado = Label(root, text="",font=('Arial', 12), fg='#FFFFFF', justify='left') # resultado del campo eléctrico
    label_resultado.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    crear_interfaz()