# -*- coding: utf-8 -*-
"""ProyectoFinal_PDS_code1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yFYurZ1jzN0zATxvSAIw9YdcqbJq-kkJ

Librerías
"""

pip install librosa --upgrade

from scipy.io.wavfile import write, read
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from numpy import fft
from IPython.display import Audio
import scipy.signal
from scipy.signal import lfilter, hamming
import librosa
import pandas as pd

from google.colab import auth
auth.authenticate_user()
import gspread
from oauth2client.client import GoogleCredentials
gc = gspread.authorize(GoogleCredentials.get_application_default())
from gspread_dataframe import set_with_dataframe

"""Captura de audios para base de datos"""

fonema=['A','B','THETA','CH','D','E','F','G','I','J','K','L','LL','M','N','Ñ','O','P','R','RR','S','T','U','KS','Y']
header=['FONEMA',	'EDAD',	'GENERO',	'ID',	'FORMANTE 1',	'FORMANTE 2',	'FORMANTE 3',	'FORMANTE 4','FORMANTE 5','FORMANTE 6','FORMANTE 7']
gen=['H','M']
edad=['N','P','A']

sheet=gc.open_by_url('https://docs.google.com/spreadsheets/d/1r_nu3vtCngaU2RCSibHOx3r0alogaUriaAKh9fY1-Rg/edit#gid=0').sheet1

#prueba=pd.DataFrame(abc)
#set_with_dataframe(sheet,prueba)

rate, audio1Chan = read("A_A_H_26.wav")


rate, audio1Chan = read("A_A_H_3.wav")

oneChannelOnly(audio1Chan)

def oneChannelOnly(file):
  try:
      res = file[:,1]
  except:
      res = file
  return np.array(res)

matrixOfFormant=[header]
for letter in fonema:
  for g in gen:
    for age in edad:
      for i in range(1,28):
        try:  
          text=letter+'_'+age+'_'+g+'_'+str(i)+'.wav'
          #try:
          rate, audio1Chan=read(text)
          audio1Chan=oneChannelOnly()
          N = len(audio1Chan)
          hamming = scipy.signal.hamming(N)
          file_H = audio1Chan * hamming
          res = lfilter([1],[1, 0.63],file_H)
          A = librosa.lpc(res, 16)
          raices = np.roots(A) #formantes!
          formantes=[]
          for k in raices:
            if(k.imag>0):
              w = np.arctan2(k.imag, k.real)
              Fk = w*(rate/(2*np.pi))
              Bw = (-1/2)*(rate/(2*np.pi))*np.log((k.real**2+k.imag**2)**(1/2))
              if(Fk>90 and Bw<450):
                formantes.append(Fk)

          resFormantes=[]
          resFormantes.append(letter) #Fonema
          resFormantes.append(age) #Edad
          resFormantes.append(g) #Genero
          resFormantes.append(i) #iD
          for k in np.round(np.sort(formantes),2): #Formantes en orden
            resFormantes.append(k)
        #Meterla en el csv

          matrixOfFormant.append(resFormantes)
        except:
          a = 1
          #print(text)
          #break;

matrixOfFormant=[header]
for letter in fonema:
  for g in gen:
    for age in edad:
      for i in range(1,28):
        try:  
          text=letter+'_'+age+'_'+g+'_'+str(i)+'.wav'
          #try:
          rate, audio1Chan=read(text)
          audio1Chan=oneChannelOnly()
          N = len(audio1Chan)
          hamming = scipy.signal.hamming(N)
          file_H = audio1Chan * hamming
          res = lfilter([1],[1, 0.63],file_H)
          A = librosa.lpc(res, 16)
          raices = np.roots(A) #formantes!
          formantes=[]
          for k in raices:
            if(k.imag>0):
              w = np.arctan2(k.imag, k.real)
              Fk = w*(rate/(2*np.pi))
              Bw = (-1/2)*(rate/(2*np.pi))*np.log((k.real**2+k.imag**2)**(1/2))
              if(Fk>90 and Bw<450):
                formantes.append(Fk)

          resFormantes=[]
          resFormantes.append(letter) #Fonema
          resFormantes.append(age) #Edad
          resFormantes.append(g) #Genero
          resFormantes.append(i) #iD
          for k in np.round(np.sort(formantes),2): #Formantes en orden
            resFormantes.append(k)
        #Meterla en el csv

          matrixOfFormant.append(resFormantes)
        except:
          a = 1
          #print(text)
          #break;

