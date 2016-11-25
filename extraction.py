import urllib
import os.path
import re
import time
import BeautifulSoup

# Questo script scarica e memorizza gli url ricavandoli dai link nel file links

# Si ricavano i link dell' archivio
input = open('other/links','r')
urls = input.readlines()
input. close()

intermediate_dir = 'other/inter/'
archive = intermediate_dir + 'archive'
compressed_urls =  intermediate_dir + "compressed"

repo_dir = 'repo'
pages_dir = repo_dir + '/pages'
urls_dir = repo_dir + "/urls"
news_dir = repo_dir + '/news'

if( not os.path.isdir(intermediate_dir)):
    print 'creating dir "intermediate"'
    os.mkdir(intermediate_dir)

if(not os.path.isdir(archive)):
    print 'creating dir "archive"'
    os.mkdir(archive)

if (not os.path.isdir(compressed_urls)):
    print 'creating dir "urls archive"'
    os.mkdir(compressed_urls)

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
            time.sleep(1)
        except IOError:
            print 'Errore in File'
            j += 1
        print "Done single download " + str(i)
    i += 1
print 'Errori in lettura: ' + str(j)


inputs = os.listdir(archive)

for input in inputs:
    print input
