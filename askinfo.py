import sys
import os
import signal
import json
import wrterr

info = "[i]"
warn = "[!]"
okay = "[/]"
terrdir = "E:\\Trabajo\\Proyectos\\terrframework\\terrdir\\"

def signal_handler(sig, frame):
    print(f"\n{info} Saliendo del script")
    # ngrok.disconnect()  # Asegúrate de definir ngrok si es necesario
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def impwrterr(terrdir):
    try:
        import wrterr
        print(f"{info} archivo wrterr.py se ha podido importar correctamente")
        wrterr.chkf(terrdir)
    
        return 0
    except OSError as e:
        print(f"{warn} archivo wrterr.py no se ha podido importar correctamente")
        return 1

def showinfo(terr, terrdir, mode):
    fls = len(os.listdir(terrdir))
    if fls == 103:
        print(f"{okay} Directorio cargado")
    else:
        print(f"{warn} Error relacionado con el directorio")

    if mode == "1":
        getinfo(terrdir, mode, terr)
    elif mode == "2":
        try:
            print(f"{okay} Mostrando información sobre el territorio: \n")
            fltrd = os.path.join(terrdir, f"{terr}.json")
            with open(fltrd, "r") as fl:
                rd = json.load(fl)
                print(json.dumps(rd, indent=4))
        except OSError as e:
            print(e)

def getinfo(terrdir, mode, terr):
    print(f"{info} Listo para modificar")
    wrterr.wreverything(terrdir, mode, terr)
def main(terrdir):
    if impwrterr(terrdir) == 0:
        print(f"{info} Listo para ingresar datos")
        terrsel = str(input(f"{info} Ingresa el territorio a modificar o dar información: "))
        print("\n¿En qué modo vas a operar?\n 1) = Escritura \n 2) = Leer")
        mode = str(input(f"{info} Modo: "))
        showinfo(terrsel, terrdir, mode)
    else:
        print(f"{warn} Reinicia el script")

if __name__ == "__main__":
    main(terrdir)