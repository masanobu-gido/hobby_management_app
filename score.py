import pandas as pd
import psycopg2 as pg
import datetime

now = datetime.datetime.now()

def hobby_score(user_id):

   
    DATABASE_URL = ""

    connection = pg.connect(DATABASE_URL, sslmode='require')

    try:
        
        #df = pd.read_sql("SELECT * FROM hobbes;", engine)
        df = pd.read_sql("SELECT * FROM hobbies;", connection) 
        df.loc[:, 'time*feeling'] = df.loc[:, 'time'] * df.loc[:, 'feeling']
        user_df = df[df["user_id"] == user_id]
        user_df = user_df[user_df["created_at"] > now - datetime.timedelta(days=7)]
        #print(user_df.head())
        log_ids = user_df["log_id"].tolist()
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
        
        return score_dict, max_score, log_ids
    
    except pd.io.sql.DatabaseError:
        print('pd.io.sql.DatabaseError!!!')
        connection.close()
        return {}, 100

def hobby(user_id):

    DATABASE_URL = ""
    #DATABASE_URL = os.environ['DATABASE_URL']
    connection = pg.connect(DATABASE_URL, sslmode='require')
    try:
        df = pd.read_sql("SELECT * FROM hobbies;", connection)
        user_df = df[df["user_id"] == user_id]
        user_df = user_df[user_df["created_at"] > now - datetime.timedelta(days=7)]
        hobbies = user_df["hobby"].unique()
        connection.close()
        
        return hobbies
    
    except pd.io.sql.DatabaseError:
        connection.close()
        return []

if __name__ == '__main__':
    hobby_score(2)