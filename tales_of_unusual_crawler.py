#! python3
# tales_of_unusual_crawler.py
import requests, os, bs4, logging, time
logging.basicConfig(filename='crawler.log', filemode='w', level=logging.DEBUG,format=' %(asctime)s - %(levelname)s- %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
start_time = time.time()


# Crawler to get image of episodes
def imageCrawler(url):
    folderName = os.path.basename(url).split('&')[1]
    os.makedirs(folderName,exist_ok=True) # store comics ./episode=XX
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': url
        }
    # Download the page
    logging.debug('Downloading episode page %s...' % url)
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,'lxml')
    # Find the URL of the comic image.
    comicElem = soup.select('#_imageList img')
    if comicElem == []:
        logging.debug('Could not find comic images.')
    else:
        logging.debug(len(comicElem))
        for elem in comicElem:
            comicUrl = elem.get('data-url')
            filebasename = os.path.basename(comicUrl)
            filename = filebasename.split('?')[0]
            imageFilePath = os.path.join(folderName, filename)
            if not os.path.exists(imageFilePath):
                logging.debug('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl,headers=headers)
                try:
                    res.raise_for_status()
                except Exception as exc:
                    logging.debug('There was a problem: %s' % (exc))
                
                imageFile = open(imageFilePath,'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
            
# Crawler to get pageLink
def pageLinkCrawler(startUrl):
    pageLinks = set()
    pageLinks.add(startUrl)
    # Download the page
    while not startUrl.endswith('21'):
        res = requests.get(startUrl)
        try:
            res.raise_for_status()
        except Exception as exc:
            logging.debug('There was a problem: %s' % (exc))
        soup = bs4.BeautifulSoup(res.text,"lxml")
        # Find the pagenite urls
        paginateElem = soup.select('.paginate a')
        next_page_link = ''
        # Find the URL of each page
        if paginateElem == []:
            logging.debug('Could not find paginate links.')
        else:
            for elem in paginateElem:
                if not elem.get('href').endswith('#'):
                    pageLink = 'http://www.webtoons.com'+elem.get('href')
                    pageLinks.add(pageLink)
                    next_page_link = pageLink
        startUrl = next_page_link
    return pageLinks
# Crawler to get Get the episodeLink
def episodeLinkCrawler(pageLinks):
    episodeLinks = []
    episodeLinksFile = open('episodeLinks.txt', 'w')
    for pageLink in pageLinks:
        logging.debug('Downloading page %s...' % pageLink)
        res = requests.get(pageLink)
        try:
            res.raise_for_status()
        except Exception as exc:
            logging.debug('There was a problem: %s' % (exc))
        soup = bs4.BeautifulSoup(res.text,"lxml")
        # Find the episode links
        episodeElem = soup.select('#_listUl li a')
        if episodeElem == []:
            print('Could not find episodeElem')
        else:
            for elem in episodeElem:
                episodeLink = elem.get('href')
                logging.debug('EpisodeLink %s...' % episodeLink)
                episodeLinks.append(episodeLink)
                episodeLinksFile.write(episodeLink+'\n')
    episodeLinksFile.close()
    return episodeLinks

startUrl = 'http://www.webtoons.com/zh-hant/thriller/tales-of-the-unusual/list?title_no=290&page=1'  # starting url
logging.info('Start of program')
pagelinkstart_time = time.time()
pageLinks = pageLinkCrawler(startUrl)
logging.info("pageLinkCrawler time--- %s seconds ---" % (time.time() - pagelinkstart_time))
logging.info("Total time--- %s seconds ---" % (time.time() - start_time))
episodelinkstart_time = time.time()
episodeLinks = episodeLinkCrawler(pageLinks)
logging.info("episodeLinkCrawler time--- %s seconds ---" % (time.time() - episodelinkstart_time))
logging.info("Total time--- %s seconds ---" % (time.time() - start_time))
logging.info('Total episodeLink amount: %s...' % len(episodeLinks))

for episodeLink in episodeLinks:
    episodestart_time = time.time()
    logging.info('Carwling %s...' % episodeLink.split('&')[1])
    imageCrawler(episodeLink)
    logging.info("episodeImageCrawler time--- %s seconds ---" % (time.time() - episodestart_time))
    logging.info("Total time--- %s seconds ---" % (time.time() - start_time))



