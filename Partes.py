# -*- coding: latin-1 -*-

'''
Para navegar sujetos y partes
y las causas asociadas a ellos
'''

import Tabla

from Casos import *
from Tabla import *
from Nomen import CargaTabla
from utiles import debug
PATH_LEX='c:/lex6'    

class Partes(TablaHija):
    "Partes"
    _indices=['Codi','Suje','Punt']
    def __init__(self,path=''):
        Tabla.__init__(self,'PARTES',path)
    
    def get_caracter(self):
        'devuelve el caracter del justiciable'
        if not hasattr(self,"caracter"):
            self.caracter=CargaTabla(self.Path,'A')
        try:
            return self.caracter[self.get('punt')]
        except KeyError:
            return ''
    
   
class Sujetos(Tabla):
    'Sujetos'
    _indices=['Sujetos','Apynom']
    def __init__(self,path=''):
        Tabla.__init__(self,'SUJETOS',path)
        self.TablaParte=Partes(path)
        self.TablaParte.order_by('Suje')

    def parte(self):
        'devuelve el objeto parte, del cual se puede sacar el expte.'
        suje=self.get('Suje')
        self.TablaParte.tabla.SetScope(suje)
        if self.TablaParte['suje']==self.get('suje'):
            return self.TablaParte
        else:
            debug('no fue posible encontrar el sujeto %s' % suje)
            return []
        


if __name__=='__main__':
    def prueba1():
        tabla=Partes(PATH_LEX)
        tabla.order_by('Suje')
        for p in tabla:
            print '%(exp0)s %(caracter)s' % tabla
            if tabla.leidos > 10:
                break
            
    def prueba2():
        tabla=Sujetos(PATH_LEX)
        tabla.order_by('Apynom')
        tabla.tabla.GoTop()
        tabla.tabla.Seek('CAMP')
        for p in tabla:
            if tabla['docu']=='34.431.283':
                print '-------------------------'
            print '>%(apel)s %(nomb)s %(docu)s' % tabla    
                #~ obj=tabla.parte()
                #~ for n in obj:
                    #~ try:
                        #~ print '%(exp0)s %(exp1)s %(caracter)s' % obj
                    #~ except TypeError:
                        #~ print obj.caso
            if tabla.leidos > 500:
                break
        print tabla.campos()
    prueba2()