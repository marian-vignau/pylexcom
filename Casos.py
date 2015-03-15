# -*- coding: latin-1 -*-
from Tabla import *
from Nomen import CargaTabla
from utiles import debug
import Depen

class Casos(Tabla):
    "Casos"
    def __init__(self,path=''):
        Tabla.__init__(self,'casos',path)
        self.Depen=Depen.Depen(path)
        self.Depen.order_by('ID')
        self.tipos_proc=CargaTabla(self.Path,'H')

    def get_tipoproc(self):
        'devuelve el tipo de proceso'
        try:
            return self.tipos_proc[self.get('punt')]
        except KeyError:
            return ''

    def get_fiscalia(self):
        'devuelve la fiscalia en la que esta el expte'
        punt=self.get('FISC')
        self.Depen.tabla.Seek('%08d'% int(punt))
        if self.Depen['DEPE']==punt:
            return self.Depen['DESC']
        else:
            return 'error al buscar la fiscalia, no encontrada'
            
    def go_procid(self,ProcID):
        "si retorna True: encontró el valor"
        if self.n_order!=1: 
            self.tabla.SetOrder(1)
        return self.tabla.Seek(ProcID)
    
    def get_nexp(self):
        'retorna el numero de expediente'
        value=self.get('exp0')
        value=value.replace('O','0') 
        if value.find('/') < 0 or \
            not value.split('/')[0].isdigit() or \
            int(value.split('/')[0])<=0:
            return 0
        else:
            return int(value.split('/')[0])

class TablaHija(Tabla):
    def caso(self):
        if not hasattr(self,"cas"):
            self.cas=Casos(self.Path)
        #~ id=self.get('procid')
        id=self.get('codi')
        if self.cas.go_procid(id):
            return self.cas
        else:
            #raise IOError, 'No fué posible encontrar el caso asociado'
            debug('No fue posible encontrar el caso asociado',self.__doc__)
            return None

    def get_cara(self):
        return self.caso()['cara']
    
    def get_tipoproc(self):
        return self.caso()['tipoproc']

    def get_exp1(self):
        return self.caso()['exp1']
    
    def get_codigo(self):
        return self.caso()['codi']

    def get_exp0(self):
        return self.caso()['exp0']

    def get_fiscalia(self):
        return self.caso()['fiscalia']

def test_param():
    par=Tabla('param')
    par.set_scope('H')
    par.set_order(0)
    n=0
    for p in par:
        print n,par['punt'],par['tipo'],par['desc'],par['orde']
        n+=1
        if n>300: break

def test_cas1():
    cas=Casos()
    n=0
    pru={}
    for c in cas:        
        pru[cas['procid']]= cas['cara']
        n+=1
        if n>10: break
    print '------',len(pru)
    ok=0
    for k,v in pru.iteritems():
        cas.go_procid(k)
        if cas['cara']==v:
            ok+=1
            print cas['codi'],k
        else:
            print 'error: %s != %s' % (cas['cara'],v)
    print 'pasamos bien %d de %d' % (ok, len(pru))
    
if __name__=='__main__':
    cas=Casos('C:/LEX6')
    cas.tabla.SetOrder(1)
    def leer(cas):
        cas.tabla.GoTop()
        n=0
        for c in cas:
            print '\n%(exp0)s %(cara)s %(fiscalia)s' % cas
            #~ print '%(votacion)s' % cas
            n+=1
            if n>10:break
    
    #~ for ord in range(7):
        #~ print '--orden:',ord, cas.tabla.SetOrder(ord)
    leer(cas)
    
