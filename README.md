# Galaxias

Juego arcade espacial desarrollado en Python con [Pygame](https://www.pygame.org/). El jugador controla una nave, dispara a los meteoritos que aparecen desde la parte superior de la pantalla y debe sobrevivir el mayor tiempo posible mientras aumenta su puntuación y avanza de nivel.

El proyecto está pensado como un ejemplo sencillo y didáctico de un videojuego 2D: todo el código se encuentra en `Galaga.py` y los gráficos se generan directamente con figuras de Pygame, por lo que no necesita imágenes, sonidos ni archivos adicionales.

## Características

- Ventana de juego de `800 × 600` píxeles.
- Bucle de juego limitado a `60 FPS`.
- Nave controlable con las flechas izquierda y derecha.
- Disparos con la barra espaciadora.
- Meteoritos generados aleatoriamente con:
  - Tamaños variables.
  - Colores y formas irregulares.
  - Movimiento horizontal y vertical.
  - Rebote en los bordes laterales.
- Sistema de puntuación:
  - Cada meteorito destruido otorga `10 puntos`.
- Sistema de niveles:
  - Se avanza de nivel al alcanzar `100 × nivel` puntos.
  - La velocidad de los meteoritos aumenta `0.5` por nivel.
  - La cantidad máxima de enemigos permitidos también aumenta con el nivel.
- Tres vidas iniciales.
- Efectos de explosión animados al destruir meteoritos.
- Tiempo de supervivencia visible durante la partida.
- Pantalla de menú inicial.
- Pantalla de fin de juego con puntuación y duración de la partida.
- Opción para reiniciar la partida sin cerrar la ventana.

## Requisitos

- Python 3.8 o superior.
- Pygame 2.x.
- Un sistema operativo compatible con la ventana gráfica de Pygame:
  - Windows
  - macOS
  - Linux

No se requieren imágenes, fuentes, sonidos ni otros recursos externos.

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Galaxias
```

Si ya tienes el proyecto descargado, entra directamente en la carpeta donde se encuentra `Galaga.py`.

### 2. Crear un entorno virtual (recomendado)

Crear un entorno virtual evita mezclar las dependencias de este juego con las de otros proyectos de Python.

#### Linux y macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows (Símbolo del sistema)

```bat
py -m venv .venv
.\.venv\Scripts\activate.bat
```

### 3. Instalar Pygame

```bash
python -m pip install pygame
```

En Windows también puedes usar:

```powershell
py -m pip install pygame
```

Para comprobar que Pygame está instalado correctamente:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

## Ejecutar el juego

Desde la carpeta del proyecto, ejecuta:

```bash
python Galaga.py
```

En Windows, si `python` no está disponible, utiliza:

```powershell
py Galaga.py
```

Se abrirá una ventana con el menú principal. Presiona cualquier tecla para comenzar.

## Controles

| Tecla | Acción |
|---|---|
| `←` | Mover la nave hacia la izquierda |
| `→` | Mover la nave hacia la derecha |
| `ESPACIO` | Disparar |
| `ESC` | Terminar la ronda actual y mostrar la pantalla de fin de juego |
| `R` | Reiniciar desde la pantalla de fin de juego |
| Cualquier tecla | Comenzar desde el menú principal |
| Cerrar la ventana | Salir del juego |

La nave solo se mueve horizontalmente y permanece dentro de los límites de la ventana.

## Cómo se juega

1. Inicia el programa.
2. Presiona cualquier tecla en el menú.
3. Mueve la nave con `←` y `→`.
4. Dispara a los meteoritos con `ESPACIO`.
5. Evita las colisiones con los meteoritos.
6. Destruye enemigos para conseguir puntos.
7. Al alcanzar la puntuación requerida, sube de nivel.
8. La partida termina cuando se pierden las tres vidas o se presiona `ESC`.
9. En la pantalla final, presiona `R` para volver a jugar o `ESC` para salir.

## Reglas y lógica del juego

### Puntuación y niveles

Cada meteorito destruido suma `10 puntos`. El nivel comienza en `1` y aumenta cuando la puntuación alcanza el umbral del nivel actual:

```text
umbral = 100 × nivel
```

Por ejemplo:

| Nivel actual | Puntuación necesaria para avanzar |
|---:|---:|
| 1 | 100 |
| 2 | 200 |
| 3 | 300 |

Al subir de nivel:

- La velocidad base de los enemigos aumenta en `0.5`.
- La cantidad máxima de enemigos pasa a ser `4 + nivel`.

### Meteoritos

Los meteoritos aparecen aleatoriamente en la parte superior de la pantalla. Cada uno tiene:

- Un tamaño aleatorio entre `30` y `50` píxeles.
- Una forma poligonal generada aleatoriamente.
- Un color elegido entre varias tonalidades.
- Una velocidad horizontal aleatoria.
- Una velocidad vertical aleatoria basada en la velocidad del nivel.

Cuando un meteorito toca un borde lateral, invierte su dirección horizontal. Si sale por la parte inferior, se elimina de la partida.

### Colisiones

El juego comprueba dos tipos principales de colisión:

- **Nave contra meteorito:** se pierde una vida y el meteorito desaparece.
- **Disparo contra meteorito:** ambos objetos desaparecen, se crea una explosión y se suman `10 puntos`.

Cuando las vidas llegan a cero, termina la ronda.

### Explosiones

Cada destrucción genera una animación de seis imágenes. La explosión cambia de tamaño cada tres fotogramas y se elimina automáticamente cuando termina la animación.

## Estructura del proyecto

```text
Galaxias/
├── Galaga.py     # Código completo del juego
└── README.md     # Documentación del proyecto
```

## Organización del código

### Configuración global

Al inicio de `Galaga.py` se definen los valores principales:

```python
ANCHO, ALTO = 800, 600
FPS = 60
COLOR_FONDO = (10, 10, 30)
```

- `ANCHO` y `ALTO` determinan el tamaño de la ventana.
- `FPS` limita la frecuencia de actualización.
- `COLOR_FONDO` se utiliza en la pantalla final.

También se inicializan Pygame, la ventana, el reloj y las fuentes de texto.

### `dibujar_fondo_galaxia()`

Dibuja el fondo de cada fotograma. Está compuesto por:

- Líneas horizontales con un degradado azul oscuro.
- Treinta estrellas colocadas aleatoriamente.

### Clase `Nave`

Representa la nave del jugador. Su imagen se construye con:

- Un polígono azul para el cuerpo.
- Un círculo cian para el centro.
- Un rectángulo azul para la parte inferior.

El método `update()` lee el teclado y mueve la nave. También limita su posición para que no salga de la ventana.

### Clase `Disparo`

Representa los proyectiles de la nave. Los disparos:

- Se crean en la posición superior de la nave.
- Se desplazan hacia arriba.
- Se eliminan cuando salen de la pantalla.

### Clase `Meteorito`

Representa a los enemigos. Su forma, tamaño, color, posición inicial y velocidad se generan de forma aleatoria.

### Clase `Explosion`

Gestiona la animación visual que aparece después de destruir un meteorito. Utiliza varias superficies dibujadas con círculos de diferentes tamaños.

### `mostrar_menu()`

Dibuja el menú inicial, muestra las instrucciones y espera a que el jugador presione una tecla. También permite cerrar el programa desde el evento de cierre de la ventana.

### `formatear_tiempo(segundos)`

Convierte una cantidad de segundos a formato `MM:SS`, utilizado para mostrar la duración de la partida.

### `juego()`

Contiene el bucle principal de una ronda. En cada iteración:

1. Limita la velocidad a los FPS configurados.
2. Procesa eventos del teclado y de la ventana.
3. Actualiza la nave, los disparos, los meteoritos y las explosiones.
4. Genera nuevos meteoritos cuando corresponde.
5. Comprueba las colisiones.
6. Actualiza puntuación, vidas y nivel.
7. Dibuja todos los elementos.
8. Actualiza la pantalla.

Al finalizar la ronda, muestra la pantalla de fin de juego y espera una acción del jugador.

### `main()`

Mantiene el juego funcionando mediante un ciclo que muestra el menú y comienza una nueva partida.

La condición:

```python
if __name__ == "__main__":
    main()
```

hace que el juego se ejecute solo cuando `Galaga.py` se lanza directamente, y no cuando se importa como módulo.

## Personalización rápida

Puedes modificar estos valores al principio de `Galaga.py`:

### Tamaño de la ventana y FPS

```python
ANCHO, ALTO = 800, 600
FPS = 60
```

### Velocidad de la nave

Dentro de `Nave.__init__()`:

```python
self.velocidad = 5
```

Un número mayor hace que la nave se mueva más rápido.

### Velocidad de los disparos

Dentro de `Disparo.__init__()`:

```python
self.velocidad = 10
```

### Vidas iniciales

Dentro de `juego()`:

```python
vidas = 3
```

### Frecuencia y cantidad de meteoritos

La generación de enemigos se controla mediante:

```python
if random.random() < 0.02 and len(enemigos) < 4 + nivel:
```

- `0.02` controla la probabilidad de generar un meteorito en cada fotograma.
- `4 + nivel` establece el máximo de enemigos simultáneos.

### Puntuación y dificultad

La puntuación por enemigo se encuentra en:

```python
puntuacion += 10
```

El aumento de velocidad por nivel se controla mediante:

```python
velocidad_enemigos += 0.5
```

## Solución de problemas

### `ModuleNotFoundError: No module named 'pygame'`

Instala Pygame en el mismo entorno de Python con el que ejecutas el juego:

```bash
python -m pip install pygame
```

Si utilizas un entorno virtual, actívalo antes de instalar y ejecutar.

### `python` no se reconoce como comando

Instala Python desde [python.org](https://www.python.org/downloads/) y asegúrate de habilitar la opción para agregar Python al `PATH`. En Windows también puedes probar:

```powershell
py Galaga.py
```

### La ventana se cierra inmediatamente

Ejecuta el programa desde una terminal para poder leer el mensaje de error:

```bash
python Galaga.py
```

Comprueba también que estás dentro de la carpeta correcta y que el archivo se llama exactamente `Galaga.py`.

### No se puede abrir una ventana gráfica

El juego necesita un entorno con interfaz gráfica. Si lo ejecutas en un servidor sin escritorio, una sesión SSH sin reenvío gráfico o un contenedor sin configuración gráfica, Pygame no podrá mostrar la ventana.

## Desarrollo y posibles mejoras

Algunas extensiones que se pueden incorporar en futuras versiones:

- Agregar sonidos de disparos, impactos y explosiones.
- Incorporar música de fondo.
- Añadir diferentes tipos de enemigos.
- Crear oleadas o patrones de ataque.
- Implementar un sistema de récords.
- Guardar la puntuación más alta en un archivo.
- Añadir una pausa.
- Permitir más controles, como `A` y `D`.
- Agregar animaciones más detalladas para la nave y los meteoritos.
- Crear una pantalla específica de selección de nivel.
- Separar el proyecto en varios módulos.
- Añadir pruebas automatizadas para la lógica que no depende de la ventana.
- Empaquetar el juego como ejecutable para Windows, macOS o Linux.

## Estado del proyecto

Proyecto funcional en una etapa inicial. La jugabilidad principal está implementada, pero todavía puede ampliarse con recursos audiovisuales, más contenido y una estructura modular.

## Licencia

Este repositorio no incluye actualmente un archivo de licencia. Hasta que se agregue una licencia explícita, los permisos de uso, modificación y redistribución deben considerarse no definidos por el proyecto.
