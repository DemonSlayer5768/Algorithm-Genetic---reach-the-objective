# Algoritmo Genético - Navegación hacia un Objetivo

## 📋 Objetivo

Este proyecto implementa un **algoritmo genético** que evoluciona una población de agentes virtuales para encontrar el camino más eficiente hacia un objetivo en un entorno con obstáculos. Los individuos "aprenden" a través de generaciones sucesivas, mejorando gradualmente hasta que consiguen alcanzar la meta.

---

## 🧬 ¿Qué es un Algoritmo Genético?

Un algoritmo genético es una técnica de **optimización inspirada en la evolución biológica natural**. Funciona simulando el proceso de selección natural de Darwin:

1. **Población inicial**: Se crea un grupo de soluciones (individuos) aleatorias
2. **Evaluación (fitness)**: Se califica qué tan buena es cada solución
3. **Selección**: Los mejores individuos son elegidos para reproducirse
4. **Cruzamiento**: Se combinan genes de dos padres para crear hijos
5. **Mutación**: Se introducen cambios aleatorios para explorar nuevas soluciones
6. **Nuevo ciclo**: El proceso se repite hasta encontrar una buena solución

**Aplicaciones reales**: Aviación, ingeniería, medicina, inteligencia artificial, diseño de redes, etc.

---

## 🎮 Funcionamiento en este Proyecto

### El Entorno
- **Pantalla**: 1000x650 píxeles
- **Inicio**: Centro inferior (agentes comienzan aquí) 🟢
- **Objetivo**: Centro superior (meta a alcanzar) 🔴
- **Obstáculos**: Dos barreras grises que bloquean el camino directo

### Los Individuos (Agentes)
Cada individuo es un "ser" con características:

```
Posición inicial: Centro inferior
Velocidad: Comienza en (0, 0)
Genes: 800 genes (pasos de movimiento)
      Cada gen es un vector de fuerza (vx, vy)
```

Cada paso:
1. Se aplica un gene (fuerza) a la velocidad
2. La velocidad se normaliza a máximo 4 píxeles/frame
3. Se actualiza la posición
4. Se verifica colisiones con obstáculos y límites

### El Proceso Evolutivo

#### 1️⃣ **Generación Inicial**
- 500 individuos con genes aleatorios
- La mayoría muere rápidamente sin avanzar

#### 2️⃣ **Evaluación del Fitness**
Se califica cada individuo con base en:
- **Progreso (5.0×)**: Qué tan cerca llegó del objetivo
  - `fitness_progreso = 1 / (distancia_mínima + 1)`
- **Logro (30.0×)**: ¿Tocó el objetivo? (+30 puntos si sí)
- **Eficiencia (0.5×)**: Cuántos pasos usó (menos pasos = mejor)
- **Suavidad (0.1×)**: Cambios de dirección (camino más recto)
- **Colisiones (-3.0×)**: Penalización por chocar obstáculos

#### 3️⃣ **Selección Natural**
- Se seleccionan los **10 mejores individuos** (élite)
- Usamos **ruleta de selección**: mejor fitness = mayor probabilidad
- Estos serán los "padres" de la siguiente generación

#### 4️⃣ **Reproducción**
```
Padres → Hijos (con sus genes copiados)
           ↓
Nuevos padres + Cruzamiento de genes
           ↓
Mutaciones aleatorias para explorar
           ↓
Nueva generación de 500 individuos
```

**Cruzamiento**: Se toma genes del padre A hasta el punto de corte, luego del padre B
```
Padre A: [gen1, gen2, gen3, gen4, gen5]
Padre B: [gen1', gen2', gen3', gen4', gen5']
         ↓ punto de corte = 3
Hijo:    [gen1, gen2, gen3, gen4', gen5']  ← combina ambos
```

**Mutación**: El 8% de los genes mutan (cambian a valores aleatorios)
```
Antes: genes = [fuerza1, fuerza2, fuerza3, ...]
Después: genes = [fuerza1, NUEVA_FUERZA, fuerza3, ...]
```

#### 5️⃣ **Evolución**
- Con cada generación, la población mejora
- Los individuos que se acercan más al objetivo tienen más hijos
- Eventualmente, algunos cruzan sistemas de obstáculos
- **Generación X**: Algunos llegan al objetivo 🔴

---

## 📊 Parámetros Configurables

En [config.py](src/config.py):

```python
POBLACION = 500          # Individuos por generación
PASOS = 800              # Pasos máximos por individuo
GENERACIONES = 10        # Generaciones a simular (aprox.)

ELITISMO = 10            # Mejores individuos seleccionados
TASA_MUTACION = 0.08     # 8% de genes mutan por generación
FUERZA_MAX = 8.0         # Fuerzas máximas en cada dirección
```

