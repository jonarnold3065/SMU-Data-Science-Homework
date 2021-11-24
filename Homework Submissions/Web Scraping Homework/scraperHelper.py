# SCRAPING IMPORTS
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time
from datetime import datetime

class ScraperHelper():
    def __init__(self):
        pass

    def scrapeMars(self):
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        # NASA MARS website news
        url = "https://redplanetscience.com/"
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, "lxml")

        news = soup.find("div", {"id": "news"})

        rows = news.find_all("div", {"class", "row"})
        first_row = rows[0]

        news_title = first_row.find("div", {"class", "content_title"}).text
        news_paragraph = first_row.find("div", {"class": "article_teaser_body"}).text

        ## JPL Mars Space website Images
        url = "https://spaceimages-mars.com/"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "lxml")
        image = soup.find("img", {"class": "headerimage"})
        featured_image_url = url + image["src"]

        # Mars website facts
        url = "https://galaxyfacts-mars.com/"
        browser.visit(url)
        html = browser.html
        dfs = pd.read_html(html)
        facts = dfs[1]
        facts_html = facts.to_html(header=False)

        # Hemispheres
        url = "https://marshemispheres.com/"
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, "lxml")

        hemis = soup.find_all("div", {"class":"item"})

        hemi_info = []
        for hemi in hemis:
            hemi_url = url + hemi.find("a", {"class": "itemLink"})["href"]
            browser.visit(hemi_url)
            time.sleep(1)
            
            html = browser.html
            soup = BeautifulSoup(html, "lxml")
            
            link = url + soup.find("img", {"class", "wide-image"})["src"]
            title = soup.find("h2", {"class", "title"}).text
            
            data = {
                "img_url": link,
                "title": title
            }
            
            hemi_info.append(data)

        # DONE
        browser.quit()

        # Combine
        final_data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image_url": featured_image_url,
            "mars_facts": facts_html,
            "hemispheres": hemi_info,
            "last_updated": datetime.utcnow()
        }
        return (final_data)
