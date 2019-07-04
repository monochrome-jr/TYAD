from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime
from itertools import chain
import pandas as pd
import numpy as np
import urllib.parse
import requests
import re
import os

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)


# these functions are modified from "https://github.com/WillKoehrsen/Data-Analysis/tree/master/medium"

# fname will be the name of downloaded html file (ex: Medium.html)
def get_table_rows(fname):
    
    #convert html file to soup object
    soup = BeautifulSoup(open(fname, 'r', encoding='utf8'), features='lxml')
    
    # find entry (article) in soup object
    table_rows = soup.find_all(attrs={'class': 'sortableTable-row js-statsTableRow'})
    
    # feedback of entry (article) amount
    print(f'Found {len(table_rows)} articles from {fname}.')
    
    return table_rows


# used in function 'process_entry'
def convert_timestamp(ts: int, tz: str):
    return pd.to_datetime(ts, origin='unix', unit='ms').tz_localize('UTC').tz_convert(tz).tz_localize(None)

# process data for each entry (article)
def process_entry(entry, tz='Asia/Taipei'):

    # convert row string to soup object
    entry = BeautifulSoup(entry, features='lxml').body.tr
    
    # create dictionary for data storing
    entry_dict = {}
    
    # extract data ('published_date', 'views', 'reads', 'ratio', 'fans')
    for value, key in zip(entry.find_all(attrs={'class': 'sortableTable-value'}),['published_date', 'views', 'reads', 'ratio', 'fans']):
        entry_dict[key] = float(value.text) if key == 'ratio' else int(value.text)
    
    # extract data ('read_time')
    entry_dict['read_time'] = int(entry.find_all(attrs={'class': 'readingTime'})[0].get('title').split(' ')[0])
    
    # extract data ('publication')
    publication = entry.find_all(attrs={'class': 'sortableTable-text'})
    if 'In' in publication[0].text:
        entry_dict['publication'] = publication[0].text.split('In ')[1].split('View')[0]
    else:
        entry_dict['publication'] = 'None'

    # extract data ('published_date')
    entry_dict['published_date'] = convert_timestamp(entry_dict['published_date'], tz=tz)
    
    # extract data ('started_date')
    entry_dict['started_date'] = convert_timestamp(entry.get('data-timestamp'), tz=tz)
    
    # extract data ('link')
    link = entry.find_all(text='View story', attrs={'class': 'sortableTable-link'})[0].get('href')
    entry_dict['link'] = urllib.parse.unquote_plus(link)
    
    # request html content through entry (article) link
    entry = requests.get(link).content
    entry_soup = BeautifulSoup(entry, features='lxml')
    
    # extract data ('title')
    entry_dict['title'] = entry_soup.h1.text

    # extract data ('text')
    entry_text = [p.text for p in entry_soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'blockquote', 'pre'])]
    entry_text = ' '.join(entry_text)
    entry_dict['text'] = entry_text
    
    # extract data ('claps')
    clap_pattern = re.compile('^[0-9]{1,} claps|^[0-9]{1,}.[0-9]{1,}K claps|^[0-9]{1,}K claps')
    claps = entry_soup.find_all(text=clap_pattern)
    if len(claps) > 0:
        if 'K' in claps[0]:
            clap_number = int(1e3 * float(claps[0].split('K')[0]))
        else:
            clap_number = int(claps[0].split(' ')[0])
    else:
        clap_number = 0
    entry_dict['claps'] = clap_number

    # extract data ('tags')
    tags = entry_soup.find_all('a', href = re.compile('/tag/'))
    tags = [a.text for a in tags]
    entry_dict['tags'] = tags

    # extract data ('days_since_publication')
    entry_dict['days_since_publication'] = int((datetime.now() - entry_dict['published_date']).total_seconds() / (3600 * 24))

    # feedback for finished entry (article)
    print("✓ " + entry_dict['title'])
    return entry_dict


# combine all data to dataframe
def construct_dataframe(table_rows):
    
    # processing for all entries (articles)
    results = []
    for rows_str in table_rows:
        results.append(process_entry(str(rows_str)))

    # convert to dataframe
    df = pd.DataFrame(results)
    
    # add additional information ('editing_days')
    df['editing_days'] = ((df['published_date'] - df['started_date']).dt.total_seconds() / (60 * 60 * 24)).astype(int)

    # do rounding
    df['published_date'] = df['published_date'].dt.round('min')
    df['started_date'] = df['started_date'].dt.round('min')
    df['ratio'] = df['ratio'].round(2)

    # get most common tags (change n to include more)
    n = 3
    all_tags = list(chain(*df['tags'].tolist()))
    tag_counts = Counter(all_tags)
    tags = tag_counts.most_common(n)

    # add indication column for tag
    for tag, count in tags:
        flag = [1 if tag in tags else 0 for tags in df['tags']]
        df.loc[:, f'<tag>{tag}'] = flag

    # sorted by published_date
    df.sort_values('published_date', inplace=True)
    
    return df


# parsing downloaded html file
os.chdir("C:/Users/user/Downloads")
table_rows = get_table_rows(fname="Medium.html")

# processing
output = construct_dataframe(table_rows)

# rename columns for better understanding
output.rename(columns={'claps': '拍手數',
                       'days_since_publication': '已發佈天數',
                       'fans': '增加的粉絲數',
                       'link': '文章連結',
                       'publication': '發佈平台',
                       'published_date': '發佈日期',
                       'ratio': '閱畢比例',
                       'read_time': '閱讀文章所需時間',
                       'reads': '閱畢人數',
                       'started_date': '起始編輯日期',
                       'tags': '標籤',
                       'text': '文章內容',
                       'title': '文章標題',
                       'views': '瀏覽人數',
                       'editing_days': '編輯天數'}, inplace=True)


# directory for storing
os.chdir("C:/Users/user/Desktop/Coding/TYAD/Medium/data")

# give each file a timestamp
time_string = datetime.now().strftime("%Y%m%d_%H%M")

# give each file a format version number
format_version = 1

# save it! (thanks god)
output.to_excel(time_string + "_fv" + str(format_version) + ".xlsx")
