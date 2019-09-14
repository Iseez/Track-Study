import csv, random, copy
from fuzzywuzzy import fuzz

#Función para desordenar de forma "ordenada" arreglos
def shuf(l,arr):
    sa = []     #Aquí se van a poner los indices de la matriz
    arr1 = copy.deepcopy(arr)   #Se copia el arreglo para modificarlo
    #Aqui se le introducen los indices
    for i in range(l):
        sa.append(i)
    random.shuffle(sa)      #Se revuelven los indices
    arr_s = []      #Aquí se introducirá la matriz desordenada "en orden"
    #Se desordena la matriz con el desorden preestablecido
    for i in range(l):
        arr_s.append(arr1[sa[i]])
        arr_s[i].append(sa[i])
    return arr_s

#Función que evalua que tan parecidos son dos strings
def comp(str1,str2):
    r = fuzz.ratio(str1,str2)   #Comparación directa
    p = fuzz.partial_ratio(str1,str2)       #Comparación por separación parcial
    to = fuzz.token_sort_ratio(str1,str2)   #Investigar bien
    te = fuzz.token_set_ratio(str1,str2)    #x2
    return (r+p+to+te)/400      #Se devuelve el promedio sin porcentaje.

#Esta función va a realizar las preguntas y a unir todo en varios arrays
def preguntas(path):
    arr = []        #En este array se introducirá el archivo csv
    #Se lee el archivo csv y se introduce en el array anterior, el encoding a usar es utf-8, para que se muestren
    #las preguntas correctamente
    with open(path,encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            arr.append(row)
    l = len(arr)        #Número de filas que tiene el arreglo
    arr_s = shuf(l,arr)     #Se desordena de "de forma ordenada el arreglo"
    resp = []       #Aquí se introducirán las respuestas
    val = [0]*l     #Aquí se introducirá el que tan parecidos son las respuestas introducidas a las preestablecidas
    print("Escriba 'Salir!' en cualquier momento para salir del programa")
    #Aquí sucede la magía:
    for i in range(l):
        r = input(arr_s[i][0]+":\n")    #Se hace la pregunta y se espera una respuesta
        if r == "Salir!":       #De esta forma se sale del programa
            return 0
        else:
            arr_s[i].append(r)              #Se agrega la respuesta introducida al array desordenado de Q&A
            arr[int(arr_s[i][2])].append(r)        #Se agrega la respuesta al array de respuestas
            o = arr_s[i][1]     #Le llamamos "o" a la respuesta original
            n = arr_s[i][3]     #Le llamamos "n" a la respuesta nueva
            #Se separan las preguntas, si se espera un numero o no
            if o.isdigit():     #Si es un numero entonces:
                if n.isdigit():     #Si el nuevo string es un número se evalua
                    val[int(arr_s[i][2])]=fuzz.ratio(o,n)/100       #Se comparan los string
                    if val[int(arr_s[i][2])] >= 0.8:       #Si es mayor a 0.8 está bien
                        print("Correcto")
                        arr[int(arr_s[i][2])].append("Correcto")    #Se agrega la revisión
                    else:
                        print("Incorrecto")     #Si es menor a 0.8 está mal
                        arr[int(arr_s[i][2])].append("Incorrecto")
                else:       #Si el nuevo string es un número, automaticamente está mal
                    val[int(arr_s[i][2])]=0
                    print("Incorrecto")
                    arr[int(arr_s[i][2])].append("Incorrecto")
            else:
                if o == n:      #Si son identicos o y n, inmediatamente está bien
                    val[int(arr_s[i][2])] = 1   #Al ser identicos el valor de comparación es 1. Este valor se va al arreglo
                    print("Correcto")           #de valores*    #Se indica que la respuesta fue correcta**
                    arr[int(arr_s[i][2])].append("Correcto")     #Esto se va al arreglo de respuestas***
                else:
                    val[int(arr_s[i][2])] = comp(o,n)   #Se hace la comparación entre las respuestas nuevas y las originales
                    if val[int(arr_s[i][2])] >= 0.75:   #Si es al menos un 75% parecida se considera correcta
                        print("Correcto")       #**
                        arr[int(arr_s[i][2])].append("Correcto")      #***
                    elif val[int(arr_s[i][2])] >= 0.65: #Si está entr 65% y 75% su parecido, podría estar o no correcta
                        print("Revisar")        #Se indica que es buena idea revisar esta respuesta
                        arr[int(arr_s[i][2])].append("Revisar")   #***
                    else:
                        print("Incorrecto")     #Si el paecido es menor al 65%, se considera que la respuesta está mal
                        arr[int(arr_s[i][2])].append("Incorrecto")    #***
    ca = 0      #Se va a dar una calificación
    for i in range(l):
        ca += val[i]
    ca /=l
    print("Calificación: ",ca*10)
    return arr       #Estos arreglos son necesarios para generar el csv con feedback para el usuario

#Esta función genera un csv con tus respuestas y las originales, tambén muestra si fue correcta o no
def genfile(arr):
    if arr == 0:
        print("Se interrumpió la sesión")
        return 0
    else:
        #Se pide la dirección donde se generará el archivo
        path = input("Selecciona la ruta del archivo y nombre. Ejemplo: C:/Ruta/del/archivo/my_archivo.csv")
        #Numero de preguntas que hay
        l = len(arr)
        #Titulos de las columnas
        rs = [["Pregunta","La respuesta","Tu respuesta","Calificación"]]    #Aquí se agragará todo lo que se desea en el csv
        for i in range(l):
            rs.append(arr[i])
        #En la dirección indicada se guarda como csv el array creado, el encoding a usar es ANSI, ya que este nos
        #permite visualizar el archivo correctamente el archivo en excel y bloc de notas
        with open(path,"w",encoding="ANSI") as myfile:
            writer = csv.writer(myfile,dialect="excel")
            writer.writerows(rs)
        #El programa finalizó con exito
        print("El archivo de evaluación ha sido generado")
    return rs

def cuestionario(path):
    genfile(preguntas(path))

print("Selecciona la ruta del archivo y nombre. Ejemplo: C:/Ruta/del/archivo/my_archivo.csv")
path = input("Dirección del archivo:")

#Se ejecuta la función
cuestionario(path)
#C:/Users/Acer/Documents/compu2/Proyecto/
