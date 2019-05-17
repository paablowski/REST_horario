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

@app.route("/di")
def horario_lunes(dia,rut):
    time_init = time.time()
    periodos = []

    if 1 <= int(dia) < 7:
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

    else: periodos.append({"Error 202": "Ingresa día válido (1 - 6, de lunes a sábado, respectivamente)"})

    # Encoding periodos a json
    json_horario = json.dumps(periodos, ensure_ascii=False, indent=4)

    return Response(json_horario, mimetype='application/json')



@app.route("/<dia>/<matricula>")
def get_horario(dia, matricula):
    time_init = time.time()
    horario = []

    if 0 < int(dia) < 7:
        for i in range(1,12):
            periodo = {
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
            url = 'https://intranet.ufro.cl/horario/horario_alumno_detalle2.php?matricula={}&periodo={}&dia={}&ano=2019&nro_semest=1&estado=N'.format(matricula,i,dia)
            bs = BeautifulSoup(requests.get(url).text, 'lxml')
            
            buscar = bs.find_all('td')
            print(len(buscar))
            if len(buscar) == 11:
                for i,(k,v) in enumerate(periodo.items()):
                        periodo[k] = buscar[i].text.strip()
                horario.append(periodo)
            

        # Caso: día sin clases
        if len(horario) == 0:
            horario.append({200: "No tienes clases este día"})
    else:
        horario.append({202: "Ingresa día válido (1 - 6, de lunes a sábado, respectivamente)"})
    
    # Calcula tiempo de ejecución
    time_finish = time.time()
    time_dif = time_finish-time_init
    horario.append({"Ejecutado en": "{} segundos".format(round(time_dif,3))})

    # Encode a json
    json_horario = json.dumps(horario, ensure_ascii=False, indent=4)
    
    return Response(json_horario, mimetype='application/json')

if __name__ == '__main__':
    app.run()