# REST-horario

Script hecho en Python, con las bibliotecas BeautifulSoup y Flask. 
- [x] Así evitamos estar perdiendo tiempo al intentar conectar a Intranet


## Uso:
###### Consultar las clases dentro de un día específico
```
/<dia>/<rut>
```

- donde **_dia_** es un entero entre 1 al 6, de lunes a sábado, respectivamente.
- Y **_rut_** son los 8 dígitos del rut más el dígito verificador, sin puntos ni guiones y las dos últimas cifras del año en que se matriculó.
> Ej.: /3/12345678115/
