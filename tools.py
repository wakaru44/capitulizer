# script con herramientas para ayudar a experimentar mejor
# y para hacer algunas pruebas con los test.

from bs4 import BeautifulSoup

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    appengine_home = "/home/wakaru/workspace/google_appengine/"
    archivo = appengine_home + "capitulizer/test/fixtures/" + fixture
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
        


#    return 0

def sendEmail(
                html = "<html><body><h1>Exito</h1></body></html>",
                me = "wakaru44@gmail.com", 
                you = "trigger@ifttt.com" 
            ):
    # me == my email address
    # you == recipient's email address
     gmail_user = me
     gmail_pwd  = "tresvs5."


     # Create message container - the correct MIME type is multipart/alternative.
     msg = MIMEMultipart('alternative')
     msg['Subject'] = "Probando a enviar a traves de python scripts #NewChapter"
     msg['From'] = me
     msg['To'] = you

     # Create the body of the message (a plain-text and an HTML version).
     text = "Email, byPythonScript"
     #html = """\
     #<html>
     #  <head></head>
     #  <body>
     #    <p>Hi!<br>
     #       How are you?<br>
     #       Here is the <a href="http://www.python.org">link</a> you wanted.
     #    </p>
     #  </body>
     #</html>
     #"""

     # Record the MIME types of both parts - text/plain and text/html.
     part1 = MIMEText(text, 'plain')
     part2 = MIMEText(html, 'html')

     # Attach parts into message container.
     # According to RFC 2046, the last part of a multipart message, in this case
     # the HTML message, is best and preferred.
     msg.attach(part1)
     msg.attach(part2)


     # Send the message via gmail.
     mailServer = smtplib.SMTP("smtp.gmail.com", 587)
     mailServer.ehlo()
     mailServer.starttls()
     mailServer.ehlo()
     mailServer.login(gmail_user, gmail_pwd)
     mailServer.sendmail(gmail_user, you , msg.as_string())

     # Send the message via local SMTP server.
     #s = smtplib.SMTP('localhost')
     ## sendmail function takes 3 arguments: sender's address, recipient's address
     ## and message to send - here it is sent as one string.
     #s.sendmail(me, you, msg.as_string())
     #print msg.as_string()
     #s.quit()

def mandarPrueba():
    mensaje = cargar_fixt("blogger-oneEpisode.html")
    sendEmail(mensaje)

