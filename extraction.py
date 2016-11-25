import urllib
import os.path
import re

# Questo script scarica e memorizza gli url ricavandoli dai link nel file links

# Si ricavano i link dell' archivio
input = open('other/links','r')
urls = input.readlines()
input. close()

archive = 'other/inter'
repo_dir = 'repo'
pages_dir = repo_dir + '/pages'
urls_dir = repo_dir + "/urls"
news_dir = repo_dir + '/news'

if( not os.path.isdir(archive)):
    print 'creating dir "intermediate"'
    os.mkdir(archive)

if (not os.path.isdir(repo_dir)):
    print 'creating dir "repo"'
    os.mkdir(repo_dir)

if (not os.path.isdir(urls_dir)):
    print 'creating dir "urls"'
    os.mkdir(urls_dir)

if (not os.path.isdir(news_dir)):
    print 'creating dir "news"'
    os.mkdir(news_dir)
#print urls
# per ogni url se presente lo apro altrimenti lo scarico
# attendo un secondo tra un download e l'altro
i = j = 0
for url in urls:
    # mantengo solo i caratteri non speciali
    filename = re.sub('[^a-zA-Z0-9]+', '-', url)
    # scarico la pagina solo se non  presente
    download_path = os.path.join(archive, filename)
    print download_path
    if not os.path.exists(download_path):
        try:
            urllib.urlretrieve(url, download_path)
        except IOError:
            print 'Errore in File'
            j += 1
        print "Done single download " + str(i)
    i += 1
print 'Errori in lettura: ' + str(j)


inputs = os.listdir('other/inter')

for input in inputs:
    print input