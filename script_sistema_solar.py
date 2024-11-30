from vpython import sphere, vector, rate, color, canvas, distant_light, textures, label
import numpy as np
import random

# esto genera el canvas
scene = canvas(title="Sistema Solar 3D", width=1400, height=700, background=color.black)
scene.lights = []  
distant_light(direction=vector(1, 0, 0), color=color.white)

# Parámetros del sistema solar
planetas = ['mercurio', 'venus', 'tierra', 'marte', 'jupiter', 'saturno', 'urano', 'neptuno']
radios_orbita = [57.9, 108.2, 149.6, 227.9, 778.3, 1427, 2871, 4497]  # Distancias en millones de km
radios_planeta = [2.4, 6.0, 6.3, 3.4, 69, 58, 25, 24]  # Radios de los planetas en km
periodos_orbitales = [88, 225, 365, 687, 4333, 10759, 30687, 60190]  # Periodos en días
retrogrados = [False, True, False, False, False, True, False, False]  # Saturno tiene retrogradación
inclinaciones = [0, 3.39, 0, 1.85, 0, 2.49, 82.2, 1.77]  # Inclinaciones de los planetas

# Texturas para los planetas (están en la carpeta local)
texturas = [f"texturas/{planeta}.png" for planeta in planetas]

# Escala de distancias y velocidades
factor_distancia = 0.5  # Escala de distancias orbitales
factor_velocidad = 1.0  # Velocidad de rotación orbital
factor_rotacion = 0.05  # Velocidad de rotación propia de los planetas

# Esto genera el sol
sol = sphere(pos=vector(0, 0, 0), radius=10, color=color.yellow, emissive=True)

# Esto en teoría debería generar la textura de estrellas (si tienes la textura adecuada)
textura_estrellas = "texturas/estrellas.png"
esfera_fondo = sphere(
    pos=vector(0, 0, 0),
    radius=1000,
    texture=textura_estrellas,
    emissive=True,
    opacity=0.2
)

# Crear estrellas aleatorias en el fondo
num_estrellas = 1000
for _ in range(num_estrellas):
    sphere(
        pos=vector(random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000)),
        radius=random.uniform(0.1, 0.3),
        color=color.white,
        emissive=True
    )

# Crear los planetas y sus etiquetas
planetas_obj = []
etiquetas = []
for i in range(len(planetas)):
    # Aquí aumento el tamaño de los planetas para mejorar la cobertura de las texturas
    planeta = sphere(
        pos=vector(radios_orbita[i] * factor_distancia, 0, 0),
        radius=radios_planeta[i] * 0.8,  # Escalamos los planetas para que se vean más grandes
        texture=texturas[i],  # no funcionan la textura
        make_trail=True,
        trail_radius=0.05,
        trail_color=color.white,
        retain=100
    )
    etiqueta = label(
        text=planetas[i].capitalize(),
        pos=planeta.pos + vector(0, 0.1, 0),
        xoffset=10,
        yoffset=20,
        height=12,
        border=6,
        font="sans",
        color=color.white,
        opacity=0.7
    )
    planetas_obj.append(planeta)
    etiquetas.append(etiqueta)

# Animación
t = 0
cam_radius = 400  # Radio de la órbita de la cámara

while True:
    rate(60)  # Controlar la velocidad de la animación
    t += factor_velocidad

    # Movimiento de la cámara
    cam_angle = 0.0005 * t  # Ángulo de rotación de la cámara
    scene.camera.pos = vector(
        cam_radius * np.cos(cam_angle),
        100,  # Altura de la cámara
        cam_radius * np.sin(cam_angle)
    )
    scene.camera.axis = vector(0, 0, 0) - scene.camera.pos  # La cámara siempre apunta al Sol

    # Actualización de la posición de los planetas
    for i in range(len(planetas)):
        angulo_orbital = 2 * np.pi * (t / periodos_orbitales[i])  # Cálculo del ángulo orbital
        if retrogrados[i]:
            angulo_orbital = -angulo_orbital  # Ajustar el sentido de rotación si es retrógrado

        inclinacion = np.radians(inclinaciones[i])  # cambiamos a radianes
        a = radios_orbita[i] * factor_distancia  # Distancia de la órbita
        b = a * 0.9  # Forma de la órbita (elipsoide porque no son círculos)

        x = a * np.cos(angulo_orbital)  # Coordenada X del planeta
        y = b * np.sin(angulo_orbital)  # Coordenada Y del planeta
        z = y * np.sin(inclinacion)  # Coordenada Z del planeta

        planetas_obj[i].pos = vector(x, y, z)  # posición de los planetas
        etiquetas[i].pos = planetas_obj[i].pos + vector(0, 0.1, 0)  # Actualizamos la posición de la etiqueta
        planetas_obj[i].rotate(angle=factor_rotacion, axis=vector(0, 1, 0))  # Rotación del planeta
