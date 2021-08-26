#### twitter_data_pipeline.py

- Note: script will not run without adding a bearer token for access to the twitter api.
- This file accesses the twitter endpoint
- Does data processing to clean up the data and add a date
- Stores it all into free cloud postgreSQL table from Heroku
- Filters the data to Canada only and stores in a different postgreSQL table
- Creates tables when they don't exist
- Checks to see if database already has today's data to prevent duplicate data


<img src="https://i.ibb.co/kqv9zgN/image.png" width="800"/>


----------------------------------

#### visualization_from_database.ipynb

- This file performs a query on the postgreSQL database
- Displays the returned data in a table
- Displays a graph of today's data grouped by country

![graph](https://i.ibb.co/ZBcDm0B/graph.png)

----------------------------
#### automation_guide.md

- This file describes basic steps to set up script automation using local machine or cloud