matrixOfFormant=[header]
for letter in fonema:
  for g in gen:
    for age in edad:
      for i in range(1,28):
        try:  
          text=letter+'_'+age+'_'+g+'_'+str(i)+'.wav'
          #try:
          rate, audio1Chan=read(text)
          audio1Chan=oneChannelOnly(audio1Chan)
          N = len(audio1Chan)
          hamming = scipy.signal.hamming(N)
          file_H = audio1Chan * hamming
          res = lfilter([1],[1, 0.63],file_H)
          A = librosa.lpc(res, 16)
          raices = np.roots(A) #formantes!
          formantes=[]
          for k in raices:
            if(k.imag>0):
              w = np.arctan2(k.imag, k.real)
              Fk = w*(rate/(2*np.pi))
              Bw = (-1/2)*(rate/(2*np.pi))*np.log((k.real**2+k.imag**2)**(1/2))
              if(Fk>90 and Bw<450):
                formantes.append(Fk)

          resFormantes=[]
          resFormantes.append(letter) #Fonema
          resFormantes.append(age) #Edad
          resFormantes.append(g) #Genero
          resFormantes.append(i) #iD
          for k in np.round(np.sort(formantes),2): #Formantes en orden
            resFormantes.append(k)
        #Meterla en el csv

          matrixOfFormant.append(resFormantes)
        except:
          a = 1
          #print(text)
          #break;

matrixOfFormant

prueba=pd.DataFrame(matrixOfFormant)
set_with_dataframe(sheet,prueba)

"""Creacion de base de datos con sus estadísticas"""

wb=gc.open_by_url('https://docs.google.com/spreadsheets/d/1r_nu3vtCngaU2RCSibHOx3r0alogaUriaAKh9fY1-Rg/edit#gid=0').sheet1
newDBHeader=['CODIGO','FORMANTE 1','FORMANTE 2','FORMANTE 3','FORMANTE 4','FORMANTE 5','FORMANTE 6','FORMANTE 7']
statisticDB=[newDBHeader]
data1=pd.DataFrame(wb.get_all_values())
new_header=data1.iloc[1]
data1=data1[2:]
data1.columns=new_header
data1

statisticDB = []
for letter in fonema:
  for g in gen:
    for age in edad:
      dataAux=data1[((data1['FONEMA']==letter) &  (data1['EDAD']==age) & (data1['GENERO']==g))]
      #dataAux=data[(data['FONEMA']==letter)]
      dic={}
      for j in range(1,8):
        nums=np.array(dataAux['FORMANTE '+str(j)])
        res=[]
        for i in range(len(nums)):
          if(nums[i]!='0'):
            res.append(float(nums[i]))
        
        if(len(res)!=0):
          res=np.array(res)
          mean=np.mean(res)
          #std=np.std(res)
          #dic['FORMANTE '+str(j)]=[mean,std]
          dic['FORMANTE '+str(j)]=mean
        restuple=[]
        restuple.append(letter+'_'+age+'_'+g)
        #restuple.append(letter)
      for i in dic.values():
        restuple.append(i)

      statisticDB.append(restuple)

statisticDB

statisticDB=pd.DataFrame(statisticDB)
statisticDB.columns=newDBHeader
statisticDB

