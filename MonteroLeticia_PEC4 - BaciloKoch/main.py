# -----------------------------------------------------------------------------
# ------------------------------ Código principal -----------------------------
# -----------------------------------------------------------------------------

# Importamos la librerías que vamos a utilizar. Entre ellas, nuestro utilities
import utilities as utl
import visual

# Definimos las rutas de los ficheros
func_file = './data/tb_functions.pl'
orfs_dir = './data/orfs/'


print('--- Ejecutando el proyecto BaciloKoch ---')
print('NOTA: Las gráficas del proyecto se guardan en la librería principal '
      'con extensión .png\n')

# ¿Cuántos ORFs pertenecen a cada clase?
cl_nm = utl.classes_num(func_file)
print('El número de ORFs que pertenecen a cada clase se puede visualizar en'
      ' bar_classes.png')
# Generamos el gráfico correspondiente
visual.bar_classes(cl_nm)

# ¿Cuántos de ellos pertenecen a la clase con 'Respiration' como descripción?
des = 'Respiration '
respiration = utl.orf_des_class(func_file, des)
print('El número de ORFs que pertenecen a la clase con '
      'la descripción {} es: {}'.format(des, respiration))

# ¿Cuántas clases tienen como mínimo un ORF con el patrón de 'protein'?
protein_orfs = utl.des_orf(func_file)['protein']
protein = utl.class_des_orf(func_file, protein_orfs)['clnum']
print('El número de clases con al menos un ORF con el patrón "protein" '
      'es: {}'.format(protein))

# ¿Y con el patrón 'hydro?
hydro_orfs = utl.des_orf(func_file)['hydro']
hydro = utl.class_des_orf(func_file, hydro_orfs)['clnum']
print('El número de clases con al menos un ORF con el patrón "hydro" '
      'es: {}'.format(hydro))

# Generemos un gráfico con la proporción de estas clases frente al total
visual.pie_classes(len(cl_nm), protein, hydro)

# ¿Cuál es el promedio de ORFs relacionados con alguno de los del patrón de 'protein'?
# ¿Y con 'hydro'?
# Primero obtenemos el diccionario con todas las relaciones
# Nota: la funcion 'multi_p_orfrelations' requiere indicar con cuantos procesos
# queremos ejecutar, en este caso indicamos 2.
relations = utl.multi_p_orfrelations(orfs_dir, 2)

# Ahora obtenemos los promedios
# Para 'protein'
protein_rel = {orf: orfs for orf, orfs in relations.items() if orf in protein_orfs}
protein_rel_mean = utl.mean_rel(protein_rel)
print('El promedio de ORFs relacionados con alguno con el patrón "protein" '
      'es: {}'.format(protein_rel_mean))
# Para 'hydro'
hydro_rel = {orf: orfs for orf, orfs in relations.items() if orf in hydro_orfs}
hydro_rel_mean = utl.mean_rel(hydro_rel)
print('El promedio de ORFs relacionados con alguno con el patrón "hydro" '
      'es: {}'.format(hydro_rel_mean))

# Generamos gráficamente los resultados
visual.bar_patron(protein_rel, protein_rel_mean, 'protein')
visual.bar_patron(hydro_rel, hydro_rel_mean, 'hydro')

# ¿Cuántas clases tienen como mínimo una dimensión mayor estricta (>) que 0
# y a la vez múltiplo de M, siendo M un entero entre 2 y 9?
m_classes = utl.m_dict(list(utl.classes_num(func_file).keys()), 9)

print('Para cada valor de M entre 2 y 9, el número de clases que '
      'tienen al menos una dimensión múltiplo de M es:\n')
for m, c in m_classes.items():
    print('M = {} lo cumplen {} clases'.format(m, c))

# Generamos un gráfico con el que ver los resultados
visual.bar_dimensions(m_classes)

print('\n--- Fin de la ejecución del proyecto BaciloKoch ---')
