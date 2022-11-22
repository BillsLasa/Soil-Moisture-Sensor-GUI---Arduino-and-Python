import serial	#Librería para Comunicación Serial
import time		#Esperar un tiempo
import collections

from matplotlib import pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import keyboard

import pygame #IMPORTAR LA LIBRERÍA PARA CREAR VIDEOJUEGOS

pygame.init() #INICIAR LA LIBRERÍA
pygame.mixer.init()

size = [600, 724] #DEFINIR TAMAÑO DE LA VENTANA PRINCIPAL

screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN) #CREAR VENTANA 
clock = pygame.time.Clock() #CREAR RELOJ
pygame.mouse.set_visible(0) #VOLVER INVISIBLE EL MOUSE DE LA PC

fondoSensor = pygame.image.load("imagenes/fondoSensor.jpg").convert() #FONDO PRINCIPAL
aguaHumedad = pygame.image.load("imagenes/agua.png").convert_alpha() #AGUA QUE REPRESENTA LA HUMEDAD
tanqueCubierta = pygame.image.load("imagenes/tanqueCubierta.png").convert_alpha() #CUBIERTA DEL TANQUE ENCIMA DEL AGUA

anchoAgua = 160
altoAguaOriginal = 370
posicionYOriginal = 250

nivelAgua = pygame.transform.scale(aguaHumedad, (anchoAgua, altoAguaOriginal))

def obtenerDatos(self,Samples,serialConnection,lines,lineValueText,lineLabel):
	#GRÁFICA EN TIEMPO REAL
	global i
	global tiempo
	global Ts

	if keyboard.is_pressed("a"):
		plt.close()
		datosAExportar = {'Tiempo': tiempo, 'Humedad Suelo': data}
		df = pd.DataFrame(datosAExportar, columns = ['Tiempo', 'Humedad Suelo'])

		df.to_excel('datoHumedadSuelo.xlsx', sheet_name='Hoja1')

	tiempo.append(i)

	value = 512
	voltaje = value*5/1023
	humedadSuelo = voltaje*20
	data.append(humedadSuelo)	#GUARDA EL VALOR

	plt.xlim(i-5,i+5)
	lines.set_data(tiempo,data)		#DIBUJAR NUEVA LÍNEA
	lineValueText.set_text(lineLabel+' = '+str(round(humedadSuelo,2)))		#MOSTRAR VALOR DEL SENSOR

	i = i+Ts
	#print(i)

	#INTERFAZ PYGAME
	altoAgua = int(humedadSuelo*altoAguaOriginal/100)
	nivelAgua = pygame.transform.scale(aguaHumedad, (anchoAgua, altoAgua))
	posicionY = posicionYOriginal+(posicionYOriginal+altoAguaOriginal-(posicionYOriginal+altoAgua)) 

	screen.blit(fondoSensor, [0,0]) ##MOSTRAR FONDO PRINCIPAL EN LAS COORDENADAS 0,0
	screen.blit(nivelAgua, [265,posicionY]) ##MOSTRAR FONDO PRINCIPAL EN LAS COORDENADAS 0,0
	screen.blit(tanqueCubierta, [0,0]) ##MOSTRAR FONDO PRINCIPAL EN LAS COORDENADAS 0,0

	pygame.display.flip() ##ACTUALIZAR LA PANTALLA
	clock.tick(12000) ##DEFINIR FPS

#try:
#	serialConnection = serial.Serial('COM4', baudrate = 9600, bytesize=8, parity='N', stopbits=1)	#CONECTAR
#except:
#	print('NO SE PUDO CONECTAR CON ARDUINO')

global i
global tiempo
global Ts

Ts = 0.1

Samples = 100	#NÚMERO DE MUESTRAS
tiempo = collections.deque([0]*Samples, maxlen=Samples)
data = collections.deque([0]*Samples, maxlen=Samples)
sampleTime = 100	#TIEMPO DE MUESTREO
i = 0

xmin = 0
xmax = 10
ymin = 0
ymax = 100

fig = plt.figure(figsize=(8,5))
ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
plt.title("Señal Sensada")
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Humedad del Suelo (%)")

lineLabel = "Humedad"
lines = ax.plot([],[],label = lineLabel)[0]
lineValueText = ax.text(0.85,0.95,'',transform = ax.transAxes)

anim = animation.FuncAnimation(fig,obtenerDatos,fargs=(Samples,1,lines,lineValueText,lineLabel),interval = sampleTime)
#plt.show()

#serialConnection.close()
pygame.quit()