'''
for i in matrixFormantsSpectro:
  print("En la sección "+str(i[0]))
  contFormante=1
  dictRes={}
  for z in i[1]:
      #print('formante '+ str(contFormante))
      for j in range(1,len(statisticDB)):
        try:
          mean=statisticDB[j][contFormante][0]
          std=statisticDB[j][contFormante][1]
          if(z>=mean-std and z<=mean+std):
            #print('Posible en: '+statisticDB[j][0])
            try:
              dictRes[statisticDB[j][0]]=dictRes[statisticDB[j][0]]+(7-contFormante)
            except:
              dictRes[statisticDB[j][0]]=7-contFormante
        except:
          fallas=1      
      contFormante = contFormante + 1

  print(dictRes)
  
  if(len(dictRes)!=0):
    mejor=max(dictRes, key=dictRes.get)
    print(" ")
    print(mejor)
  print(" ")
  '''

"""Código de ejecución"""

#Segundo intento: Espectrograma

audioPrueba='Hola_Mundo_M.wav'

rate,audio=read(audioPrueba)
try:
  audio=audio[:,1]
except:
    audio=audio
###################################
#Plot audio in time
#n = np.arange(lenaudio) 
plt.plot(audio)
###################################
muestras= 1024   # 21 ms

#######################################
#Spectrogram

#Preenfasis
audioFiltrado = lfilter([1],[1, 0.63],audio)

s, w, t, im=plt.specgram(audioFiltrado,Fs=rate,NFFT=muestras,window=scipy.signal.blackman(muestras))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

print("Vector que van a poblar nuestras frecuencias es de tamaño:")
print(len(s))
print("Número de ventanas:")
print(len(s[0]))
print("Tenemos la siguiente cantidad de frecuencia")
print(len(w))

i = 0
matrixFormantsSpectro=[]
for i in range(len(s[0])):
  try:
    valor = findFormantes(s[:,i])
    if(len(valor)>1):
      matrixFormantsSpectro.append([i,valor])
  except:
    a = 1

matrixFormantsSpectro

"""Uso de Kneighbours"""

#Base de datos generada
wb=gc.open_by_url('https://docs.google.com/spreadsheets/d/1r_nu3vtCngaU2RCSibHOx3r0alogaUriaAKh9fY1-Rg/edit#gid=0').sheet1
newDBHeader=['CODIGO','FORMANTE 1','FORMANTE 2','FORMANTE 3','FORMANTE 4','FORMANTE 5','FORMANTE 6','FORMANTE 7']
distance_columns=newDBHeader[1:4] 
data1=pd.DataFrame(wb.get_all_values())
new_header=data1.iloc[1]
data1=data1[2:]
data1.columns=new_header
data1

wb=gc.open_by_url('https://docs.google.com/spreadsheets/d/1KGZJcvLskCMgPWkXqsr6ySL8ept5V4czYBRPqg46irU/edit?usp=drive_web&ouid=107092201184289528225').sheet1
newDBHeader=['CODIGO','FORMANTE 1','FORMANTE 2','FORMANTE 3','FORMANTE 4','FORMANTE 5','FORMANTE 6','FORMANTE 7']
#distance_columns=newDBHeader[1:4] 
dataVocals=pd.DataFrame(wb.get_all_values())
new_header=dataVocals.iloc[1]

dataVocals=dataVocals[2:]
dataVocals.columns=new_header
dataVocals

statisticDBVocals = []
for letter in ['A','E','I','O','U']:
  #for g in gen:
    #for age in edad:
      #dataAux=dataVocals[((dataVocals['FONEMA']==letter) &  (dataVocals['EDAD']==age) & (dataVocals['GENERO']==g))]
  dataAux=dataVocals[((dataVocals['FONEMA']==letter))]
  #dataAux=data[(data['FONEMA']==letter)]
  dic={}
  for j in range(1,8):
    nums=np.array(dataAux['FORMANTE '+str(j)])
    res=[]
    for i in range(len(nums)):
      if(nums[i]!='0'):
        res.append(float(nums[i]))
    
    if(len(res)!=0):
      res=np.array(res)
      mean=np.mean(res)
      #std=np.std(res)
      #dic['FORMANTE '+str(j)]=[mean,std]
      dic['FORMANTE '+str(j)]=mean
    restuple=[]
    #restuple.append(letter+'_'+age+'_'+g)
    restuple.append(letter)
    #restuple.append(letter)
  for i in dic.values():
    restuple.append(i)

  statisticDBVocals.append(restuple)

