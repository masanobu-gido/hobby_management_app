import pandas as pd
import psycopg2 as pg
import os

def hobby_score(user_id):
    #connection = pg.connect("host='localhost' port=5432 dbname=hobbysql user=postgres password='mg-94371210'")
    #connection = pg.connect("host='ec2-3-222-204-187.compute-1.amazonaws.com' port=5432 dbname=davqklevog6vet user=gpwjeheomhdmfu password='afe549ec72373ac34258388ca47b4e8a18281263998b9f773860a7c8b522e2fb'", sslmode='require')
    DATABASE_URL = 'postgres://gpwjeheomhdmfu:afe549ec72373ac34258388ca47b4e8a18281263998b9f773860a7c8b522e2fb@ec2-3-222-204-187.compute-1.amazonaws.com:5432/davqklevog6vet'
    connection = pg.connect(DATABASE_URL)
    df = pd.read_sql_query('SELECT * FROM hobbes;', connection)
    df.loc[:, 'time*feeling'] = df.loc[:, 'time'] * df.loc[:, 'feeling']
    user_df = df[df["user_id"] == user_id]
    #print(user_df.head())
    #print(user_df.head())
    #print(user_df["hobby"].unique())
    hobbies = user_df["hobby"].unique()
    score_dict = {}
    for hobby in hobbies:
        score = user_df[user_df["hobby"] == hobby]['time*feeling'].sum()
        score_dict[hobby] = score
        
    if any(score_dict):
        max_score = max(score_dict.values())
    else:
        max_score = 100
        
    connection.close()
    
    return score_dict, max_score

def hobby(user_id):
    connection = pg.connect("host='localhost' port=5432 dbname=hobbysql user=postgres password='mg-94371210'")
    df = pd.read_sql_query('SELECT * FROM hobbes;', connection)
    user_df = df[df["user_id"] == user_id]
    hobbies = user_df["hobby"].unique()
    connection.close()
    
    return hobbies

if __name__ == '__main__':
    hobby_score(2)