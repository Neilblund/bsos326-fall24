from requests import get
import numpy as np 
import pandas as pd 

def get_nyt_archive(month, year, key):
    '''
    Arguments:
        month: Number of the month for which we want the NYT archive. 
            For example, 1 for January, 2 for February, etc.
        year: year for which we want NYT archive
        key: API key
        
    Returns:
        List of dictionaries representing the articles for that month.
    '''
    
    base_url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json"
    r = get(base_url, params= {'api-key':key})  
    
    if r.status_code != 200:
        print('Failed with status code:', r.status_code)
    else:
        return r.json()['response']['docs']
    

def get_nyt_abstracts(month, year, key):
    '''
    Arguments:
        month: Number of the month for which we want the NYT archive. 
            For example, 1 for January, 2 for February, etc.
        year: year for which we want NYT archive
        key: API key
        
    Returns:
        DataFrame of article abstracts for that month. Includes fields for date and type of article
    '''
    
    keys = ['abstract', 'web_url', 'type_of_material','pub_date']
    articles = get_nyt_archive(month, year, key)
    nyt_dict = {key:[article[key] for article in articles] for key in keys}
    return pd.DataFrame(nyt_dict)