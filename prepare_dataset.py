from datasets import load_dataset
import random
import numpy as np
import pandas as pd
import os

# set random flag for reproducibility
RANDOM_SEED = 420
def set_random_seeds(seed):
    random.seed(seed)
    np.random.seed(seed)
    return seed
set_random_seeds(RANDOM_SEED)

# Get MultiHal dataset
data = load_dataset("ernlavr/multihal")

# create a dataframe from the dataset
df = pd.DataFrame(data['test'])

# group by source_dataset
grouped = df.groupby('source_dataset')

# get 10 random samples from each group
random_ids = []
for name, group in grouped:
    random_sample_df = group['id'].drop_duplicates().sample(n=10, random_state=42)
    random_ids.extend(random_sample_df)
    
# group by language
eng_df = df[df['language'] == 'eng']
rest_df = df[df['language'] != 'eng']

def get_rows_for_translation(reference, pool, lang, ids):
    
    # create a df with columns, id, ref_q, ref_a, ref_kg and trans_q, trans_a, trans_kg, lang, source_dataset
    output = pd.DataFrame(columns=['id', 'ref_q', 'ref_a', 'ref_kg', 'trans_a', 'trans_q', 'trans_kg', 'language', 'source_dataset'])
    
    # get the corresponding language and ids from pool
    pool_by_lang = pool[pool['language'] == lang]

    # get the rows by ID from pool
    reference_rows = reference[reference['id'].isin(ids)]
    pool_rows = pool_by_lang[pool_by_lang['id'].isin(ids)]
    
    # match the reference rows and pool rows by id
    for idx in ids:
        ref_row = reference_rows[reference_rows['id'] == idx].iloc[0]
        pool_row = pool_rows[pool_rows['id'] == idx].iloc[0]
        
        # create a new row
        new_row = {
            'id': idx,
            'ref_q': ref_row['input'],
            'ref_a': ref_row['output'],
            'ref_kg': ref_row['trip_labels'],
            'trans_q': pool_row['input'],
            'trans_a': pool_row['output'],
            'trans_kg': pool_row['trip_labels'],
            'language': lang,
            'source_dataset': pool_row['source_dataset']
        }
        output = pd.concat([output, pd.DataFrame([new_row])], ignore_index=True)
    return output

# for each language, get the rows with random ids
os.makedirs("tmp", exist_ok=True)
for lang, group in rest_df.groupby('language'):
    
    translation_df = get_rows_for_translation(eng_df, rest_df, lang, random_ids) 
    translation_df.to_csv(f'tmp/multihal_{lang}_sample.csv', index=False)
    