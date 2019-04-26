# Author: Pablo Soto González
# 26-04-19

from bs4 import BeautifulSoup
from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route("/rut/<rut>")
def hola(rut):
    source = requests.get('https://intranet.ufro.cl/horario/horario_alumno_detalle2.php?matricula='+rut+'&periodo=10&dia=1&ano=2019&nro_semest=1&estado=N').text
    horario = []
    hora = {
        "dia": "",
        "periodo": "",
        "hora_inicio": "",
        "hora_termino": "",
        "tipo_clase": "",
        "fecha_inicio": "",
        "fecha_termino": "d",
        "sector": "g",
        "sala": "",
        "asignatura": "",
        "docente": "1",
    }

    soup = BeautifulSoup(source, 'lxml')
    for detalle in soup.find_all('td'):
        horario.append(detalle.text.strip())

    i = 0
    for x in hora:
        hora[x] = horario[i]
        i+=1
    
    return json.dumps(hora, ensure_ascii=False)


if __name__ == '__main__':
    app.run()