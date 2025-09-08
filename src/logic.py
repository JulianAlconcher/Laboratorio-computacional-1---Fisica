# -*- coding: utf-8 -*-
"""
Funciones básicas para el Laboratorio Computacional 1:
- Campo eléctrico E(x,y) por superposición
- Potencial eléctrico V(x,y)
- Cortes sobre el eje x
- Búsqueda de puntos de equilibrio sobre el eje x (Ex=0)

Formato de cargas: [(q, xq, yq), ...]
Unidades esperadas (SI): q en C, x,y en m.
"""
import numpy as np

K = 8.9875517923e9  # 1/(4πϵ0) [N·m²/C²]

def _clip_r(r: np.ndarray | float, eps: float = 1e-12):
    """Evita singularidades r→0."""
    return np.maximum(r, eps)

def E_point(charges, x: float, y: float):
    """Devuelve (Ex,Ey) en (x,y) por superposición de cargas puntuales."""
    Ex = 0.0
    Ey = 0.0
    for q, xq, yq in charges:
        dx = x - xq
        dy = y - yq
        r = _clip_r(np.hypot(dx, dy))
        Ex += K * q * dx / r**3
        Ey += K * q * dy / r**3
    return Ex, Ey

def V_point(charges, x: float, y: float):
    """Devuelve V(x,y) por superposición de cargas puntuales."""
    V = 0.0
    for q, xq, yq in charges:
        r = _clip_r(np.hypot(x - xq, y - yq))
        V += K * q / r
    return V

def E_on_x(charges, xs: np.ndarray):
    """Devuelve Ex(xs,0) como array (solo componente x sobre el eje x)."""
    return np.array([E_point(charges, x, 0.0)[0] for x in xs], dtype=float)

def V_on_x(charges, xs: np.ndarray):
    """Devuelve V(xs,0) como array (potencial sobre el eje x)."""
    return np.array([V_point(charges, x, 0.0) for x in xs], dtype=float)

def equilibria_on_x(charges, xs: np.ndarray, max_iter: int = 40):
    """
    Encuentra puntos de equilibrio sobre el eje x (Ex=0).
    1) Busca cambios de signo en Ex(x)
    2) Refina por bisección en cada intervalo que cambió de signo.
    """
    Exs = E_on_x(charges, xs)
    roots = []

    # detectar intervalos con cambio de signo
    for i in range(len(xs) - 1):
        a, b = xs[i], xs[i+1]
        fa, fb = Exs[i], Exs[i+1]

        if fa == 0.0:
            roots.append(a)
            continue
        if fa * fb > 0:
            continue  # no hay cambio de signo

        # bisección
        left, right = a, b
        fleft, fright = fa, fb
        for _ in range(max_iter):
            mid = 0.5 * (left + right)
            fmid = E_point(charges, mid, 0.0)[0]
            # elegimos el subintervalo que contiene el cambio de signo
            if fleft == 0.0:
                left = mid; fleft = fmid
            if fleft * fmid <= 0:
                right, fright = mid, fmid
            else:
                left, fleft = mid, fmid
        roots.append(0.5 * (left + right))

    # eliminar duplicados cercanos (si el muestreo fue muy fino)
    roots = np.array(sorted(roots), dtype=float)
    if roots.size == 0:
        return roots
    dedup = [roots[0]]
    for r in roots[1:]:
        if abs(r - dedup[-1]) > 1e-6:
            dedup.append(r)
    return np.array(dedup, dtype=float)
