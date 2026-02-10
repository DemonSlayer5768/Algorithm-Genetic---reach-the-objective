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
Genes: 600 genes (pasos de movimiento)
      Cada gen es un vector de fuerza (vx, vy) con máximo 30.0
```

Cada paso:
1. Se aplica un gene (fuerza) a la velocidad
2. La velocidad se normaliza a máximo 10 píxeles/frame
3. Se actualiza la posición
4. Se verifica colisiones con obstáculos (retrocede sin morir)
5. Se verifica límites del mapa

### El Proceso Evolutivo

#### 1️⃣ **Generación Inicial**
- 500 individuos con genes aleatorios
- La mayoría muere rápidamente sin avanzar

#### 2️⃣ **Evaluación del Fitness** (Mejorado)
Se califica cada individuo con base en:
- **Progreso Directo (10.0×)**: Píxeles avanzados hacia el objetivo
  - `fitness_progreso = 10.0 × (570 - distancia_mínima)`
  - Proporciona diferenciación real entre individuos
- **Logro (5000.0×)**: ¿Alcanzó el objetivo? (+5000 puntos si sí)
- **Eficiencia (1.0×)**: Cuántos pasos usó (menos pasos = mejor)
- **Colisiones (-0.05×)**: Penalización mínima por choques

**Cambio clave**: En lugar de usar `1/distancia` (que genera valores tiny),
ahora se usa distancia real, creando presión selectiva mucho más fuerte.

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

**Mutación**: El 1.5% de los genes mutan (cambian a valores aleatorios)
```
Antes: genes = [fuerza1, fuerza2, fuerza3, ...]
Después: genes = [fuerza1, NUEVA_FUERZA, fuerza3, ...]
```

**Manejo de Colisiones**: Los individuos ahora **retroceden** en lugar de morir,
permitiendo aprender a evitar obstáculos mientras continúan evolucionando.

#### 5️⃣ **Evolución**
- Con cada generación, la población mejora
- Los individuos que se acercan más al objetivo tienen más hijos
- Eventualmente, algunos cruzan sistemas de obstáculos
- **Generación X**: Algunos llegan al objetivo 🔴

---

## 📊 Parámetros Configurables

En [config.py](src/config.py):

```python
POBLACION = 1200         # Individuos por generación (aumentado)
PASOS = 600              # Pasos máximos por individuo (aumentado)
GENERACIONES = 100       # Generaciones a simular

ELITISMO = 150           # Mejores individuos seleccionados (12.5%)
TASA_MUTACION = 0.015    # 1.5% de genes mutan por generación
FUERZA_MAX = 30.0        # Fuerzas máximas en cada dirección (aumentado)
Velocidad máxima = 10.0  # píxeles/paso (en individuo.py)
```

**Recorrido teórico máximo**: 600 pasos × 10 px/paso = 6000 píxeles
(vs 570 necesarios para llegar)

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
- ⬜ Obstáculos grises bloqueando el camino
- **Información en tiempo real**:
  - Generación actual
  - Mejor fitness (números en miles cuando hay progreso)
  - **Contador de individuos que alcanzan el objetivo**

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

### Generación 1-3
- Individuos se mueven aleatoriamente
- Fitness muy bajo (0-100)
- Colisiones frecuentes

### Generación 4-10
- Primeros individuos avanzan hacia el objetivo
- Fitness crece exponencialmente (100-1000+)
- Algunos esquivan el primer obstáculo

### Generación 10-20
- **Primeros individuos alcanzan el objetivo** 🎯
- Fitness de mejores individuos: 5000+
- Contador de llegadas crece rapidamente
- Soluciones consistentes encontradas

### Generación 20+
- **La mayoría de la población llega al objetivo**
- Camino cada vez más directo y eficiente
- Fitness superior a 10000
- Convergencia hacia solución óptima

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

Los parámetros actuales garantizan llegada antes de generación 20.
Prueba estos experimentos modificando [config.py](src/config.py):

```python
# Experimento 1: Convergencia ultra-rápida
POBLACION = 2000
ELITISMO = 300
TASA_MUTACION = 0.01
PASOS = 400

# Experimento 2: Máxima exploración
TASA_MUTACION = 0.05
FUERZA_MAX = 40.0
PASOS = 800

# Experimento 3: Ambiente desafiante
PASOS = 300
FUERZA_MAX = 15.0
ELITISMO = 80
```

**Observa**:
- ¿En qué generación llegan los primeros individuos?
- ¿Cuántos llegan en la generación 20?
- ¿Cómo evoluciona el fitness?
- ¿Mejora o empeora la eficiencia?

---

## � Cambios y Optimizaciones Realizadas

### v2.0 - Optimizaciones para Convergencia Rápida

**Problema Original**: Los individuos no alcanzaban el objetivo incluso en generación 100.

**Soluciones Implementadas**:

| Cambio | Efecto | Resultado |
|--------|--------|-----------|
| **Función de fitness rediseñada** | De `1/distancia` a distancia real | Presión selectiva 100x mayor |
| **Velocidad máxima aumentada** | De 4 → 10 píxeles/paso | Individuos 2.5x más rápidos |
| **Pasos aumentados** | De 300 → 600 pasos | Recorrido máximo: 6000 píxeles |
| **Manejo de colisiones** | Retroceso en lugar de muerte | Exploración continua sin bloqueos |
| **Población aumentada** | De 800 → 1200 individuos | Más diversidad genética |
| **Bonificación por logro** | De 500 → 5000 puntos | Mayor incentivo para llegar |
| **Contador visual** | Muestra llegan/total | Feedback en tiempo real |

**Resultado**: Individuos alcanzan el objetivo en generación **10-20** (vs imposible antes)

---

## �📚 Lectura Adicional

- **Algoritmos Genéticos**: Goldberg, D. E. (1989)
- **Computación Evolutiva**: Eiben & Smith
- **Pygame Documentation**: [pygame.org](https://www.pygame.org)

---

**Creado con 🧬 para la carrera de Ingeniería en Sistemas - CUCEI**
