import os
import urllib
import time
import re
# SCRIPT 2 / 5
# -- INTRODUZIONE --
#   In questo script vengono scaricate e memorizzate le pagine
#   web contenti le notizie

# NB: viene supposto che in precedenza sia stato eseguito lo script @setup.py

OTHER_DIR = 'other'
REPO_DIR = 'repo'
PAGES_DIR = os.path.join(REPO_DIR,'pages')
URLS_DIR = os.path.join(REPO_DIR,'urls')
DATA_FILE = os.path.join(URLS_DIR,'urls')

# qi leggiamo il file prodotto
# da @setup.py che contiene gli url delle pagine
# da scaricare
with open(DATA_FILE,'r') as f:
    urls = f.read().split("\n")
    f.close()

#queste variabili servono solo come indicatori e
# per dare un feedback all' utilizzatore
i = j = k = 0

# paths contiene i path ai file delle pagine web
paths = []

# qui si scaricano le pagine web
# solo e non precedentemente scaricate
# tra un download e l' altro si aspetta 1 secondo
for url in urls[10000:12000]:
    filename = re.sub('[^a-zA-Z0-9]+', '-', url)
    download_path = os.path.join(PAGES_DIR, filename)
    if not os.path.exists(download_path):
        try:
            urllib.urlretrieve(url, download_path)
            i += 1
            time.sleep(1)
            print download_path
            paths.append(download_path) # salvo i path solo delle news che scarico perhe' se non scarico una pagina
            # allora il suo path e' gia' memorizzato o la pagina ha avuto errori
        except (IOError,ValueError) as e:
            print 'something is going wrong'
            j += 1
    else:
        print 'already present page ' + download_path
        k += 1


print str(i) + ' pages downloaded'
print str(k) + ' pages already stored'
print str(j) + ' errors occurred'

# qui si salvano i path ai vari file, in modo simile a quanto fatto
# per gli urls
# i path nuovi vengono accodati al file
with open(os.path.join(URLS_DIR,'files'),mode='ab') as f:
    for path in paths:
        f.write(path)
        f.write('\n')

# -- FINE SCRIPT --
