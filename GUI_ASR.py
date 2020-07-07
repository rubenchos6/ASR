from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from scipy.io.wavfile import write, read
import pyaudio, wave
import threading
import pandas as pd
import matplotlib as plt
plt.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
#import librosa

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure



########################## Config DataBase

def config():
    fonema = ['A', 'B', 'THETA', 'CH', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L', 'LL', 'M', 'N', 'Ñ', 'O', 'P', 'R', 'RR',
              'S', 'T', 'U', 'KS', 'Y']
    gen = ['H', 'M']
    edad = ['N', 'P', 'A']
    ######################################################################################
    # Base de datos generada

    newDBHeader = ['CODIGO', 'FORMANTE 1', 'FORMANTE 2', 'FORMANTE 3', 'FORMANTE 4', 'FORMANTE 5', 'FORMANTE 6',
                   'FORMANTE 7']
    global distance_columns
    distance_columns = newDBHeader[1:4]
    global data1
    data1 = pd.read_csv('BD_Formantes.xlsx')
    new_header = data1.iloc[0]
    data1 = data1[1:]
    data1.columns = new_header

    ######################################################################################
    # Base de datos sólo vocales

    global dataVocals
    dataVocals = pd.read_csv('BD_Formantes2.xlsx')
    new_header = dataVocals.iloc[0]
    dataVocals = dataVocals[1:]
    dataVocals.columns = new_header

    ######################################################################################
    # Creamos base de datos estadística localmente solo Fonemas
    global statisticDBA
    statisticDBA = []
    for letter in fonema:
        dataAux = data1[((data1['FONEMA'] == letter))]
        dic = {}
        for j in range(1, 8):
            nums = np.array(dataAux['FORMANTE ' + str(j)])
            res = []
            for i in range(len(nums)):
                if (nums[i] != '0'):
                    res.append(float(nums[i]))

            if (len(res) != 0):
                res = np.array(res)
                mean = np.mean(res)
                dic['FORMANTE ' + str(j)] = mean
            restuple = []
            restuple.append(letter)
        for i in dic.values():
            restuple.append(i)
        statisticDBA.append(restuple)

    statisticDBA = pd.DataFrame(statisticDBA)
    statisticDBA.columns = newDBHeader
    ######################################################################################
    # Creamos base de datos estadística localmente con TODO
    statisticDB = []
    for letter in fonema:
        for g in gen:
            for age in edad:
                dataAux = data1[((data1['FONEMA'] == letter) & (data1['EDAD'] == age) & (data1['GENERO'] == g))]
                dic = {}
                for j in range(1, 8):
                    nums = np.array(dataAux['FORMANTE ' + str(j)])
                    res = []
                    for i in range(len(nums)):
                        if (nums[i] != '0'):
                            res.append(float(nums[i]))

                    if (len(res) != 0):
                        res = np.array(res)
                        mean = np.mean(res)
                        dic['FORMANTE ' + str(j)] = mean
                    restuple = []
                    restuple.append(letter + '_' + age + '_' + g)
                for i in dic.values():
                    restuple.append(i)

                statisticDB.append(restuple)
    statisticDB = pd.DataFrame(statisticDB)
    statisticDB.columns = newDBHeader

    ######################################################################################
    # Creacion de base de datos estadística local con TODO

    global statisticDBVocals
    statisticDBVocals = []
    for letter in ['A', 'E', 'I', 'O', 'U']:
        for g in gen:
            for age in edad:
                dataAux = data1[
                    ((dataVocals['FONEMA'] == letter) & (dataVocals['EDAD'] == age) & (dataVocals['GENERO'] == g))]
                dic = {}
                for j in range(1, 8):
                    nums = np.array(dataAux['FORMANTE ' + str(j)])
                    res = []
                    for i in range(len(nums)):
                        if (nums[i] != '0'):
                            res.append(float(nums[i]))

                    if (len(res) != 0):
                        res = np.array(res)
                        mean = np.mean(res)
                        dic['FORMANTE ' + str(j)] = mean
                    restuple = []
                    restuple.append(letter)
                for i in dic.values():
                    restuple.append(i)

                statisticDBVocals.append(restuple)

            statisticDBVocals = pd.DataFrame(statisticDBVocals)
            statisticDBVocals.columns = newDBHeader
    ######################################################################################
    # Creacion de base de datos estadística local sólo Vocales
    global statisticDBVocalsA
    statisticDBVocalsA = []
    for letter in ['A', 'E', 'I', 'O', 'U']:
        dataAux = dataVocals[((dataVocals['FONEMA'] == letter))]
        dic = {}
        for j in range(1, 8):
            nums = np.array(dataAux['FORMANTE ' + str(j)])
            res = []
            for i in range(len(nums)):
                if (nums[i] != '0'):
                    res.append(float(nums[i]))

            if (len(res) != 0):
                res = np.array(res)
                mean = np.mean(res)
                dic['FORMANTE ' + str(j)] = mean
            restuple = []
            restuple.append(letter)
        for i in dic.values():
            restuple.append(i)

        statisticDBVocalsA.append(restuple)

    statisticDBVocalsA = pd.DataFrame(statisticDBVocalsA)
    statisticDBVocalsA.columns = newDBHeader

