#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Autores: Natalia Bustacara, Nicolas Vergara y en colaboracion de Alejandro Rojas


import web
import json
import sys
from sys import *

render = web.template.render('templates/')
#global env

urls = (
    '/', 'index',
    '/paraderos_cercanos/.*', 'paraderos_cercanos',
)

class index:
    def GET(self):
        mapa = web.template.frender('templates/mapa.html')
        return mapa(None)

class paraderos_cercanos:
    def arcpy_geo_processing(self, cx, cy, tipo):
        print "Cargando entorno"
        import arcpy
        reload(arcpy) #Recargo modulo arcpy 
        tabla = [] # Salida
        entorno = "C:/Users/Natalia/Desktop/PI-PY/Mapa_Bogota.mdb"
        arcpy.env.workspace = entorno
        print "Entorno cargado"
        coordenada_Lamda = cx
        coordenada_Phi = cy
        #Elimina tablas previas
        try:
            arcpy.Delete_management("paraderos_tmp")
            arcpy.Delete_management("estaciones_tmp")
        except:
            pass
        #Genera tabla con paraderos en el rango
        #arcpy.AddMessage("Buscando estaciones y paraderos en el rango")
        # Se define el punto con coordenadas geográficas
        pto=arcpy.Point(float(coordenada_Lamda),float(coordenada_Phi))
        ptolist=[arcpy.PointGeometry(pto)]
        #Crea una tabla analizando las distancias entre features
        if tipo == "both" or tipo=="sitp":
            arcpy.PointDistance_analysis(ptolist,"Paraderos_SITP","paraderos_tmp","400 Meters")
            cursor1=arcpy.da.SearchCursor("paraderos_tmp",["NEAR_FID", "DISTANCE"])
            resultados_paraderos=[]
            for row in cursor1:
                resultados_paraderos.append(row)
            resultados_paraderos.sort(key=lambda x: x[1])
            resultados_paraderos = resultados_paraderos[0:5]
            for resultado in resultados_paraderos:
                cursor3=arcpy.da.SearchCursor("paraderos_SITP", ("Name", "SHAPE@XY", 'FolderPath'), "OBJECTID="+ str(resultado[0]))
                for row in cursor3:
                    cursor5=arcpy.da.SearchCursor("Rutas_Paraderos", "RUTA", "PARADERO='%s'" % (row[0]))
                    rutas=""
                    for ruta in cursor5:
                        rutas += str(ruta[0]) + ","
                    tabla.append({'name': row[0], 'cx': round(row[1][0], 4), 'cy': round(row[1][1], 4), 'description': row[2], 'rutas': rutas, 'tipo': "sitp"})
                    #arcpy.AddMessage("El paradero más cercano es %s, y las rutas que pasan por este son: %s " % (paradero_cercano, Rutas))
            arcpy.Delete_management("paraderos_tmp")
        if tipo == "both" or tipo=="tm":
            arcpy.PointDistance_analysis(ptolist,"Estaciones_Transmilenio","estaciones_tmp","400 Meters")
            cursor2=arcpy.da.SearchCursor("estaciones_tmp",["NEAR_FID", "DISTANCE"])
            resultados_estaciones = []
            arcpy.AddMessage("Buscando estacion mas cercana")
            #Revisa estación mas cercana
            for row in cursor2:
                resultados_estaciones.append(row)
            resultados_estaciones.sort(key=lambda x: x[1])
            resultados_estaciones = resultados_estaciones[0:5]
            for resultado in resultados_estaciones:
                cursor4 = arcpy.da.SearchCursor("Estaciones_Transmilenio", ("Name", "SHAPE@XY", 'FolderPath'), "OBJECTID=" + str(resultado[0]))
                for row in cursor4:
                    tabla.append({'name': row[0], 'cx': round(row[1][0], 4), 'cy': round(row[1][1], 4), 'description': row[2], 'rutas': "" ,'tipo' : "tm"})
         
            #Imprime los resultados de busqueda
            arcpy.Delete_management("estaciones_tmp")
        
            #Geoprocessing

        return tabla
        #Consulta tabla y almacena el ID del objeto del paradero y la distancia
        

        #Revisa paradero mas cercano
        

    def GET(self):
        cy = float(web.input().cy)
        cx = float(web.input().cx)
        tipo = str(web.input().tipo)
        resultados = self.arcpy_geo_processing(cx, cy, tipo)
        web.header('content-Type', 'application/json')
        return json.dumps(resultados)        


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()