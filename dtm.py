#! python3
# tales_of_unusual_crawler.py
import requests, os, bs4, csv

def episodeLinkCrawler():
    a=open('web.html','r') 
    htmlline=a.read() 
    soup=bs4.BeautifulSoup(htmlline,"html.parser") 
    divs = soup.findAll("article")
    count = 0
    with open('web.csv', 'w', newline='') as csvfile:
        fieldnames = ['web_name', 'web_url','web_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for div in divs:
                    count = count + 1
                    name = div.find("h1").text
                    url  = div.find("p").text
                    status  = div.findAll("p")[1].text
                    print(name,url, status)
                    writer.writerow({'web_name': name, 'web_url': url, 'web_status': status})
        print(count)
episodeLinkCrawler()





