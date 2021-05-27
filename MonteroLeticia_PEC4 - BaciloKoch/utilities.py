# -----------------------------------------------------------------------------
# ------- Código con una serie de funciones que nos serán de utilidad. -------
# -----------------------------------------------------------------------------

# Importamos las librerías que necesitaran nuestras funciones
import re
import os


# Todas las lecturas de ficheros las hemos hecho línea a línea ya que en cada
# función obtenemos una información concreta por lo que así evitamos cargar
# y guardar mucha información innecesaria.


# Función con la que leemos las clases del fichero 'tb_functions.pl' y contamos
# cuantos ORFs pertenecen a cada una de ellas.
def classes_num(file_input):
    """
    Dado un fichero con la estructura de 'tb_functions.pl', devuelve un
    diccionario con el número de ORFs que pertenecen a cada clase.

    :param file_input: normalmente 'tb_functions.pl'
    :return: classes: diccionario con el número de ORFs que pertenecen a cada
                      clase
    """
    # Inicializamos el diccionario
    classes = dict()

    # Abrimos el fichero y tomamos las líneas
    with open(file_input) as f:
        data = f.readlines()
        # Recorremos cada línea, que puede ser class o function
        # Si es class, añadimos la clase y si es function,
        # sumamos uno a la clase correspondiente
        for line in data:
            lineinfo = line.split('(')
            if lineinfo[0] == 'class':
                cls = lineinfo[1].split(',"')[0]
                classes[cls] = 0
            else:
                cls = '[' + lineinfo[1].split(',[')[1].split(']')[0] + ']'
                classes[cls] += 1
    return classes


# Función similar a la anterior pero, en vez de devolver el número de ORFs
# pertenecientes a la clase, devuelve la lista de los mismos
def classes_list(file_input):
    """
    Dado un fichero con la estructura de 'tb_functions.pl', devuelve un
    diccionario con la lista de ORFs que pertenecen a cada una de las clases.

    :param file_input: normalmente 'tb_functions.pl'
    :return: classes: diccionario con las listas de los de ORFs que pertenecen
                      a cada clase
    """
    # Inicializamos el diccionario
    classes = dict()

    # Abrimos el fichero y tomamos las líneas
    with open(file_input) as f:
        data = f.readlines()
        # Recorremos cada línea, que puede ser class o function
        # Si es class, añadimos la clase y si es function,
        # añadimos el orf a la lista de la clase correspondiente
        for line in data:
            lineinfo = line.split('(')
            if lineinfo[0] == 'class':
                cls = lineinfo[1].split(',"')[0]
                classes[cls] = list()
            else:
                cls = '[' + lineinfo[1].split(',[')[1].split(']')[0] + ']'
                orf = lineinfo[1].split(',')[0]
                classes[cls].append(orf)
    return classes


# Función con la buscamos qué clase tiene una descripción dada
def des_class(file_input, classdes):
    """
    Dado un fichero con la estructura de 'tb_functions.pl', devuelve la clase
    que tiene la descripción 'classdes'.

    En caso de no encontrar ninguna, devuelve la clase [0,0,0,0].

    :param file_input: normalmente 'tb_functions.pl'
    :param classdes: string con la descripción que buscamos
    :return: def_class: clase con la definición que buscamos
    """
    # Definimos una clase por defecto en caso de no encontrar ninguna con la
    # descripción dada
    def_class = '[0,0,0,0]'

    # Abrimos el fichero y tomamos las líneas
    with open(file_input) as f:
        data = f.readlines()

        # Recorremos cada línea, buscando las clases que tengan
        # la descripción 'classdes'
        for line in data:
            lineinfo = line.split('(')
            if lineinfo[0] == 'class':
                des = lineinfo[1].split('"')[1]
                if des == classdes:
                    return lineinfo[1].split(',"')[0]
    return def_class


# Función que extrae el número de ORFs pertenecientes a una clase
# con una descripción concreta
def orf_des_class(file_input, classdes):
    """
    Dado un fichero con la estructura de 'tb_functions.pl', devuelve el número
    de ORFs que pertenecen a la clase con la descripción 'classdes'.

    En caso de no encontrar ninguna, devuelve 0.

    :param file_input: normalmente 'tb_functions.pl'
    :param classdes: string con la descripción que buscamos
    :return: num_orfs: número de ORFs en la clase con dicha descripción
    """
    # Predefinimos el número de ORFs como 0
    num_orfs = 0

    # Buscamos si hay alguna clase con la descripción dada
    classdes_class = des_class(file_input, classdes)

    # En caso de encontrarla, actualizamos el valor de 'num_orfs'
    if classdes_class != '[0,0,0,0]':
        classes = classes_num(file_input)
        num_orfs = classes[classdes_class]

    return num_orfs


