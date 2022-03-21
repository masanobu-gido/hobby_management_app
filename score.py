import pandas as pd
import psycopg2 as pg

def hobby_score(user_id):
    connection = pg.connect("host='localhost' port=5432 dbname=hobbysql user=postgres password='mg-94371210'")
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