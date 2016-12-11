import os
import re
import BeautifulSoup
import codecs
import HTMLParser
# SCRIPT 3 / 5
# -- INTRODUZIONE --
#   In questo script vengono estratte e memorizzate le notizie
#   lo script non controlla se la notizia esiste gia', sovrascrive.

# NB: viene supposto che in precedenza siano stati eseguiti gli script @setup.py e @collect.py
OTHER_DIR = 'other'
REPO_DIR = 'repo'
PAGES_DIR = os.path.join(REPO_DIR,'pages')
URLS_DIR = os.path.join(REPO_DIR,'urls')
NEWS_DIR = os.path.join(REPO_DIR,'news')
FILES = os.path.join(URLS_DIR,'files')


i = 0
files = []
h = HTMLParser.HTMLParser()
# leggiamo i path delle pagine
# questo paggassio e' figlio di un problema di duplicazione di indirizzi
# ovvero alcune notizie apparivano piu' di una volta
# e' stato quindi utile salvare i percorsi su un file separato per controllo
# il problema e' stato risolto ma questo passaggio rimane
with open(FILES,mode='r') as f:
    files = f.read().split('\n')
# leggo le pagine
for filename in files:
    try:
        with open( filename) as f:
            page = f.read()
            f.close()
    except IOError as e:
        print 'cannot read this page ' + filename

    # estraggo tutti i tag div con classe terminante con 'Par'
    soup = BeautifulSoup.BeautifulSoup(page)
    document_list = soup.findAll('div',{ "class" : re.compile('Par$')}) # ottengo la notizia come lista di paragrafi
    document = ''

    # trasformo i documenti in stringhe
    for div in document_list:
        document = document + div.text + '\n'
    print 'extracted news ' + str(i)
    # se la pagina ha una notizia la salvo su file
    if len(document_list) >0:
        try:
            filename = re.sub('[^a-zA-Z0-9]+', '-', filename)
            with codecs.open(os.path.join(NEWS_DIR,filename),mode='wb',encoding='utf-8') as fd:
                fd.write( h.unescape(document)) # questo passaggio serve perinterpretare i caratteri codificati
                # all' interno del documento (&#...;)
                i += 1
        except IOError as e:
            print 'failed to write news ' + filename

print 'total news extracted: ' + str(i) + '\n'

# -- FINE SCRIPT --
