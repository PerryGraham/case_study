import psycopg2
import requests
import datetime
import pandas as pd
from secret import bearer_token
from sqlalchemy import create_engine, inspect

headers = {'Authorization': 'Bearer {}'.format(
    bearer_token())}  # Used for authentication, imports token from local file

endpoint = "https://api.twitter.com/1.1/trends/available.json"

# Get request that returns the raw data
raw_data = requests.get(endpoint, headers=headers).json()

dataframe = pd.DataFrame(raw_data)

# Decided to unwind placeType column into 2 seperate columns and then drop the old one.
dataframe["placeType_code"] = dataframe["placeType"].apply(lambda x: x["code"])
dataframe["placeType_name"] = dataframe["placeType"].apply(lambda x: x["name"])
dataframe = dataframe.drop(columns=["placeType"])

# Adding a datetime to each row to know when it was added
day_today = datetime.datetime.today().strftime("%d-%m-%Y")
dataframe["date"] = day_today

# Getting only data from Canada for different table
canada_data = dataframe[dataframe["country"] == "Canada"]

# Connecting to cloud postgresql database
engine = create_engine(
    "postgresql://dwedsgyktzzhsf:98e9d76a13ce7cef3bba5bc1ad08c65a37b83afca5f1cfbccb562b136779a19c@ec2-18-214-238-28.compute-1.amazonaws.com:5432/d7nvap8mgbgtm6")
engine.connect()

# stores current table names from database for later
insp = inspect(engine)
tables_in_database = insp.get_table_names()

with engine.begin() as connection:
    # All country table
    if "twitter_trending_locations" in tables_in_database:
        # Query to check if script has already save todays data, prevent duplicates
        query = "SELECT * FROM twitter_trending_locations WHERE date = '{}' LIMIT 1".format(
            day_today)
        dup_check = pd.read_sql(query, con=connection)
        if len(dup_check) > 0:  # Dont insert into database if data from today already exsist
            print(
                "{} data already exists in twitter_trending_locations".format(day_today))
        else:  # If it doesn't exsist, insert it
            dataframe.to_sql("twitter_trending_locations",
                             con=connection, if_exists='append')
            print("Data saved for twitter_trending_locations on {}".format(day_today))

    else:  # Catches case when the table has not been created yet
        dataframe.to_sql("twitter_trending_locations",
                         con=connection, if_exists='append')
        print("Data saved for twitter_trending_locations on {}".format(day_today))

    # Canada only table
    if "twitter_trending_locations_canada" in tables_in_database:
        # Query to check if script has already save todays data, prevent duplicates
        query = "SELECT * FROM twitter_trending_locations_canada WHERE date = '{}' LIMIT 1".format(
            day_today)
        dup_check = pd.read_sql(query, con=connection)
        if len(dup_check) > 0:  # Dont insert into database if data from today already exsist
            print("{} data already exists in twitter_trending_locations_canada".format(
                day_today))
        else:  # If it doesn't exsist, insert it
            canada_data.to_sql("twitter_trending_locations_canada",
                               con=connection, if_exists='append')
            print(
                "Data saved for twitter_trending_locations_canada on {}".format(day_today))
    else:  # Catches case when the table has not been created yet
        canada_data.to_sql("twitter_trending_locations_canada",
                           con=connection, if_exists='append')
        print("Data saved for twitter_trending_locations_canada on {}".format(day_today))
