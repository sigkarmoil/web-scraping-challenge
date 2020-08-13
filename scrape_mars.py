from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

#initialize browser to make this usable

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #for mac users
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", headless=False)

## Get Latest Title and Teaser ##

def scrape():
## Get Latest Title and Teaser ##
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

        #if you need to give space
    time.sleep(1)

        # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")

    # Get the news title #
    stripped_title=[]
    titles = soup.find_all('div', class_='content_title')
    for title in titles:
        stripped_title.append(title.text.strip())
    latest_title = stripped_title[1]

        # Get the news teaser
    get_teaser = soup.find('div', class_='article_teaser_body') 
    latest_teaser = get_teaser.text

## Get featured image ##
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

            #if you need to give space
    time.sleep(1)

        # Click featured image button
    try:
        browser.click_link_by_partial_text('FULL IMAGE')

    except:
        print("Clicking Failed")

        # Click More Info
    try:
        browser.click_link_by_partial_text('more info')

    except:
        print("Clicking Failed")

        # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    featured_image_url = "https://www.jpl.nasa.gov"+ str(soup.find('img', class_='main_image')['src']) 

## Scrape Twitter ##

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
            # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    latest_temp = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather = latest_temp.text

## Get mars facts ##

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)

    import pandas as pd
            # Parse the image
            # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    table = pd.read_html(url)
    table_df=table[0]
    html_table = table_df.to_html()

## Store data in dictionary ##
    scrape_data = {
        "latest_title": latest_title,
        "latest_teaser": latest_teaser,
        "featured_image_url": featured_image_url,
        "twitter_scrape":mars_weather,
        "html_table":html_table
    }

# Close the browser after scraping
    browser.quit()

    # Return results
    return scrape_data