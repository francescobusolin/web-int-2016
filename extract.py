import os
import urllib2
import time
# it is supposed that the @collect.py script had been previously run
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

DATA_FILE = os.path.join(URLS_DIR,'urls')


with open(DATA_FILE,'r') as f:
    urls = f.read().split("\n")
    f.close()
i = j =  0
pages = []
for url in urls:
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        page = response.read()
        pages.append(page)
        i += 1
        time.sleep(1)
        print str(i) + ' -- ' + str(j)
    except (IOError,ValueError) as e:
        print 'something is going wrong'
        j += 1

print str(i) + ' pages downloaded'
print str(j) + ' errors occurred'
i = 0
for page in pages:
    filename = 'PAGE_' + str(i)
    with open(os.path.join(PAGES_DIR,filename),mode='w') as fd:
        fd.write(page)
        i += 1
        print 'saved ' + filename