# Función con la que extraemos cuántos y cuáles ORFs tienen el patrón 'protein'
# o el 'hydro'
def des_orf(file_input):
    """
    Dado un fichero con la estructura de 'tb_functions.pl', devuelve un
    diccionario con cuántos ORFs pertenecen al patrón 'protein', cuántos
    al 'hydro' y cuáles son esos ORFs para ambos casos.

    :param file_input: normalmente 'tb_functions.pl'
    :return: totaldict{'proteinlen', 'hydrolen', 'protein', 'hydro'}
    """
    # Inicializamos un diccionario para cada patrón
    orfprot = list()
    orfhydr = list()

    # Abrimos el fichero y tomamos las líneas
    with open(file_input) as f:
        data = f.readlines()

        # Recorremos cada línea, buscando los patrones que tengan
        # las descripciones indicadas
        for line in data:
            lineinf = line.split('(')
            # Nos quedamos con las líneas de 'function'
            if lineinf[0] == 'function':
                # Tomamos la descripción
                des = lineinf[1].split('"')[1]

                # Guardamos los ORF con 'protein'
                if len(re.findall(r"protein", des)) > 0:
                    orf = lineinf[1].split(',')[0]
                    orfprot.append(orf)

                # Guardamos los ORF con 'hydro' en un palabra con len()=13
                hydrolist = re.findall(r"\w*hydro\w*|$", des)
                for w in hydrolist:
                    if len(w) == 13:
                        orf = lineinf[1].split(',')[0]
                        orfhydr.append(orf)
                # Quitamos los posible duplicados
                orfhydr = list(dict.fromkeys(orfhydr))

    # Recogemos toda la información en un único diccionario
    totaldict = {'proteinlen': len(orfprot), 'hydrolen': len(orfhydr)}
    totaldict.update({'protein': orfprot, 'hydro': orfhydr})
    return totaldict


# Función que extrae cuántas y cuáles clases contienen como mínimo
# un ORF con un patrón indicado (entraran como lista los ORFs con el patrón)
def class_des_orf(file_input, orf_list):
    """
    Dada una lista de ORFs, devuelve un diccionario con, por un lado, la lista
    de clases que tienen al menos uno de esos ORFs y, por otro, la longitud de
    dicha lista.

    :param file_input: normalmente 'tb_functions.pl'
    :param orf_list: lista de ORFs
    :return: orf_classes: diccionario con la lista de clases ('cllist') y el
                          número de ellas ('clnum') que tienen al menos uno
                          de los ORF de orf_list
    """
    # Definimos la función con la que comprobar la intersección de listas
    def intersection(lst1, lst2):
        return len(list(set(lst1) & set(lst2)))

    # Inicializamos el diccionario final
    orf_classes = dict()
    orf_classes['cllist'] = list()
    orf_classes['clnum'] = 0

    # Tomamos el total de las clases con los ORFs que pertenencen a cada una
    total_classes = classes_list(file_input)

    # Recorremos las clases comprobando cuales contienen alguno de los ORFs
    # indicados
    for cl in total_classes.keys():
        if intersection(total_classes[cl], orf_list) > 0:
            orf_classes['cllist'].append(cl)
            orf_classes['clnum'] += 1

    return orf_classes


# Definimos un par de funciones con las que extraemos las relaciones entre ORFs
# de forma 'multiprocess'.
# Elegimos esta forma de obtener la información, en vez de la secuencial,ya que
# no necesitamos haber acabado de leer un fichero para empezar con otro.
# Descartamos la opción 'multithreaded' porque vamos a realizar cálculos que
# utilizarán cómputo de la CPU.

# Función para extraer las relaciones entre ORFs de un archivo concreto
def orf_relations_read(archive):
    """
    Dado un archivo del tipo 'tb_data_nn', extrae las relaciones entre los
    distintos ORFs introduciéndolas en el diccionario 'orf_rel'

    :param archive: archivo con información de las relaciones entre ORFs
    :return: diccionario 'orf_rel' con las relaciones entre ORFs
    """
    # Inicializamos el diccionario y la lista de los ORF relacionados
    orf_rel = dict()
    orf_list = list()

    # Almacenamos la lista de los ORF relacionados que encontramos en 'archive'
    with open(archive) as f:
        data = f.readlines()
        # Recorremos las líneas buscando cada ORF y sus relaciones
        # Comenzamos listando los ORF que aparecen en sentencias
        # 'tb_to_tb'. Estos son los relacionados con el ORF que
        # aparezca en la sentencia 'end(model())'
        for line in data:
            lineinfo = line.split('(')
            if lineinfo[0] == 'tb_to_tb_evalue':
                orf = lineinfo[1].split(',')[0]
                orf_list.append(orf)
            if lineinfo[0] == 'end':
                orf = lineinfo[2].split(')')[0]
                orf_rel[orf] = orf_list
                # Reiniciamos la lista para el siguiente ORF
                orf_list = list()

    return orf_rel


