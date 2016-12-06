import os
import re
import io
import collections
import unicodecsv as csv
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

DATA_FILE = os.path.join(URLS_DIR,'urls')
def tokenize(document):
    document = document.lower()
    document = re.sub('[!"#$%&\'()*+,-./:;<=>?@\[\\\\\]^_`{|}~]', ' ', document)
    return document.split()
documents = []
for filename  in os.listdir(NEWS_DIR):
    with io.open(os.path.join(NEWS_DIR,filename),encoding='utf-8') as f:
        document = f.read()
        documents.append(document)
        f.close()

texts = [tokenize(document) for document in documents]
occurences = collections.Counter()
for text in texts:
    occurences.update(text)

most_common_overall = occurences.most_common(500)
file = 'common_overall.csv'
print most_common_overall
with open(os.path.join(OTHER_DIR,file),mode='w') as f:
    csv_writer = csv.writer(f,dialect='excel',delimiter = ',',encoding='utf-8')
    csv_writer.writerow(['word','count'])
    for key, count in most_common_overall:
        word = key
        print [word,count]
        csv_writer.writerow([word,count])