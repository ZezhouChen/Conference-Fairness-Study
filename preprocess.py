# from ethnicolr import pred_census_ln, pred_wiki_ln
import pandas as pd
from genderize import Genderize

# Example of loading data
path = "./iclr2017_papers.csv"
df = pd.read_csv(path)
# print(df[['authors', 'decision']])


# Example of predicting race
# names = [{'name': 'chen'},
#          {'name': 'zhang'},
#          {'name': 'shinde'},
#          {'name': 'mehta'},
#          {'name': 'aldakheel'},
#          {'name': 'fanti'}]
# df = pd.DataFrame(names)
# print(pred_wiki_ln(df, 'name'))


# Example of predicting gender
# names = ['Zezhou', 'Zitong', 'Mehul', 'Yash', 'Ali', 'Giulia']
# print(Genderize().get(names))


# authors -> first author
df['first_author'] = df['authors'].str.split(',').str[0]

# split first/last name

df.loc[:,'first_name'] = df.loc[:,'first_author'].str.split().str[0]
df.loc[:,'last_name'] = df.loc[:,'first_author'].str.split().str[1]
df = df[['paper_id', 'first_author' ,'first_name', 'last_name']]

# first name column -> first name list -> genderize -> gender list -> gender column

first_name_list = list(df['first_name'])

genders = Genderize().get(first_name_list)

gender_df = pd.DataFrame(genders)
df['gender'] = gender_df['gender']

print(df)

# last name column -> race

# clear some uncessary columns

# save to csv