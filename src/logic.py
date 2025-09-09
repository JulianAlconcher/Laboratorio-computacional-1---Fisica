"""
logic.py
Funciones de física para el proyecto de Física 2 IS.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# Constante de Coulomb [N·m²/C²]
K = 1 / (4 * np.pi * 8.854187817e-12)  # 1/(4πε₀)

def calcular_campo_electrico(carga, x_carga, y_carga, x_punto, y_punto):
    """
    Calcula el campo eléctrico debido a una carga puntual en un punto específico.
    
    Parámetros:
    - carga: magnitud de la carga [C]
    - x_carga, y_carga: posición de la carga [m]
    - x_punto, y_punto: punto donde se calcula el campo [m]
    
    Retorna: (Ex, Ey) componentes del campo eléctrico [N/C]
    """
    # Calcular la distancia entre la carga y el punto
    dx = x_punto - x_carga
    dy = y_punto - y_carga
    r = np.sqrt(dx**2 + dy**2)
    
    # Evitar división por cero
    if r == 0:
        return 0.0, 0.0
    
    # Calcular el campo eléctrico usando la ecuación (2)
    factor = K * carga / (r**3)
    Ex = factor * dx
    Ey = factor * dy
    
    return Ex, Ey

def calcular_campo_total(cargas, x_punto, y_punto):
    """
    Calcula el campo eléctrico total en un punto debido a múltiples cargas.
    Aplica el principio de superposición.
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - x_punto, y_punto: punto donde se calcula el campo [m]
    
    Retorna: (Ex_total, Ey_total, magnitud, angulo) 
    """
    Ex_total = 0.0
    Ey_total = 0.0
    
    # Aplicar principio de superposición
    for carga, x_carga, y_carga in cargas:
        Ex, Ey = calcular_campo_electrico(carga, x_carga, y_carga, x_punto, y_punto)
        Ex_total += Ex
        Ey_total += Ey
    
    # Calcular magnitud y ángulo del campo total
    magnitud = np.sqrt(Ex_total**2 + Ey_total**2)
    angulo = np.degrees(np.arctan2(Ey_total, Ex_total))
    
    return Ex_total, Ey_total, magnitud, angulo

def parsear_coordenadas(coord_str):
    """
    Parsea una cadena de coordenadas como "1.5, 2.3" o "1.5 2.3"
    
    Parámetros:
    - coord_str: string con las coordenadas
    
    Retorna: (x, y) como floats
    """
    try:
        # Reemplazar comas por espacios y dividir
        coords = coord_str.replace(',', ' ').split()
        if len(coords) != 2:
            raise ValueError("Deben ser exactamente 2 coordenadas")
        
        x = float(coords[0])
        y = float(coords[1])
        return x, y
    except (ValueError, IndexError):
        raise ValueError("Formato de coordenadas inválido. Use formato: 'x, y' o 'x y'")

def formatear_resultado(Ex, Ey, magnitud, angulo):
    """
    Formatea el resultado del campo eléctrico para mostrar en la interfaz.
    
    Retorna: string formateado con el resultado
    """
    resultado = f"Campo Eléctrico:\n"
    resultado += f"Ex = {Ex:.2e} N/C\n"
    resultado += f"Ey = {Ey:.2e} N/C\n"
    resultado += f"Magnitud = {magnitud:.2e} N/C\n"
    resultado += f"Ángulo = {angulo:.1f}°"
    
    return resultado

def calcular_campo_x(carga, x_carga, y_carga, x_values):
    """
    Calcula el campo eléctrico Ex para una carga a lo largo del eje x (y=0).
    
    Parámetros:
    - carga: magnitud de la carga [C]
    - x_carga, y_carga: posición de la carga [m]
    - x_values: array de valores x donde calcular el campo
    
    Retorna: array de valores Ex
    """
    Ex_values = []
    for x in x_values:
        Ex, _ = calcular_campo_electrico(carga, x_carga, y_carga, x, 0.0)
        Ex_values.append(Ex)
    return np.array(Ex_values)

def graficar_campo_electrico(cargas, x_punto, y_punto, rango_x=(-2, 2), num_puntos=1000):
    """
    Genera el gráfico de E(x) vs x para cargas individuales y superposición.
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - x_punto, y_punto: punto donde se calculó el campo
    - rango_x: tupla (x_min, x_max) para el rango del gráfico
    - num_puntos: número de puntos para el gráfico
    
    Retorna: path del archivo guardado
    """
    x_values = np.linspace(rango_x[0], rango_x[1], num_puntos)
    
    # Crear la figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Campo Eléctrico E(x) vs x', fontsize=16, fontweight='bold')
    
    # Primer subplot: Cargas individuales
    ax1.set_title('Cargas Individuales')
    colors = ['red', 'blue', 'green']
    
    for i, (carga, x_carga, y_carga) in enumerate(cargas):
        Ex_values = calcular_campo_x(carga, x_carga, y_carga, x_values)
        ax1.plot(x_values, Ex_values, color=colors[i], linewidth=2, 
                label=f'Carga {i+1}: q={carga:.1e} C en ({x_carga}, {y_carga})')
        
        # Marcar la posición de la carga
        ax1.axvline(x=x_carga, color=colors[i], linestyle='--', alpha=0.5)
    
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('Ex [N/C]')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.axhline(y=0, color='black', linewidth=0.5)
    
    # Segundo subplot: Superposición
    ax2.set_title('Superposición de las 3 cargas')
    
    # Calcular campo total
    Ex_total_values = np.zeros_like(x_values)
    for x_val in range(len(x_values)):
        Ex_total, _, _, _ = calcular_campo_total(cargas, x_values[x_val], 0.0)
        Ex_total_values[x_val] = Ex_total
    
    ax2.plot(x_values, Ex_total_values, color='purple', linewidth=3, 
             label='Campo Total (Superposición)')
    
    # Marcar el punto donde se calculó el campo
    if rango_x[0] <= x_punto <= rango_x[1]:
        Ex_punto, _, _, _ = calcular_campo_total(cargas, x_punto, y_punto)
        ax2.plot(x_punto, Ex_punto, 'ro', markersize=8, 
                label=f'Punto calculado ({x_punto}, {y_punto})')
    
    ax2.set_xlabel('x [m]')
    ax2.set_ylabel('Ex [N/C]')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.axhline(y=0, color='black', linewidth=0.5)
    
    # Marcar posiciones de las cargas en ambos subplots
    for i, (_, x_carga, _) in enumerate(cargas):
        ax2.axvline(x=x_carga, color=colors[i], linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar en la carpeta graphics
    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics')
    if not os.path.exists(graphics_dir):
        os.makedirs(graphics_dir)
    
    filename = 'campo_electrico_vs_x.png'
    filepath = os.path.join(graphics_dir, filename)
    
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    
    return filepath
