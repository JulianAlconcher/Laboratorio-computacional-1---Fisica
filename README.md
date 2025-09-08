# Laboratorio Computacional 1 - Física

## Descripción

Este proyecto simula el comportamiento de cargas eléctricas puntuales y calcula campos eléctricos y potenciales. El programa genera visualizaciones gráficas que incluyen:

- Campo eléctrico sobre el eje x (individual y total)
- Potencial eléctrico sobre el eje x (individual y total)
- Puntos de equilibrio
- Líneas de campo y equipotenciales en 2D

## Autores Principales
- **Julian Alconcher**
- **Antonio Carlos**
- otros...

## Estructura del Proyecto

```
├── README.md
├── requirements.txt
├── src/
│   ├── main.py          # Archivo principal de ejecución
│   └── logic.py         # Lógica de cálculos físicos
├── graphics/            # Carpeta para gráficos generados
└── .venv/              # Entorno virtual de Python
```

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/JulianAlconcher/Laboratorio-computacional-1---Fisica.git
cd Laboratorio-computacional-1---Fisica
```

### 2. Crear y activar el entorno virtual

#### En macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### En Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Cómo Ejecutar el Proyecto

### Ejecución desde la raíz del proyecto:

```bash
python src/main.py
```

### Ejecución desde la carpeta src:

```bash
cd src
python main.py
```
