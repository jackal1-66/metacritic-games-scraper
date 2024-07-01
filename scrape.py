#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import random

# URL of the page you want to scrape
baseurl = "https://www.metacritic.com"

# Send a GET request to the URL with a Windows user agent
userAgents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"]

def getList():
    global userAgents
    gameref = []
    url = "https://www.metacritic.com/browse/game/nintendo-switch/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2024&platform=nintendo-switch&page="
    session = requests.Session()
    for i in range(1, 81):
        urlp = url + str(i)
        print("Getting URL: " + urlp)
        userAgent = {"User-Agent": random.choice(userAgents)}
        response = session.get(urlp, headers=userAgent)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            # Find the elements you want to scrape
            # Example: scraping game titles
            game_titles = soup.find_all("a", href=True, class_="c-finderProductCard_container g-color-gray80 u-grid")

            # Print the scraped data
            for title in game_titles:
                #title = title.find_next('span').find_next('span').text
                gameref.append(title['href'])
        else:
            print("Failed to retrieve data from the URL in list")
        sleep(0.01)    
    return gameref

def f_date(rel):
    try:
        date = rel[0].find_next('span').find_next('span').text
        date = date.replace("\"", "")
    except(IndexError):
        date = "N/A"
    return date

def f_genre(gen):
    try:
        genre = " ".join(gen[0].text.split())
    except(IndexError):
        genre = "N/A"   
    return genre

def f_publish(pub):
    try:
        publish = pub[0].find_next('span').find_next('span').text
    except(IndexError):
        publish = "N/A"
    return publish

def f_devel(dev):
    try:     
        devel = dev[0].find_next('li')
        devel = " ".join(devel.text.split())
    except(IndexError):
        devel = "N/A"
    return devel

def f_score(scores):
    try:
        meta_score = scores[0].find_next('span').text
    except(IndexError):
        meta_score = "N/A"
    try:
        user_score = scores[1].find_next('span').text
    except(IndexError):
        user_score = "N/A"  
    return meta_score, user_score

def f_nuser(rev):
    try:
        revcr = rev[0].find_next('a').text
        revcr = revcr.split()[2].replace(",", "")
    except(IndexError):
        revcr = "N/A"
    try:
        revus = rev[1].find_next('a').text
        revus = revus.split()[2].replace(",", "")
        if revus == "Reviews":
            revus = "N/A"
    except(IndexError):
        revus = "N/A"    
    return revcr, revus   


def getGameInfo(gameref):
    global userAgents, baseurl
    gameinfo = {'Title': [], 'Genre': [], 'Release date': [], 'Metascore': [], "N. Critics": [], 'User Score': [], "N. Users": [], 'Developer': [], 'Publisher': []}
    session = requests.Session()
    a = 0
    for i in gameref:
        url = baseurl + str(i)
        print("Index " + str(a) + " getting URL: " + url)
        a += 1
        userAgent = {"User-Agent": random.choice(userAgents)}
        response = session.get(url, headers=userAgent)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            # Find the elements you want to scrape
            # Example: scraping game titles
            title = soup.find_all("div", class_="c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium")
            rel = soup.find_all("div", class_="c-gameDetails_ReleaseDate u-flexbox u-flexbox-row")
            gen = soup.find_all("a", class_="c-globalButton_container g-text-normal g-height-100 u-flexbox u-flexbox-alignCenter u-pointer u-flexbox-justifyCenter g-width-fit-content")
            pub = soup.find_all("div", class_="c-gameDetails_Distributor u-flexbox u-flexbox-row")
            developer = soup.find_all("div", class_="c-gameDetails_Developer u-flexbox u-flexbox-row")
            scores = soup.find_all("div", class_="c-productScoreInfo_scoreNumber u-float-right")
            rev = soup.find_all("div", class_="c-productScoreInfo_text g-outer-spacing-right-auto")
            
            # Append the scraped data
            gameinfo['Title'].append(title[0].text)
            rel = f_date(rel)
            gameinfo['Release date'].append(rel)
            gen = f_genre(gen)
            gameinfo['Genre'].append(gen)                
            pub = f_publish(pub)
            gameinfo['Publisher'].append(pub)
            dev = f_devel(developer) 
            gameinfo['Developer'].append(dev)   
            meta_score, user_score = f_score(scores)   
            gameinfo['Metascore'].append(meta_score)
            gameinfo['User Score'].append(user_score)
            revcr, revus = f_nuser(rev)
            gameinfo['N. Critics'].append(revcr)
            gameinfo['N. Users'].append(revus)
        else:
            print("Failed to retrieve data from the URL in info")
        sleep(0.01)        
    return gameinfo

def test():
    data = getGameInfo(["/game/switch/the-legend-of-zelda-breath-of-the-wild","/game/switch/solas-128"])
    print(data)

def main():
    names = getList()
    data = getGameInfo(names)
    pd.DataFrame(data).to_csv("switchInfo.csv", index=False)

if __name__ == "__main__":
    main()