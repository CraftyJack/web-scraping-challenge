from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import time
import re

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    
    # Run all scraping code (copied from jupyter notebook) and store in dictionary

    # 1.......Get Mars news
    # Start with the Nasa Mars News page.
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find_all(class_='content_title')[1].text
    news_p = soup.find_all(class_='article_teaser_body')[0].text


    # 2.......Get featured image
    # Now let's get some images from our friends at JPL.
    # Visit the page and then drill down to the featured image detail page.
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    browser.links.find_by_partial_text('FULL IMAGE').first.click()
    time.sleep(1)
    browser.links.find_by_partial_text('more info').first.click()
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the featured image
    relative_image_url = soup.find_all(class_='main_image')[0].get('src')
    featured_image_url = 'https://www.jpl.nasa.gov' + relative_image_url



    # 3.......Get hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls = []
    for thing in soup.find_all(class_='item'):
        # make a little dictionary
        hemisphere_dict = {}
        # add the name of the hemisphere and
        # get rid of the ' Enhanced' after the name
        hemisphere_name = thing.find('h3').string.replace(' Enhanced', '')
        hemisphere_dict['title'] = hemisphere_name
        # get the url for the image detail page
        target_url = 'https://astrogeology.usgs.gov/' + thing.find('a')['href']
        # go to the image detail page
        browser.visit(target_url)
        time.sleep(1)
        # scrape it
        html = browser.html
        new_soup = bs(html, "html.parser")
        # extract the image url and add it to the dictionary
        # I went with the jpg rather than the tif here. If I wanted the tif, I'd use '5' instead of '4'.
        hemisphere_dict['url'] = new_soup.find_all('a')[4].get('href')
        # add the dictionary to the list
        hemisphere_image_urls.append(hemisphere_dict)



    # 4.......Get twitter weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Extract the weather info.
    mars_weather = soup.find_all(class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[27].text



    # 5........Get mars facts
    #use pd.read_html and df.to_html
    url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url)[0]
    mars_table.columns = ['description', 'value']
    mars_table.set_index('description', inplace=True)
    mars_table_html = (mars_table.to_html()).replace('\n', '')


    # Store all scraped data in a dictionary
    data = {'news_title': news_title, 'news_p': news_p, 'featured_image_url': featured_image_url, 'hemisphere_image_urls': hemisphere_image_urls, 'weather': mars_weather, 'mars_table':mars_table_html}

    # Stop webdriver and return data
    browser.quit()

    return data
    # End Function

 
if __name__ == "__main__":
    scrape_all()