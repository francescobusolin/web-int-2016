import os
import urllib
import time
import re
import io
# it is supposed that the @setup.py script had been previously run
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
i = j = k = 0
#pages = []
paths = []
for url in urls:
    filename = re.sub('[^a-zA-Z0-9]+', '-', url)
    download_path = os.path.join(PAGES_DIR, filename)
    if not os.path.exists(download_path):
        try:
            urllib.urlretrieve(url, download_path)
            #req = urllib2.Request(url)
            #esponse = urllib2.urlopen(req)
           # page = response.read()
#            pages.append(page)
            i += 1
           # time.sleep(1)
         #   with io.open(os.path.join(PAGES_DIR, filename), mode='wb') as fd:
                #fd.write(page)
        except (IOError,ValueError) as e:
            print 'something is going wrong'
            j += 1
        print str(i) + ' -- ' + str(j)
    else:
        print 'already present page ' + download_path
        k += 1
    paths.append(download_path)

print str(i) + ' pages downloaded'
print str(k) + ' pages already stored'
print str(j) + ' errors occurred'

with open(os.path.join(URLS_DIR,'files'),mode='wb') as f:
    for path in paths:
        f.write(path)
        f.write('\n')
