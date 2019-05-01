# Author: Pablo Soto González
# 26-04-19

from bs4 import BeautifulSoup
from flask import Response, Flask
import requests
import json
import time

app = Flask(__name__)

@app.route("/")
def bienvenida():
    return "Bienvenido, ingresa a /dia/rut/periodo para ver un período específico."

@app.route("/<dia>/<rut>")
def horario_lunes(dia,rut):
    time_init = time.time()
    periodos = []
    # Iteración de períodos en cierto día
    for i in range(1,12):
        url = 'https://intranet.ufro.cl/horario/horario_alumno_detalle2.php?matricula={}&periodo={}&dia={}&ano=2019&nro_semest=1&estado=N'.format(rut,i,dia)
        source = requests.get(url).text
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
            "docente": ""
        }
        
        soup = BeautifulSoup(source, 'lxml')

        for dato in soup.find_all('td'):
            detalle.append(dato.text.strip())
        
        if len(detalle) == 11:
            i = 0
            for x in horario:
                horario[x] = detalle[i]
                i+=1

            periodos.append(horario)
            
        # En caso de un período vacío
        else:
            periodo_vacio = {418 : "periodo vacío"} 
            # periodos.append(periodo_vacio)

    # Cálculo del runtime y agrega a periodos
    time_finish = time.time()
    periodos.append({"ejecutado en": "{} segundos".format(round(time_finish-time_init,3)) })

    # Encoding periodos a json
    json_horario = json.dumps(periodos, ensure_ascii=False, indent=4)

    return Response(json_horario, mimetype='application/json')


@app.route("/<dia>/<rut>/<periodo>")
def get_horario(rut, dia, periodo):
    url = 'https://intranet.ufro.cl/horario/horario_alumno_detalle2.php?matricula={}&periodo={}&dia={}&ano=2019&nro_semest=1&estado=N'.format(rut,periodo,dia)
    source = requests.get(url).text
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
        "docente": ""
    }

    soup = BeautifulSoup(source, 'lxml')
    # Búsqueda de etiquetas HTML td
    for dato in soup.find_all('td'):
        detalle.append(dato.text.strip())

    # Llenado de dict
    if len(detalle) == 11:
        i = 0
        for x in horario:
            horario[x] = detalle[i]
            i+=1

        horario = json.dumps(horario)
        horario_json = json.loads(horario)
    # En caso de período vacío        
    else: horario_json = {404 : "ERROR!"}
    
    return Response(json.dumps(horario_json, ensure_ascii=False, indent=4), mimetype='application/json')
    

if __name__ == '__main__':
    app.run()