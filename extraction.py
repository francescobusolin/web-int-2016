import urllib2
import time
import os.path
from __builtin__ import input
# Questo script scarica e memorizza gli url ricavandoli dai link nel file links

# Si ricavano i link dell' archivio
input = open('other/links','r')
urls = input.readlines()
input. close()
#print urls
# per ogni url se presente lo apro altrimenti lo scarico
# attendo un secondo tra un download e l'altro
for url in urls:
    file = 'other/inter/' + url.replace('/','-')
    if not os.path.isfile(file):
        page = urllib2.urlopen(url)
        output = open(file,'w')
        output.writelines(page)
       # print 'sleeping for' + file
        time.sleep(1)
    else:
        print 'already present ' + file

target = 'repo/urls/'   # cartella su cui salvare gli urls delle singole notizie