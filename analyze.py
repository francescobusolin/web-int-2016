import os
import re
import io
import collections
import csv
import gensim
# SCRIPT 4 / 5
# -- INTRODUZIONE --
#   In questo script vengono analizzate le notizie,
#   vengono prodotti due file csv i quali rappresenano
#   i conteggi delle parole.
#   - common_overall.csv contiene i conteggi delle parole inalterate
#   - common_lemma.csv contiene i conteggi dei lemmi

# NB: viene supposto che in precedenza siano stati eseguiti gli script @setup.py, @collect.py e extract.py
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
# questa funzione serve per dividere il testo in parole e eliminare tutti i caratteri
# non significativi (punteggiatura, caratteri particolari, e altro)
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
# ciascuna notizia diventa una lista di parole (token)
texts = [tokenize(document) for document in documents]
# contiamo le occorrenze delle parole
occurences = collections.Counter()
print 'counting terms...'
for text in texts:
    occurences.update(text)
# ricaviamo le 500 parole piu' comuni
# le salviamo nel file common_overall.csv
most_common_overall = occurences.most_common(500)
print 'building common terms table...'
file_ovr = 'common_overall.csv'
if not os.path.isfile(os.path.join(OTHER_DIR,file_ovr)):
    with open(os.path.join(OTHER_DIR,file),mode='w') as f:
            csv_writer = csv.writer(f,dialect='excel',delimiter = ',',encoding='utf-8')
            csv_writer.writerow(['word','count'])
            for key, count in most_common_overall:
                word = key
                csv_writer.writerow([word,count])
print 'wrote overall table'
# leggiamo le stopwords
with io.open(os.path.join(OTHER_DIR,'stopwords_eng.txt'),encoding='utf-8') as f:
    content = f.read()
stop = content.split('\n')
# eliminiamo tutte le parole con frequenza 1 e le stopwords
texts = [[word for word in text if word not in stop and occurences[word] > 1]for text in texts]
lemma = []
#  usiamo gensim per costruire i lemmi
print 'lemmatizing...'
for news in texts:
    news_lemma = []
    for word in news:
        news_lemma.append(gensim.utils.lemmatize(word))
    lemma.append(news_lemma)
print 'counting lemmas...'
# contiamo i lemmi e li salviamo nel file common_lemma.csv
lemma_counter = collections.Counter()
for row in lemma:
    for cell in row:
        lemma_counter.update(cell)
most_common_lemmatized = lemma_counter.most_common(500)
print 'building lemmas table...'
file_lemma = 'common_lemma.csv'
if not os.path.isfile(os.path.join(OTHER_DIR,file_lemma)):
    with open(os.path.join(OTHER_DIR,file),mode='w') as f:
        csv_writer = csv.writer(f,dialect='excel',delimiter = ',',encoding='utf-8')
        csv_writer.writerow(['word','count'])
        for key, count in most_common_lemmatized:
            word = key
            csv_writer.writerow([word,count])
print 'wrote lemmas table'