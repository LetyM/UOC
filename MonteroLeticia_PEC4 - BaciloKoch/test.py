# -----------------------------------------------------------------------------
# ------------------------------------ Test -----------------------------------
# -----------------------------------------------------------------------------

import unittest
import utilities as utl


# Creamos una única clase para los test del proyecto
class TestBaciloKoch(unittest.TestCase):

    # Inicializamos algunas variables que vamos a usar en general
    def setUp(self):
        self.f = './testdocs/testclassesnum.pl'
        self.dir = './testdocs/orfs/'

    # Creamos un test para cada una de las funciones de utilities.py
    def test_classes_num(self):
        cn = {'[1,0,0,0]': 3, '[1,1,0,0]': 0, '[1,1,1,0]': 1, '[1,1,2,0]': 4}
        self.assertEqual(utl.classes_num(self.f), cn)

    def test_classes_list(self):
        cl = {'[1,0,0,0]': ['tb1852', 'tb2913', 'tb3551'],
              '[1,1,0,0]': [], '[1,1,1,0]': ['tb186'],
              '[1,1,2,0]': ['tb1905', 'tb2531', 'tb2780', 'tb1538']}
        self.assertEqual(utl.classes_list(self.f), cl)

    def test_des_class(self):
        des = "Small-molecule metabolism "
        c = '[1,0,0,0]'
        self.assertEqual(utl.des_class(self.f, des), c)

    def test_orf_des_class(self):
        des = "Small-molecule metabolism "
        self.assertEqual(utl.orf_des_class(self.f, des), 3)

    def test_des_orf(self):
        d = {'proteinlen': 1, 'hydrolen': 2}
        d.update({'protein': ['tb1852'], 'hydro': ['tb2780', 'tb1538']})
        self.assertEqual(utl.des_orf(self.f), d)

    def test_class_des_orf(self):
        lst = ['tb2780', 'tb1538']
        d = {'cllist': ['[1,1,2,0]'], 'clnum': 1}
        self.assertEqual(utl.class_des_orf(self.f, lst), d)

    def test_multi_p_orfrelations(self):
        d = {'tb4': ['tb3671', 'tb405', 'tb3225']}
        d.update({'tb5': ['tb3672', 'tb406', 'tb3227', 'tb3228']})
        self.assertEqual(utl.multi_p_orfrelations(self.dir, 2), d)

    def test_mean_rel(self):
        d = {'tb4': ['tb3671', 'tb405', 'tb3225']}
        d.update({'tb5': ['tb3672', 'tb406', 'tb3227', 'tb3228']})
        self.assertEqual(utl.mean_rel(d), 3.5)

    def test_m_funct(self):
        c = ['[2,3,4,5]', '[6,7,8,9]', '[4,4,4,18]']
        self.assertEqual(utl.m_funct(c, 2), 3)
        self.assertEqual(utl.m_funct(c, 3), 3)
        self.assertEqual(utl.m_funct(c, 4), 3)
        self.assertEqual(utl.m_funct(c, 5), 1)
        self.assertEqual(utl.m_funct(c, 6), 2)
        self.assertEqual(utl.m_funct(c, 7), 1)
        self.assertEqual(utl.m_funct(c, 8), 1)
        self.assertEqual(utl.m_funct(c, 9), 2)

    def test_m_dict(self):
        c = ['[2,3,4,5]', '[6,7,8,9]', '[4,4,4,18]']
        d = {2: 3, 3: 3, 4: 3, 5: 1, 6: 2, 7: 1, 8: 1, 9: 2}
        self.assertEqual(utl.m_dict(c, 9), d)


# Decomentar la siguiente línea si se quieren probar los test desde Pycharm
# Desde la consola no es necesario descomentarla
# unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False)
