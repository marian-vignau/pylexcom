# -*- coding: latin-1 -*-

'''
para acceder al lex 6
'''
import win32com.client
import os
from utiles import debug, ver_err, f_format
import dbfpy.dbf #para poder mostrar la lista de nombre de campos

class Tabla(object):
    def __init__(self,nom="",path='',version=6):
        self.tabla=win32com.client.Dispatch('LexUtil.LexOLETable')
        #~ self.tabla=win32com.client.Dispatch('lexcom.table')
        os.chdir(path) #para ver si funka como SET DEFA
        self.path=path #para tenerlo al path en alguna parte
        self.nombre, self.version=nom.upper(), version
        self.n_order, self.leidos = 0, 0
        if nom:
            self.open(nom,path)
            self.tabla.GoTop()
            self.auto_init()
    
    def __del__(self):
        self.tabla.Close()
        debug('cerre la tabla %s' % self.nombre,self.__doc__)
            
    def open(self,nom,path):
        'para abrir la tabla'
        self.Path=path
        #abro la tabla para sólo lectura
        if (self.version == 6 and self.tabla.Open(nom+'.DBF',True,False)) or \
                (self.version == 8 and self.tabla.Open(self.path, nom+'.DBF',True,False)):
            debug ('abri %s' % nom,nom)
            #~ debug('\n'.join(dir(self.tabla)))
        else:
            ver_err('no se pudo abrir %s' % nom)
            raise IOError, 'la tabla %s no pudo ser abierta' % nom
    
    def auto_init(self):
        '''aca simplemente reviso que funciones 
        get tengo para no hacer hasattr (supuestam es mas rapido)'''
        func=[(n[4:],getattr(self,n)) for n in dir(self) 
            if n.startswith('get_')]
        self.func=dict(func)
        
    def order_by(self,order,flip=False):
        'ordena segun el indice solicitado'
        if hasattr(self,'_indices') and order in self._indices:
            n_order=self._indices.index(order)+1
            
            self.tabla.SetOrder(n_order)
            # no existe la funcion FlipOrder en LexCom 6.1
            #~ if flip: 
                #~ self.tabla.FlipOrder()
            return self.tabla.GoTop()
        else:
            raise KeyError, 'no existe el orden %s entre los disponibles' % order

    
    def __iter__(self):
        self.leidos=0
        return self
    
    def next(self):
        if self.leidos > 0:
            self.tabla.Skip(1)
        self.leidos += 1
        if self.tabla.Eof():
            raise StopIteration
                
    def campos(self):
        '''devuelve una lista con nombres de campos
        esta funcion utiliza el modulo dbfpy
        '''
        try:
            return self.lista
        except:
            dbf1 = dbfpy.dbf.Dbf()
            if self.version>=8:
                nom='GESTION/%s.DBF'% self.nombre
            else:
                nom='%s.DBF'% self.nombre
            dbf1.openFile(nom, readOnly=1)
            #~ dbf1.reportOn()
            self.lista = dbf1.fieldNames()
            dbf1.close()
            return self.lista
        
    def __getitem__(self,campo): 
        'aca se implementa la magia del retorno de valor como dict'
        return self.get(campo)
    def get(self,campo):
        format=''
        #para facilitar un formateo rapido de los campos
        if campo.startswith('*'):
            
            format='*'
            campo=campo[1:]
        if self.func.has_key(campo):
            value = self.func[campo]()
            return f_format(value,format)
        else:
            value=self.tabla.GetField(campo.upper())
            value=value.encode('latin-1','replace').strip()
            return f_format(value,format)

    def get_text(self, format='TXT'):
        value=self.tabla.GetText(format)
        value=value.encode('latin-1','replace').strip()
        return value

if __name__=='__main__':
    #~ path='C:/backup/f1/fisc1/LEX6'
    path='c:/lexampar'
    t=Tabla('casos',path,8)
    for x in t:
        print '%(cara)s %(exp1)s' % t
        if t.leidos > 10:
            break
        