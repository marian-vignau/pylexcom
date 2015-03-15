# -*- coding: latin-1 -*-

DEBUG=False
ERROR=True

def debug(mensaje,tabla=''):
    if DEBUG:
        print mensaje
        
        
def ver_err(mensaje,tabla=''):
    if DEBUG or ERROR:
        print mensaje

def f_format(value,format):
    '''intenta sacar formateado el contenido del campo, 
    si parece ser fecha'''
    if format=='*':
        value=value.strip()
        if len(value)==8:
            return '%s/%s/%s' % (value[6:8],value[4:6],value[0:4])
        else:
            val=unicode(value,'latin-1',errors='replace')
            return val.encode('ascii','replace')
    else:
        return value
        

