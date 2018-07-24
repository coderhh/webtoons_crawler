#! python3
# tales_of_unusual_crawler.py
import requests, os, bs4, csv

def episodeLinkCrawler():
    a=open('sandbox.html','r') 
    htmlline=a.read() 
    soup=bs4.BeautifulSoup(htmlline,"html.parser") 
    trs = soup.findAll("tr", {"class": "approved"})
    count = 0
    with open('sandbox.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'event','activation','status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for tr in trs:
                    count = count + 1
                    name = tr.findAll("td")[1]['title']
                    event  = tr.findAll("td")[2].text
                    activation  = tr.findAll("td")[7].text
                    status  = tr.findAll("td")[8].text
                    
                    writer.writerow({'name': name, 'event': event, 'activation': activation,'status':status})
        print(count)
episodeLinkCrawler()





