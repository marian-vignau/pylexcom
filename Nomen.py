# -*- coding: latin-1 -*-

'''
para cargar nomencladores
los carga de una vez en memoria

'''

import Tabla

def MiembrosJuzgado(path):
    return CargaTabla(path,'K')


def CargaTabla(path, codigo):
	'Para cargar un tabla de parámetros'
	par=Tabla.Tabla('param',path)
	par.tabla.SetOrder(2)	
	par.tabla.Seek(codigo)
	dict={}
	for p in par:
		if par['TIPO']==codigo:
			dict[par['PUNT']]=par['DESC']
		else:
			break
	return dict