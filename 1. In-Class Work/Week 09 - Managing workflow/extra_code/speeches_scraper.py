#####################################################################################
# This script compiles the full text of a bunch of presidential speech transcripts 
# There's about 200 pages to iterate through here, and I've put a pause of 1 second
# between each get request, so this takes a little over 3 minutes to run. Once we have
# all the speeches, there's probably no reason to run this again, so ideally I would 
# run this once and then store the results in a csv file. 
# 

# import any packages you need
from bs4 import BeautifulSoup
from requests import get
import time
import csv
import pandas as pd


def parse_page(response):
    page = BeautifulSoup(response.content, 'html.parser')
        # get all of the text, and concatenate paragraphs
    result = {
   'fulltext': '\n'.join([i.get_text() for i in page.select('#transcription p')]),
   'headline': page.select_one('.fl-heading-text').get_text(),
   'link': response.url}
    return result


###########################################################
# Step 1: loop through the main page and extract all links
###########################################################
# i'm using a set here so we can avoid adding any duplicate links
links = set() 
# some sites may not return a result if you don't specify a user agent of some kind. # 
# We can add this as a "header" parameter:
headers = {'User-Agent': 'Webscraper'}


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



#################################################################
# Step 2: iterate through the links and extract the response object
##################################################################


pages = []
# create a speeches csv
for i in links_list:
    # go to link i
    response = get(i, headers= headers)
    page.append(response)


#################################################################
# Step 3: format as data frame and write to file
##################################################################


df= pd.DataFrame([parse_page(i) for i in pages])
df.to_csv('speeches.csv', index=False)





