# -----------------------------------------------------------------------------
# ----------- Código con visualizaciones que nos serán de utilidad. -----------
# -----------------------------------------------------------------------------

# Importamos las librerías que necesitaran nuestras funciones
import matplotlib.pyplot as plt
import operator


# Función con la que visualizamos el número de ORFs por clase.
# Elegimos un gráfico de barras que nos permite mostrar todas
# las clases y comparar las que tienen más o menos ORFs.
# Además, lo mostramos en horizontal y ordenado de mayor a menor.
def bar_classes(cl_nm):
    """
    Dado un diccionario con las clasese y el número de ORF por clase,
    guarda en 'bar_classes.png' el gráfico de barras correspondiente
    ordenando horizontalmente los valores de mayor a menor.

    :param cl_nm: diccionario con las clases y el número de ORFs
    :return: None
    """
    # Reseteamos los valores por defecto
    plt.rcdefaults()

    # Establecemos la figura del gráfico
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot()

    # Establecemos los valores de x y de y, ordenando primero el diccionario
    cl_nm_sorted = sorted(cl_nm.items(), key=operator.itemgetter(1), reverse=True)
    # No mostramos los registros que valen 0 para simplificar el gráfico
    c = [i[0] for i in cl_nm_sorted if i[1] > 0]
    o = [i[1] for i in cl_nm_sorted if i[1] > 0]

    # Gráfico de barras
    ax.barh(range(len(c)), o, align='center')

    # Establecemos los títulos y otras opciones
    ax.set_yticks(range(len(c)))
    ax.set_yticklabels(c)
    ax.invert_yaxis()
    # Incluimos el valor de cada barra
    for i, v in enumerate(o):
        ax.text(v + 3, i + .25, str(v), fontweight='bold')
    ax.set_xlabel("Número de ORFs")
    ax.set_title("ORFs por clase")

    # Guardamos el gráfico
    fig.savefig("bar_classes.png")


# Función con la que mostramos la proporción de clases que contienen
# al menos un ORF con el patrón 'protein' o con el de 'hydro' respecto
# del total.
# Elegimos un gráfico de tarta para visualizar la proporción.
def pie_classes(total, protein, hydro):
    """
    Dado el total de clases, las que tienen al menos un ORF con el patrón
    'protein' o con el 'hydro', guarda en 'pie_classes.png' un gráfico
    de tarta con la proporción de cada uno.

    :param total: total de clases
    :param protein: clases con al menos un ORF con el patrón 'protein'
    :param hydro: clases con al menos un ORF con el patrón 'hydro'
    :return: None
    """
    # Reseteamos los valores por defecto
    plt.rcdefaults()

    # Establecemos la figura del gráfico
    fig = plt.figure()
    ax = fig.add_subplot()

    # Introducimos en una lista los valores y establecemos las etiquetas
    # Calculamos los porcentajes de 'protein', de 'hydro' y del 'resto'
    protein_p = protein / total
    hydro_p = hydro/total
    rest_p = (total - protein - hydro) / total
    sizes = [protein_p, hydro_p, rest_p]
    labels = 'Protein', 'Hydro', 'Resto'

    # Definimos una función que nos va a permitir mostrar los porcentajes
    def func(sz):
        return "{:.1f}%".format(sz)

    # Gráfico de tarta
    ax.pie(sizes, labels=labels, autopct=lambda sz: func(sz))

    # Establecemos los títulos y otras opciones
    ax.set_title("Proporción de clases con ORFs 'protein' e 'hydro'")

    # Guardamos el gráfico
    fig.savefig("pie_classes.png")


# Función con la que mostramos el promedio de relaciones que tienen los
# ORFs con un patrón determinado
# Utilizamos un gŕafico de barras junto con la línea del promedio para ver
# el número de relaciones de cada ORF comparado con la media (así podemos
# comprobar cuales superan o se quedan por debajo de la media)
def bar_patron(total_rel, mean_rel, patron):
    """
    Dado el total de ORFs con un patrón y sus relaciones, así como la media
    de relaciones, guarda en 'bar_patron_'patron'.png' un gráfico de barras
    con el número de relaciones por clase y una línea marcando la media.

    :param total_rel: diccionario con las clases y el total de relaciones
    :param mean_rel: media de las relaciones
    :param patron: tipo de patron que siguen los ORFs
    :return: None
    """
    # Reseteamos los valores por defecto
    plt.rcdefaults()

    # Establecemos la figura del gráfico
    fig = plt.figure(figsize=(40, 5))
    ax = fig.add_subplot()

    # Establecemos los valores de x y de y
    x = [k for k in total_rel.keys()]
    y = [len(v) for v in total_rel.values()]

    # Gráfico de barras
    ax.bar(x, y)
    ax.plot(x, [mean_rel] * len(x))

    # Establecemos los títulos y otras opciones
    fig.autofmt_xdate(rotation=90)
    ax.set_xlabel("ORF")
    ax.set_title("ORFs relacionados con los del patrón " + patron)

    # Guardamos el gráfico
    fig.savefig("bar_patron_" + patron + ".png")


# Función con la que mostramos el número de ORFs que tienen al menos una
# dimensión tal que es mayor estricta (>) que 0 y a la vez múltiple de un
# valor m siendo m un valor entre 2 y otro dado.
# Elegimos este gráfico para comparar los resultados para los distintos
# valores de m
def bar_dimensions(m_classes):
    """
    Dado un diccionario con los números del 2 a otro dado como claves y la
    cantidad de ORFs que tienen al menos una dimensión > 0 y a la vez múltiplo
    de la clave como valores, guarda en 'bar_dimensions.png' el gráfico de
    barras correspondiente

    :param m_classes: diccionario con los enteros del 2 a uno dado y la
            cantidad de ORFs que cumplen la condición
    :return: None
    """
    # Reseteamos los valores por defecto
    plt.rcdefaults()

    # Establecemos la figura del gráfico
    fig = plt.figure()
    ax = fig.add_subplot()

    # Establecemos los valores de x y de y, ordenando primero el diccionario
    x = [k for k in m_classes.keys()]
    y = [v for v in m_classes.values()]

    # Gráfico de barras
    ax.bar(x, y, align='center')

    rects = ax.patches

    for rect, label in zip(rects, y):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')

    # Establecemos los títulos y otras opciones
    ax.set_xlabel("M")
    ax.set_title("ORFs con al menos una dimensión múltiplo de M")

    # Guardamos el gráfico
    fig.savefig("bar_dimensions.png")
