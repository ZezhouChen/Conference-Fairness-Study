from ethnicolr import pred_wiki_ln
import pandas as pd
from genderize import Genderize

# Example of loading data
path = "./iclr2017_papers.csv"
df = pd.read_csv(path)

# authors -> first author
df['first_author'] = df['authors'].str.split(',').str[0]

# split first/last name
df.loc[:,'first_name'] = df.loc[:,'first_author'].str.split().str[0]
df.loc[:,'last_name'] = df.loc[:,'first_author'].str.split().str[1]
df = df[['paper_id', 'first_author' ,'first_name', 'last_name', 'decision']]

# first name column -> first name list -> genderize -> gender list -> gender column
first_name_list = list(df['first_name'])

genders = Genderize(
    user_agent='GenderizeDocs/0.0',
    api_key='c2a7acf70ef5f74435f0bcf4d075a5e4',
    timeout=5.0
).get(first_name_list)


gender_df = pd.DataFrame(genders)
df['gender'] = gender_df['gender']

print(df)

# last name column -> race
df = pred_wiki_ln(df, 'last_name')
df['race'] = df['race'].apply(lambda x : str(x).split(',')[-1])

# save to csv
df['decision'] = df['decision'].apply(lambda x : str(x).split(' ')[0])
df = df[['paper_id', 'gender', 'race', 'decision']]
df.to_csv('iclr2017_papers_preprocessed.csv', index=False)