statisticDBVocals=pd.DataFrame(statisticDBVocals)
statisticDBVocals.columns=newDBHeader
statisticDBVocals

statisticDB = []
for letter in fonema:
  dataAux=data1[((data1['FONEMA']==letter))]
  #dataAux=data[(data['FONEMA']==letter)]
  dic={}
  for j in range(1,8):
    nums=np.array(dataAux['FORMANTE '+str(j)])
    res=[]
    for i in range(len(nums)):
      if(nums[i]!='0'):
        res.append(float(nums[i]))
    
    if(len(res)!=0):
      res=np.array(res)
      mean=np.mean(res)
      #std=np.std(res)
      #dic['FORMANTE '+str(j)]=[mean,std]
      dic['FORMANTE '+str(j)]=mean
    restuple=[]
    restuple.append(letter)
    #restuple.append(letter)
  for i in dic.values():
    restuple.append(i)

  statisticDB.append(restuple)

statisticDB=pd.DataFrame(statisticDB)
statisticDB.columns=newDBHeader
statisticDB

#Normalizamos las 3 primeras formantes
data_2Formants=data1[distance_columns].astype(float)
data_2F_norm=(data_2Formants-data_2Formants.mean())/data_2Formants.std()
data_2F_norm

letraAPrueba=[2300,5000,12000]
letraANorm=(letraAPrueba-data_2Formants.mean())/data_2Formants.std()
letraANorm

data=pd.read_excel('BD_Formantes.xlsx')
newDBHeader=['CODIGO','FORMANTE 1','FORMANTE 2','FORMANTE 3','FORMANTE 4','FORMANTE 5','FORMANTE 6','FORMANTE 7']

distance_columns=newDBHeader[1:4] 
new_header=data.iloc[0]
data=data[1:]
data.columns=new_header

data