##########################  Read File
def fileDialog():
    global rate, audio1Chan
    filename = filedialog.askopenfile(initialdir="/", title="Select a File", filetype=(("wav", "*.wav"), ("All Files", "*.*")))
    #label = Label(window, text="")
    #label.grid( row=8, column=0)
    #label.configure(text=filename.name)


    text = filename.name
    e1.delete(0, "end")
    e1.insert(0, text)
    rate, audio1Chan = read(filename.name)


##########################  Record audio

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
frames = []


def startrecording():
    global p
    global stream
    global isrecording
    isrecording = False
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format, channels=channels, rate=fs,
                              frames_per_buffer=chunk, input=True)
    isrecording = True

    text2= 'Recording'
    e2.delete(0, "end")
    e2.insert(0, text2)
    t = threading.Thread(target=record)
    t.start()

def stoprecording():
    isrecording = False
    text2 = 'recording complete'
    e2.delete(0, "end")
    e2.insert(0, text2)
    filename = e1.get()
    filename = filename + ".wav"
    e1.delete(0, "end")
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def record():
    while isrecording:
        data = stream.read(chunk)
        frames.append(data)


########################## PLOT

def plot():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    v = np.array([16, 16.31925, 17.6394, 16.003, 17.2861, 17.3131, 19.1259, 18.9694, 22.0003, 22.81226])
    p = np.array([16.23697, 17.31653, 17.22094, 17.68631, 17.73641, 18.6368,
                  19.32125, 19.31756, 21.20247, 22.41444, 22.11718, 22.12453])

    fig = Figure(figsize=(6, 6))
    a = fig.add_subplot(111)
    a.scatter(v, x, color='red')
    a.plot(p, range(2 + max(x)), color='blue')
    a.invert_yaxis()

    a.set_title("Estimation Grid", fontsize=16)
    a.set_ylabel("Y", fontsize=14)
    a.set_xlabel("X", fontsize=14)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()

########################### ASR

def findFormantes(datos):
    datos = np.asfortranarray(datos)
    A = librosa.lpc(datos, 16)
    raices = np.roots(A)  # formantes!
    formantes = []
    for k in raices:
        if (k.imag > 0):
            w = np.arctan2(k.imag, k.real)
            Fk = w * (rate / (2 * np.pi))
            Bw = (-1 / 2) * (rate / (2 * np.pi)) * np.log((k.real ** 2 + k.imag ** 2) ** (1 / 2))
            if (Fk > 90 and Bw < 450):
                formantes.append(Fk)

    return np.sort(formantes)


def findLetra(newFonema, data, distance_columns, distance):
    #################################################
    # Encuentra letra más cercana
    data_Formants = data[distance_columns].astype(float)
    data_Formants.fillna(0, inplace=True)
    data_F_norm = (data_Formants - data_Formants.mean()) / data_Formants.std()
    letraNorm = (newFonema - data_Formants.mean()) / data_Formants.std()

    euclidian_distances = data_F_norm.apply(lambda row: scipy.spatial.distance.euclidean(row, letraNorm), axis=1)
    indices = euclidian_distances.sort_values().index
    cont = 0
    # print(indices)
    res = []
    for i in indices[:5]:
        if (euclidian_distances.sort_values().iloc[cont] > distance):
            break
        try:
            res.append(data.iloc[i - 2][['FONEMA', 'EDAD', 'GENERO', 'ID']],
                       euclidian_distances.sort_values().iloc[cont])  # global
        except:
            res.append(data.iloc[i - 2]['CODIGO'], euclidian_distances.sort_values().iloc[cont])  # statisticDB
        cont += 1
    return res

def aproxWord(matrixOfFormants,data,distance_columns,distance,res):
  #################################################
  res=[]
  #Divide el espectrograma en sus partes
  for i in matrixOfFormants:
    j=i[1][0:3]
    res.append("Ventana: "+str(i[0]))
    for j in (findLetra(j,data,distance_columns,distance)):
      res.append(j)
  return res


