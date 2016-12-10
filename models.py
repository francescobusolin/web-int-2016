import os
import re
import io
import collections
import gensim

# SCRIPT 5 / 5
# -- INTRODUZIONE --
#   In questo script vengono usati due modelli diversi
#   costruire due Content Based Recommender
#   I modelli usati sono TF-IDF e LSI.
#   In particolare nell' analisi LSI
#   vengono usati in  serie 3 diversi valori di k

# NB: viene supposto che in precedenza siano stati eseguiti gli script @setup.py, @collect.py e extract.py
OTHER_DIR = 'other'
REPO_DIR = 'repo'
NEWS_DIR = os.path.join(REPO_DIR,'news')

# questa funzione serve per dividere il testo in parole e eliminare tutti i caratteri
# non significativi (punteggiatura, caratteri particolari)
def tokenize(document):
    document = document.lower()
    document = re.sub('[!"#$%&\'()*+,-./:;<=>?@\[\\\\\]^_`{|}~]', ' ', document)
    return document.split()

# questa funzione serve per ricavare, dato un lessico, un modello, un documento, e la numerosita'
# la lista degli n articoli piu' simili al documento dato come input
def recommendations(lexicon, model, document, n=10):
    index = gensim.similarities.MatrixSimilarity(model, num_features=len(lexicon)) # costruiamo la matrice di similarita'
    scores = index[document] # prendiamo i valori del documento in esame
    top = sorted(enumerate(scores), key=lambda (k, v): v, reverse=True) # ordiniamo rispetto alla similarita'
    return top[1:n] # ritorniamo i primi n documenti tranne il primo che ha similarita'
    # pari a 1 perche' e' document stesso


#vengono lette le notizie
documents = []
for filename  in os.listdir(NEWS_DIR):
    with io.open(os.path.join(NEWS_DIR,filename),encoding='utf-8') as f:
        document = f.read()
        documents.append(document)
        f.close()

# come in precedenza le notizie vengono suddivise in token
texts = [tokenize(document) for document in documents]
# vengono contate le occorrenze dei token
occurences = collections.Counter()
for text in texts:
    occurences.update(text)
# vengono lette le stopwords
with io.open(os.path.join(OTHER_DIR,'stopwords_eng.txt'),encoding='utf-8') as f:
    content = f.read()
stop = content.split('\n')

# vengono eliminate le stopwords e le parole con frequenza unitaria
texts = [[word for word in text if word not in stop and occurences[word] > 1]for text in texts]

#Ora viene usata la libreria gensim per analizzare il testo e costruire
# un Content Based Recommender

# viene costruito il lessico
lexicon = gensim.corpora.Dictionary(texts)
print 'built lexicon'

# vengono trasformati i documenti in bag of words
# ogni documento diventa un array di 2-uple
# ogni tupla rappresenta una parola e il numero di volte
# che essa appare nel documento
corpus = [lexicon.doc2bow(text) for text in texts]
print ' built corpus'

#TF-IDF analysis

print 'TF-IDF recomendations'
indexes = range(0,20,1) # prendiamo come campione i primi 20 documenti
tfidf = gensim.models.TfidfModel(corpus) # costruima il modello con gensim
for i in indexes: # diamo per ciascun documento i primi 5 documenti piu' simili
    print ('\nfor document %d we recommend:' % i)
    print recommendations(lexicon,tfidf[corpus],tfidf[corpus[i]],5)

print '-----------------------------------------------------------'

# LSI analysis
# l'ananili LSI e' del tutto analoga a quella TF-IDF
# gli unici cambiamenti sono il modello usato
# ed il fatto che viene ripetuta 3 volte con 3 valori di k distinti
k1 = 5
k2 = 50
k3 = 200

print 'LSI analysis for k = %d' % k1
indexes = range(0,20,1)
lsi = gensim.models.LsiModel(corpus,id2word=lexicon,num_topics=k1)
for i in indexes:
    print ('\nfor document %d we recommend:' % i)
    print recommendations(lexicon,lsi[corpus],lsi[corpus[i]],5)

print '--------------------------------------------------------'

print 'LSI analysis for k = %d' % k2
lsi = gensim.models.LsiModel(corpus,id2word=lexicon,num_topics=k2)
for i in indexes:
    print ('\nfor document %d we recommend:' % i)
    print recommendations(lexicon,lsi[corpus],lsi[corpus[i]],5)

print '---------------------------------------------------------'

print 'LSI analysis for k = %d' % k3
lsi = gensim.models.LsiModel(corpus,id2word=lexicon,num_topics=k3)
for i in indexes:
    print ('\nfor document %d we recommend:' % i)
    print recommendations(lexicon,lsi[corpus],lsi[corpus[i]],5)

# -- FINE SCRIPT --
