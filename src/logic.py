"""
logic.py
Funciones de física para el proyecto de Física 2 IS.
"""
from fileinput import filename
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
from scipy.optimize import brentq
from scipy.integrate import odeint

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

def calcular_potencial_electrico(carga, x_carga, y_carga, x_punto, y_punto):
    """
    Calcula el potencial eléctrico debido a una carga puntual en un punto específico.
    
    Parámetros:
    - carga: magnitud de la carga [C]
    - x_carga, y_carga: posición de la carga [m]
    - x_punto, y_punto: punto donde se calcula el potencial [m]
    
    Retorna: V - potencial eléctrico [V]
    """
    # Calcular la distancia entre la carga y el punto
    dx = x_punto - x_carga
    dy = y_punto - y_carga
    r = np.sqrt(dx**2 + dy**2)
    
    # Evitar división por cero
    if r == 0:
        return float('inf') if carga > 0 else float('-inf')
    
    # Calcular el potencial eléctrico usando V = k*q/r
    V = K * carga / r
    
    return V

def calcular_potencial_total(cargas, x_punto, y_punto):
    """
    Calcula el potencial eléctrico total en un punto debido a múltiples cargas.
    Aplica el principio de superposición.
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - x_punto, y_punto: punto donde se calcula el potencial [m]
    
    Retorna: V_total - potencial eléctrico total [V]
    """
    V_total = 0.0
    distancia_minima = 1e-6  # Distancia mínima para evitar singularidades (1 micrómetro)
    
    # Aplicar principio de superposición
    for carga, x_carga, y_carga in cargas:
        # Calcular distancia
        dx = x_punto - x_carga
        dy = y_punto - y_carga
        r = np.sqrt(dx**2 + dy**2)
        
        # Si el punto está muy cerca de una carga, usar distancia mínima
        if r < distancia_minima:
            if r == 0:
                return float('inf') if carga > 0 else float('-inf')
            else:
                r = distancia_minima
        
        # Calcular potencial de esta carga
        V = K * carga / r
        V_total += V
    
    return V_total

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

def formatear_resultado_potencial(V_total):
    """
    Formatea el resultado del potencial eléctrico para mostrar en la interfaz.
    
    Retorna: string formateado con el resultado
    """
    if np.isinf(V_total):
        resultado = "Potencial Eléctrico:\n"
        resultado += "V = ∞ (punto coincide con una carga)"
    else:
        resultado = "Potencial Eléctrico:\n"
        resultado += f"V = {V_total:.2e} V"
    
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

