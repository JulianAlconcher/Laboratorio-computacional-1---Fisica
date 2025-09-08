"""
logic.py
Funciones de física para el proyecto de Física 2 IS.
"""
import numpy as np

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
