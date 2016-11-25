import urllib
import os.path
import re
import time
import BeautifulSoup

# this script is used to collect some news links from
# the archive of the telegraph

#in the first step we setup the environment creating dirs
# and initializing some global variables

# here we read the references to the archive
# at the moment there are links to
# the news from the 1st of November 2014 to the 16th November 2014
archive_file = open('other/links', 'r')
urls = archive_file.readlines()
archive_file. close()
# here we setup all the globally used references
INTERMEDIATE_DIR = 'other/inter/'
ARCHIVE_DIR = INTERMEDIATE_DIR + 'archive'
COMPRESSED_URLS = INTERMEDIATE_DIR + "compressed"

REPO_DIR = 'repo'
PAGES_DIR = REPO_DIR + '/pages'
URLS_DIR = REPO_DIR + "/urls"
NEWS_DIR = REPO_DIR + '/news'

REMOTE_BASE = 'http://www.telegraph.co.uk'

# here we create (if not present) every directory used later
if(not os.path.isdir(INTERMEDIATE_DIR)):
    print 'creating dir "intermediate"'
    os.mkdir(INTERMEDIATE_DIR)

if(not os.path.isdir(ARCHIVE_DIR)):
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

# here we download every page from the archive and we store them in our
# archive directory, we also wait 1 second between each download
i = j = 0
for url in urls:
    filename = re.sub('[^a-zA-Z0-9]+', '-', url)
    download_path = os.path.join(ARCHIVE_DIR, filename)
    #print download_path
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


news_links = []
# here we extract the useful links from each page
# after examinating the structure of nthe web pages
# we know that the links useful to us are inside a 'href'
# property and they are like'/news/<name of article>.html'
for line in os.listdir(ARCHIVE_DIR):
    with open(os.path.join(ARCHIVE_DIR, filename)) as f:
        page = f.read()
        f.close()
    soup = BeautifulSoup.BeautifulSoup(page)
    #print page
    hrefs = []
    links =  soup.findAll('a',href = True)
    for link in links:
        hrefs.append(link['href'])
    for href in hrefs:
        str(href)
        if(href.startswith('/news')):
            news_links.append(REMOTE_BASE + href)

print 'collected ' + str(len(news_links)) + ' links'
# after collecting all the links we store them in a unique file
# in the urls directory
f = open(os.path.join(URLS_DIR + '/urls'), 'w')
for url in news_links:
    f.write(url+'\n')

f.close()
print 'wrote all links into the file ' + URLS_DIR + '/urls'

# this is the end of the extraction script