# Función para extraer las relaciones entre ORFs de los distintos archivos.
# Esta función llama a la anterior tantas veces como archivos haya
def orf_relations(archives_q, results_q):
    """
    Dados unos queues de archivos y resultados, vamos almacenando en este
    último, las relaciones entre ORFs que encontramos en los archivos.

    :param archives_q: cola de archivos
    :param results_q: cola de resultados
    :return: None
    """

    # Obtenemos el primer archivo
    archive = archives_q.get()
    # Mientras haya archivos pendientes, los leemos
    while archive:
        # Leemos el archivo
        orf = orf_relations_read(archive)
        # Guardamos el resultado en la cola de resultados
        results_q.put(orf)
        # Indicamos que hemos finalizado la tarea
        archives_q.task_done()
        # Obtenemos el siguiente archivo
        archive = archives_q.get()

    # Indicamos que hemos finalizado con el último archivo
    archives_q.task_done()


# Función para aplicar la anterior utilizando varios procesos
def multi_p_orfrelations(dir_name, num_processes):
    """
    Dado un directorio y un número de procesos, aplica la función orf_relations
    a los archivos del directorio, procesándolos con el número de procesos
    indicados.

    :param dir_name: directorio de los archivos. Normalmente, 'data/orfs'.
    :param num_processes: número de procesos
    :return: orf_r: diccionario con los ORF y las listas de los relacionados
    con ellos
    """
    # importamos los objetos que necesitamos de multiprocesos
    from multiprocessing import Process, JoinableQueue, Queue

    # Creamos la cola de resultados
    results_q = Queue()
    # Creamos la cola de tareas que realizar (los archivos que tenemos)
    archives_q = JoinableQueue()
    # Añadimos los archivos a la cola de tareas
    for archive in os.listdir(dir_name):
        full_ar = os.path.join(dir_name, archive)
        archives_q.put(full_ar)

    # Añadimos un indicador de final de tarea al final de la lista
    # de tareas para cada proceso
    for _ in range(num_processes):
        archives_q.put(None)

    # Iniciamos los `num_processes` procesos con la tarea de obtener
    # las relaciones por ORF
    for i in range(num_processes):
        process = Process(target=orf_relations, args=(archives_q, results_q))
        process.start()

    # Esperamos a que se hayan completado todas las tareas
    archives_q.join()

    orf_r = {}
    while not results_q.empty():
        e = results_q.get()
        for k, v in e.items():
            orf_r[k] = v

    return orf_r


# Función para el promedio de ORFs relacionados con un patrón dado
def mean_rel(orf_rel_dict):
    """
    Dado un diccionario con los ORFs de un patrón y sus relacionados,
    devuelve el promedio de relaciones.

    :param orf_rel_dict: diccionario con los ORF que siguen un patrón
    :return:
    """
    # Iniciamos a cero el total de relaciones
    total_rels = 0

    for lst in orf_rel_dict.values():
        total_rels += len(lst)

    return total_rels / len(orf_rel_dict)


# Función con la que calculamos el número de clases que tienen al menos
# una dimensión mayor que cero y múltiplo de un entero m
def m_funct(classes, m):
    """
    Dada una lista de clases 'classes', devuelve el número de ellas que
    tienen al menos una dimensión mayor que cero y múltiplo de m.

    :param classes: lista de clases
    :param m: entero
    :return: número de clases que cumplen la condición
    """
    # Ponemos como lista las dimensiones de cada una de las clases
    cl_list_lst = list(
        map(lambda x: x.split('[')[1].split(']')[0].split(','), classes))

    # Inicializamos la lista en la que vamos a ir guardando las clases
    # que cumplen la condición. Cada clase aparecerá, al principio, tantas
    # veces como dimensiones cumplan la condición.
    m_list = list()
    for i in range(0, 4):
        m_list += list(
            filter(lambda x: int(x[i]) > 0 | int(x[i]) % m == 0, cl_list_lst))

    # Volvemos a dejar las clases como strings entre corchetes
    cl_list_str = list(
        map(lambda x: '[' + x[0] + ',' + x[1] + ',' + x[2] + ',' + x[3] + ']',
            m_list))

    # Eliminamos duplicados de clases
    cl_list_str = list(dict.fromkeys(cl_list_str))

    # Devolvemos la longitud de la lista de clases que cumplen la condición
    return len(cl_list_str)


#  Función que devuelve cuantas clases cumplen la condicion de la función
#  'm_funct' para cada entero entre 2 y 'num_m'
def m_dict(classes, num_m):
    """
    Dada una lista de clases y un número 'num_m', devuelve cuantas clases
    cumplen la condicion de la función 'm_funct' para cada entero entre
    2 y 'num_m'

    :param classes: lista de clases
    :param num_m: número hasta el que comprobamos si la clase cumple 'm_funct'
    :return: m: diccionario con eñ número de clases que cumplen las
             condiciones de 'm_funct' para cada valor entre 2 y 'num_m'
    """
    m = dict()
    for i in range(2, num_m+1):
        m[i] = m_funct(classes, i)
    return m