def encontrar_puntos_equilibrio(cargas, rango_x=(-5, 5)):
    """
    Encuentra los puntos de equilibrio en el eje x donde E(x) = 0 analíticamente.
    
    Para 3 cargas, la ecuación es:
    E(x) = k*q1*(x-x1)/|x-x1|³ + k*q2*(x-x2)/|x-x2|³ + k*q3*(x-x3)/|x-x3|³ = 0
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - rango_x: tupla (x_min, x_max) para buscar puntos de equilibrio
    
    Retorna: lista de puntos de equilibrio [(x1, estabilidad1), (x2, estabilidad2), ...]
    """
    puntos_equilibrio = []
    
    # Extraer información de las cargas
    q = [carga[0] for carga in cargas]  # cargas
    x_pos = [carga[1] for carga in cargas]  # posiciones x
    y_pos = [carga[2] for carga in cargas]  # posiciones y
    
    # Ordenar cargas por posición x para análisis sistemático
    datos_ordenados = sorted(zip(q, x_pos, y_pos), key=lambda item: item[1])
    q_ord, x_ord, y_ord = zip(*datos_ordenados)
    
    def campo_en_x(x):
        """Calcula E(x) en el punto x sobre el eje y=0"""
        Ex_total = 0
        for i in range(3):
            dx = x - x_ord[i]
            dy = 0 - y_ord[i]  # y = 0 en el eje x
            r = np.sqrt(dx**2 + dy**2)
            if r > 1e-10:  # Evitar división por cero
                Ex_total += K * q_ord[i] * dx / (r**3)
        return Ex_total
    
    # Buscar puntos de equilibrio en intervalos específicos
    intervalos = [
        (rango_x[0], x_ord[0] - 0.01),      # Antes de la primera carga
        (x_ord[0] + 0.01, x_ord[1] - 0.01), # Entre primera y segunda carga
        (x_ord[1] + 0.01, x_ord[2] - 0.01), # Entre segunda y tercera carga
        (x_ord[2] + 0.01, rango_x[1])       # Después de la tercera carga
    ]
    
    for x_min, x_max in intervalos:
        if x_max <= x_min:
            continue
            
        try:
            # Evaluar el campo en los extremos del intervalo
            E_min = campo_en_x(x_min)
            E_max = campo_en_x(x_max)
            
            # Si hay cambio de signo, existe un punto de equilibrio
            if E_min * E_max < 0:
                x_eq = brentq(campo_en_x, x_min, x_max)
                
                # Verificar que el punto esté en el rango solicitado
                if rango_x[0] <= x_eq <= rango_x[1]:
                    # Analizar la estabilidad del punto de equilibrio
                    estabilidad = analizar_estabilidad_equilibrio(cargas, x_eq)
                    puntos_equilibrio.append((x_eq, estabilidad))
                    
        except (ValueError, RuntimeError):
            # No hay raíz en este intervalo o error numérico
            continue
    
    # Ordenar por posición x
    puntos_equilibrio.sort(key=lambda p: p[0])
    
    return puntos_equilibrio

def analizar_estabilidad_equilibrio(cargas, x_eq, delta=1e-4):
    """
    Analiza la estabilidad de un punto de equilibrio.
    
    Parámetros:
    - cargas: lista de cargas
    - x_eq: posición x del punto de equilibrio
    - delta: pequeño desplazamiento para analizar estabilidad
    
    Retorna: 'estable', 'inestable' o 'neutral'
    """
    # Calcular campo a la izquierda y derecha del punto de equilibrio
    Ex_izq, _, _, _ = calcular_campo_total(cargas, x_eq - delta, 0.0)
    Ex_der, _, _, _ = calcular_campo_total(cargas, x_eq + delta, 0.0)
    
    # Si el campo apunta hacia el punto de equilibrio desde ambos lados, es estable
    if Ex_izq > 0 and Ex_der < 0:
        return 'estable'
    elif Ex_izq < 0 and Ex_der > 0:
        return 'inestable'
    else:
        return 'neutral'

