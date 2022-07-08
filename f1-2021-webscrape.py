# -*- coding: utf-8 -*-
"""F1 Web Scraping

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MDSWXjjJigyBX8EHwk9iVomkUV6owGUy
"""

# import libaries
import pandas as pd
import urllib
from bs4 import BeautifulSoup
from google.colab import files

# takes one parameter of type string
# returns urls with race results data for each race in [input] year
def get_result_urls(year):
  # create list to store urls
  result_urls = []

  # scrape urls on the general page for the input year
  source = urllib.request.urlopen(f"https://www.formula1.com/en/results.html/{year}/"
                                    f"races.html").read()
  soup = BeautifulSoup(source,'lxml')
    
  for url in soup.find_all('a'):
    # check if the urls has the specified year, has race results data, and is unique; if so, add to result_urls
    if year in str(url.get('href')) and 'race-result' in str(url.get('href')) and url.get('href') not in result_urls:
      result_urls.append(url.get('href'))
  
  return result_urls

# takes two parameters of type string
# returns urls with [input] data for each race in [input] year
def get_urls(year,data):

  # if input data is race-results, call the get_result_urls() function
  if data == 'race-results':
    return get_result_urls(year)
  
  urls_list = []

  for url in get_result_urls(year):
    source = urllib.request.urlopen(f'https://www.formula1.com/{url}')
    soup = BeautifulSoup(source,'lxml')

    for url in soup.find_all('a'):
      if year in str(url.get('href')) and data in str(url.get('href')) and url.get('href') not in urls_list:
        urls_list.append(url.get('href'))
  
  # if input data is fastest-laps, remove the first url from list, which is '/en/results.html/2021/fastest-laps.html'
  if data == 'fastest-laps':
    urls_list.pop(0)

  return urls_list

# takes two parameters of type string
# returns dataframe for input data and input year
def season_df(year, data):
  race_urls = get_urls(year,data)
  season_df = pd.DataFrame()

  for url in race_urls:
    # load in website to scrape data from
    source = urllib.request.urlopen(f'https://www.formula1.com/{url}').read()
    
    # find table and race metadata
    soup = BeautifulSoup(source,'lxml')
    table = soup.find_all('table')[0]
    race_name = url.split('/')[6]
    race_year = url.split('/')[3]
    race_num = url.split('/')[5]
    
    # read into dataframe
    df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
    
    # add race_name and race_year as dataframe column
    df['race_name'] = race_name
    df['race_year'] = race_year
    df['race_num'] = race_num
    
    # append df to season_results_df
    season_df = season_df.append(df)

  # drop unecessary columns based on input data
  if data == 'race-results' or data == 'sprint-results':
    season_df.drop(["Unnamed: 0","Unnamed: 8"], axis=1, inplace=True)
  elif data == 'starting-grid':
    season_df.drop(season_df.columns.difference(['Pos','Driver','Car','race_name','race_year','race_num']), axis=1, inplace=True)
  elif data == 'fastest-laps' or data=='qualifying':
    season_df.drop(["Unnamed: 0","Unnamed: 9"], axis=1, inplace=True)
  else:
    pass

  # reset index
  season_df = season_df.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')

  return season_df

"""**RETRIEVING DATAFRAMES**

"""

results2021 = season_df('2021','race-results')

starts2021 = season_df('2021','starting-grid')

sprints2021 = season_df('2021','sprint-results')

flaps2021 = season_df('2021','fastest-laps')

qualis2021 = season_df('2021','qualifying')

"""**DOWNLOADING DATA ONTO DESKTOP**"""

results2021.to_csv('results2021.csv')
starts2021.to_csv('starts2021.csv')
sprints2021.to_csv('sprints2021.csv')
flaps2021.to_csv('flaps2021.csv')
qualis2021.to_csv('qualis2021.csv')

files.download('results2021.csv')
files.download('starts2021.csv')
files.download('sprints2021.csv')
files.download('flaps2021.csv')
files.download('qualis2021.csv')