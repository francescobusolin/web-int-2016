import os
import re
import io
import collections
import gensim
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

def recommendations(lexicon, model, document, n=10):
    index = gensim.similarities.MatrixSimilarity(model, num_features=len(lexicon))
    scores = index[document]
    top = sorted(enumerate(scores), key=lambda (k, v): v, reverse=True)
    return top[1:n]

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
with io.open(os.path.join(OTHER_DIR,'stopwords_eng.txt'),encoding='utf-8') as f:
    content = f.read()
stop = content.split('\n')

texts = [[word for word in text if word not in stop and occurences[word] > 1]for text in texts]

lexicon = gensim.corpora.Dictionary(texts)
print 'built lexicon'

corpus = [lexicon.doc2bow(text) for text in texts]
print ' built corpus'

#TF-IDF analysis
indexes = range(15,35,1)
tfidf = gensim.models.TfidfModel(corpus)
for i in indexes:
    print ('\nfor document %d we recommend:' % i)
    print recommendations(lexicon,tfidf[corpus],tfidf[corpus[i]],20)