def config():
  fonema=['A','B','THETA','CH','D','E','F','G','I','J','K','L','LL','M','N','Ñ','O','P','R','RR','S','T','U','KS','Y']
  gen=['H','M']
  edad=['N','P','A']
  ######################################################################################
  #Base de datos generada

  newDBHeader=['CODIGO','FORMANTE 1','FORMANTE 2','FORMANTE 3','FORMANTE 4','FORMANTE 5','FORMANTE 6','FORMANTE 7']
  global distance_columns
  distance_columns=newDBHeader[1:4] 
  global data1
  data1=pd.read_excel('BD_Formantes.xlsx')
  new_header=data1.iloc[0]
  data1=data1[1:]
  data1.columns=new_header

  ######################################################################################
  #Base de datos sólo vocales

  global dataVocals
  dataVocals=pd.read_excel('BD_Formantes_Vocales.xlsx')
  new_header=dataVocals.iloc[0]
  dataVocals=dataVocals[1:]
  dataVocals.columns=new_header
  
  ######################################################################################
  #Creamos base de datos estadística localmente solo Fonemas
  global statisticDBA
  statisticDBA = []
  for letter in fonema:
    dataAux=data1[((data1['FONEMA']==letter))]
    dic={}
    for j in range(1,8):
      nums=np.array(dataAux['FORMANTE '+str(j)])
      res=[]
      for i in range(len(nums)):
        if(nums[i]!='0'):
          res.append(float(nums[i]))
      
      if(len(res)!=0):
        res=np.array(res)
        mean=np.mean(res)
        dic['FORMANTE '+str(j)]=mean
      restuple=[]
      restuple.append(letter)
    for i in dic.values():
      restuple.append(i)
    statisticDBA.append(restuple)

  statisticDBA=pd.DataFrame(statisticDBA)
  statisticDBA.columns=newDBHeader
  ######################################################################################
  #Creamos base de datos estadística localmente con TODO
  statisticDB = []
  for letter in fonema:
    for g in gen:
      for age in edad:
        dataAux=data1[((data1['FONEMA']==letter) &  (data1['EDAD']==age) & (data1['GENERO']==g))]
        dic={}
        for j in range(1,8):
          nums=np.array(dataAux['FORMANTE '+str(j)])
          res=[]
          for i in range(len(nums)):
            if(nums[i]!='0'):
              res.append(float(nums[i]))
          
          if(len(res)!=0):
            res=np.array(res)
            mean=np.mean(res)
            dic['FORMANTE '+str(j)]=mean
          restuple=[]
          restuple.append(letter+'_'+age+'_'+g)
        for i in dic.values():
          restuple.append(i)

        statisticDB.append(restuple)
  statisticDB=pd.DataFrame(statisticDB)
  statisticDB.columns=newDBHeader

  ######################################################################################
  #Creacion de base de datos estadística local con TODO
  
  global statisticDBVocals
  statisticDBVocals = []
  for letter in ['A','E','I','O','U']:
    for g in gen:
      for age in edad:
        dataAux=data1[((dataVocals['FONEMA']==letter) &  (dataVocals['EDAD']==age) & (dataVocals['GENERO']==g))]
        dic={}
        for j in range(1,8):
          nums=np.array(dataAux['FORMANTE '+str(j)])
          res=[]
          for i in range(len(nums)):
            if(nums[i]!='0'):
              res.append(float(nums[i]))
          
          if(len(res)!=0):
            res=np.array(res)
            mean=np.mean(res)
            dic['FORMANTE '+str(j)]=mean
          restuple=[]
          restuple.append(letter)
        for i in dic.values():
          restuple.append(i)

        statisticDBVocals.append(restuple)

      statisticDBVocals=pd.DataFrame(statisticDBVocalsA)
      statisticDBVocals.columns=newDBHeader
  ######################################################################################
  #Creacion de base de datos estadística local sólo Vocales
  global statisticDBVocalsA
  statisticDBVocalsA = []
  for letter in ['A','E','I','O','U']:
    dataAux=dataVocals[((dataVocals['FONEMA']==letter))]
    dic={}
    for j in range(1,8):
      nums=np.array(dataAux['FORMANTE '+str(j)])
      res=[]
      for i in range(len(nums)):
        if(nums[i]!='0'):
          res.append(float(nums[i]))
      
      if(len(res)!=0):
        res=np.array(res)
        mean=np.mean(res)
        dic['FORMANTE '+str(j)]=mean
      restuple=[]
      restuple.append(letter)
    for i in dic.values():
      restuple.append(i)

    statisticDBVocalsA.append(restuple)

  statisticDBVocalsA=pd.DataFrame(statisticDBVocalsA)
  statisticDBVocalsA.columns=newDBHeader

def findFormantes(datos):
  datos = np.asfortranarray(datos)
  A = librosa.lpc(datos, 16)
  raices = np.roots(A) #formantes!
  formantes=[]
  for k in raices:
    if(k.imag>0):
      w = np.arctan2(k.imag, k.real)
      Fk = w*(rate/(2*np.pi))
      Bw = (-1/2)*(rate/(2*np.pi))*np.log((k.real**2+k.imag**2)**(1/2))
      if(Fk>90 and Bw<450):
        formantes.append(Fk)

  return np.sort(formantes)

