import json
import os

# Contenido a escribir en cada archivo JSON
contenido = [
    {
        "Fecha en que se comenzo": "12",
        "Fecha en que se termino": "12",
        "Hermano asignado": "12",
        "Notas": "12"
    }
]

# Ruta donde se crearán los archivos
ruta_directorio = "E:\\Trabajo\\Proyectos\\terrframework\\terrdir"  # Cambia esto según sea necesario

# Crear la carpeta si no existe
os.makedirs(ruta_directorio, exist_ok=True)

# Crear 103 archivos JSON
for i in range(1, 104):
    nombre_archivo = os.path.join(ruta_directorio, f"{i}.json")
    with open(nombre_archivo, 'w') as f:
        json.dump(contenido, f, indent=4)

print("Archivos JSON creados exitosamente.")