import sys
import os
import signal
import json
import ngrok
import time
info = "[i]"
warn = "[!]"
okay = "[/]"
terrdir = "E:\\Trabajo\\Proyectos\\terrframework\\terrdir\\"



    
def signal_handler(sig, frame):
    print(f"\n{info} Saliendo del script")
    # ngrok.disconnect()  # Asegúrate de tener ngrok definido si es necesario
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def bCrTerrFile(trfile):
    try:
        trfile = str(trfile)
        terrdpfile = terrdir + trfile
        with open(f"{terrdpfile}.json", "x") as crfile:
            json.dump({}, crfile)
    except Exception as e:
        print(e)

def chkf(terrdir):
    fls = os.listdir(terrdir)
    xptfiles = range(1, 104)
    for i in xptfiles:
        flnm = f"{i}.json"
        if flnm not in fls:
            flth = terrdir + flnm
            with open(flth, "x") as f:
                json.dump({}, f)
            print(f"{info} Archivo faltante creado {flth}")


def wreverything(terrdir, terr, new_data):
    flpth = os.path.join(terrdir, f"{terr}.json")

    # Cargar datos existentes si el archivo ya existe
    if os.path.exists(flpth):
        with open(flpth, "r") as f:
            try:
                existing_data = json.load(f)
                print("Datos cargados")
            except json.JSONDecodeError:
                existing_data = []  # Si el archivo está vacío o corrupto
    else:
        existing_data = []  # Si el archivo no existe

    # Asegurarse de que existing_data sea una lista
    if not isinstance(existing_data, list):
        existing_data = []  # Reiniciar si no es una lista

    # Agregar nuevos datos a la lista
    existing_data.append(new_data)

    # Guardar los datos en el archivo (sobrescribiendo el JSON)
    with open(flpth, "w") as f:
        json.dump(existing_data, f, indent=4)  # Sobrescribir el archivo con la nueva lista
    print("Datos añadidos al archivo.")
def svtojson(terrdir, new_data, terr):
    flpth = os.path.join(terrdir, f"{terr}.json")
    
    if os.path.exists(flpth):
        with open(flpth, "r+") as f:
            try:
                existingdt = json.load(f)
                print(f"{info} Datos cargados")
                
                if isinstance(existingdt, list):
                    existingdt.append(new_data)
                else:
                    existingdt = [existingdt, new_data]
                
            except json.JSONDecodeError:
                existingdt = [new_data]

            f.seek(0)
            json.dump(existingdt, f, indent=4)
            f.truncate()
            print(f"{info} Datos añadidos.")
    else:
        with open(flpth, "w") as f:
            json.dump([new_data], f, indent=4)
            print(f"{info} Archivo creado y datos añadidos.")

def main(terrdir):
    if len(os.listdir(terrdir)) == 0:
        for i in range(1, 104):
            terr = i
            bCrTerrFile(terr)
    else:
        print(f"{info} Archivos detectados: {len(os.listdir(terrdir))} ")

if __name__ == "__main__":
    main(terrdir)