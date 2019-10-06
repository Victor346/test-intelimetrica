# Script used to upload the restaurant information into the database from the .csv file in the root directory
import psycopg2
import os
import csv

# Get the connection URI from the environment variable
connection_url = os.environ['DATABASE_URL']

# Establish connection with the database
con = psycopg2.connect(connection_url)

cur = con.cursor()

sql_create_table = '''CREATE TABLE Restaurants(
    id TEXT PRIMARY KEY,
    rating INTEGER,
    name TEXT,
    site TEXT,
    email TEXT,
    phone TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    lat FLOAT,
    lng FLOAT);
    
    ALTER TABLE Restaurants ADD CONSTRAINT valid_rating CHECK(
    rating >= 0
    AND rating <= 4);'''

cur.execute(sql_create_table)

with open('../restaurantes.csv', encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # ignore the headers row
        if line_count == 0:
            line_count += 1
        else:
            # Create the insert query for each row in the csv
            sql_query = '''INSERT INTO Restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng) 
            VALUES (\'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\', 
            \'{}\', \'{}\', \'{}\', {}, {});'''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                       row[8], row[9], row[10])
            print(sql_query)
            # Encode the string query in order to ensure proper data storage
            sql_query.encode(encoding='UTF-8', errors='strict')
            # execute the query
            cur.execute(sql_query)
            line_count += 1
# Commit database changes
con.commit()
# Close connection with the satabase
con.close()
