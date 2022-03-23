from sqlite3 import DatabaseError
import pandas as pd
import psycopg2 as pg
import os
import sqlalchemy

def hobby_score(user_id):

    #connection = pg.connect("host='localhost' port=5432 dbname=hobbysql user=postgres password='mg-94371210'")
    #connection = pg.connect("host=ec2-174-129-243-38.compute-1.amazonaws.com dbname=d2g6vau23oegqv user=lkmpgyrwoildlh port=5432 password=20528f08836974c86b49632c641133e72432643b3b92193a18b0143787632739")
    DATABASE_URL = "postgres://lkmpgyrwoildlh:20528f08836974c86b49632c641133e72432643b3b92193a18b0143787632739@ec2-174-129-243-38.compute-1.amazonaws.com:5432/d2g6vau23oegqv"
    #DATABASE_URL = 'postgres://gpwjeheomhdmfu:afe549ec72373ac34258388ca47b4e8a18281263998b9f773860a7c8b522e2fb@ec2-3-222-204-187.compute-1.amazonaws.com:5432/davqklevog6vet'
    #DATABASE_URL = os.environ.get('DATABASE_URL')
    #print(DATABASE_URL)
    connection = pg.connect(DATABASE_URL, sslmode='require')
    #engine = sqlalchemy.create_engine(DATABASE_URL).raw_connection()
    try:
        
        #df = pd.read_sql("SELECT * FROM hobbes;", engine)
        df = pd.read_sql_table("SELECT * FROM hobbies;", connection) 
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
    
    except pd.io.sql.DatabaseError:
        print('pd.io.sql.DatabaseError!!!')
        connection.close()
        return {}, 100

def hobby(user_id):
    #connection = pg.connect("host='ec2-3-222-204-187.compute-1.amazonaws.com' port=5432 dbname=davqklevog6vet user=gpwjeheomhdmfu password='afe549ec72373ac34258388ca47b4e8a18281263998b9f773860a7c8b522e2fb'", sslmode='require')
    #connection = pg.connect("host='localhost' port=5432 dbname=hobbysql user=postgres password='mg-94371210'")
    DATABASE_URL = "postgres://lkmpgyrwoildlh:20528f08836974c86b49632c641133e72432643b3b92193a18b0143787632739@ec2-174-129-243-38.compute-1.amazonaws.com:5432/d2g6vau23oegqv"
    connection = pg.connect(DATABASE_URL, sslmode='require')
    try:
        df = pd.read_sql("SELECT * FROM hobbies;", connection)
        user_df = df[df["user_id"] == user_id]
        hobbies = user_df["hobby"].unique()
        connection.close()
        
        return hobbies
    
    except pd.io.sql.DatabaseError:
        connection.close()
        return []

if __name__ == '__main__':
    hobby_score(2)