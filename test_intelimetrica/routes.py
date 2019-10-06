from test_intelimetrica import app
from .models.restaurant import get_all_restaurants as get_restaurants_db
from .models.restaurant import create_new_restaurant as create_new_restaurant_db
from .models.restaurant import update_all_restaurants as update_all_restaurants_db
from .models.restaurant import erase_all_restaurants as erase_all_restaurants_db
from .models.restaurant import get_one_restaurant
from .models.restaurant import update_one_restaurant
from .models.restaurant import delete_one_restaurant
from flask import jsonify, request


# The route /api/restaurants is used to obtain the interact with the Restaurants table from the database

# It only allows the GET http verb
# It returns JSON data containing an array of all restaurants
@app.route('/api/restaurants', methods=['GET'])
def get_all_restaurants():
    try:
        list_restaurants = get_restaurants_db(request.args)
    except:
        # TODO: Handle models exceptions properly
        return {'message': 'Internal Server Error'}, 500
    return jsonify(list_restaurants)


# This route will only accept the POST http verb
# It creates a new restaurant row using the information contained in the form data
@app.route('/api/restaurants', methods=['POST'])
def create_new_restaurant():
    try:
        args = {'id': request.form['id'], 'rating': request.form['rating'], 'name': request.form['name'],
                'site': request.form['site'], 'email': request.form['email'],
                'phone': request.form['phone'], 'street': request.form['street'], 'city': request.form['city'],
                'state': request.form['state'], 'lat': request.form['lat'], 'lng': request.form['lng']}
    except:
        return {'message': 'Missing Form Data'}, 400
    try:
        create_new_restaurant_db(args)

    except:
        # TODO: Handle models exceptions properly
        return {'message': 'Internal Server Error'}, 500

    return {'message': 'The restaurant was created correctly'}, 201


# This route will only accept the PUT http verb
# It updates all the restaurants according to the parameters in the URL
@app.route('/api/restaurants', methods=['PUT'])
def update_all_restaurants():
    try:
        # Checks if any parameters were passed and if not it raises an exception
        if len(request.args) == 0:
            return {'message': 'No parameters were passed'}, 400

        update_all_restaurants_db(request.args)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Bulk update processed'}


# This route will only accept the DELETE http verb
# This route deletes all restaurant entries in the database. It will leave the empty Restaurants table that can be
# loaded with initial data using the ./util/load_database.py script
@app.route('/api/restaurants', methods=['DELETE'])
def delete_all_restaurants():
    erase_all_restaurants_db()
    return {'message': 'Successfully erased all restaurant entries.'}


# This route will only accept the GET http verb
# This route is used to obtain the information of a certain restaurant that is identified by its id
@app.route('/api/restaurants/<id>', methods=['GET'])
def retrieve_restaurant(id):
    # Get restaurant from the database
    try:
        restaurant = get_one_restaurant(id)
    except:
        return {'message': 'Internal Server Error'}, 500
    # Send the restaurant back
    return jsonify(restaurant)


# This route will only accept the PUT http verb
# This route is used to update the information of a certain restaurant that is identified by its id
@app.route('/api/restaurants/<id>', methods=['PUT'])
def update_restaurant(id):
    try:
        # Checks if any parameters were passed and if not it raises an exception
        if len(request.args) == 0:
            return {'message': 'No parameters were passed'}, 400

        update_one_restaurant(request.args, id)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Restaurant with id {} has been updated'.format(id)}


# This route will only accept the DELETE http verb
# This route is used to update the information of a certain restaurant that is identified by its id
@app.route('/api/restaurants/<id>', methods=['DELETE'])
def delete_restaurant(id):
    try:
        delete_one_restaurant(id)
    except:
        # TODO: Handle each database exception properly
        return {'message': 'Internal Server Error'}, 500
    return {'message': 'Restaurant with id {} has been updated'.format(id)}
