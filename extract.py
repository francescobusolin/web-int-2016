import os
import re
import BeautifulSoup
import io
# it is supposed that both @setup.py and @collect.py scripts had been previously run
# here we setup all the globally used references
OTHER_DIR = 'other'
INTERMEDIATE_DIR = os.path.join(OTHER_DIR,'inter')
ARCHIVE_DIR = os.path.join(INTERMEDIATE_DIR,'archive')
COMPRESSED_URLS = os.path.join(INTERMEDIATE_DIR,'compressed')

REPO_DIR = 'repo'
PAGES_DIR = os.path.join(REPO_DIR,'pages')
URLS_DIR = os.path.join(REPO_DIR,'urls')
NEWS_DIR = os.path.join(REPO_DIR,'news')

REMOTE_BASE = 'http://www.telegraph.co.uk'
documents = []
i = 0
for filename in os.listdir(PAGES_DIR):
    with open(os.path.join(PAGES_DIR, filename)) as f:
        page = f.read()
        f.close()
    soup = BeautifulSoup.BeautifulSoup(page)
    document_list = soup.findAll('div',{ "class" : re.compile('Par$')})
    document = ''
    for div in document_list:
        document = document + div.text + '\n'
    print 'extracted news ' + str(i)
    documents.append(document)
    i += 1
print 'total news extracted: ' + str(i) + '\n'
i = 0
for doc in documents:
    filename = 'NEWS_' + str(i)
    with io.open(os.path.join(NEWS_DIR,filename),mode='w',encoding='utf-8') as f:
        f.write(unicode(doc))
        print 'saved news ' + str(i)
    i += 1
print '\ntotal saved news ' + str(i)