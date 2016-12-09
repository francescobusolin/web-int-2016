import urllib
import os.path
import re
import time
import BeautifulSoup

# SCRIPT 1 / 5
# -- INTRODUZIONE --
#   In questo script viene creato l' ambiente e vengono estratti i link
#   alle pagine contententi le notizie.

# qui vengono create delle costanti raffiguranti le directory usate
OTHER_DIR = 'other'
INTERMEDIATE_DIR = os.path.join(OTHER_DIR,'inter')
ARCHIVE_DIR = os.path.join(INTERMEDIATE_DIR,'archive')
COMPRESSED_URLS = os.path.join(INTERMEDIATE_DIR,'compressed')

REPO_DIR = 'repo'
PAGES_DIR = os.path.join(REPO_DIR,'pages')
URLS_DIR = os.path.join(REPO_DIR,'urls')
NEWS_DIR = os.path.join(REPO_DIR,'news')

REMOTE_BASE = 'http://www.telegraph.co.uk'


# Qui vengono letti i link all 'archivio web
# al momento i link riguardano le notizie del telegraph
# da 1/11/2014 al 16/11/2014
archive_file = open(os.path.join(OTHER_DIR,'links'), 'r')
urls = archive_file.readlines()
archive_file. close()

# Qui si creano ( se non presenti le directory usate)
# NB: da qui in avanti si supporranno esistenti
if(not os.path.isdir(INTERMEDIATE_DIR)):
    print 'creating dir "intermediate"'
    os.mkdir(INTERMEDIATE_DIR)

if (not os.path.isdir(ARCHIVE_DIR)):
    print 'creating dir "archive"'
    os.mkdir(ARCHIVE_DIR)

if (not os.path.isdir(COMPRESSED_URLS)):
    print 'creating dir "urls archive"'
    os.mkdir(COMPRESSED_URLS)

if (not os.path.isdir(REPO_DIR)):
    print 'creating dir "repo"'
    os.mkdir(REPO_DIR)

if (not os.path.isdir(URLS_DIR)):
    print 'creating dir "urls"'
    os.mkdir(URLS_DIR)

if (not os.path.isdir(NEWS_DIR)):
    print 'creating dir "news"'
    os.mkdir(NEWS_DIR)
if (not os.path.isdir(PAGES_DIR)):
    print 'creating dir "pages"'
    os.mkdir(PAGES_DIR)

# qui si scaricano le pagine web
# solo e non precedentemente scaricate
# tra un download e l' altro si aspetta 1 secondo
i = j = 0
for url in urls:
    filename = re.sub('[^a-zA-Z0-9]+', '-', url)
    download_path = os.path.join(ARCHIVE_DIR, filename)
    if not os.path.exists(download_path):
        try:
            urllib.urlretrieve(url, download_path)
            time.sleep(1)
        except IOError:
            print 'Error in File'
            j += 1
        print "Done single download " + str(i)
    i += 1

print 'Reading Errors: ' + str(j)

i = 0
news_links = []
# qui vengono estratti gli url alle pagine delle notizie
# dall 'analisi della struttura delle pagine si deduce che
# i link utili sono contenuti in un campo 'href'
#  e hanno la forma: '/news/<titolo>.html'
for line in os.listdir(ARCHIVE_DIR):
    with open(os.path.join(ARCHIVE_DIR, line)) as f:
        page = f.read()
        f.close()
    soup = BeautifulSoup.BeautifulSoup(page)
    #print page
    divs = soup.findAll('a',href = True )
    with open(os.path.join(URLS_DIR, 'urls'), mode='ab') as f:
        for div in divs:
            if div['href'].startswith('/') and len(div['href']) > 5 and div['href'] not in news_links:
                f.write(REMOTE_BASE + div['href']+ '\n')
                news_links.append(div['href'])
                i  = i + 1
                #print str(i)
print 'wrote all links into the file ' + URLS_DIR + '/urls'
print 'wrote ' + str(i) + ' links'

# -- FINE SCRIPT --