def graficar_campo_electrico(cargas, x_punto, y_punto, rango_x=(-5, 5), num_puntos=1000):
    """
    Genera el gráfico de E(x) vs x para cargas individuales y superposición.
    Incluye detección y marcado de puntos de equilibrio.
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - x_punto, y_punto: punto donde se calculó el campo
    - rango_x: tupla (x_min, x_max) para el rango del gráfico
    - num_puntos: número de puntos para el gráfico
    
    Retorna: (path del archivo guardado, lista de puntos de equilibrio)
    """
    x_values = np.linspace(rango_x[0], rango_x[1], num_puntos)
    
    # Encontrar puntos de equilibrio
    puntos_equilibrio = encontrar_puntos_equilibrio(cargas, rango_x)
    
    # Crear la figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Campo Eléctrico E(x) vs x - Análisis de Equilibrio', fontsize=16, fontweight='bold')
    
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
    
    # Segundo subplot: Superposición con puntos de equilibrio
    ax2.set_title('Superposición - Detección de Puntos de Equilibrio')
    
    # Calcular campo total
    Ex_total_values = np.zeros_like(x_values)
    for x_val in range(len(x_values)):
        Ex_total, _, _, _ = calcular_campo_total(cargas, x_values[x_val], 0.0)
        Ex_total_values[x_val] = Ex_total
    
    ax2.plot(x_values, Ex_total_values, color='purple', linewidth=3, 
             label='Campo Total (Superposición)')
    
    # Marcar puntos de equilibrio
    if puntos_equilibrio:
        x_eq_list = [p[0] for p in puntos_equilibrio]
        y_eq_list = [0 for _ in puntos_equilibrio]  # Los puntos de equilibrio están en Ex = 0
        
        ax2.scatter(x_eq_list, y_eq_list, color='red', s=100, marker='o', 
                   zorder=5, label=f'Puntos de Equilibrio ({len(puntos_equilibrio)})')
        
        # Anotar cada punto de equilibrio
        for i, (x_eq, estabilidad) in enumerate(puntos_equilibrio):
            color_est = {'estable': 'green', 'inestable': 'red', 'neutral': 'orange'}[estabilidad]
            
            ax2.annotate(f'Eq{i+1}: x={x_eq:.3f}m\n({estabilidad})', 
                        xy=(x_eq, 0), xytext=(x_eq, max(Ex_total_values)*0.3),
                        arrowprops=dict(arrowstyle='->', color=color_est, lw=2),
                        fontsize=10, ha='center',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor=color_est, alpha=0.3))
    
    # Marcar el punto donde se calculó el campo
    if rango_x[0] <= x_punto <= rango_x[1]:
        Ex_punto, _, _, _ = calcular_campo_total(cargas, x_punto, y_punto)
        ax2.plot(x_punto, Ex_punto, 'bo', markersize=8, 
                label=f'Punto calculado ({x_punto}, {y_punto})')
    
    ax2.set_xlabel('x [m]')
    ax2.set_ylabel('Ex [N/C]')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.axhline(y=0, color='black', linewidth=1, linestyle='-', alpha=0.8)
    
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
    
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    return filepath, puntos_equilibrio

