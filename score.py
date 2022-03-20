import sys
from datetime import datetime, timedelta
import pytz
import pandas as pd
import sqlite3

def hobby_score(user_id):
    date_now = datetime.now(pytz.timezone('Asia/Tokyo'))
    file_sqlite3 = "./hobby.db"
    connection = sqlite3.connect(file_sqlite3)
    df = pd.read_sql_query('SELECT * FROM hobbes', connection)
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
    max_score = max(score_dict.values())
    connection.close()
    
    return score_dict, max_score

def hobby(user_id):
    file_sqlite3 = "./hobby.db"
    connection = sqlite3.connect(file_sqlite3)
    df = pd.read_sql_query('SELECT * FROM hobbes', connection)
    user_df = df[df["user_id"] == user_id]
    hobbies = user_df["hobby"].unique()
    connection.close()
    
    return hobbies
    

if __name__ == '__main__':
    hobby_score(2)