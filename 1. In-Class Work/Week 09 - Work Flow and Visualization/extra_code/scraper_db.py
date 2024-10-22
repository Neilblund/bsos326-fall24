# import any packages you need
from bs4 import BeautifulSoup
from requests import get
import time
import pandas as pd
import sqlite3


###########################################################
# Step 1: loop through the main page and extract all links
###########################################################
# i'm using a set here so we can avoid adding any duplicate links
links = set() 
# some sites may not return a result if you don't specify a user agent of some kind. # 
# We can add this as a "header" parameter:
headers = {'User-Agent': 'Webscraper'}

print("checking links")
page = 1
morepages = True
while morepages == True:
    url = f'https://www.rev.com/blog/transcript-category/2024-election/page/{page}'
    response = get(url, headers=headers)
    # make the soup
    mainpage = BeautifulSoup(response.content, 'html.parser')
    # add links to the set
    [links.add(i.get('href')) for i in mainpage.select("div.fl-post-column a")]
    # check for the next page URL, if it doesn't exist, then 
    # the while loop ends:
    nextpage = mainpage.select('li a.next')
    if len(nextpage)>0 : 
        page += 1
    else:
        morepages = False
    # sleep for a second between each iteration
    time.sleep(1)


# convert the set to a list 
links_list = list(links)


###########################################################
# Step 2: check the data base and see if there's anything new here
###########################################################
conn = sqlite3.connect('./speeches.db')


# check if a table already exists, if it doesn't then create one
cur = conn.cursor()
print("checking for table")
try: 
    cur.execute('SELECT * from transcripts limit 1')
    print("table exists")
except sqlite3.OperationalError:
    print("No such table: creating")
    cur.execute('''
                CREATE TABLE transcripts(
                link text,
                headline text,
                fulltext text)''')


scraped_links = pd.read_sql('SELECT link FROM transcripts', conn)


########################################################################
# Step 3: if any new links are detected, scrape the full text
########################################################################

# get a list of links in the current set that are not in the data base: 
links_to_scrape = pd.Index(links_list).difference(scraped_links.link).values
print(f'scraping {len(links_to_scrape)} new speeches')

# iterate through links
pages = []

for i in links_to_scrape:
    # go to link i
    response = get(i, headers= headers)
    pages.append(response)
    print(i)

        # write the results as a new row
    
        # wait 1 second between each iteration
    time.sleep(1)

def parse_page(response):
    page = BeautifulSoup(response.content, 'html.parser')
        # get all of the text, and concatenate paragraphs
    result = {
   'fulltext': '\n'.join([i.get_text() for i in page.select('#transcription p')]),
   'headline': page.select_one('.fl-heading-text').get_text(),
   'link': response.url}
    return result


df= pd.DataFrame([parse_page(i) for i in pages])
df.to_sql(name='transcripts', con=conn, if_exists = 'append', index=False)

print(f'{df.shape[0]} new rows appended to data base')
conn.close()


# To execute from a notebook, run: 
# %run ./scraper_db.py

# To read the results to a data frame, run: 
# import sqlite3
# import pandas as pd
# conn = sqlite3.connect('./speeches.db')
# transcripts = pd.read_sql('SELECT * FROM transcripts', conn)
# conn.close()
