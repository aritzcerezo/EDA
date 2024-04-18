'''
En este Script, se definiran las funciones tales que dada una url de 'transfermarkt' que contiene a los jugadores 
de alguno de los equipos de la primera división española de futbol, devuelve un DataFrame con los siguientes datos de
los jugadores: Nombre Completo, Posición, Edad, Nacionalidad (No se considera que hayan obtenido una nueva nacionalidad), y valor de mercado.
'''

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 
import requests
from fake_useragent import UserAgent    

def get_soup(url):
    '''
    Esta función crea la 'Soup' mediante BeautifulSoup
    '''
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup=BeautifulSoup(response.text, 'html.parser')
    return soup

def nombres(soup):
    '''
    Esta función devuelve una lista con los nombres de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("table", class_="inline-table")
    for jug in jugadores:
        link=jug.find("a")
        nombre=link.text.strip()
        list.append(nombre)
    return list


def posiciones(soup):
    '''
    Esta función devuelve una lista con las posiciones de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td", class_="posrela")
    for jg in jugadores:
        posi=jg.find_all("tr")[-1]
        list.append(posi.text.strip())
    return list

def edades(soup):
    '''
    Esta función devuelve una lista con las edades de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td",class_="zentriert")
    for i in range(len(jugadores)):
        if i%4==1:
            edad=jugadores[i]   
            list.append(edad.text.strip())
    return list

def nacionalidades(soup):
    '''
    Esta función devuelve una lista con las nacionalidades de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td",class_="zentriert")
    for i in range(len(jugadores)):
        if i%4==2:
            nac=jugadores[i].find("img")['title']
            list.append(nac)
    return list

def valores(soup):
    '''
    Esta función devuelve una lista con los valores de mercado de los jugadores
    '''
    list=[]
    jugadores = soup.find("table", class_="items").find_all("td", class_="rechts hauptlink")
    for jg in jugadores:
        precio=jg.find("a")
        if precio:
            list.append(precio.text.strip())
        else:
            list.append("Desconocido")
    return list

def crear_df(soup):
    '''Crea un DataFrame de un equipo de futbol a partir de una sopa de BeautifulSoup con Nombre, Edad, Posición
     Nacionalidad y Valor de Mercado '''
    dict = {'Nombre' : nombres(soup),
        'Edad':edades(soup),
        'Posición' : posiciones(soup),
        'Nacionalidad': nacionalidades(soup),
        'Valor_Mercado':valores(soup)
    }
    df=pd.DataFrame(dict)
    return df
    

def data_equipo(df,equipo):
    '''Dado un data frame con datos de partidos de futbol, devuelve un dataframe especifico de
    los datos de un equipo concreto'''
    partidos_equipo=df[(df['HomeTeam'] == equipo) | (df['AwayTeam'] == equipo)]
    return partidos_equipo

def victorias(df_equipo,equipo):
     '''Dado un data frame con los datos de los partidos de un equipo, devuelve el número de victorias de ese equipo'''
     return len(df_equipo[(df_equipo['HomeTeam'] == equipo) & (df_equipo['FTR'] == 'H')]) + len(df_equipo[(df_equipo['AwayTeam'] == equipo) & (df_equipo['FTR'] == 'A')])

def empates(df_equipo,equipo):
    '''Dado un data frame con los datos de los partidos de un equipo, devuelve el número de empates de ese equipo'''
    return len(df_equipo[(df_equipo['HomeTeam'] == equipo) & (df_equipo['FTR'] == 'D')]) + len(df_equipo[(df_equipo['AwayTeam'] == equipo) & (df_equipo['FTR'] == 'D')])

def derrotas(df_equipo,equipo):
    '''Dado un data frame con los datos de los partidos de un equipo, devuelve el número de derrotas de ese equipo'''
    return len(df_equipo[(df_equipo['HomeTeam'] == equipo) & (df_equipo['FTR'] == 'A')]) + len(df_equipo[(df_equipo['AwayTeam'] == equipo) & (df_equipo['FTR'] == 'H')])

def goles_marcados(df_equipo,equipo):
    '''Devuelve el número de goles que ha marcado el equipo en la temporada'''
    return df_equipo[df_equipo['HomeTeam'] == equipo]['FTHG'].sum() + df_equipo[df_equipo['AwayTeam'] == equipo]['FTAG'].sum()
    

def goles_en_contra(df_equipo,equipo):
    '''Devuelve el número de goles que le han marcado al equipo en la temporada'''
    return df_equipo[df_equipo['HomeTeam'] == equipo]['FTAG'].sum() + df_equipo[df_equipo['AwayTeam'] == equipo]['FTHG'].sum()
    
def data_local(df_equipo,equipo):
    '''Devuelve un DataFrame con los partidos que ha jugado de Local un equipo '''
    df_local=df_equipo[df_equipo['HomeTeam']==equipo]
    return df_local

def data_visitante(df_equipo,equipo):
    '''Devuelve un DataFrame con los partidos que ha jugado de Visitante un equipo '''
    df_visitante=df_equipo[df_equipo['AwayTeam']==equipo]
    return  df_visitante