def graficar_lineas_campo(cargas, x_punto, y_punto, rango=(-3, 3), resolucion=20):
    """
    Genera el gráfico de líneas de campo eléctrico resultante.
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - x_punto, y_punto: punto donde se calculó el campo
    - rango: tupla (min, max) para el rango del gráfico
    - resolucion: número de puntos de inicio para líneas de campo
    
    Retorna: path del archivo guardado
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    def campo_en_punto(x, y):
        """Calcula las componentes del campo eléctrico en un punto"""
        Ex, Ey, _, _ = calcular_campo_total(cargas, x, y)
        return Ex, Ey
    
    def ecuacion_linea_campo(r, t):
        """Ecuación diferencial para las líneas de campo"""
        x, y = r
        Ex, Ey = campo_en_punto(x, y)
        magnitud = np.sqrt(Ex**2 + Ey**2)
        if magnitud == 0:
            return [0, 0]
        return [Ex/magnitud, Ey/magnitud]
    
    # Generar grid de puntos iniciales para las líneas de campo
    n_lineas = resolucion
    
    # Para cada carga positiva, generar líneas radiales hacia afuera
    for q, x_carga, y_carga in cargas:
        if q > 0:  # Carga positiva - líneas salen
            angulos = np.linspace(0, 2*np.pi, n_lineas, endpoint=False)
            for angulo in angulos:
                # Punto inicial cercano a la carga
                x_inicio = x_carga + 0.05 * np.cos(angulo)
                y_inicio = y_carga + 0.05 * np.sin(angulo)
                
                # Integrar hacia adelante
                t = np.linspace(0, 2, 200)
                try:
                    trayectoria = odeint(ecuacion_linea_campo, [x_inicio, y_inicio], t)
                    x_traj, y_traj = trayectoria[:, 0], trayectoria[:, 1]
                    
                    # Filtrar puntos dentro del rango
                    mask = (x_traj >= rango[0]) & (x_traj <= rango[1]) & \
                           (y_traj >= rango[0]) & (y_traj <= rango[1])
                    
                    if np.any(mask):
                        ax.plot(x_traj[mask], y_traj[mask], 'b-', alpha=0.6, linewidth=0.8)
                        
                        # Agregar flechas para indicar dirección
                        if len(x_traj[mask]) > 10:
                            idx_medio = len(x_traj[mask]) // 2
                            dx = x_traj[mask][idx_medio+1] - x_traj[mask][idx_medio-1]
                            dy = y_traj[mask][idx_medio+1] - y_traj[mask][idx_medio-1]
                            ax.arrow(x_traj[mask][idx_medio], y_traj[mask][idx_medio], 
                                   dx*0.1, dy*0.1, head_width=0.05, head_length=0.05, 
                                   fc='blue', ec='blue', alpha=0.8)
                except:
                    continue
        
        else:  # Carga negativa - líneas entran
            angulos = np.linspace(0, 2*np.pi, n_lineas, endpoint=False)
            for angulo in angulos:
                # Punto inicial alejado de la carga
                x_inicio = x_carga + 1.5 * np.cos(angulo)
                y_inicio = y_carga + 1.5 * np.sin(angulo)
                
                # Verificar que el punto esté en el rango
                if not (rango[0] <= x_inicio <= rango[1] and rango[0] <= y_inicio <= rango[1]):
                    continue
                
                # Integrar hacia atrás (hacia la carga negativa)
                t = np.linspace(0, -2, 200)
                try:
                    trayectoria = odeint(ecuacion_linea_campo, [x_inicio, y_inicio], t)
                    x_traj, y_traj = trayectoria[:, 0], trayectoria[:, 1]
                    
                    # Filtrar puntos dentro del rango
                    mask = (x_traj >= rango[0]) & (x_traj <= rango[1]) & \
                           (y_traj >= rango[0]) & (y_traj <= rango[1])
                    
                    if np.any(mask):
                        ax.plot(x_traj[mask], y_traj[mask], 'r-', alpha=0.6, linewidth=0.8)
                        
                        # Agregar flechas para indicar dirección
                        if len(x_traj[mask]) > 10:
                            idx_medio = len(x_traj[mask]) // 2
                            dx = x_traj[mask][idx_medio+1] - x_traj[mask][idx_medio-1]
                            dy = y_traj[mask][idx_medio+1] - y_traj[mask][idx_medio-1]
                            ax.arrow(x_traj[mask][idx_medio], y_traj[mask][idx_medio], 
                                   dx*0.1, dy*0.1, head_width=0.05, head_length=0.05, 
                                   fc='red', ec='red', alpha=0.8)
                except:
                    continue
    
    # Marcar las cargas
    for i, (q, x_carga, y_carga) in enumerate(cargas):
        color = 'red' if q > 0 else 'blue'
        symbol = '+' if q > 0 else '-'
        ax.plot(x_carga, y_carga, 'o', color=color, markersize=12, markeredgecolor='black', linewidth=2)
        ax.text(x_carga, y_carga, symbol, ha='center', va='center', fontsize=16, fontweight='bold', color='white')
        ax.text(x_carga, y_carga + 0.2, f'q{i+1}={q:.1e}C', ha='center', va='bottom', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.3))
    
    # Marcar el punto de cálculo
    if rango[0] <= x_punto <= rango[1] and rango[0] <= y_punto <= rango[1]:
        ax.plot(x_punto, y_punto, 'ko', markersize=8, markeredgecolor='yellow', linewidth=2)
        ax.text(x_punto, y_punto + 0.15, f'P({x_punto}, {y_punto})', ha='center', va='bottom', 
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    
    # Configurar el gráfico
    ax.set_xlim(rango)
    ax.set_ylim(rango)
    ax.set_xlabel('x [m]', fontsize=14)
    ax.set_ylabel('y [m]', fontsize=14)
    ax.set_title('Líneas de Campo Eléctrico - Campo Resultante', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Agregar leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='blue', lw=2, label='Líneas desde cargas positivas'),
        Line2D([0], [0], color='red', lw=2, label='Líneas hacia cargas negativas'),
        Line2D([0], [0], marker='o', color='red', lw=0, markersize=8, label='Carga positiva'),
        Line2D([0], [0], marker='o', color='blue', lw=0, markersize=8, label='Carga negativa'),
        Line2D([0], [0], marker='o', color='black', lw=0, markersize=8, label='Punto de cálculo')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))

    plt.tight_layout()

    # Crear ruta absoluta para el directorio de gráficos
    project_root = os.path.dirname(os.path.dirname(__file__))
    graphics_dir = os.path.join(project_root, 'graphics')
    os.makedirs(graphics_dir, exist_ok=True)

    # Guardar la figura
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'lineas_campo_{timestamp}.png'
    filepath = os.path.join(graphics_dir, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

    return filepath

def graficar_superficies_equipotenciales(cargas, rango=(-5, 5), num_puntos=100, niveles=20):
    """
    Genera un gráfico de contorno que representa las superficies equipotenciales.

    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - rango: tupla (min, max) para el rango del gráfico en ambos ejes
    - num_puntos: número de puntos en cada dirección para la malla
    - niveles: número de curvas de nivel a mostrar

    Retorna: path del archivo guardado
    """
    # Crear malla de puntos
    x = np.linspace(rango[0], rango[1], num_puntos)
    y = np.linspace(rango[0], rango[1], num_puntos)
    X, Y = np.meshgrid(x, y)

    # Vectorizar el cálculo del potencial para mayor eficiencia
    V = np.zeros_like(X)
    for carga, x_carga, y_carga in cargas:
        dx = X - x_carga
        dy = Y - y_carga
        # Añadir un pequeño épsilon para evitar la división por cero en la posición exacta de la carga
        r = np.sqrt(dx**2 + dy**2) + 1e-9
        V += K * carga / r

    # Limitar los valores extremos del potencial para una mejor visualización de los contornos
    # Esto evita que los infinitos en las posiciones de las cargas dominen la escala de colores
    v_max = np.nanpercentile(V[np.isfinite(V)], 98)
    v_min = np.nanpercentile(V[np.isfinite(V)], 2)
    V = np.clip(V, v_min, v_max)

    # 4. Ajustar niveles de contorno para incluir siempre V=0
    max_abs_v = max(abs(v_min), abs(v_max))
    v_levels = np.linspace(-max_abs_v, max_abs_v, niveles)
    # Asegurarse de que el nivel 0.0 esté presente para visualizar la línea de potencial nulo
    if 0.0 not in v_levels:
        v_levels = np.sort(np.append(v_levels, 0.0))

    # Crear figura
    plt.figure(figsize=(10, 8))

    # Graficar contornos de potencial
    contorno = plt.contour(X, Y, V, levels=v_levels, colors='purple', linewidths=1, linestyles='solid')
    plt.clabel(contorno, inline=True, fontsize=8, fmt='%1.1f V')

    # 2. Validación en el bucle de dibujo de cargas
    for carga, x_carga, y_carga in cargas:
        if abs(carga) < 1e-9:  # Ignorar cargas prácticamente nulas
            continue
        color = 'red' if carga > 0 else 'blue'
        plt.scatter(x_carga, y_carga, color=color, s=100, edgecolors='black', zorder=5)
        plt.text(x_carga + 0.1, y_carga + 0.1, f'{carga:.1e} C', fontsize=9, 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    # Configuración del gráfico
    plt.title('Superficies Equipotenciales', pad=20)
    plt.xlabel('Posición X (m)')
    plt.ylabel('Posición Y (m)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.axis('equal')

    # Crear ruta absoluta para el directorio de gráficos
    project_root = os.path.dirname(os.path.dirname(__file__))
    graphics_dir = os.path.join(project_root, 'graphics')
    os.makedirs(graphics_dir, exist_ok=True)

    # Guardar la figura
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'equipotenciales_{timestamp}.png'
    filepath = os.path.join(graphics_dir, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    return filepath
    
    
def graficar_potencial(cargas, x_punto, y_punto, rango_x=(-5, 5), num_puntos=1000):
    x_values = np.linspace(rango_x[0], rango_x[1], num_puntos)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Potencial Eléctrico V(x) vs x', fontsize=16, fontweight='bold')

    colors = ['red', 'blue', 'green']
    todos_valores = []  # acá guardamos todos los valores para calcular min y max global

    # ---- Potenciales individuales ----
    ax1.set_title("Potenciales Individuales")
    for i, (carga, x_carga, y_carga) in enumerate(cargas):
        V_values = []
        for x in x_values:
            V = calcular_potencial_electrico(carga, x_carga, y_carga, x, 0)
            if np.isinf(V):
                V = np.nan
            V_values.append(V)
        V_values = np.array(V_values)
        todos_valores.extend(V_values[~np.isnan(V_values)])  # agregamos valores finitos
        ax1.plot(x_values, V_values, color=colors[i], linewidth=2,
                 label=f'Carga {i+1}: q={carga:.1e} C en ({x_carga},{y_carga})')
        ax1.axvline(x=x_carga, color=colors[i], linestyle='--', alpha=0.5)

    ax1.set_xlabel("x [m]")
    ax1.set_ylabel("V(x) [Voltios]")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color="black", linewidth=0.5)

    # ---- Superposición total ----
    ax2.set_title("Superposición de Potenciales")
    V_total_values = []
    for x in x_values:
        Vt = calcular_potencial_total(cargas, x, 0)
        if np.isinf(Vt):
            Vt = np.nan
        V_total_values.append(Vt)
    V_total_values = np.array(V_total_values)
    todos_valores.extend(V_total_values[~np.isnan(V_total_values)])

    ax2.plot(x_values, V_total_values, color="orange", linewidth=2,
             label="Potencial Total (Superposición)")
    ax2.set_xlabel("x [m]")
    ax2.set_ylabel("V(x) [Voltios]")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color="black", linewidth=0.8)

    # ---- Ajustar misma escala en y ----
    if todos_valores:
        y_min, y_max = min(todos_valores), max(todos_valores)
        ax1.set_ylim(y_min, y_max)
        ax2.set_ylim(y_min, y_max)

    plt.tight_layout()

    graphics_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics')
    if not os.path.exists(graphics_dir):
        os.makedirs(graphics_dir)

    filepath = os.path.join(graphics_dir, "potencial_vs_x.png")
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close()

    return filepath


def calcular_potencial_en_linea(cargas, x_inicio, x_fin, y_fijo=0, num_puntos=1000):
    """
    Calcula el potencial eléctrico a lo largo de una línea.
    
    Parámetros:
    - cargas: lista de tuplas [(carga1, x1, y1), (carga2, x2, y2), ...]
    - x_inicio, x_fin: rango x para el cálculo
    - y_fijo: valor fijo de y (por defecto 0 para el eje x)
    - num_puntos: número de puntos para el cálculo
    
    Retorna: (x_values, V_values) arrays de posición y potencial
    """
    x_values = np.linspace(x_inicio, x_fin, num_puntos)
    V_values = []
    
    for x in x_values:
        V = calcular_potencial_total(cargas, x, y_fijo)
        # Limitar valores extremos
        if np.isinf(V):
            V_values.append(np.nan)
        elif V > 1e6:
            V_values.append(1e6)
        elif V < -1e6:
            V_values.append(-1e6)
        else:
            V_values.append(V)
    
    return x_values, np.array(V_values)
