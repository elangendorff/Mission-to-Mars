# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

from urllib.parse import urljoin    # https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse

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
    
    # Run all scraping functions and store results in dictionary
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "facts":mars_facts(),
        "hemispheres":mars_hemispheres(browser),    # list of hemisphere image URLs and titles
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
    news_soup = soup(browser.html, 'html.parser')
    
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
    img_soup = soup(browser.html, 'html.parser')
    
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

# ## Mars hemisphere images and information
def mars_hemispheres(browser):
    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemispheres_soup = soup(browser.html, 'html.parser')
    
    # Get code blocks containing links to pages with individual hemisphere information
    item_links = (
        hemispheres_soup
        .find('div', class_='collapsible results')
        .find_all('div', class_="description")
    )
    
    # Extract list of URLs from the links
    img_page_urls = [urljoin(url, link.a["href"]) for link in item_links]
    
    # Create list to hold hemisphere images and titles.
    hemisphere_list = []
    
    # Retrieve image URLs and titles for each hemisphere.
    for page in img_page_urls:
        browser.visit(page)
        # browser.is_text_present('Sample', wait_time=2)  # Optional delay for loading the page
        page_soup = soup(browser.html, 'html.parser')
        hemisphere_list.append({
            'img_url':urljoin(page, page_soup.find('a', text='Sample')['href']),
            'title':page_soup.find('h2', class_='title').text
        })
    
    return hemisphere_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
