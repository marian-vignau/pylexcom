# -*- coding: latin-1 -*-
''' este es memos que no accede a registro
para evitar referencias circulares
inheritan de esta clase
la clase de Memos_Reg
y la clase Registro'''

from Casos import *
    
class Memos(TablaHija):
    "Memos"
    _indices=['CodiFech','Fech','Tipo','Fipo','Regi']
    tipos={}
    def __init__(self,path=''):
        Tabla.__init__(self,'MEMOS',path)
    
    def get_firstline(self):
        '''devuelve la primer linea del texto asoc.
        si la 1ra no tiene mucha info, devuelve las 2 primeras
        '''
        s=self.get_text('TXT')
        ret=''
        if s:
            for l in s.split('\r'):
                if l.strip()>'':
                    ret+=l
                    if len(ret.strip()) >= 20:
                        return ret
                        break
        return '---'

def veo_textos():
    mem=Memos('C:/backup/f1/fisc1/LEX6')
    mem.order_by('CodiFech',True)
    for c in mem:
        print '%(codi)s %(fech)s %(regi)s %(exp1)s %(cara)s %(*desc)s' % mem
        if mem.leidos >15:break
                

def invest_ord():
    mem=Memos('C:/backup/f1/fisc1/LEX6')
    mem.tabla.SetOrder(1)
    def leer(mem):
        mem.tabla.GoTop()
        for c in mem:
            print '%(*fech)s %(regi)s %(exp1)s %(cara)s %(desc)s "%(firstline)s"' % mem
            if mem.leidos >15:break

                
    for ord in range(7):
        print '--orden:',ord, mem.tabla.SetOrder(ord)
        leer(mem)

if __name__=='__main__':
    invest_ord()
