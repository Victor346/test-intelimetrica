import psycopg2
import os
import csv

connection_url = os.environ['DATABASE_URL']
print('Connection URI:' + connection_url)
con = psycopg2.connect(connection_url)

cur = con.cursor()

sql_query = '''SELECT * FROM Restaurants WHERE id=\'edb50561-46f9-4541-9c04-8de82401cc13\''''
print(sql_query)
cur.execute(sql_query)

rows = cur.fetchall()

for row in rows:
    print("COSA =", row[2])

"""
'''CREATE TABLE STUDENT
              (ADMISSION INT PRIMARY KEY     NOT NULL,
              NAME           TEXT    NOT NULL,
              AGE            INT     NOT NULL,
              COURSE        CHAR(50),
              DEPARTMENT        CHAR(50));'''
"""

con.commit()
con.close()