### Impacto de los parámetros:

| Parámetro | Aumentar | Disminuir |
|-----------|----------|-----------|
| **POBLACION** | Más diversidad, mejor exploración | Evolución más rápida |
| **PASOS** | Más tiempo para llegar | Menos tiempo de vida |
| **ELITISMO** | Menos cambios, converge rápido | Más innovación |
| **TASA_MUTACION** | Más exploración, menos convergencia | Convergencia rápida a local |
| **FUERZA_MAX** | Mayor velocidad, movimientos amplios | Movimientos más finos |

---

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.8+
- pygame

### Instalación
```bash
# En la raíz del proyecto
python -m venv env              # Crear entorno virtual
env\Scripts\activate            # Activar (Windows)
# o: source env/bin/activate   # (Linux/Mac)

pip install pygame
```

### Ejecución
```bash
cd src
python main.py
```

**Lo que verás:**
- 🔴 Objetivo rojo en el centro superior
- 🔵 Individuos vivos (azules) moviéndose
- 🟢 Mejor individuo de la generación (verde)
- 🟦 Obstáculos grises bloqueando el camino
- **Generación actual** y **mejor fitness** en la esquina

---

## 📁 Estructura del Código

```
src/
├── main.py         # Bucle principal de simulación y renderizado
├── individuo.py    # Clase Individuo (agente con genes)
├── genetico.py     # Funciones de selección, cruzamiento y mutación
├── entorno.py      # Definición del mapa (obstáculos, inicio, objetivo)
└── config.py       # Parámetros configurables
```

### Flujo del Programa

```
1. INICIALIZACIÓN
   ├─ Crear 500 individuos aleatorios
   └─ Mostrar pantalla

2. CICLO PRINCIPAL (cada frame)
   ├─ Procesar eventos (cerrar ventana)
   ├─ Actualizar posiciones de individuos
   ├─ Dibujar mundo, obstáculos, objetivo
   ├─ ¿Todos los individuos están muertos?
   │  └─ SÍ:
   │     ├─ Calcular fitness de cada uno
   │     ├─ Seleccionar élite (10 mejores)
   │     ├─ Reproducir con cruzamiento
   │     ├─ Aplicar mutaciones
   │     └─ Crear nueva población
   └─ Repetir

3. TERMINA CUANDO: El usuario cierra la ventana
```

---

## 🔍 Lo Que Verás Evolucionar

### Generación 1-5
- Individuos se mueven aleatoriamente
- Raros alcanzan el primer obstáculo
- Algunos caen fuera del mapa

### Generación 6-15
- Primeros individuos esquivan el primer obstáculo
- Mejor orientación general hacia el objetivo
- Fitness promedio aumenta notablemente

### Generación 20+
- Soluciones robustas para ambos obstáculos
- Individuos llegan consistentemente al objetivo
- El camino se vuelve más directo y eficiente

---

## 🎯 Conceptos Clave

| Concepto | Significado | En este proyecto |
|----------|------------|------------------|
| **Gen** | Unidad básica de información hereditaria | Vector de fuerza (vx, vy) |
| **Cromosoma** | Conjunto de genes | 800 genes = 800 pasos |
| **Fenotipo** | Características observables | Posición, velocidad, ruta |
| **Fitness** | Qué tan apto es para el entorno | Distancia al objetivo, colisiones |
| **Selección natural** | Sobreviven los más aptos | Mejores 10 individuos se reproducen |
| **Cruzamiento** | Combinación de dos padres | Genes de papá A o mamá B |
| **Mutación** | Cambio aleatorio de genes | 8% de genes se cambian |

---

## 💡 Experimentación

Prueba modificar estos valores en [config.py](src/config.py):

```python
# Experimento 1: Evolución rápida
POBLACION = 1000
ELITISMO = 20
TASA_MUTACION = 0.05

# Experimento 2: Máxima exploración
TASA_MUTACION = 0.2
FUERZA_MAX = 10.0

# Experimento 3: Menos tiempo, máxima intensidad
PASOS = 500
POBLACION = 1000
```

**Observa cómo cambia el comportamiento**:
- ¿Converge más rápido o lento?
- ¿Encuentran soluciones mejores?
- ¿Cuál es el balance óptimo?

---

## 📚 Lectura Adicional

- **Algoritmos Genéticos**: Goldberg, D. E. (1989)
- **Computación Evolutiva**: Eiben & Smith
- **Pygame Documentation**: [pygame.org](https://www.pygame.org)

---

**Creado con 🧬 para la carrera de Ingeniería en Sistemas - CUCEI**
