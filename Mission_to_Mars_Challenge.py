#!/usr/bin/env python
# coding: utf-8

# # 10.3.3 Scrape Mars Data: The News

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}


# In[3]:


browser = Browser(
    'chrome',
    **executable_path,
    headless=False,
    incognito=True
)


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# The line `browser.is_element_present_by_css('div.list_text', wait_time=1)` searches for elements with a specific combination of tag (`div`) and attribute (`list_text`).
# 
# For example: `ul.item_list` would be found in HTML as `<ul class="item_list">`.

# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')


# In[6]:


slide_elem = news_soup.select_one('div.list_text')


# The "parent element" `slide_elem` looks for the `<div />` tag and its descendents (other tags within the `<div />` element). We'll reference it when we want to filter search results even further. The `.` is used for selecting classes, such as `list_text`, so the code `'div.list_text'` pinpoints the `<div />` tag with the class of `list_text`.
# 
# CSS works from right to left, and returns the last item on the list instead of the first. Because of this, when using `select_one`, the first matching element returned will be a `<li />` element with a class of `slide` and all nested elements within it

# In[7]:


slide_elem.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

news_p


# # 10.3.4 Scrape Mars Data: Featured Image

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]  # There are three buttons on the page, and the one we want is
                                                    # the 1st (starting from 0)
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

img_url_rel


# In[14]:


# Use the base URL to create an absolute URL
img_url = f'{url}/{img_url_rel}'

img_url


# # 10.3.5 Scrape Mars Data: Mars Facts

# In[15]:


pd.read_html('https://galaxyfacts-mars.com')


# In[16]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]    # The scrape returns two tables; use the 0th one.
df.columns=['description', 'Mars', 'Earth']             # The columns are unnamed; name them.
df.set_index('description', inplace=True)
df


# In[17]:


print(df.to_html())


# In[18]:


browser.quit()


# # Challenge

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

from urllib.parse import urljoin    # https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse


# In[2]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser(
    'chrome',
    **executable_path,
    headless=False,
    incognito=True  # To prevent visits from going into history
)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base url to create an absolute url
img_url = f'{url}/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


print(df.to_html())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

hemispheres_soup = soup(browser.html, 'html.parser')

print(hemispheres_soup.prettify())
# In[17]:


item_links = (
    hemispheres_soup
    .find('div', class_='collapsible results')
    .find_all('div', class_="description")
)

item_links

# syntax test 
display(
    item_links[0].a,
    item_links[0].a["href"],
    item_links[0].a.h3.text
)
# In[18]:


img_page_urls = [url + link.a["href"] for link in item_links]

img_page_urls

# syntax test
browser.visit(img_page_urls[0])

page_soup = soup(browser.html, 'html.parser')

print(page_soup.prettify())
print(page_soup.find('a', text='Sample')['href'])
print(page_soup.find('h2', class_='title').text)
# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for page in img_page_urls:
    browser.visit(page)
#     browser.is_text_present('Sample', wait_time=2)  # Optional delay for loading the page
    page_soup = soup(browser.html, 'html.parser')
    hemisphere_image_urls.append({
        'img_url':urljoin(page, page_soup.find('a', text='Sample')['href']),
        'title':page_soup.find('h2', class_='title').text
    })


# In[20]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[21]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




