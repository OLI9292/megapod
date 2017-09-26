import csv
import glob
import sys
import pandas as pd
from urlparse import urlparse

# READ URLS FROM CSV

df = pd.DataFrame()

ALL = pd.read_csv('domains/ALL.csv')

directory = 'backlinks/' + sys.argv[1] + '/*'

for f in glob.glob(directory):
  print 'OK: ' + f
  df_ = pd.read_csv(f, error_bad_lines=False, warn_bad_lines=False, quoting=csv.QUOTE_NONE)
  df = df.append(df_)

def tryconvert(url):
  try:
    clean = urlparse(url)
    clean = clean.hostname
    return clean
  except:
    return None

df = df[['"Domain Rating"', '"Referring Page URL"', '"Link URL"']]
df = df.rename(columns = {
  '"Domain Rating"': 'domain_rating', 
  '"Referring Page URL"': 'referring_page', 
  '"Link URL"': 'link_url'})
df['domain'] = ''
df.domain = df.referring_page.apply(lambda x: tryconvert(x))
df = df.drop_duplicates(subset='domain')
df = df.loc[~df.domain.isin(ALL.domain)]
print("\n* * * DONE * * *\n")
print("csv length: " + str(len(df)))

ALL = pd.concat([ALL, df])

ALL.to_csv('domains/ALL.csv', index=False)

df.to_csv('domains/without_emails/' + sys.argv[1] + '.csv', index=False)
