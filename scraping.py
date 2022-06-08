# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

# # Set up Splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}

# browser = Browser(
#     'chrome',
#     **executable_path,
#     headless=False,
#     incognito=True
# )

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser(
        'chrome',
        **executable_path,
        headless=True,
        incognito=True  # No need to save sites visited in browser History
    )
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "facts":mars_facts(),
        "last_modified":dt.datetime.now()
    }
    
    # Stop Web-driver and return data
    browser.quit()
    return data

# Scrape Mars News
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first `div` tag that has class `'content_title'``, and save its text as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_paragraphs = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_paragraphs

# ## JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]  # There are three buttons on the page, and the one we want is
                                                        # the 1st (starting from 0)
    full_image_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'{url}/{img_url_rel}'
    
    return img_url

# ## Mars Facts
def mars_facts():
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]    # The scrape returns two tables; use the 0th one.
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth'] # The columns are unnamed; name them.
    df.set_index('description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
