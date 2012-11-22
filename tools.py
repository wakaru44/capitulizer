# script con herramientas para ayudar a experimentar mejor

from bs4 import BeautifulSoup

def salvar_foo(cadena):
    """guarda una cadena en un archivo llamado foo.html"""
    fh = open("./tests/fixtures/foo.html","w")
    fh.write(cadena)
    fh.close()
    return 0


def mostrar_lista(lista):
    """muestra en pantalla una lista con separaciones"""
    numero = 0
    for elemento in lista:
        print "\n--------------------------\n"
        print "\n numero : ", numero
        print elemento
        numero += 1

    print "\ntotal: ", numero 

def cargar_fixt(fixture):
    """carga un elemento de la carpeta de fixtures en forma de string"""
    archivo = "./tests/fixtures/" + fixture
    fhfixt = open(archivo, "r")
    content = fhfixt.read()
    fhfixt.close()
    return content



def print_list(l, colums = 2):
    """prints a list in column mode"""
    #c = 0  # counter
    #line = []
    #for a in l:
    #    if c < colums:
    #        c += 1
    #        line.append(a)
    #    else:
    #        c = 0
    #        print line
    #        line.pop()
    #        line.pop()
    while len(l) > 0:
        for i in range(colums):
            try:
                e = l.pop()
                print e
            except:
                pass
        


    return 0


