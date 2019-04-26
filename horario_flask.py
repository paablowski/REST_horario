# Author: Pablo Soto González
# 26-04-19

from bs4 import BeautifulSoup
from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route("/")
def bienvenida():
    return "Ingresa tu rut en /rut/<rut>"

@app.route("/rut/<rut>")
def get_horario(rut):
    source = requests.get('https://intranet.ufro.cl/horario/horario_alumno_detalle2.php?matricula='+rut+'&periodo=10&dia=1&ano=2019&nro_semest=1&estado=N').text
    detalle = []
    horario = {
        "dia": "",
        "periodo": "",
        "hora_inicio": "",
        "hora_termino": "",
        "tipo_clase": "",
        "fecha_inicio": "",
        "fecha_termino": "",
        "sector": "",
        "sala": "",
        "asignatura": "",
        "docente": "",
    }

    soup = BeautifulSoup(source, 'lxml')
    for dato in soup.find_all('td'):
        detalle.append(dato.text.strip())

    i = 0
    for x in horario:
        horario[x] = detalle[i]
        i+=1
    
    return json.dumps(horario, ensure_ascii=False)


if __name__ == '__main__':
    app.run()