def runASR(audio, rate, muestras, distance_columns, distance):
    # Plot audio

    rate, audio = read(audioName)
    try:
        audio = audio[:, 1]
    except:
        audio = audio

    plt.plot(audio)
    print(len(audio))

    ############################################################################
    # Plot Spectrogram and characteristics
    plt.figure()
    audioFiltrado = lfilter([1], [1, 0.63], audio)
    # muestras= 1024   # 21 ms
    s, w, t, im = plt.specgram(audioFiltrado, Fs=rate, NFFT=muestras, window= scipy.signal.blackman(muestras),
                               noverlap=100)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

    print("Vector que van a poblar nuestras frecuencias es de tamaño:")
    print(len(s))
    print("Número de ventanas:")
    print(len(s[0]))
    print("Tenemos la siguiente cantidad de frecuencia")
    print(len(w))
    # print(s)
    #############################################################################
    # Creamos una matriz con las formantes de todo el audio arrojadas por el espectro
    i = 0
    matrixFormantsSpectro = []
    for i in range(len(s[0])):
        try:
            valor = findFormantes(s[:, i])
            if (len(valor) > 2):
                matrixFormantsSpectro.append([i, valor])
        except:
            a = 1
    #############################################################################
    # Llamamos función para calcular la palabra aproximada

    array1 = aproxWord(matrixFormantsSpectro, statisticDBVocalsA, distance_columns, distance)
    array2 = aproxWord(matrixFormantsSpectro, statisticDBVocals, distance_columns, distance)
    array3 = aproxWord(matrixFormantsSpectro, statisticDB, distance_columns, distance)
    array4 = aproxWord(matrixFormantsSpectro, statisticDBA, distance_columns, distance)

    for l1 in array1:
        list1.insert(END, l1)
    for l2 in array2:
        list2.insert(END, l2)
    for l3 in array3:
        list3.insert(END, l3)
    for l4 in array4:
        list4.insert(END, l4)

def runASR2():
    runASR(audio, rate, 1024, distance_columns, 0.25)

##########################  WINDOW

def window():

    global window
    global isrecording
    window = Tk()
    window.minsize(700, 700)


    l1 = Label(window,text='File')
    l1.grid(row=0, column=0)


    # Define Entries
    global e1
    file_text = StringVar()
    e1 = Entry(window, textvariable = file_text)
    e1.grid(row=0,column=1)

    l6 = Label(window, text='Status')
    l6.grid(row=0, column=2)

    # Define Entries
    global e2
    status_text = StringVar()
    e2 = Entry(window, textvariable=status_text)
    e2.grid(row=0, column=3)


    l2 = Label(window, text='Vocals')
    l2.grid(row=2, column=0)
    #Define list box
    global list1
    list1 = Listbox(window, height=6, width=35 )
    list1.grid(row=3, column=0,rowspan=6, columnspan=2)


    # Atach scrollbarr to the list
    sb1 = Scrollbar(window)
    sb1.grid(row=3, column=2, rowspan=6)

    list1.configure(yscrollcommand =sb1.set)

    sb1.configure(command=list1.yview)

    # Define list box
    global list2
    list2 = Listbox(window, height=6, width=35)
    list2.grid(row=3, column=3, rowspan=6, columnspan=2)

    # Atach scrollbarr to the list
    sb2 = Scrollbar(window)
    sb2.grid(row=3, column=5, rowspan=6)

    list2.configure(yscrollcommand=sb2.set)

    sb2.configure(command=list2.yview)


    l3 = Label(window, text='All Fonemas')
    l3.grid(row=10, column=0)
    # Define list box
    global list3
    list3 = Listbox(window, height=6, width=35)
    list3.grid(row=11, column=0, rowspan=6, columnspan=2)

    # Atach scrollbarr to the list
    sb3 = Scrollbar(window)
    sb3.grid(row=11, column=2, rowspan=6)

    list3.configure(yscrollcommand=sb3.set)

    sb3.configure(command=list3.yview)

    # Define list box
    global list4
    list4 = Listbox(window, height=6, width=35)
    list4.grid(row=11, column=3, rowspan=6, columnspan=2)

    # Atach scrollbarr to the list
    sb4 = Scrollbar(window)
    sb4.grid(row=11, column=5, rowspan=6)

    list4.configure(yscrollcommand=sb4.set)

    sb4.configure(command=list4.yview)

    l4 = Label(window, text='Posible Word')
    l4.grid(row=17, column=0)

    # Define list box
    global list5
    list5 = Listbox(window, height=6, width=35)
    list5.grid(row=18, column=0, rowspan=6, columnspan=2)

    # Atach scrollbarr to the list
    sb5 = Scrollbar(window)
    sb5.grid(row=18, column=2, rowspan=6)

    list5.configure(yscrollcommand=sb5.set)

    sb5.configure(command=list5.yview)



    #Define buttons
    b1 = Button(window, text="File",width=12, command=fileDialog)
    b1.grid(row=5, column=10)

    b1 = Button(window, text="Record", width=12, command=startrecording)
    b1.grid(row=6, column=10)

    b1 = Button(window, text="Stop", width=12, command=stoprecording)
    b1.grid(row=7, column=10)

    b1 = Button(window, text="Run ASR", width=12, command=runASR2)
    b1.grid(row=8, column=10)

    b1 = Button(window, text="Reset", width=12)
    b1.grid(row=9, column=10)
    plot()

if __name__ == '__main__':
    try:
        window()

    except:
        pass

window.title('Sistema de reconocimiento de voz automático')
window.mainloop()


