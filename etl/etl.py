#%%
import requests 
import os
import sqlite3
import sqlalchemy
import pandas as pd
# %%
github_url =  'https://api.github.com/repos/olist/work-at-olist-data/contents/datasets'
# %%
local_dir = '../data'
# %%
def dowloader_files_GitHub(url,path):
    response = requests.get(github_url)
    data = response.json()
    if not os.path.exists(local_dir):
        os.mkdir('../data')
    for file_info in data:
        if file_info['name'].endswith('.csv'):
            file_url = file_info['download_url']
            file_name = os.path.join(local_dir,file_info['name'])

            file_response = requests.get(file_url)

        with open(file_name,'wb') as file: 
            file.write(file_response.content)
        print(file_info['name'], ' baixado com sucesso!')
# %%
dowloader_files_GitHub(github_url,local_dir)

# %%
def insert_data(db_name,files_path):
    connection = sqlite3.connect(os.path.join(local_dir,db_name))
    str_connection = f'sqlite:///{os.path.join(files_path, db_name)}'
    conn = sqlalchemy.create_engine(str_connection)
    files_names = [file for file in os.listdir(files_path) if file.endswith('csv')]
    for file in files_names: 
        table_name = file.replace('olist','tb').replace('_dataset.csv','')
        file_dir = os.path.join(local_dir, file) 
        df = pd.read_csv(file_dir) 
        df.to_sql(table_name,conn,if_exists='replace')
        print(file, ' inserido com sucesso no ', db_name)
    conn.dispose()
    
    

# %%
insert_data('olist.db',local_dir)
# %%
