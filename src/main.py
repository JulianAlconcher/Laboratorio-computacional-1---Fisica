
from logging import root
from tkinter import Frame, Tk, Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar, Canvas, Scale, HORIZONTAL
from tkinter.ttk import Separator
from logic import calcular_campo_total, parsear_coordenadas, formatear_resultado, graficar_campo_electrico, encontrar_puntos_equilibrio, analizar_estabilidad_equilibrio, graficar_lineas_campo, calcular_potencial_total, graficar_potencial
from PIL import Image, ImageTk
import os
import json
import numpy as np

# Variable global para mantener referencia de imágenes
photo_references = []

def mostrar_ventana_resultados(cargas, x_punto, y_punto, Ex, Ey, magnitud, angulo, imagen_path, puntos_equilibrio, imagen_lineas_path):
    ventana = Toplevel()
    ventana.title("Resultados - Campo Eléctrico")
    ventana.geometry("1100x900")
    ventana.configure(bg="#fdfdfd")
    ventana.resizable(False, False)  # Hacer la ventana no redimensionable

    # Frame principal
    main_frame = Frame(ventana, bg="#fdfdfd")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ===== IZQUIERDA (Texto) =====
    left_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
    left_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=20, ipady=20)

    # Título principal
    Label(left_frame, text="Configuración de Cargas", 
          font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=(10, 20))

    # Información de cada carga
    for i, (carga, x, y) in enumerate(cargas, 1):
        # Frame para cada carga
        carga_frame = Frame(left_frame, bg="#f8f9fa", relief="solid", bd=1)
        carga_frame.pack(fill="x", padx=10, pady=5)
        
        Label(carga_frame, text=f"Carga {i}:", 
              font=("Arial", 12, "bold"), bg="#f8f9fa", fg="black").pack(anchor="w", padx=10, pady=(5,0))
        Label(carga_frame, text=f"Valor: {carga:.2e} C", 
              font=("Arial", 11), bg="#f8f9fa", fg="black").pack(anchor="w", padx=20)
        Label(carga_frame, text=f"Posición: ({x}, {y}) m", 
              font=("Arial", 11), bg="#f8f9fa", fg="black").pack(anchor="w", padx=20, pady=(0,5))

    # Punto de cálculo
    Label(left_frame, text="Punto de Cálculo:", 
          font=("Arial", 14, "bold"), bg="white", fg="black").pack(anchor="w", padx=10, pady=(25,5))
    
    punto_frame = Frame(left_frame, bg="#e8f4fd", relief="solid", bd=1)
    punto_frame.pack(fill="x", padx=10, pady=5)
    Label(punto_frame, text=f"Coordenadas: ({x_punto}, {y_punto}) m", 
          font=("Arial", 12), bg="#e8f4fd", fg="black").pack(anchor="w", padx=15, pady=8)

    # Separador visual
    separator = Frame(left_frame, height=2, bg="#bdc3c7")
    separator.pack(fill="x", padx=10, pady=20)

    # Resultados del campo eléctrico
    Label(left_frame, text="Resultados del Campo Eléctrico:", 
          font=("Arial", 14, "bold"), bg="white", fg="black").pack(anchor="w", padx=10, pady=(5,10))

    # Frame para los resultados
    resultado_frame = Frame(left_frame, bg="#f0f8ff", relief="solid", bd=2)
    resultado_frame.pack(fill="x", padx=10, pady=5)

    # Componentes del campo
    Label(resultado_frame, text="Componentes:", 
          font=("Arial", 12, "bold"), bg="#f0f8ff", fg="black").pack(anchor="w", padx=15, pady=(10,5))
    
    Label(resultado_frame, text=f"• Ex = {Ex:.3e} N/C", 
          font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25)
    Label(resultado_frame, text=f"• Ey = {Ey:.3e} N/C", 
          font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25, pady=(0,8))

    # Magnitud y ángulo
    Label(resultado_frame, text="Características:", 
          font=("Arial", 12, "bold"), bg="#f0f8ff", fg="black").pack(anchor="w", padx=15, pady=(5,5))
    
    Label(resultado_frame, text=f"• Magnitud = {magnitud:.3e} N/C", 
          font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25)
    Label(resultado_frame, text=f"• Ángulo = {angulo:.1f}°", 
          font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25, pady=(0,10))

    # Puntos de equilibrio
    Label(left_frame, text="Puntos de Equilibrio (y = 0):", 
          font=("Arial", 14, "bold"), bg="white", fg="black").pack(anchor="w", padx=10, pady=(20,10))

    equilibrio_frame = Frame(left_frame, bg="#fff0f5", relief="solid", bd=2)
    equilibrio_frame.pack(fill="x", padx=10, pady=5)

    if puntos_equilibrio:
        Label(equilibrio_frame, text="Puntos encontrados:", 
              font=("Arial", 12, "bold"), bg="#fff0f5", fg="black").pack(anchor="w", padx=15, pady=(10,5))
        
        for i, (x_eq, estabilidad) in enumerate(puntos_equilibrio, 1):
            color_estabilidad = "black" if estabilidad == "estable" else "#dc143c"
            Label(equilibrio_frame, text=f"• Punto {i}: x = {x_eq:.3f} m ({estabilidad})", 
                  font=("Arial", 11), bg="#fff0f5", fg=color_estabilidad).pack(anchor="w", padx=25)
        
        Label(equilibrio_frame, text="", bg="#fff0f5").pack(pady=5)  # Espaciado
    else:
        Label(equilibrio_frame, text="No se encontraron puntos de equilibrio", 
              font=("Arial", 11), bg="#fff0f5", fg="#8b4513").pack(anchor="w", padx=15, pady=10)
        Label(equilibrio_frame, text="en el rango [-5, 5] metros", 
              font=("Arial", 11), bg="#fff0f5", fg="#8b4513").pack(anchor="w", padx=15, pady=(0,10))

    # ===== DERECHA (Gráfico con Slider) =====
    right_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
    right_frame.pack(side="right", fill="both", expand=True)

    # Frame para el control de gráficos
    control_frame = Frame(right_frame, bg="white")
    control_frame.pack(fill="x", padx=10, pady=10)

    # Variable para rastrear el gráfico actual
    grafico_actual = {"valor": 0}  # 0 = E(x) vs x, 1 = Líneas de campo
    
    def cambiar_grafico(tipo_grafico):
        """Función que cambia el gráfico según el tipo seleccionado"""
        try:
            # Actualizar el valor actual
            grafico_actual["valor"] = tipo_grafico
            
            # Limpiar el canvas anterior
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            
            # Seleccionar imagen según el tipo de gráfico
            if tipo_grafico == 0:
                imagen_actual = imagen_path
                titulo_actual = "E(x) vs x - Análisis de Equilibrio"
                # Actualizar estilo de botones
                btn_ex_vs_x.config(bg="#4CAF50", fg="black", relief="solid", bd=2)
                btn_lineas.config(bg="#f0f0f0", fg="black", relief="raised", bd=1)
            else:
                imagen_actual = imagen_lineas_path
                titulo_actual = "Líneas de Campo Eléctrico"
                # Actualizar estilo de botones
                btn_ex_vs_x.config(bg="#f0f0f0", fg="black", relief="raised", bd=1)
                btn_lineas.config(bg="#4CAF50", fg="black", relief="solid", bd=2)
            
            # Actualizar título
            titulo_grafico.config(text=titulo_actual)
            
            # Cargar y mostrar la nueva imagen
            img = Image.open(imagen_actual)
            img.thumbnail((850, 600))
            photo = ImageTk.PhotoImage(img)
            
            canvas = Canvas(canvas_frame, bg="white", 
                           width=img.width, height=img.height, 
                           highlightthickness=0)
            canvas.pack()
            canvas.create_image(img.width//2, img.height//2, image=photo)
            
            # Mantener referencia para evitar garbage collection
            photo_references.append(photo)
            
        except Exception as e:
            # Mostrar error si no se puede cargar la imagen
            Label(canvas_frame, text=f"Error cargando gráfico: {str(e)}", 
                  font=("Arial", 12), bg="white", fg="red").pack(pady=30)

    # Título del gráfico (dinámico)
    titulo_grafico = Label(control_frame, text="E(x) vs x - Análisis de Equilibrio", 
                          font=("Arial", 16, "bold"), bg="white", fg="#2c3e50")
    titulo_grafico.pack(pady=(0, 15))

    # Frame para los botones de selección
    botones_frame = Frame(control_frame, bg="white")
    botones_frame.pack(pady=5)
    
    # Botón para gráfico E(x) vs x
    btn_ex_vs_x = Button(botones_frame, text="📊 E(x) vs x", 
                        command=lambda: cambiar_grafico(0),
                        font=("Arial", 12, "bold"), 
                        bg="#4CAF50", fg="black",
                        relief="solid", bd=2,
                        padx=20, pady=8,
                        cursor="hand2")
    btn_ex_vs_x.pack(side="left", padx=5)
    
    # Botón para líneas de campo
    btn_lineas = Button(botones_frame, text="🌐 Líneas de Campo", 
                       command=lambda: cambiar_grafico(1),
                       font=("Arial", 12, "bold"), 
                       bg="#f0f0f0", fg="black",
                       relief="raised", bd=1,
                       padx=20, pady=8,
                       cursor="hand2")
    btn_lineas.pack(side="left", padx=5)
    
    # Efectos hover para los botones
    def on_enter_ex(e):
        if grafico_actual["valor"] != 0:
            btn_ex_vs_x.config(bg="#45a049")
    
    def on_leave_ex(e):
        if grafico_actual["valor"] != 0:
            btn_ex_vs_x.config(bg="#f0f0f0")
    
    def on_enter_lineas(e):
        if grafico_actual["valor"] != 1:
            btn_lineas.config(bg="#45a049")
    
    def on_leave_lineas(e):
        if grafico_actual["valor"] != 1:
            btn_lineas.config(bg="#f0f0f0")
    
    btn_ex_vs_x.bind("<Enter>", on_enter_ex)
    btn_ex_vs_x.bind("<Leave>", on_leave_ex)
    btn_lineas.bind("<Enter>", on_enter_lineas)
    btn_lineas.bind("<Leave>", on_leave_lineas)

    # Descripción de los gráficos
    descripcion_frame = Frame(control_frame, bg="#f8f9fa", relief="solid", bd=1)
    descripcion_frame.pack(fill="x", pady=(10, 5), padx=20)
    
    descripcion_text = ""
    if grafico_actual["valor"] == 0:
        descripcion_text = "• Muestra la variación del campo eléctrico Ex a lo largo del eje x\n• Detecta y marca puntos de equilibrio con análisis de estabilidad"
    else:
        descripcion_text = "• Visualiza las líneas de campo eléctrico resultante\n• Las líneas salen de cargas positivas y entran a cargas negativas"
    
    descripcion_label = Label(descripcion_frame, text=descripcion_text,
                             font=("Arial", 10), bg="#f8f9fa", fg="#34495e",
                             justify="left")
    descripcion_label.pack(pady=5, padx=10)
    
    # Función para actualizar descripción
    def actualizar_descripcion():
        if grafico_actual["valor"] == 0:
            descripcion_text = "• Muestra la variación del campo eléctrico Ex a lo largo del eje x\n• Detecta y marca puntos de equilibrio con análisis de estabilidad"
        else:
            descripcion_text = "• Visualiza las líneas de campo eléctrico resultante\n• Las líneas salen de cargas positivas y entran a cargas negativas"
        descripcion_label.config(text=descripcion_text)
    
    # Modificar la función cambiar_grafico para actualizar descripción
    def cambiar_grafico_con_descripcion(tipo_grafico):
        cambiar_grafico(tipo_grafico)
        actualizar_descripcion()
    
    # Actualizar los comandos de los botones
    btn_ex_vs_x.config(command=lambda: cambiar_grafico_con_descripcion(0))
    btn_lineas.config(command=lambda: cambiar_grafico_con_descripcion(1))

    # Frame para el canvas del gráfico
    canvas_frame = Frame(right_frame, bg="white")
    canvas_frame.pack(fill="both", expand=True, pady=10)

    # Mostrar inicialmente el primer gráfico
    cambiar_grafico_con_descripcion(0)

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
        
        # Generar el gráfico E(x) vs x y obtener puntos de equilibrio
        print("Generando gráfico E(x) vs x...")
        imagen_path, puntos_equilibrio = graficar_campo_electrico(cargas, x_punto, y_punto)
        
        # Generar el gráfico de líneas de campo
        print("Generando gráfico de líneas de campo...")
        imagen_lineas_path = graficar_lineas_campo(cargas, x_punto, y_punto)
        
        # Mostrar la nueva ventana de resultados
        mostrar_ventana_resultados(cargas, x_punto, y_punto, Ex_total, Ey_total, 
                                 magnitud, angulo, imagen_path, puntos_equilibrio, imagen_lineas_path)
        
        print(f"Cargas: {cargas}")
        print(f"Punto: ({x_punto}, {y_punto})")
        print(f"Campo eléctrico: Ex={Ex_total:.2e}, Ey={Ey_total:.2e}")
        print(f"Magnitud: {magnitud:.2e} N/C, Ángulo: {angulo:.1f}°")
        print(f"Gráfico guardado en: {imagen_path}")
        
    except Exception as e:
        messagebox.showerror("Error de cálculo", f"Error al calcular el campo eléctrico: {str(e)}")
        print(f"Error: {e}")

def mostrar_resultado_potencial_numerico(cargas, x_punto, y_punto, V_total):
    """
    Muestra una ventana emergente con el resultado numérico del potencial eléctrico
    """
    print(f"DEBUG: Abriendo ventana de potencial - V = {V_total}")
    
    try:
        ventana = Toplevel()
        ventana.title("Resultado - Potencial Eléctrico V(x,y)")
        ventana.geometry("700x600")
        ventana.configure(bg="#fdfdfd")
        ventana.resizable(True, True)

        # Frame principal
        main_frame = Frame(ventana, bg="white", relief="solid", bd=2)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título principal
        titulo = Label(main_frame, text="POTENCIAL ELÉCTRICO V(x,y)", 
                      font=("Arial", 20, "bold"), bg="white", fg="#2c3e50")
        titulo.pack(pady=(15, 25))

        # Mostrar configuración de cargas
        config_label = Label(main_frame, text="Configuración de Cargas:", 
                            font=("Arial", 14, "bold"), bg="white", fg="black")
        config_label.pack(anchor="w", padx=20, pady=(0,10))
        
        for i, (carga, x, y) in enumerate(cargas, 1):
            carga_info = f"• Carga {i}: {carga:.2e} C en posición ({x}, {y}) m"
            carga_label = Label(main_frame, text=carga_info, 
                               font=("Arial", 12), bg="white", fg="black")
            carga_label.pack(anchor="w", padx=40, pady=2)

        # Punto de cálculo
        punto_label = Label(main_frame, text=f"Punto de Cálculo: ({x_punto}, {y_punto}) m", 
                           font=("Arial", 14, "bold"), bg="white", fg="#2c3e50")
        punto_label.pack(pady=(20,30))

        # RESULTADO PRINCIPAL - Frame destacado
        resultado_frame = Frame(main_frame, bg="#e8f5e8", relief="solid", bd=3)
        resultado_frame.pack(fill="x", padx=20, pady=20)

        resultado_titulo = Label(resultado_frame, text="RESULTADO:", 
                                font=("Arial", 16, "bold"), bg="#e8f5e8", fg="#2c3e50")
        resultado_titulo.pack(pady=(15,10))

        # Mostrar el valor del potencial
        if np.isinf(V_total):
            valor_label = Label(resultado_frame, text="V = ∞ Voltios", 
                               font=("Arial", 24, "bold"), bg="#e8f5e8", fg="red")
            valor_label.pack(pady=10)
            
            explicacion_label = Label(resultado_frame, text="(El punto coincide con una carga)", 
                                     font=("Arial", 12), bg="#e8f5e8", fg="red")
            explicacion_label.pack(pady=(0,15))
        else:
            valor_label = Label(resultado_frame, text=f"V = {V_total:.6e} V", 
                               font=("Arial", 24, "bold"), bg="#e8f5e8", fg="#2e8b57")
            valor_label.pack(pady=(10,15))

        # Información de la fórmula
        formula_frame = Frame(main_frame, bg="#fff8dc", relief="solid", bd=1)
        formula_frame.pack(fill="x", padx=20, pady=15)

        formula_titulo = Label(formula_frame, text="Fórmula utilizada:", 
                              font=("Arial", 12, "bold"), bg="#fff8dc", fg="#8b4513")
        formula_titulo.pack(pady=(10,5))

        formula_texto = Label(formula_frame, text="V = Σ(k·qi/ri)", 
                             font=("Arial", 14, "bold"), bg="#fff8dc", fg="#8b4513")
        formula_texto.pack(pady=2)

        constante_texto = Label(formula_frame, text="donde k = 8.99×10⁹ N·m²/C² (constante de Coulomb)", 
                               font=("Arial", 10), bg="#fff8dc", fg="#8b4513")
        constante_texto.pack(pady=(2,10))

        # Botón cerrar
        boton_cerrar = Button(ventana, text="Cerrar", command=ventana.destroy,
                             font=("Arial", 14, "bold"), bg="#f0f0f0", 
                             activebackground="#cfcfcf", width=15, pady=5)
        boton_cerrar.pack(side="bottom", pady=20)
        
        # Centrar ventana y ponerla al frente
        ventana.update_idletasks()
        ventana.lift()
        ventana.focus_force()
        ventana.grab_set()
        
        print("DEBUG: Ventana de potencial creada exitosamente")
        
    except Exception as e:
        print(f"ERROR: No se pudo crear la ventana de potencial: {e}")
        messagebox.showerror("Error", f"No se pudo mostrar el resultado del potencial: {str(e)}")

def calcular_potencial():
    """
    Calcula el potencial eléctrico V(x,y) en el punto especificado y muestra ventana con gráfico.
    """
    print("DEBUG: Función calcular_potencial llamada")

    # Obtener valores de las cargas
    carga1_val = carga1.get().strip()
    carga2_val = carga2.get().strip()
    carga3_val = carga3.get().strip()

    if not all([carga1_val, carga2_val, carga3_val]):
        messagebox.showerror("Error", "Por favor ingrese valores para todas las cargas")
        return

    es_valido, mensaje = validar_cargas(carga1_val, carga2_val, carga3_val)
    if not es_valido:
        messagebox.showerror("Error de validación", mensaje)
        return

    try:
        x1, y1 = parsear_coordenadas(carga1_xy.get().strip())
        x2, y2 = parsear_coordenadas(carga2_xy.get().strip())
        x3, y3 = parsear_coordenadas(carga3_xy.get().strip())
    except ValueError as e:
        messagebox.showerror("Error de coordenadas", str(e))
        return

    try:
        x_punto, y_punto = parsear_coordenadas(entry_punto.get().strip())
    except ValueError as e:
        messagebox.showerror("Error de punto", str(e))
        return

    try:
        q1 = float(carga1_val)
        q2 = float(carga2_val)
        q3 = float(carga3_val)
    except ValueError:
        messagebox.showerror("Error", "Error al convertir cargas a números")
        return

    cargas = [(q1, x1, y1), (q2, x2, y2), (q3, x3, y3)]

    try:
        print("DEBUG: Iniciando cálculo de potencial...")
        V_total = calcular_potencial_total(cargas, x_punto, y_punto)
        print(f"DEBUG: Potencial calculado = {V_total}")

       # Generar gráfico de potencial
        imagen_potencial_path = graficar_potencial(cargas, x_punto, y_punto, rango_x=(-5, 5))
        
        # Generar gráfico de superficies equipotenciales
        from logic import graficar_superficies_equipotenciales
        
        # Calcular el rango apropiado para las equipotenciales
        x_vals = [x for _, x, _ in cargas]
        y_vals = [y for _, _, y in cargas]
        margen = 2.0
        x_min, x_max = min(x_vals) - margen, max(x_vals) + margen
        y_min, y_max = min(y_vals) - margen, max(y_vals) + margen
        rango_max = max(x_max - x_min, y_max - y_min) / 2
        centro_x = (min(x_vals) + max(x_vals)) / 2
        centro_y = (min(y_vals) + max(y_vals)) / 2
        rango = (centro_x - rango_max - margen, centro_x + rango_max + margen)
        
        imagen_equipotenciales_path = graficar_superficies_equipotenciales(cargas, rango=rango)

        # Mostrar ventana con resultado y ambos gráficos
        mostrar_ventana_potencial_completa(cargas, x_punto, y_punto, V_total, imagen_potencial_path, imagen_equipotenciales_path)


    except Exception as e:
        messagebox.showerror("Error de cálculo", f"Error al calcular el potencial eléctrico: {str(e)}")
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def mostrar_ventana_potencial_completa(cargas, x_punto, y_punto, V_total, imagen_path, imagen_equipotenciales_path):
    ventana = Toplevel()
    ventana.title("Resultados - Potencial Eléctrico")
    ventana.geometry("1100x900")
    ventana.configure(bg="#fdfdfd")
    ventana.resizable(False, False)

    # Frame principal
    main_frame = Frame(ventana, bg="#fdfdfd")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ===== IZQUIERDA (Texto) =====
    left_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
    left_frame.pack(side="left", fill="y", padx=(0, 15), ipadx=20, ipady=20)

    # Título principal
    Label(left_frame, text="Configuración de Cargas", 
          font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=(10, 20))

    # Información de cada carga
    for i, (carga, x, y) in enumerate(cargas, 1):
        # Frame para cada carga
        carga_frame = Frame(left_frame, bg="#f8f9fa", relief="solid", bd=1)
        carga_frame.pack(fill="x", padx=10, pady=5)
        
        Label(carga_frame, text=f"Carga {i}:", 
              font=("Arial", 12, "bold"), bg="#f8f9fa", fg="black").pack(anchor="w", padx=10, pady=(5,0))
        Label(carga_frame, text=f"Valor: {carga:.2e} C", 
              font=("Arial", 11), bg="#f8f9fa", fg="black").pack(anchor="w", padx=20)
        Label(carga_frame, text=f"Posición: ({x}, {y}) m", 
              font=("Arial", 11), bg="#f8f9fa", fg="black").pack(anchor="w", padx=20, pady=(0,5))

    # Punto de cálculo
    Label(left_frame, text="Punto de Cálculo:", 
          font=("Arial", 14, "bold"), bg="white", fg="black").pack(anchor="w", padx=10, pady=(25,5))
    
    punto_frame = Frame(left_frame, bg="#e8f4fd", relief="solid", bd=1)
    punto_frame.pack(fill="x", padx=10, pady=5)
    Label(punto_frame, text=f"Coordenadas: ({x_punto}, {y_punto}) m", 
          font=("Arial", 12), bg="#e8f4fd", fg="black").pack(anchor="w", padx=15, pady=8)

    # Separador visual
    separator = Frame(left_frame, height=2, bg="#bdc3c7")
    separator.pack(fill="x", padx=10, pady=20)

    # Resultados del potencial eléctrico
    Label(left_frame, text="Resultado del Potencial Eléctrico:", 
          font=("Arial", 14, "bold"), bg="white", fg="black").pack(anchor="w", padx=10, pady=(5,10))

    # Frame para los resultados
    resultado_frame = Frame(left_frame, bg="#f0f8ff", relief="solid", bd=2)
    resultado_frame.pack(fill="x", padx=10, pady=5)

    # Valor del potencial
    Label(resultado_frame, text="Valor del Potencial:", 
          font=("Arial", 12, "bold"), bg="#f0f8ff", fg="black").pack(anchor="w", padx=15, pady=(10,5))
    
    if np.isinf(V_total):
        Label(resultado_frame, text="• V = ∞ V (punto coincide con carga)", 
              font=("Arial", 11), bg="#f0f8ff", fg="red").pack(anchor="w", padx=25)
    else:
        Label(resultado_frame, text=f"• V = {V_total:.6e} V", 
              font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25)

    # Información de la fórmula
    Label(resultado_frame, text="Fórmula utilizada:", 
          font=("Arial", 12, "bold"), bg="#f0f8ff", fg="black").pack(anchor="w", padx=15, pady=(10,5))
    
    Label(resultado_frame, text="• V = Σ(k·qi/ri)", 
          font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25)
    Label(resultado_frame, text="• k = 8.99×10⁹ N·m²/C²", 
          font=("Arial", 11), bg="#f0f8ff", fg="black").pack(anchor="w", padx=25, pady=(0,10))

    # Información adicional sobre potencial
    info_frame = Frame(left_frame, bg="#fff0f5", relief="solid", bd=2)
    info_frame.pack(fill="x", padx=10, pady=(15,5))

    Label(info_frame, text="Interpretación Física:", 
          font=("Arial", 12, "bold"), bg="#fff0f5", fg="black").pack(anchor="w", padx=15, pady=(10,5))
    
    interpretacion = ("• Potencial > 0: trabajo requerido\n"
                     "  para traer carga + desde infinito\n"
                     "• Potencial < 0: trabajo liberado\n"
                     "  al traer carga + desde infinito")
    
    Label(info_frame, text=interpretacion, 
          font=("Arial", 10), bg="#fff0f5", fg="#8b4513", justify="left").pack(anchor="w", padx=25, pady=(0,10))

    # ===== DERECHA (Gráfico con Slider) =====
    right_frame = Frame(main_frame, bg="white", relief="solid", bd=2)
    right_frame.pack(side="right", fill="both", expand=True)

    # Frame para el control de gráficos
    control_frame = Frame(right_frame, bg="white")
    control_frame.pack(fill="x", padx=10, pady=10)

    # Variable para rastrear el gráfico actual
    grafico_actual = {"valor": 0}  # 0 = V(x,y) superficial, 1 = Equipotenciales
    
    def cambiar_grafico_potencial(tipo_grafico):
        """Función que cambia el gráfico según el tipo seleccionado"""
        try:
            # Actualizar el valor actual
            grafico_actual["valor"] = tipo_grafico
            
            # Limpiar el canvas anterior
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            
            # Seleccionar imagen según el tipo de gráfico
            if tipo_grafico == 0:
                imagen_actual = imagen_path
                titulo_actual = "V(x,y) - Potencial Eléctrico 2D"
                # Actualizar estilo de botones
                btn_potencial_2d.config(bg="#4CAF50", fg="black", relief="solid", bd=2)
                btn_equipotenciales.config(bg="#f0f0f0", fg="black", relief="raised", bd=1)
            else:
                imagen_actual = imagen_equipotenciales_path
                titulo_actual = "Superficies Equipotenciales"
                # Actualizar estilo de botones
                btn_potencial_2d.config(bg="#f0f0f0", fg="black", relief="raised", bd=1)
                btn_equipotenciales.config(bg="#4CAF50", fg="black", relief="solid", bd=2)
            
            # Actualizar título
            titulo_grafico.config(text=titulo_actual)
            
            # Cargar y mostrar la nueva imagen
            img = Image.open(imagen_actual)
            img.thumbnail((850, 600))
            photo = ImageTk.PhotoImage(img)
            
            canvas = Canvas(canvas_frame, bg="white", 
                           width=img.width, height=img.height, 
                           highlightthickness=0)
            canvas.pack()
            canvas.create_image(img.width//2, img.height//2, image=photo)
            
            # Mantener referencia para evitar garbage collection
            photo_references.append(photo)
            
        except Exception as e:
            # Mostrar error si no se puede cargar la imagen
            Label(canvas_frame, text=f"Error cargando gráfico: {str(e)}", 
                  font=("Arial", 12), bg="white", fg="red").pack(pady=30)

    # Título del gráfico (dinámico)
    titulo_grafico = Label(control_frame, text="V(x,y) - Potencial Eléctrico 2D", 
                          font=("Arial", 16, "bold"), bg="white", fg="#2c3e50")
    titulo_grafico.pack(pady=(0, 15))

    # Frame para los botones de selección
    botones_frame = Frame(control_frame, bg="white")
    botones_frame.pack(pady=5)
    
    # Botón para gráfico V(x,y) 2D
    btn_potencial_2d = Button(botones_frame, text="📊 V(x,y) 2D", 
                        command=lambda: cambiar_grafico_potencial_con_descripcion(0),
                        font=("Arial", 12, "bold"), 
                        bg="#4CAF50", fg="black",
                        relief="solid", bd=2,
                        padx=20, pady=8,
                        cursor="hand2")
    btn_potencial_2d.pack(side="left", padx=5)
    
    # Botón para superficies equipotenciales
    btn_equipotenciales = Button(botones_frame, text="🗺️ Equipotenciales", 
                       command=lambda: cambiar_grafico_potencial_con_descripcion(1),
                       font=("Arial", 12, "bold"), 
                       bg="#f0f0f0", fg="black",
                       relief="raised", bd=1,
                       padx=20, pady=8,
                       cursor="hand2")
    btn_equipotenciales.pack(side="left", padx=5)
    
    # Efectos hover para los botones
    def on_enter_2d(e):
        if grafico_actual["valor"] != 0:
            btn_potencial_2d.config(bg="#45a049")
    
    def on_leave_2d(e):
        if grafico_actual["valor"] != 0:
            btn_potencial_2d.config(bg="#f0f0f0")
    
    def on_enter_equi(e):
        if grafico_actual["valor"] != 1:
            btn_equipotenciales.config(bg="#45a049")
    
    def on_leave_equi(e):
        if grafico_actual["valor"] != 1:
            btn_equipotenciales.config(bg="#f0f0f0")
    
    btn_potencial_2d.bind("<Enter>", on_enter_2d)
    btn_potencial_2d.bind("<Leave>", on_leave_2d)
    btn_equipotenciales.bind("<Enter>", on_enter_equi)
    btn_equipotenciales.bind("<Leave>", on_leave_equi)

    # Descripción de los gráficos
    descripcion_frame = Frame(control_frame, bg="#f8f9fa", relief="solid", bd=1)
    descripcion_frame.pack(fill="x", pady=(10, 5), padx=20)
    
    descripcion_label = Label(descripcion_frame, text="",
                             font=("Arial", 10), bg="#f8f9fa", fg="#34495e",
                             justify="left")
    descripcion_label.pack(pady=5, padx=10)
    
    # Función para actualizar descripción
    def actualizar_descripcion():
        if grafico_actual["valor"] == 0:
            descripcion_text = "• Muestra el potencial eléctrico V(x,y) como función 2D\n• Visualización superficial del potencial en el plano"
        else:
            descripcion_text = "• Curvas equipotenciales: líneas de potencial constante\n• El gradiente de V es perpendicular a estas líneas"
        descripcion_label.config(text=descripcion_text)
    
    # Función combinada para cambiar gráfico y descripción
    def cambiar_grafico_potencial_con_descripcion(tipo_grafico):
        cambiar_grafico_potencial(tipo_grafico)
        actualizar_descripcion()

    # Frame para el canvas del gráfico
    canvas_frame = Frame(right_frame, bg="white")
    canvas_frame.pack(fill="both", expand=True, pady=10)

    # Mostrar inicialmente el primer gráfico
    cambiar_grafico_potencial_con_descripcion(0)

    # ===== BOTÓN CERRAR =====
    Button(ventana, text="Cerrar", command=ventana.destroy,
           font=("Arial", 14, "bold"), bg="#f0f0f0", 
           activebackground="#cfcfcf", width=15).pack(side="bottom", pady=15)



def calcular_potencial_predeterminado():
    """
    Carga la configuración predeterminada y calcula el potencial automáticamente con ventana completa.
    """
    cargar_configuracion_predeterminada()
    calcular_potencial()

def graficar_equipotenciales():
    """
    Genera un gráfico de superficies equipotenciales para las cargas configuradas.
    """
    try:
        # Obtener las cargas de la interfaz
        cargas = []
        
        # Carga 1
        try:
            carga1_val = float(carga1.get())
            x1, y1 = parsear_coordenadas(carga1_xy.get())
            cargas.append((carga1_val, x1, y1))
        except (ValueError, AttributeError):
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para la Carga 1")
            return
            
        # Carga 2
        try:
            carga2_val = float(carga2.get())
            x2, y2 = parsear_coordenadas(carga2_xy.get())
            cargas.append((carga2_val, x2, y2))
        except (ValueError, AttributeError):
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para la Carga 2")
            return
            
        # Carga 3
        try:
            carga3_val = float(carga3.get())
            x3, y3 = parsear_coordenadas(carga3_xy.get())
            cargas.append((carga3_val, x3, y3))
        except (ValueError, AttributeError):
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para la Carga 3")
            return
        
        # Filtrar cargas con valor absoluto menor a 1e-6
        cargas_filtradas = [(c, x, y) for c, x, y in cargas if abs(c) >= 1e-6]

        if not cargas_filtradas:
            messagebox.showinfo("Información", "No hay cargas significativas para graficar.")
            return

        # Mejorar margen dinámico
        x_vals = [x for _, x, _ in cargas_filtradas]
        y_vals = [y for _, _, y in cargas_filtradas]
        
        margen = 2.0  # Margen mínimo
        
        # Calcular el rango basándose en la dispersión de las cargas
        x_min, x_max = min(x_vals) - margen, max(x_vals) + margen
        y_min, y_max = min(y_vals) - margen, max(y_vals) + margen
        
        # El rango del gráfico será el mayor entre el rango x e y para mantener la proporción
        rango_max = max(x_max - x_min, y_max - y_min) / 2
        centro_x = (min(x_vals) + max(x_vals)) / 2
        centro_y = (min(y_vals) + max(y_vals)) / 2
        
        rango = (centro_x - rango_max - margen, centro_x + rango_max + margen)

        # Generar el gráfico con las cargas filtradas
        try:
            from logic import graficar_superficies_equipotenciales
            filepath = graficar_superficies_equipotenciales(cargas_filtradas, rango=rango)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Gráfico de superficies equipotenciales guardado en:\n{filepath}")
            
            # Mostrar la imagen generada en una nueva ventana
            mostrar_imagen(filepath, "Superficies Equipotenciales")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {str(e)}")

def mostrar_imagen(filepath, title="Imagen"):
    """Muestra una imagen en una nueva ventana redimensionándola a la pantalla."""
    try:
        # Crear ventana
        ventana = Toplevel()
        ventana.title(title)
        ventana.update_idletasks()  # asegurar métricas de pantalla
        
        # Tamaño máximo permitido (85% de la pantalla)
        max_w = int(ventana.winfo_screenwidth() * 0.85)
        max_h = int(ventana.winfo_screenheight() * 0.85)
        
        # Cargar imagen
        # Asegurarse de que la ruta sea absoluta
        if not os.path.isabs(filepath):
            project_root = os.path.dirname(os.path.dirname(__file__))
            filepath = os.path.join(project_root, filepath)

        img = Image.open(filepath)
        # Redimensionar manteniendo relación de aspecto si excede el tamaño permitido
        if img.width > max_w or img.height > max_h:
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img)
        
        # Mantener referencia a la imagen
        global photo_references
        photo_references.append(photo)
        
        # Mostrar imagen
        label = Label(ventana, image=photo)
        label.pack(padx=10, pady=10)
        
        # Ajustar tamaño de la ventana a la imagen
        ventana.geometry(f"{img.width + 40}x{img.height + 80}")
        ventana.minsize(300, 200)
        
        # Botón para cerrar
        btn_cerrar = Button(ventana, text="Cerrar", command=ventana.destroy)
        btn_cerrar.pack(pady=10)
        
        ventana.lift()
        ventana.focus_force()
    
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se pudo encontrar la imagen en la ruta: {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

def calcular_potencial_solo_ui():
    """
    Calcula el potencial eléctrico y muestra solo el resultado en la UI principal (sin ventana emergente).
    """
    print("Función calcular_potencial_solo_ui llamada")

    # Obtener valores de las cargas (igual validación que para campo eléctrico)
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
    
    # Obtener punto donde calcular el potencial
    try:
        punto_str = entry_punto.get().strip()
        if not punto_str:
            messagebox.showerror("Error", "Por favor ingrese el punto donde calcular el potencial")
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
    
    # Calcular el potencial eléctrico total en el punto especificado
    try:
        V_total = calcular_potencial_total(cargas, x_punto, y_punto)
        
        # Mostrar resultado numérico solo en una ventana emergente
        mostrar_resultado_potencial_numerico(cargas, x_punto, y_punto, V_total)
        
        print(f"Cargas: {cargas}")
        print(f"Punto: ({x_punto}, {y_punto})")
        print(f"Potencial eléctrico: V = {V_total:.2e} V")
        
    except Exception as e:
        messagebox.showerror("Error de cálculo", f"Error al calcular el potencial eléctrico: {str(e)}")
        print(f"Error: {e}")

def crear_interfaz():
    global carga1, carga2, carga3, carga1_xy, carga2_xy, carga3_xy, entry_punto, label_resultado, frame_cargas

    root = Tk()
    root.title("Laboratorio Computacional 1 - Física")
    root.geometry("1000x500")
    
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
    
    # Frame para los botones de configuración
    config_frame = Frame(root)
    config_frame.grid(row=4, column=0, columnspan=4, pady=10)
    
    # Botón para cargar configuración predeterminada
    Button(config_frame, text="Cargar Configuración Predeterminada", 
           command=cargar_configuracion_predeterminada,
           font=('Arial', 10), bg='lightgreen', pady=5).pack(pady=5)
    
    # Frame para los botones de Campo Eléctrico
    campo_frame = Frame(root)
    campo_frame.grid(row=5, column=0, columnspan=4, pady=10)
    
    Label(campo_frame, text="CAMPO ELÉCTRICO E(x,y)", 
          font=('Arial', 12, 'bold'), fg='#2c3e50').pack(pady=(0,5))
    
    # Botones de campo eléctrico
    buttons_campo_frame = Frame(campo_frame)
    buttons_campo_frame.pack()
    
    Button(buttons_campo_frame, text="Calcular Campo con Config. Predeterminada", 
           command=calcular_y_graficar_predeterminado,
           font=('Arial', 10), bg='lightcoral', pady=5).pack(side='left', padx=5)
    
    Button(buttons_campo_frame, text="Calcular Campo Eléctrico", 
           command=calcular_graficar,
           font=('Arial', 10), bg='lightblue', pady=5).pack(side='left', padx=5)
    
    # Frame para los botones de Potencial Eléctrico
    potencial_frame = Frame(root)
    potencial_frame.grid(row=6, column=0, columnspan=4, pady=10)
    
    Label(potencial_frame, text="POTENCIAL ELÉCTRICO V(x,y)", 
          font=('Arial', 12, 'bold'), fg='#27ae60').pack(pady=(0,5))
    
    # Botones de potencial eléctrico
    buttons_potencial_frame = Frame(potencial_frame)
    buttons_potencial_frame.pack()
    
    Button(buttons_potencial_frame, text="Calcular Potencial con Config. Predeterminada", 
           command=calcular_potencial_predeterminado,
           font=('Arial', 10), bg='lightyellow', pady=5).pack(side='left', padx=5)
    
    Button(buttons_potencial_frame, text="Calcular Potencial Eléctrico", 
           command=calcular_potencial,
           font=('Arial', 10), bg='lightcyan', pady=5).pack(side='left', padx=5)
    
    # Frame para el botón de Superficies Equipotenciales
    equipotencial_frame = Frame(root)
    equipotencial_frame.grid(row=7, column=0, columnspan=4, pady=10)
    
    Label(equipotencial_frame, text="SUPERFICIES EQUIPOTENCIALES", 
          font=('Arial', 12, 'bold'), fg='#8e44ad').pack(pady=(0,5))
    
    # Botón para graficar superficies equipotenciales
    Button(equipotencial_frame, text="Graficar Superficies Equipotenciales", 
           command=graficar_equipotenciales,
           font=('Arial', 10, 'bold'), bg='#e6c9ff', pady=8).pack(pady=5)

    # Instrucciones para el usuario
    instrucciones_frame = Frame(root)
    instrucciones_frame.grid(row=8, column=0, columnspan=4, pady=10)
    
    instrucciones_text = ("Instrucciones:\n"
                         "• Use 'Cargar Configuración Predeterminada' para cargar valores de ejemplo\n"
                         "• CAMPO ELÉCTRICO: Calcula E(x,y) y genera gráficos de E(x) vs x y líneas de campo\n"
                         "• POTENCIAL ELÉCTRICO: Calcula V(x,y) numéricamente (resultado en ventana emergente)\n"
                         "• SUPERFICIES EQUIPOTENCIALES: Genera un gráfico de contorno del potencial eléctrico\n"
                         "• Formato de cargas: notación científica (ej: 3e-6 para 3×10⁻⁶ C)\n"
                         "• Formato de coordenadas: x, y (ej: 0.1, 0.2)")
    
    Label(instrucciones_frame, text=instrucciones_text, font=('Arial', 9), 
          fg='gray', justify='left').pack()

    # Frame para el resultado (inicialmente vacío)
    label_resultado = Label(root, text="", font=('Arial', 12), fg='#FFFFFF', justify='left')
    label_resultado.grid(row=9, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    crear_interfaz()