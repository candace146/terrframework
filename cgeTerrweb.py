import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g
#import webbrowser
from plyer import notification
import time 
import pyperclip
import signal
import sys
import wrterr
import alg.pyalg as alg
import socket

warn = "[!]"
info = "[i]"
okay = "[o]"
app = Flask(__name__)

app.secret_key = os.urandom(24)

def signal_handler(sig, frame):
    print(f"\n{info} Saliendo del script")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

terrdir = "/home/lau/Proyectos/terrframework/terrframework/terrdir/"
def sndnt(url):
    pyperclip.copy(url)
    spam = pyperclip.paste()
    notification.notify(
        title="Terr ngrok public URL",
        message=f"Se abrio correctamente la url publica. Ha sido copiada a la clipboard",
        app_name="Python script",
        timeout=15
    )



def get_network_ip():
    try:
        # Crea un socket y conéctate a una dirección IP pública
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conectar a Google DNS
        ip = s.getsockname()[0]  # Obtener la dirección IP de la interfaz utilizada
        s.close()  # Cierra el socket
        return ip
    except Exception as e:
        print(f"Error al obtener la IP: {e}")
        return None


    
#ngrok.disconnect()
# Start ngrok and get the public URL
#listener = ngrok.forward(80, authtoken="2fNTL8qEodi8RPtVcCUvFC7TLnP_4M6DoedLT6NGfaS8s2URL")
#public_url = listener.url()
#print(f"Public URL: {public_url}")
#webbrowser.open(public_url)
#sndnt(public_url)
@app.route('/alg')
def algpage():
    if g.user:
        data = alg.alg(terrdir)
        print(data)
        return render_template('/alg/alg.html', data=data)
    return redirect(url_for('login'))
@app.route('/dps')
def dps():
    session.pop('user', None)
    return redirect(url_for('index'))
@app.route('/', methods=['GET', 'POST'])
def index():

    if  g.user:
        print(f"{warn} User loged, show button")

        return render_template('/tmodify/modify.html', show=True)
    
    number = None
    dtjson = None
    ok = False

    if request.method == 'POST':
        # Manejar la lectura del número
        if request.form.get('number') and request.form['number'].isdigit():
            number = request.form.get('number')
            fslpth = os.path.join(terrdir, f"{number}.json")

            if os.path.exists(fslpth):
                try:
                    with open(fslpth, 'r') as f:
                        dtjson = json.load(f)
                        print(dtjson)
                except json.JSONDecodeError:
                    dtjson = "Error al leer el archivo JSON."
            else:
                dtjson = "El archivo JSON no existe."

        # Manejo de la modificación de datos
        if any(request.form.get(field) for field in ['uvezc', 'uvezf', 'her', 'note']):
            uvezc = request.form.get('uvezc')
            uvezf = request.form.get('uvezf')
            her = request.form.get('her')
            note = request.form.get('note')

            update_data = {
                "Fecha en que se comenzo": uvezc,
                "Fecha en que se termino": uvezf,
                "Hermano asignado": her,
                "Notas": note
            }

            # Actualizar el archivo JSON
            wrterr.wreverything(terrdir, number, update_data)

            # Volver a cargar los datos después de la actualización
            if os.path.exists(fslpth):
                with open(fslpth, 'r') as f:
                    dtjson = json.load(f)

            return redirect(url_for('index', number=number))

    return render_template('/tmodify/modify.html', number=number, data=dtjson)
    
@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        usr = request.form.get('usr')
        passwd = request.form.get('passwd')
        print(usr, passwd)
        if usr == "123" and passwd == "123":
            session['user'] = usr
            return redirect(url_for('home'))
    return render_template('login/login.html')

@app.route('/map/', methods=["GET", "POST"])
def mpaterr():
    if g.user:
        if request.method == 'POST':
            # Manejar la lectura del número
            number = request.form.get('terrbutton')
            print(number)
            
            if number and number.isdigit():
                fslpth = os.path.join(terrdir, f"{number}.json")
                if os.path.exists(fslpth):
                    try:
                        with open(fslpth, 'r') as f:
                            dtjson = json.load(f)
                            print(dtjson)
                            return jsonify(dtjson)  # Devolver los datos como JSON
                    except json.JSONDecodeError:
                        return jsonify({"error": "Error al leer el archivo JSON."}), 500
                else:
                    return jsonify({"error": "El archivo JSON no existe."}), 404
        
        # Para la solicitud GET, simplemente renderiza la plantilla
        return render_template('map/map.html')
    return redirect(url_for('login'))

@app.route('/home/', methods=["GET", "POST"])
def home():
    if g.user:
        ip_address = get_network_ip()
        print(ip_address)
        return render_template('home/home.html', ip=ip_address)
    

    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
@app.route('/reset/')
def reset():
    return redirect(url_for('index', referer='a'))

@app.route('/carritos')
def carritos():
    if g.user:
            try:
                # Asegúrate de que la ruta al archivo sea correcta
                with open("carritosProgram/program.json", "r") as f:
                    data = json.load(f)  # Usa json.load para leer desde el archivo

                if data:
                    for item in data:
                        dia = item["dia"]
                        hermano = item["detalle"]["hermano"]  # Corregido
                        horario = item["detalle"]["horario"] 
                        lugar = item["detalle"]["lugar"] # Corregido
                        print(f"{dia}, {hermano}, {horario}, {lugar}") 
                else:
                    print(f"{warn} Ha ocurrido un error")
                
                carritosProgram = data
                return render_template('/carritos/carritos.html', carritosProgram=carritosProgram)
                
            except FileNotFoundError:
                print(f"{warn} El archivo no se encontró.")
            except json.JSONDecodeError:
                print(f"{warn} Error al decodificar el archivo JSON.")
            except KeyError as e:
                print(f"{warn} Clave no encontrada: {e}")

            return render_template('/carritos/carritos.html', carritosProgram=None)

        

    return redirect(url_for('login'))

@app.route('/carmod/')
def carmod():
    if g.user:
        ip = get_network_ip()
        return render_template('/carmod/carmod.html', ip=ip)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)