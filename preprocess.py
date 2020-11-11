from ethnicolr import pred_census_ln, pred_wiki_ln
import pandas as pd
from genderize import Genderize

# Example of loading data
path = "./iclr2017_papers.csv"
df = pd.read_csv(path)
print(df[['authors', 'decision']])


# Example of predicting race
names = [{'name': 'chen'},
         {'name': 'zhang'},
         {'name': 'shinde'},
         {'name': 'mehta'},
         {'name': 'aldakheel'},
         {'name': 'fanti'}]
df = pd.DataFrame(names)
print(pred_wiki_ln(df, 'name'))


# Example of predicting gender
names = ['Zezhou', 'Zitong', 'Mehul', 'Yash', 'Ali', 'Giulia']
print(Genderize().get(names))


# authors -> first author


# split first/last name

# first name column -> first name list -> genderize -> gender list -> gender column

# last name column -> race
df = pred_wiki_ln(df, 'last_name')
df['race'] = df['race'].apply(lambda x : x.split(',')[-1])

# save to csv
df['decision'] = df['decision'].apply(lambda x : x.split(' ')[0])
df[['gender', 'race', 'decision']].to_csv()