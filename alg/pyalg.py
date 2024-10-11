import sys
import signal
import threading
import os
import json
import time
info = "[i]"
warn = "[!]"
okay = "[/]"
terrdir = "E:\\Trabajo\\Proyectos\\terrframework\\terrdir\\"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import wrterr

def getlastdataex(ruta_archivo):
    
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as f:
            try:
                
                datos = json.load(f)
                
                
                if isinstance(datos, list) and datos:
                    return datos[-1]  
                else:
                    print("El archivo JSON está vacío o no contiene una lista.")
                    return None
            except json.JSONDecodeError:
                print("Error al decodificar el archivo JSON.")
                return None
    else:
        print("El archivo no existe.")
        return None

def getlastdate(ruta_archivo):
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as f:
            try:
                datos = json.load(f)
                
                if isinstance(datos, list) and datos:
                    
                    lastdate = datos[-1]['Fecha en que se termino']
                    print(lastdate)
                    return lastdate
                else:
                    print("El archivo JSON está vacío o no contiene una lista.")
                    return None
            except json.JSONDecodeError:
                print("Error al decodificar el archivo JSON.")
                return None
    else:
        print("El archivo no existe.")
        return None

from datetime import datetime, timedelta

def alg(terrdir):
    iFiles = range(1, 104)
    data = []

    for n in iFiles:
        flnm = f"{n}.json"
        filespth = terrdir + flnm
        lastdate_str = getlastdate(filespth)
        print(f"Última fecha para {flnm}: {lastdate_str}")

        try:
            lastdate = datetime.strptime(lastdate_str, "%d/%m/%Y")
        except ValueError:
            print(f"Error al convertir la fecha para {flnm}: {lastdate_str}")
            continue

        fecha_actual = datetime.now()
        fecha_limite = fecha_actual - timedelta(days=90)

        if lastdate < fecha_limite:
            print(f"{flnm} Candidato a poder estar en la siguiente salida")
            data.append(n)

    
    return data
        




def main(terrdir):
    alg(terrdir)



if __name__ == "__main__":
    main(terrdir)


## EN este punto el getlastdata(ruta) devuelve toda ultima data el archivo en cuestion