def findLetra(newFonema,data,distance_columns,distance):
  #################################################
  #Encuentra letra más cercana
  data_Formants=data[distance_columns].astype(float)
  data_Formants.fillna(0, inplace=True)
  data_F_norm=(data_Formants-data_Formants.mean())/data_Formants.std()
  letraNorm=(newFonema-data_Formants.mean())/data_Formants.std()

  euclidian_distances=data_F_norm.apply(lambda row: scipy.spatial.distance.euclidean(row,letraNorm), axis=1)
  indices=euclidian_distances.sort_values().index
  cont=0
  #print(indices)
  res=[]
  for i in indices[:5]:
    if(euclidian_distances.sort_values().iloc[cont]>distance):
      break
    try:
      res.append(data.iloc[i-2][['FONEMA','EDAD','GENERO','ID']],euclidian_distances.sort_values().iloc[cont]) #global
    except:
      res.append(data.iloc[i-2]['CODIGO'],euclidian_distances.sort_values().iloc[cont]) #statisticDB
    cont+=1
  return res

def aproxWord(matrixOfFormants,data,distance_columns,distance,res):
  #################################################
  res=[]
  #Divide el espectrograma en sus partes
  for i in matrixOfFormants:
    j=i[1][0:3] 
    res.append("Ventana: "+str(i[0]))
    m=findLetra(j,data,distance_columns,distance)
    if(len(m)!=0):
      for k in m:
        res.append(k)
    else:
      try:
        res=res[:len(res)-1]
      except:
        res=[]
  return res

def runASR(audio,rate,muestras,distance_columns,distance):
  #Plot audio

  rate,audio=read(audioName)
  try:
    audio=audio[:,1]
  except:
      audio=audio
 
  plt.plot(audio)
  print(len(audio))
  
  
  ############################################################################
  #Plot Spectrogram and characteristics
  plt.figure()
  audioFiltrado = lfilter([1],[1, 0.63],audio)
  #muestras= 1024   # 21 ms
  s, w, t, im=plt.specgram(audioFiltrado,Fs=rate,NFFT=muestras,window=scipy.signal.blackman(muestras),noverlap=100)
  plt.ylabel('Frequency [Hz]')
  plt.xlabel('Time [sec]')
  plt.show()

  print("Vector que van a poblar nuestras frecuencias es de tamaño:")
  print(len(s))
  print("Número de ventanas:")
  print(len(s[0]))
  print("Tenemos la siguiente cantidad de frecuencia")
  print(len(w))
  #print(s)
  #############################################################################
  #Creamos una matriz con las formantes de todo el audio arrojadas por el espectro
  i = 0
  matrixFormantsSpectro=[]
  for i in range(len(s[0])):
    try:
      valor = findFormantes(s[:,i])
      if(len(valor)>2):
        matrixFormantsSpectro.append([i,valor])
    except:
      a = 1
  #############################################################################
  #Llamamos función para calcular la palabra aproximada
  
  array1=aproxWord(matrixFormantsSpectro,statisticDBVocalsA,distance_columns,distance)
  array2=aproxWord(matrixFormantsSpectro,statisticDBVocals,distance_columns,distance)
  array3=aproxWord(matrixFormantsSpectro,statisticDB,distance_columns,distance)
  array4=aproxWord(matrixFormantsSpectro,statisticDBA,distance_columns,distance)
    for l1 in array1:
      list1.insert(END,l1)
    
    for l2 in array2:
      list2.insert(END,l2)

    for l3 in array3:
      list3.insert(END,l3)

    for l4 in array4:
      list4.insert(END,l4)

runASR(audio,rate,1024,distance_columns,0.25)

runASR('Hola_Mundo_M.wav',1024,statisticDBVocals,distance_columns,2)

runASR('Hola_Mundo_M.wav',1024,dataVocals,distance_columns,0.3)

#Ejemplo de ejecucición

runASR('Hola_Mundo_M.wav',1024,data1,distance_columns,0.1)

runASR('Hola_Mundo_M.wav',1024,statisticDB,distance_columns,0.8)

runASR('Hola_mundo_1.wav',1024,statisticDB,distance_columns,0.3)



def funcionX():
  global prueba
  prueba=4
funcionX()
prueba

prueba