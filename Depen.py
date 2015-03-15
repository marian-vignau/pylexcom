# -*- coding: latin-1 -*-

'''
Para navegar sujetos y partes
y las causas asociadas a ellos
'''

from Tabla import *
from utiles import debug
PATH_LEX='c:/lex6'    

class Depen(Tabla):
    "Dependencias"
    _indices=['ID','Descripcion']
    def __init__(self,path=''):
        Tabla.__init__(self,'DEPEN',path)
    

if __name__=='__main__':
    def Prueba():
        tabla=Depen(PATH_LEX)
        tabla.order_by('ID')
        for p in tabla:
            print '%(DEPE)s %(DESC)s' % tabla
            if tabla.leidos > 10:
                break
            
    Prueba()