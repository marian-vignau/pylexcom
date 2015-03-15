#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''Casos de test de la biblioteca y API básica de Lex-Doctor
En esto todavía no ingresa lo que yo programo, solo verifico
la correcta instalación de todos los componentes
'''
import unittest, os.path
modo={'r':[True,False], 'w':[False,False],'w+':[False,True]}

def msg(*value):
    def proc(value):
        if isinstance(value, (str,unicode)):
            if isinstance(value,str):
                value=unicode(value,'latin-1',errors='replace')
            return value.encode('ascii','replace')
        else:
            return repr(value)
    print ','.join([proc(x) for x in value])
    
    

class TestInstalacion(unittest.TestCase):
    
    def setUp(self):
        'me fijo si tengo todo en su lugar e instalado'
        msg( '...')
        import win32com.client
        self.path='c:/Desa/Lex6'
        self.version=6
        self.assert_(os.path.exists(self.path))
        os.chdir(self.path) 
        try:
            self.tabla=win32com.client.Dispatch('LexUtil.LexOLETable')
        except:
            self.fail('No anda el Dispatch')
    
    def _open(self,nom,modo_):
        flags=modo[modo_]
        if self.version == 6:
            return self.tabla.Open('%s/%s.DBF' % (self.path,nom),flags[0],flags[1]) 
        elif self.version == 8:
            return self.tabla.Open(self.path, nom+'.DBF',flags[0],flags[1]) 
        else:
            return 0

    def testApertura(self):
        'para ver si puedo abrir una tabla'
        if self._open('CASOS','r'):
            self.tabla.Close()
        else:
            self.fail('No puedo abrir')
    
    def _testEscritura(self):
        '''Agrega un nuevo CASO
        esto no funciona, no se pueden agregar casos validos 
        xq no gen. ID nuevo'''
        self._open('CASOS','w')
        self.assert_(self.tabla.Append(),
            'No puedo agregar registro')
        self.tabla.Commit()

        self.assert_(self.tabla.SetField('CARA','caratula de ejemplo'),
            'No puedo modificar caratula')
        self.assert_(self.tabla.SetField('EXP1','101/01'),
            'No puedo modificar numero de exp')
        msg(self.tabla.RandomID()) #esto no anda
        self.tabla.Commit()
        self.tabla.Close()
        
    def testLeoCasos(self):
        'pruebo la lectura del primer caso'
        self._open('CASOS','r')
        self.tabla.GoTop()
        CODI=self.tabla.GetField('CODI')
        CARA=self.tabla.GetField('CARA')
        self.tabla.Close()
        self.assertEqual(CODI,'97127158')
        self.assertEqual(CARA.strip(),'CASCO, SERGIO DAVID')
        msg('PROCID',self.tabla.ProcID())
    
    def testOrdenCasos(self):
        'pruebo el orden correcto'
        self._open('CASOS','r')
        self.tabla.GoTop()
        self.tabla.SetOrder(1)
        c=-1
        for n in range(10):
            c1= self.tabla.GetField('CODI')
            self.failIf(int(c)>int(c1),'no sigue el orden esperado')
            c=c1
            self.tabla.Skip(1)
        self.tabla.Close()
        
    def testOrdenMemos(self):
        'pruebo el orden correcto'
        self._open('MEMOS','r')
        self.tabla.GoTop()
        self.tabla.SetOrder(1)
        c,n,vistos=-1,0,[]
        
        while n<10:
            c1= self.tabla.GetField('CODI')
            if c!=c1:
                self.failIf((c1 in vistos),'ya estaba vista la clave')
                vistos.append(c1)
                c=c1
                n+=1
#            msg(c1,self.tabla.RecNo(),self.tabla.GetField('DESC'))
            self.tabla.Skip(1)
        self.tabla.Close()

    
    def testLeoMemo(self):
        CODI='97127158'
        self._open('MEMOS','r')
        self.tabla.GoTop()
        self.tabla.SetOrder(1)
#        self.tabla.Seek(CODI)
        self.tabla.SetScope(CODI)
#        self.tabla.Skip(1)
        C = self.tabla.GetField('CODI')
        P=self.tabla.ProcID()
        msg(CODI,C,P)
#        self.assertEqual(CODI,P.strip(),
#            'No encontro memo asociado correctamente %s %s' % (CODI,P))
        n=0
#        self.tabla.SetScope(CODI)
        while not self.tabla.Eof() and n<5:
            CODI0 = self.tabla.GetField('CODI')
#            self.assertEqual(CODI,CODI0,
#                'Scope no funciono bien')
            msg(CODI0,self.tabla.RecNo())
            self.tabla.Skip(1)
            n+=1
        msg('registros',n)
        self.tabla.Close()
        

if __name__=='__main__':
    unittest.main()
    