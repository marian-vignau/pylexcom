
import Tabla, sqlite3
class Tabla_SQLite(object):
    def __init__(self,nombre,path=''):
        self.tabla= Tabla.Tabla(nombre,path)

    def crear(self):
        'SQL de creacion de tabla identica'
        armado= ['"%s" CHAR' % campo for campo in self.tabla.campos()]
        SQL = 'CREATE TABLE "%s" (' % self.tabla.nombre 
        SQL += ', '.join(armado) 
        return SQL #retorna SIN parentesis de cierre
    
    def copiar(self):
        '''uso los metodos de acceso de la API de lex
        a traves de la clase tablas'''
        # INSERT INTO tableName [(column-list)] VALUES(value-list)
        
        SQL=['INSERT INTO %s' % self.tabla.nombre]
        SQL.append('(%s)' % 
            ', '.join(['"%s"'% x for x in self.tabla.campos()]))
        SQL.append('VALUES (%s)'  % 
            ', '.join(["'%%(%s)s'"% x for x in self.tabla.campos()]))
        
        sql= ' '.join(SQL)
        print sql
        for t in self.tabla:
            #~ valores=['"%s"' % self.tabla[c] for c in self.tabla.campos()]
                
            salida=sql % self.tabla
            yield salida
                
def copio_tutto(tablas):
    path='C:/backup/Hoy/mesa/LEX6'
    nombre='C:/Mis documentos/Marian/MesaPenal/bd.sqlite'
    db=sqlite3.connect(
        nombre,isolation_level=None)
    
        
    for nom in tablas:
        try:
            db.cursor().execute('DROP TABLE %s' % nom)
        except:
            pass
        t=Tabla_SQLite(nom,path)
        db.cursor().execute(t.crear()+')')

    for nom in tablas:
        n=0
        for x in t.copiar():
            db.cursor().execute(x)
            n+=1
            if n%100==0:
                print '.',
                if n%3000==0:
                    print '\n'
            #~ if n>30:
                #~ break
    db.close()

copio_tutto('sujetos partes casos'.split())
