#!.venv\\Scripts\\python.exe
import pygame #Necesaria
import numpy as np #Necesaria
import pandas as pd #Necesaria
import os
import time
import random
import webbrowser

#Inicio
pygame.init()

#Funciones
def casilla_juego(coordenada,dic_casillas):
    pos_x, pos_y = coordenada
    pos_x = (pos_x//distancia_pequena)*distancia_pequena
    pos_y = (pos_y//distancia_pequena)*distancia_pequena
    for clave, valor in dic_casillas.items():
        if valor == (pos_x,pos_y):
            return clave
def encontar_diccionario1():
    global distancia_pequena 
    dic_casillas = {} #definir diccionario
    lista_letras = list("abcdefghi")
    posicion_y = 0
    for letra in lista_letras: #aumento de letras
        posicion_x = 0
        for numero in range(1,10): #aumento en numeros 
            dic_casillas[f"{letra}{numero}"] = (posicion_x,posicion_y)
            posicion_x += distancia_pequena #ir moviendo las coordenadas x
        posicion_y += distancia_pequena # mover coordenadas y
    return dic_casillas
def encontrar_diccionario2():
    dic_pos_array={} # definir diccionario
    lista_letras = list("abcdefghi")
    for fila_grande in range(0,3):
        for fila_pequeña in range(0,3):
            for columna_grande in range(0,3):
                for columna_pequeña in range(0,3): # este desplazamiento es para ir llenando fila a fila
                    pos_letra = 3*fila_grande + fila_pequeña
                    pos_numero = 3*columna_grande + columna_pequeña + 1
                    clave = f"{lista_letras[pos_letra]}{pos_numero}"
                    valor = (fila_grande,columna_grande,fila_pequeña,columna_pequeña)
                    dic_pos_array[clave] = valor
    return dic_pos_array
def crear_array_tablero():
    primera_fila = np.zeros((3,3,3))
    segunda_fila = np.zeros((3,3,3))
    tercera_fila = np.zeros((3,3,3))
    return [primera_fila,segunda_fila,tercera_fila]
def funcion_jugar(casilla):
    #Variables globales
    global distancia_grande
    global turno
    global bloqueados
    global lista_figuras
    global dic_casillas
    global tablero
    global ultima_jugada
    global dic_pos_array
    global tableros_bloqueados
    #recopilar informacion
    posicion = dic_casillas[casilla]
    array = dic_pos_array[casilla]
    var1,var2,var3,var4 = array
    x1,y1=posicion 
    verdad = True
    x1=(x1//distancia_grande)*distancia_grande
    y1=(y1//distancia_grande)*distancia_grande
    bloqueados,agregar_despues = bloquear_tableros(tableros_bloqueados,bloqueados,casilla,turno,x1,y1,var1,var2,var3,var4)
    bloqueados = tableros_bloqueados + bloqueados
    for cosas in bloqueados:
        x2,y2 = cosas 
        if (x1==x2) and (y1==y2):
            verdad = False
    if verdad:
        if tablero[var1][var2][var3][var4] == 0:
            if ultima_jugada == 1:
                if jugar_contra_bot:
                    time.sleep(2)
                    
                dibujo = pygame.image.load(dibujo_circulo)
                ultima_jugada = 2
            elif ultima_jugada == 2:
                dibujo = pygame.image.load(dibujo_equis)
                ultima_jugada = 1

                #Para el bot
                yo_jugue = casilla

            turno +=1
            bloqueados.append(agregar_despues)
            lista_figuras.append([dibujo,posicion])
            tablero[var1][var2][var3][var4] = ultima_jugada
            tableros_llenos(var1,var2,x1,y1)
def mostrar(lista_figuras):
    for cosas in lista_figuras:
        x,y = cosas[1]
        pantalla.blit(cosas[0],(x,y))
def ganar_un_tablero(casilla):
    global distancia_grande
    global bloqueados
    global lista_figuras
    global tableros_bloqueados
    global grupos_grandes_pos
    global pequenos_a_grandes
    array = dic_pos_array[casilla]
    coordenada = dic_casillas[casilla]
    x,y = coordenada
    x1 = x//distancia_grande
    y1 = y//distancia_grande
    x = x1*distancia_grande
    y = y1*distancia_grande
    var1,var2,var3,var4 = array
    multiplicacion1 = 1
    multiplicacion2 = 1
    multiplicacion3 = 0
    multiplicacion4 = 0
    for cosas in tablero[var1][var2][var3]:
        multiplicacion1 *= cosas
    for indice in range(0,3):
        valor = tablero[var1][var2][indice][var4]
        multiplicacion2 *= valor
    if  (var4 != 1 and var3 != 1)or(var4 == 1 and var3 == 1):
        multiplicacion3 = tablero[var1][var2][0][0] * tablero[var1][var2][1][1] * tablero[var1][var2][2][2]
        multiplicacion4 = tablero[var1][var2][2][0] * tablero[var1][var2][1][1] * tablero[var1][var2][0][2]
    if multiplicacion1 == 8 or multiplicacion2 == 8 or multiplicacion3 == 8 or multiplicacion4 == 8 :
        dibujo = pygame.image.load(circulo_rojo)
        eliminar_imagenes(x,y)
        convertir_tablero_i(var1,var2)
        lista_figuras.append([dibujo,(x,y)])
        tableros_bloqueados.append((x,y))
        tablero_grande[y1][x1] = 2
        if grupos_grandes_pos[pequenos_a_grandes[casilla]]==(x,y):
            bloqueados = []
    elif multiplicacion1 == 1 or multiplicacion2 == 1 or multiplicacion3 == 1 or multiplicacion4 == 1:
        dibujo = pygame.image.load(equis_verde)
        eliminar_imagenes(x,y)
        convertir_tablero_i(var1,var2)
        lista_figuras.append([dibujo,(x,y)])
        tableros_bloqueados.append((x,y))
        tablero_grande[y1][x1] = 1
        if grupos_grandes_pos[pequenos_a_grandes[casilla]]==(x,y):
            bloqueados = []
def eliminar_imagenes(x,y):
    global lista_figuras
    for elem in lista_figuras:
        posicion = elem[1]
        x1,y1=posicion
        if (x == x1) and (y == y1):
            del elem
def ganador_absoluto():
    ganaste = []
    global jugar
    global fin_del_juego
    global ganador
    global tablero_grande
    multiplicacion3 = tablero_grande[0][0] * tablero_grande[1][1] * tablero_grande[2][2]
    multiplicacion4 = tablero_grande[2][0] * tablero_grande[1][1] * tablero_grande[0][2]
    ganaste.append(multiplicacion3)
    ganaste.append(multiplicacion4)
    for indice in range(0,3):
        multiplicacion2 = 1
        multiplicacion1 = 1
        for seg_indice in range(0,3):
            multiplicacion1 *= tablero_grande[indice][seg_indice]
            multiplicacion2 *= tablero_grande[seg_indice][indice]
        ganaste.append(multiplicacion1)
        ganaste.append(multiplicacion2)
    if 8 in ganaste :
        jugar = False
        fin_del_juego = True
        ganador = "CIRCULO"
    elif 1 in ganaste:
        jugar = False
        fin_del_juego = True
        ganador = "EQUIS"
def texto_final():
    global ganador
    fuente = pygame.font.Font("freesansbold.ttf",32)
    if ganador == "CIRCULO":
        color = (255,0,0)
        texto = fuente.render(f"¡¡{ganador} GANA!!",True,color)
    elif ganador == "EQUIS":
        color = (0,143,57)
        texto = fuente.render(f"¡¡{ganador} GANA!!",True,color)
    elif ganador == "TABLAS":
        color == (128,128,128)
        texto = fuente.render(f"¡¡EMPATE!!",True,color)
    
    return texto
def eleccion_inicial(click):
    global pagina_principal
    global jugar
    global opciones
    x,y = click
    if (x < 455)and(x > 156)and(y<575)and(y>460):
        pagina_principal = False
        jugar = True
        opciones = False
    if (x < 450)and(x > 160)and(y<435)and(y>328):
        pagina_principal = False
        opciones = True
def eleccion_opciones(click):
    global jugar
    global jugar_contra_bot
    global opciones
    x,y = click
    if (x < 300)and(x > 35)and(y<610)and(y>485):
        opciones = False
        jugar = True
        jugar_contra_bot = False
    if (x < 575)and(x > 350)and(y<615)and(y>485):
        opciones = False
        jugar = True
        jugar_contra_bot = True
    if (x < 442)and(x > 177)and(y<459)and(y>418):
        webbrowser.open("https://es.wikipedia.org/wiki/%C3%9Altimo_tres_en_raya")
def mostrar_arreglos(tablero):
    os.system("cls")
    print(pd.DataFrame(tablero[0][0]),"\n",
        pd.DataFrame(tablero[0][1]),"\n",
        pd.DataFrame(tablero[0][2]),"\n",
        pd.DataFrame(tablero[1][0]),"\n",
        pd.DataFrame(tablero[1][1]),"\n",
        pd.DataFrame(tablero[1][2]),"\n",
        pd.DataFrame(tablero[2][0]),"\n",
        pd.DataFrame(tablero[2][1]),"\n",
        pd.DataFrame(tablero[2][2]))
def definir_subgrupos():
    global distancia_pequena
    global distancia_grande
    global dic_casillas
    grupos_grandes_pos = {}
    pequenos_a_grandes = {}
    indice = 1
    for y in range(0,3):
        for x in range(0,3):
            grupos_grandes_pos[f"grupo{indice}"]=(distancia_grande*x,distancia_grande*y)
            indice +=1
    for clave,coordenada in dic_casillas.items():
        x1,y1 = coordenada
        if distancia_grande<=x1 and 2*distancia_grande>x1:
            x1=x1-210
        if distancia_grande<=y1 and 2*distancia_grande>y1:
            y1=y1-210
        if 3*distancia_grande>=x1 and 2*distancia_grande<=x1:
            x1=x1-2*distancia_grande
        if 3*distancia_grande>=y1 and 2*distancia_grande<=y1:
            y1=y1-2*distancia_grande
        subindice = (x1//distancia_pequena)+((y1//distancia_pequena)*3)
        pequenos_a_grandes[clave]=f"grupo{subindice+1}"
    return grupos_grandes_pos,pequenos_a_grandes
def bloquear_tableros(tableros_bloqueados,bloqueados,casilla,turno,x1,y1,var1,var2,var3,var4):
    global pequenos_a_grandes
    global locacion
    global cuadro_marcado
    global mostrar_importante
    global grupos_grandes_pos
    verdadero = True
    bloqueados = bloqueados + tableros_bloqueados
    for cosas in bloqueados:
        x2,y2 = cosas 
        if (x1==x2) and (y1==y2):
            return bloqueados, (-1,-1)
    if verdadero:
        if tablero[var1][var2][var3][var4] == 0:
            grupo = pequenos_a_grandes[casilla]
            coordenada = grupos_grandes_pos[grupo]
            locacion = coordenada
            locacion = (0,0)
            mostrar_importante=fondo
            bloqueados = []
            agregar_despues = (-1,-1)
            if turno == 0:
                for clave,lugares in grupos_grandes_pos.items():
                    if clave == grupo:
                        locacion = coordenada
                        mostrar_importante=cuadro_marcado
                        continue
                    elif (x1,y1)==lugares:
                        agregar_despues = lugares
                        continue
                    else:
                        bloqueados.append(lugares)
                return bloqueados,agregar_despues
            elif coordenada in tableros_bloqueados:
                return bloqueados,(-1,-1)
            else:
                bloqueados = []
                for clave,lugares in grupos_grandes_pos.items():
                    if clave == grupo:
                        locacion = coordenada
                        mostrar_importante=cuadro_marcado
                        continue
                    elif (x1,y1)==lugares:
                        agregar_despues = lugares
                        continue
                    else:
                        bloqueados.append(lugares)
                return bloqueados,agregar_despues
        else:
            return bloqueados, (-1,-1)
def jugar_otra_vez(coordenada):
    global fin_del_juego
    global loop_infinito 
    global pagina_principal
    x,y = coordenada
    if x>155 and x<475 and y<605 and y>530:
        fin_del_juego = False
        loop_infinito = True
        pagina_principal = True
        variables_definidas()
def variables_definidas():
    global ultima_jugada
    global turno
    global locacion
    global lista_figuras
    global tableros_bloqueados
    global tablero_grande
    global bloqueados
    global tablero
    global tablero_a_jugar
    ultima_jugada = 1
    lista_figuras = []
    tableros_bloqueados = []
    bloqueados = []
    tablero_a_jugar = (0,0)
    tablero_grande = np.zeros((3,3))
    tablero = crear_array_tablero()
    turno = 0
    locacion = (-1,-1)
def verificar_tablas():
    global jugar
    global fin_del_juego
    global tablero
    global ganador
    tablas = True
    for filas1 in tablero:
        for cuadro2 in filas1:
            for fila2 in cuadro2:
                for elemento in fila2:
                    if elemento == 0:
                        tablas = False
    if tablas:
        jugar = False
        ganador = "TABLAS"
        fin_del_juego = True 
def convertir_tablero_i(var1,var2):
    global tablero
    for i1 in range(0,3):
        for i2 in range(0,3):
            tablero[var1][var2][i1][i2] = 3
def tableros_llenos(var1,var2,x1,y1):
    global tablero
    global locacion 
    global bloqueados
    global tableros_bloqueados
    bloquear = True
    for i1 in range(0,3):
        for i2 in range(0,3):
            if tablero[var1][var2][i1][i2] == 0:
                bloquear = False
    if bloquear:
        tableros_bloqueados.append((x1,y1))
        bloqueados = []
        locacion=(-1,-1)

# Codigo Experimental del robot

def turno_bot():
    indice = random.randint(0,81)
    n=0
    for casillas in dic_casillas.keys():
        if n == indice:
            verificar0 = dic_pos_array[casillas]
            var1,var2,var3,var4 = verificar0
            if tablero[var1][var2][var3][var4] == 0:
                return casillas
            else:
                return "a1"
        n+=1
    return "a1"
def juega_bot(yo_jugue):
    global turno
    global tablero
    global dic_casillas
    global dic_pos_array
    global pequenos_a_grandes
    global grupos_grandes_pos
    global distancia_grande
    global tableros_bloqueados

    if turno == 0:
        return "c3"
    else:
        pasaber_grupo = pequenos_a_grandes[yo_jugue]
        x1,y1=grupos_grandes_pos[pasaber_grupo]
        for casillas,grupos in pequenos_a_grandes:
            x2,y2=dic_casillas[casillas]
            x2 = (x2 // distancia_grande) * distancia_grande
            y2 = (y2 // distancia_grande) * distancia_grande
            if x2 == x1 and y1 == y2:
                averiguar_indices = dic_pos_array[casillas]
                q,w,e,r=averiguar_indices
                if tablero[q][w][e][r]== 0:
                    for cas, pos in dic_pos_array:
                        pass

#Variables Principales
loop_infinito = True
pagina_principal = True
jugar = False
opciones = False
fin_del_juego = False


#caracteristicas del fuego
distancia_grande=210
distancia_pequena = 70
dimensiones = (630,630)
dic_casillas = encontar_diccionario1() 
dic_pos_array= encontrar_diccionario2()
grupos_grandes_pos,pequenos_a_grandes=definir_subgrupos()

ultima_jugada = 1
lista_figuras = []
tableros_bloqueados = []
bloqueados = []
tablero_a_jugar = (0,0)
turno = 0
yo_jugue = 0

#variables de inicio
tablero_grande = np.zeros((3,3))
tablero = crear_array_tablero()
ultima_jugada = 1
lista_figuras = []
tableros_bloqueados = []
bloqueados = []
tablero_a_jugar = (0,0)
turno = 0
yo_jugue = 0

#Imagenes
camino_fondo= "imagenes\\TableroNuevo2.jpg"
camino_icono = "imagenes\\ICON.png"
camino_borroso = "imagenes\\fondoborroso.jpg"
dibujo_circulo = "imagenes\\Circle.png"
dibujo_equis = "imagenes\\Equis.png"
circulo_rojo = "imagenes\\CirculoRojo.png"
equis_verde = "imagenes\\EquisVerde.png"
game_over = "imagenes\\GameOver.png"
inicio = "imagenes\\Inicio.png"
opciones = "imagenes\\Opciones.png"
subrayado = "imagenes\\Seleccionada.jpg"
playagain = "imagenes\\PlayAgain.png"

#Fondos
icono = pygame.image.load(camino_icono)
fondo = pygame.image.load(camino_fondo)
fondo_borroso = pygame.image.load(camino_borroso)
fondo_game_over = pygame.image.load(game_over)
fondo_pagina_inicial = pygame.image.load(inicio)
fondo_opciones = pygame.image.load(opciones)
cuadro_marcado=pygame.image.load(subrayado)
playagain = pygame.image.load(playagain)

#Configuracion PYGAME
mostrar_importante = fondo
locacion=(0,0)
pantalla = pygame.display.set_mode(dimensiones)
pygame.display.set_caption("Tic Tac Toe")
pygame.display.set_icon(icono)


# hasta salir
while loop_infinito:
    #variables del robot
    jugar_contra_bot = False

    #variablesa loop infinito
    loop_infinito = False
    #Loop Inicio 
    while pagina_principal:
        pantalla.blit(fondo_pagina_inicial,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pagina_principal = False
                opciones = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click1 = pygame.mouse.get_pos()
                eleccion_inicial(click1)
        pygame.display.update()
    # Loop Opciones
    while opciones:
        pantalla.blit(fondo_opciones,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                opciones = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click2 = pygame.mouse.get_pos()
                eleccion_opciones(click2)   
        pygame.display.update()
    #Loop princial
    while jugar:
        pantalla.blit(fondo,(0,0))
        pantalla.blit(mostrar_importante,locacion)

        # codigo experimental de bot
        if jugar_contra_bot:
            if ultima_jugada == 1:
                casilla = turno_bot()
                funcion_jugar(casilla)
                ganar_un_tablero(casilla)
                ganador_absoluto()


        #print(posicion)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                jugar = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordenada = pygame.mouse.get_pos()
                casilla = casilla_juego(coordenada,dic_casillas)
                funcion_jugar(casilla)
                ganar_un_tablero(casilla)
                ganador_absoluto()
                mostrar_arreglos(tablero)  
        mostrar(lista_figuras)
        verificar_tablas()
        pygame.display.update()
    #Loop Final
    while fin_del_juego:
        pantalla.blit(fondo_borroso,(0,0))
        pantalla.blit(fondo_game_over, (30,10))
        pantalla.blit(texto_final(),(180,500))
        pantalla.blit(playagain,(155,530))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                fin_del_juego = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                coordenada = pygame.mouse.get_pos()
                jugar_otra_vez(coordenada)
        pygame.display.update()

pygame.quit()
