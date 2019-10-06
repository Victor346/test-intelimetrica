import psycopg2
import os
import time
from .database_pool import get_db_connection, release_db_connection


# Function used to return all the restaurants in a array of dictionaries
def get_all_restaurants(args):
    # Ask for a database connection from the pool
    db_connection = get_db_connection()

    # Create a cursor for this connection
    my_cur = db_connection.cursor()

    final_query = ""

    # Create SQL query to execute
    sql_query = '''SELECT * FROM Restaurants'''

    final_query = final_query + sql_query
    # Check all arguments to allow filtering
    # in this case only city, state and rating will be used to filter as they are the only filters that cam return
    # multiple restaurants
    # the first variable is used to know if its the first sql condition to be applied or not
    first = True
    if 'city' in args.keys():
        city_sql = ' WHERE city = \'{}\''.format(args['city'])
        final_query = final_query + city_sql
        first = False
    # It is unnecessary to use an if first in this case as it can only be the first or not. However in case of adding
    # another possible filter before it the if clause must be added

    if 'state' in args.keys():
        if (first):
            state_sql = ' WHERE state = \'{}\''.format(args['state'])
            first = False
        else:
            state_sql = ' AND state = \'{}\''.format(args['state'])
        final_query = final_query + state_sql

    if 'rating' in args.keys():
        if (first):
            rating_sql = ' WHERE rating = {}'.format(args['rating'])
            first = False
        else:
            rating_sql = ' AND rating = {}'.format(args['rating'])
        final_query = final_query + rating_sql

    final_query = final_query + ';'
    # Execute the query
    my_cur.execute(final_query)

    # Get all the result rows
    restaurants = my_cur.fetchall()

    list_restaurants = []

    for restaurant in restaurants:
        # Create a dictionary for each restaurant
        dict_restaurant = {'id': restaurant[0],
                           'rating': restaurant[1],
                           'name': restaurant[2],
                           'site': restaurant[3],
                           'email': restaurant[4],
                           'phone': restaurant[5],
                           'street': restaurant[6],
                           'city': restaurant[7],
                           'state': restaurant[8],
                           'lat': restaurant[9],
                           'lng': restaurant[10]}
        # append it to the list
        list_restaurants.append(dict_restaurant)

    # Release the connection
    release_db_connection(db_connection)

    # return the list
    return list_restaurants


def create_new_restaurant(args):
    # Ask for a database connection from the pool
    db_connection = get_db_connection()

    # Create a cursor for this connection
    my_cur = db_connection.cursor()

    # Create the sql query
    sql_query = '''INSERT INTO Restaurants (id, rating, name, site, email, phone, street, city, state, lat, lng) 
            VALUES (\'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\', 
            \'{}\', \'{}\', \'{}\', {}, {});'''.format(args['id'], args['rating'], args['name'], args['site'],
                                                       args['email'], args['phone'], args['street'], args['city'],
                                                       args['state'], args['lat'], args['lng'])

    sql_query.encode(encoding='UTF-8', errors='strict')
    # Perform query
    try:
        my_cur.execute(sql_query)
    except(Exception):
        db_connection.rollback()
        release_db_connection(db_connection)
        return

    db_connection.commit()
    # Release the db connection
    release_db_connection(db_connection)
    return


def update_all_restaurants(args):
    # Ask for a database connection from the pool
    db_connection = get_db_connection()

    # Create a cursor for this connection
    my_cur = db_connection.cursor()

    final_query = ''
    # Create the sql query
    sql_query = '''UPDATE Restaurants SET '''
    final_query = final_query + sql_query

    # Update all columns for every argument in the request
    for key in args.keys():
        # This if is necessary to handle numeric and text data differently
        if key == 'rating' or key == 'lat' or key == 'lng':
            final_query = final_query + '{} = {} '.format(key, args[key])
        else:
            final_query = final_query + '{} = \'{}\' '.format(key, args[key])

    final_query = final_query + ';'
    # Perform query
    try:
        my_cur.execute(final_query)
    except(Exception):
        db_connection.rollback()
        release_db_connection(db_connection)
        return

    db_connection.commit()
    # Release the db connection
    release_db_connection(db_connection)
    return


def erase_all_restaurants():
    # Ask for a database connection from the pool
    db_connection = get_db_connection()

    # Create a cursor for this connection
    my_cur = db_connection.cursor()

    # Create the sql query
    sql_query = '''DELETE FROM Restaurants;'''

    # Perform query
    try:
        my_cur.execute(sql_query)
    except:
        db_connection.rollback()
        release_db_connection(db_connection)
        return

    db_connection.commit()
    # Release the db connection
    release_db_connection(db_connection)
    return
