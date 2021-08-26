twitter_data_pipeline.py

- This file acesses the twitter endpoint
- Does data processing to clean up the data and add a date
- Stores it all into free cloud postgreSQL table from Heroku
- Filters the data to Canada only and stores in a different postgreSQL table
- Creates tables when they dont exsist
- Checks to see if database already has todays data to prevent duplicate data


visualization_from_database.ipynb

- This file performs a query on the postgreSQL database
- Displays the returned data in a table
- Displays a graph of todays data grouped by country

automation_guide.md

- This file describes basic steps to set up script automation using local machine or cloud
