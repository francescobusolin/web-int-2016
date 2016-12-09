import os
import re
import BeautifulSoup
import codecs
import HTMLParser
# SCRIPT 3 / 5
# -- INTRODUZIONE --
#   In questo script vengono estratte e memorizzate le notizie

# NB: viene supposto che in precedenza siano stati eseguiti gli script @setup.py e @collect.py
OTHER_DIR = 'other'
INTERMEDIATE_DIR = os.path.join(OTHER_DIR,'inter')
ARCHIVE_DIR = os.path.join(INTERMEDIATE_DIR,'archive')
COMPRESSED_URLS = os.path.join(INTERMEDIATE_DIR,'compressed')

REPO_DIR = 'repo'
PAGES_DIR = os.path.join(REPO_DIR,'pages')
URLS_DIR = os.path.join(REPO_DIR,'urls')
NEWS_DIR = os.path.join(REPO_DIR,'news')
FILES = os.path.join(URLS_DIR,'files')
REMOTE_BASE = 'http://www.telegraph.co.uk'

i = 0
files = []
h = HTMLParser.HTMLParser()
with open(FILES,mode='r') as f:
    files = f.read().split('\n')

for filename in files:
    try:
        with open( filename) as f:
            page = f.read()
            f.close()
    except IOError as e:
        print 'cannot read this page ' + filename
    soup = BeautifulSoup.BeautifulSoup(page)
    document_list = soup.findAll('div',{ "class" : re.compile('Par$')})
    document = ''
    for div in document_list:
        document = document + div.text + '\n'
    print 'extracted news ' + str(i)
    if len(document_list) >0:
        try:
            filename = re.sub('[^a-zA-Z0-9]+', '-', filename)
            with codecs.open(os.path.join(NEWS_DIR,filename),mode='wb',encoding='utf-8') as fd:
                fd.write( h.unescape(document))
                i += 1
        except IOError as e:
            print 'failed to write news ' + filename
print 'total news extracted: ' + str(i) + '\n'
