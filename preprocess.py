from ethnicolr import pred_wiki_ln
import pandas as pd
from genderize import Genderize

# Example of loading data
path = "./iclr2019_papers.csv"
df = pd.read_csv(path)

# authors -> first author
df['first_author'] = df['authors'].str.split(',').str[0]
df['second_author'] = df['authors'].str.split(',').str[1]

df_pp_1 = df[['paper_id', 'first_author', 'decision']]
df_pp_2 = df[['paper_id', 'second_author', 'decision']]

# split first/last name
df_pp_1.loc[:,'first_name'] = df_pp_1['first_author'].str.split().str[0]
df_pp_1['last_name'] = df_pp_1['first_author'].str.split().str[1]

df_pp_2.loc[:,'first_name'] = df_pp_2['second_author'].str.split().str[0]
df_pp_2['last_name'] = df_pp_2['second_author'].str.split().str[1]

frames = [df_pp_1, df_pp_2]
df_pp = pd.concat(frames, ignore_index=True)
df_pp.drop('first_author', inplace=True, axis=1)
df_pp.drop('second_author', inplace=True, axis=1)

df = df_pp[['paper_id','first_name', 'last_name', 'decision']]

# last name column -> race
df = pred_wiki_ln(df, 'last_name')
df['race'] = df['race'].apply(lambda x : str(x).split(',')[-1])


# first name column -> first name list -> genderize -> gender list -> gender column
first_name_list = list(df['first_name'])

genders = Genderize(
    user_agent='GenderizeDocs/0.0',
    api_key='83a79cbb58ff2af93ced58f65482f6c9',
    timeout=5.0
).get(first_name_list)


gender_df = pd.DataFrame(genders)
df['gender'] = gender_df['gender']


# save to csv
df['decision'] = df['decision'].apply(lambda x : str(x).split(' ')[0])
df = df[['paper_id', 'gender', 'race', 'decision']]
df.to_csv('iclr2019_papers_preprocessed.csv', index=False)